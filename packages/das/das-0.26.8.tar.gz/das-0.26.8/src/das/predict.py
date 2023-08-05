"""Code for training and evaluating networks."""
import logging
import os
import scipy
import flammkuchen
import librosa
import numpy as np
from . import utils, data, models, event_utils, segment_utils, annot
from typing import List, Optional, Dict, Any
import glob


def predict_probabililties(x, model, params, verbose=None, prepend_data_padding: bool = True):
    """[summary]

    Args:
        x ([samples, ...]): [description]
        model (tf.keras.Model): [description]
        params ([type]): [description]
        verbose (int, optional): Verbose level for predict_generator (see tf.keras docs). Defaults to None.
        prepend_data_padding (bool, optional): Restores samples that are ignored
                    in the beginning of the first and the end of the last chunk
                    because of "ignore_boundaries". Defaults to True.
    Returns:
        y_pred - output of network for each sample [samples, nb_classes]
    """
    pred_gen = data.AudioSequence(x=x, y=None, shuffle=False, **params)  # prep data
    y_pred = model.predict(pred_gen, verbose=verbose)  # run the network
    y_pred = data.unpack_batches(y_pred, pred_gen.data_padding)  # reshape from [batches, nb_hist, ...] to [time, ...]
    if prepend_data_padding:   # to account for loss of samples at the first and last chunks
        y_pred = np.pad(y_pred,
                        pad_width=((params['data_padding'], params['data_padding']), (0, 0)),
                        mode='constant', constant_values=0)
    return y_pred


def labels_from_probabilities(probabilities, threshold: Optional[float] = None):
    """Convert class-wise probabilities into labels.

    Args:
        probabilities ([type]): [samples, classes] or [samples, ]
        threshold (float, Optional): Argmax over all classes (Default, 2D - corresponds to 1/nb_classes or 0.5 if 1D).
                                     If float, each class probability is compared to the threshold.
                                     First class to cross threshold wins.
                                     If no class crosses threshold label will default to the first class.
    Returns:
        labels [samples,] - index of "winning" dimension for each sample
    """
    if probabilities.ndim == 1:
        if threshold is None:
            threshold = 0.5
        labels = (probabilities > threshold).astype(np.intp)
    elif probabilities.ndim == 2:
        if threshold is None:
            labels = np.argmax(probabilities, axis=1)
        else:
            thresholded_probabilities = probabilities.copy()
            thresholded_probabilities[thresholded_probabilities < threshold] = 0
            labels = np.argmax(thresholded_probabilities > threshold, axis=1)
    else:
        raise ValueError(f'Probabilities have to many dimensions ({probabilities.ndim}). Can only be 1D or 2D.')

    return labels


def predict_segments(class_probabilities: np.ndarray,
                     samplerate: float = 1.0,
                     segment_dims: Optional[List[int]] = None,
                     segment_names: Optional[List[str]] = None,
                     segment_ref_onsets: Optional[List[float]] = None,
                     segment_ref_offsets: Optional[List[float]] = None,
                     segment_thres: float = 0.5,
                     segment_minlen: Optional[float] = None,
                     segment_fillgap: Optional[float] = None,
                     segment_labels_by_majority: bool = True) -> Dict:
    """[summary]

    TODO: document different approaches for single-type vs. multi-type segment detection

    Args:
        class_probabilities ([type]): [T, nb_classes] with probabilities for each class and sample
                                      or [T,] with integer entries as class labels
        samplerate (float, optional): Hz. Defaults to 1.0.
        segment_dims (Optional[List[int]], optional): set of indices into class_probabilities corresponding
                                                      to segment-like song types.
                                                      Needs to include the noise dim.
                                                      Required to ignore event-like song types.
                                                      Defaults to None (all classes are considered segment-like).
        segment_names (Optional[List[str]], optional): Names for segment-like classes.
                                                       Defaults to None (use indices of segment-like classes).
        segment_ref_onsets (Optional[List[float]], optional):
                            Syllable onsets (in seconds) to use for estimating labels.
                            Defaults to None (will use onsets est from class_probabilitieslabels as ref).
        segment_ref_offsets (Optional[List[float]], optional): [description].
                            Syllable offsets (in seconds) to use for estimating labels.
                            Defaults to None (will use offsets est from class_probabilitieslabels as ref).
        segment_thres (float, optional): [description]. Defaults to 0.5.
        segment_minlen (Optional[float], optional): seconds. Defaults to None.
        segment_fillgap (Optional[float], optional): seconds. Defaults to None.
        segment_labels_by_majority (bool, optional): Segment labels given by majority of label values within on- and offsets. Defaults to True.

    Returns:
        dict['segmentnames']['denselabels-samples'/'onsets'/'offsets'/'probabilities']
    """
    probs_are_labels = class_probabilities.ndim == 1
    if segment_dims is None:
        if not probs_are_labels:  # class_probabilities is [T, nb_classes]
            nb_classes = class_probabilities.shape[1]
        else:  # class_probabilities is [T,] with integer entries as class labels
            nb_classes = int(np.max(class_probabilities))
        segment_dims = list(range(nb_classes))

    if segment_names is None:
        segment_names = segment_dims

    segments = dict()
    if len(segment_dims):
        segments['samplerate_Hz'] = samplerate
        segments['index'] = segment_dims
        segments['names'] = segment_names
        if not probs_are_labels:
            prob = class_probabilities[:, segment_dims]
            segments['probabilities'] = prob
            labels = labels_from_probabilities(prob, segment_thres)
        else:
            segments['probabilities'] = None
            labels = class_probabilities

        # turn into song (0), no song (1) sequence to detect onsets (0->1) and offsets (1->0)
        song_pred = (labels > 0).astype(np.float)
        if segment_fillgap is not None:
            song_pred = segment_utils.fill_gaps(song_pred, segment_fillgap * samplerate)
        if segment_minlen is not None:
            song_pred = segment_utils.remove_short(song_pred, segment_minlen * samplerate)

        # detect syllable on- and offsets
        # pre- and post-pend 0 so we detect on and offsets at boundaries
        segments['onsets_seconds'] = np.where(np.diff(np.insert(song_pred, 0, values=[0], axis=0)) == 1)[0].astype(np.float) / samplerate
        segments['offsets_seconds'] = np.where(np.diff(np.append(song_pred, values=[0], axis=0)) == -1)[0].astype(np.float) / samplerate
        segments['durations_seconds'] = segments['offsets_seconds'] - segments['onsets_seconds']

        if len(segment_dims) == 2:  # there is just a single segment type plus noise - in that case we use the gap-filled, short-deleted pred
            labels = song_pred
            segments['sequence'] = [str(segment_names[1])] * len(segments['offsets_seconds'])   # syllable-type for each syllable as int
        elif len(segment_dims) > 2 and segment_labels_by_majority:  # if >1 segment type (plus noise) label sylls by majority vote on un-smoothed labels
            # if no refs provided, use use on/offsets from smoothed labels
            if segment_ref_onsets is None:
                segment_ref_onsets = segments['onsets_seconds']
            if segment_ref_offsets is None:
                segment_ref_offsets = segments['offsets_seconds']

            sequence, labels = segment_utils.label_syllables_by_majority(labels,
                                                                         segment_ref_onsets,
                                                                         segment_ref_offsets,
                                                                         samplerate)
            segments['sequence'] = sequence  # syllable-type for each syllable as int
        else:
            segments['sequence'] = []
        segments['samples'] = labels
    return segments


def predict_events(class_probabilities, samplerate: float = 1.0,
                   event_dims: List[int] = None, event_names: List[str] = None,
                   event_thres: float = 0.5, events_offset: float = 0.0, event_dist: float = 100.0,
                   event_dist_min: float = 0.0, event_dist_max: float = np.inf):
    """[summary]

    Args:
        class_probabilities ([type]): [samples, classes][description]
        samplerate (float, optional): Hz
        event_dims (List[int], optional): [description]. Defaults to np.arange(1, nb_classes) (excludes noise-class at index 0).
        event_names ([type], optional): [description]. Defaults to event_dims.
        event_thres (float, optional): [description]. Defaults to 0.5.
        events_offset (float, optional): . Defaults to 0 seconds.
        event_dist (float, optional): minimal distance between events for detection (in seconds). Defaults to 100 seconds.
        event_dist_min (float, optional): minimal distance to nearest event for post detection interval filter (in seconds). Defaults to 0 seconds.
        event_dist_max (float, optional): maximal distance to nearest event for post detection interval filter (in seconds). Defaults to None (no upper limit).

    Raises:
        ValueError: [description]

    Returns:
        dict[index/names/sequence/seconds/probabilities]
    """
    if event_dims is None:
        nb_classes = class_probabilities.shape[1]
        event_dims = np.arange(1, nb_classes).astype(np.uintp)

    if event_names is None:
        event_names = [str(dim) for dim in event_dims]

    if event_dist_max is None:
        event_dist_max = np.inf

    events: Dict[str, Any] = dict()
    if len(event_dims):
        events['samplerate_Hz'] = samplerate
        events['index'] = event_dims
        events['names'] = event_names

        events['seconds'] = []
        events['probabilities'] = []
        events['sequence'] = []

        for event_dim, event_name in zip(event_dims, event_names):
            event_indices, event_probabilities = event_utils.detect_events(class_probabilities, index=event_dim,
                                                                           thres=event_thres, min_dist=event_dist * samplerate)
            events_seconds = event_indices.astype(np.float) / samplerate
            events_seconds += events_offset

            good_event_indices = event_utils.event_interval_filter(events_seconds,
                                                                   event_dist_min, event_dist_max)
            # good_event_indices = np.arange(len(events_seconds))
            events['seconds'].extend(events_seconds[good_event_indices])
            events['probabilities'].extend(event_probabilities[good_event_indices])
            events['sequence'].extend([event_name for _ in events_seconds[good_event_indices]])

    return events


def predict_song(class_probabilities: np.ndarray, params: Dict[str, Any],
                 event_thres: float = 0.5, event_dist: float = 0.01,
                 event_dist_min: float = 0, event_dist_max: float = None,
                 segment_ref_onsets: Optional[List[float]] = None,
                 segment_ref_offsets: Optional[List[float]] = None,
                 segment_thres: float = 0.5, segment_minlen: float = None,
                 segment_fillgap: float = None):

    samplerate = params['samplerate_x_Hz']
    events_offset = 0

    segment_dims = np.where([val == 'segment' for val in params['class_types']])[0]
    segment_names = [params['class_names'][segment_dim] for segment_dim in segment_dims]
    segments = predict_segments(class_probabilities, samplerate,
                                segment_dims, segment_names,
                                segment_ref_onsets, segment_ref_offsets,
                                segment_thres, segment_minlen, segment_fillgap)

    event_dims = np.where([val == 'event' for val in params['class_types']])[0]
    event_names = [params['class_names'][event_dim] for event_dim in event_dims]
    events = predict_events(class_probabilities, samplerate,
                            event_dims, event_names,
                            event_thres, events_offset, event_dist,
                            event_dist_min, event_dist_max)
    return events, segments


def predict(x: np.ndarray, model_save_name: str = None, verbose: int = 1,
            batch_size: int = None,
            model: models.keras.models.Model = None, params: dict = None,
            event_thres: float = 0.5, event_dist: float = 0.01,
            event_dist_min: float = 0, event_dist_max: float = None,
            segment_thres: float = 0.5, segment_use_optimized: bool = True,
            segment_minlen: float = None, segment_fillgap: float = None,
            pad: bool = True, prepend_data_padding: bool = True):
    """[summary]

    Usage:
    Calling predict with the path to the model will load the model and the
    associated params and run inference:
    `das.predict.predict(x=data, model_save_name='tata')`

    To re-use the same model with multiple recordings, load the modal and params
    once and pass them to `predict`
    ```my_model, my_params = das.utils.load_model_and_params(model_save_name)
    for data in data_list:
        das.predict.predict(x=data, model=my_model, params=my_params)
    ```

    Args:
        x (np.array): Audio data [samples, channels]
        model_save_name (str): path with the trunk name of the model. Defaults to None.
        model (keras.model.Models): Defaults to None.
        params (dict): Defaults to None.

        verbose (int): display progress bar during prediction. Defaults to 1.
        batch_size (int): number of chunks processed at once . Defaults to None (the default used during training).
                         Larger batches lead to faster inference. Limited by memory size, in particular for GPUs which typically have 8GB.
                         Large batch sizes lead to loss of samples since only complete batches are used.
        pad (bool): Append zeros to fill up batch. Otherwise the end can be cut.
                    Defaults to False

        event_thres (float): Confidence threshold for detecting peaks. Range 0..1. Defaults to 0.5.
        event_dist (float): Minimal distance between adjacent events during thresholding.
                            Prevents detecting duplicate events when the confidence trace is a little noisy.
                            Defaults to 0.01.
        event_dist_min (float): MINimal inter-event interval for the event filter run during post processing.
                                Defaults to 0.
        event_dist_max (float): MAXimal inter-event interval for the event filter run during post processing.
                                Defaults to None (no upper limit).

        segment_thres (float): Confidence threshold for detecting segments. Range 0..1. Defaults to 0.5.
        segment_use_optimized (bool): Use minlen and fillgap values from param file if they exist.
                                      If segment_minlen and segment_fillgap are provided,
                                      then they will override the values from the param file.
                                      Defaults to True.
        segment_minlen (float): Minimal duration in seconds of a segment used for filtering out spurious detections. Defaults to None.
        segment_fillgap (float): Gap in seconds between adjacent segments to be filled. Useful for correcting brief lapses. Defaults to None.

        pad (bool): prepend values (repeat last sample value) to fill the last batch. Otherwise, the end of the data will not be annotated because
                    the last, non-full batch will be skipped.
        prepend_data_padding (bool, optional): Restores samples that are ignored
                    in the beginning of the first and the end of the last chunk
                    because of "ignore_boundaries". Defaults to True.
    Raises:
        ValueError: [description]

    Returns:
        events: [description]
        segments: [description]
        class_probabilities (np.array): [T, nb_classes]
        class_names (List[str]): [nb_classes]
    """

    if model_save_name is not None:
        model, params = utils.load_model_and_params(model_save_name)
    else:
        assert isinstance(model, models.keras.models.Model)
        assert isinstance(params, dict)

    # use postprocessing values from params and/or args
    if segment_use_optimized and 'post_opt' in params and isinstance(params['post_opt'], dict):
        if segment_minlen is None:
            segment_minlen = params['post_opt']['min_len']
        if segment_fillgap is None:
            segment_fillgap = params['post_opt']['gap_dur']

    if batch_size is not None:
        params['batch_size'] = batch_size

    if pad:
        # figure out length in multiples of batches

        batch_len = params['batch_size'] * params['nb_hist'] + params['nb_hist']
        x_len_original = len(x)
        pad_len = 0
        if np.remainder(len(x), batch_len) > 0:
            pad_len = batch_len - np.remainder(len(x), batch_len)
        # pad with end val to fill
        x = np.pad(x, ((0, pad_len), (0, 0)), mode='edge')

    class_probabilities = predict_probabililties(x, model, params, verbose, prepend_data_padding)

    if pad:
        # trim probs to original len of x
        class_probabilities = class_probabilities[:x_len_original, :]
        # set all song probs in padded section to zero to avoid out of bounds detections!
        # assumes that the non-song class is at index 0
        # class_probabilities[-pad_len:, 1:] = 0
        # class_probabilities[-pad_len:, 0] = 1

    events, segments = predict_song(class_probabilities=class_probabilities, params=params,
                                    event_thres=event_thres, event_dist=event_dist,
                                    event_dist_min=event_dist_min, event_dist_max=event_dist_max,
                                    segment_ref_onsets=None, segment_ref_offsets=None,
                                    segment_thres=segment_thres, segment_minlen=segment_minlen,
                                    segment_fillgap=segment_fillgap)

    return events, segments, class_probabilities, params['class_names']


def cli_predict(path: str, model_save_name: str, *,
                save_filename: Optional[str] = None, save_format: str = 'csv',
                verbose: int = 1, batch_size: Optional[int] = None,
                event_thres: float = 0.5, event_dist: float = 0.01,
                event_dist_min: float = 0, event_dist_max: Optional[float] = None,
                segment_thres: float = 0.5, segment_use_optimized: Optional[bool] = None,
                segment_minlen: Optional[float] = None, segment_fillgap: Optional[float] = None,
                resample: bool = True):
    """Predict song labels for a wav file or a folder of wav files.

    Saves hdf5 files with keys: events, segments, class_probabilities
    OR csv files with columns: label/start_seconds/stop_seconds

    Args:
        path (str): Path to a single WAV file with the audio data or to a folder with WAV files.
        model_save_name (str): Stem of the path for the model (and parameters). File to load will be MODEL_SAVE_NAME + _model.h5.
        save_filename (Optional[str]): Path to save annotations to.
                                       If omitted, will construct save_filename by
                                       stripping the extension from recording_filename and adding '_das.h5' or '_annotations.csv'.
                                       Will be ignored if `path` is a folder.
        save_format (str): 'csv' or 'h5'.
                           csv: tabular text file with label, start and end seconds for each predicted song.
                           h5: same information as in csv plus confidence values for each sample and song type.
                           Defaults to 'csv'.
        verbose (int): Display progress bar during prediction. Defaults to 1.
        batch_size (Optional[int]): Number of chunks processed at once.
                                    Defaults to None (the default used during training).

        event_thres (float): Confidence threshold for detecting events. Range 0..1. Defaults to 0.5.
        event_dist (float): Minimal distance between adjacent events during thresholding.
                            Prevents detecting duplicate events when the confidence trace is a little noisy.
                            Defaults to 0.01.
        event_dist_min (float): MINimal inter-event interval for the event filter run during post processing.
                                Defaults to 0.
        event_dist_max (Optional[float]): MAXimal inter-event interval for the event filter run during post processing.
                                          Defaults to None (no upper limit).

        segment_thres (float): Confidence threshold for detecting segments. Range 0..1. Defaults to 0.5.
        segment_use_optimized (Optional[bool]): Use minlen and fillgap values from param file if they exist.
                                      If segment_minlen and segment_fillgap are provided,
                                      then they will override the values from the param file.
                                      Defaults to True.
        segment_minlen (Optional[float]): Minimal duration of a segment used for filtering out spurious detections.
                                          Defaults to None (keep all segments).
        segment_fillgap (Optional[float]): Gap between adjacent segments to be filled. Useful for correcting brief lapses.
                                           Defaults to None (do not fill gaps).
        resample (bool): Resample audio data to the rate expected by the model. Defaults to True.

    Raises:
        ValueError on unknown save_format
    """
    if not (save_format == 'csv' or save_format == 'h5'):
        raise ValueError(f"Unknown save_format '{save_format}'. Should be either 'csv' or 'h5'.")

    if os.path.isdir(path) and save_filename is not None:
        logging.warning(f'{path} is a folder. Will ignore save_filename argument {save_filename}.')

    # if path is folder: glob contents - all files
    if os.path.isdir(path):
        filenames = glob.glob(f'{path}/*.wav')
        filenames = [filename for filename in filenames if not os.path.isdir(filename)]
    elif os.path.isfile(path):
        filenames = [path]

    logging.info(f"Loading model from {model_save_name}.")
    model, params = utils.load_model_and_params(model_save_name)
    fs_model = params['samplerate_x_Hz']

    for recording_filename in filenames:
        logging.info(f"   Loading data from {recording_filename}.")
        try:
            # else if path is file - predict only on file but make it single-item list
            x, fs_audio = librosa.load(recording_filename, sr=None, mono=False)
            x = x.T
            x = x[:, np.newaxis] if x.ndim == 1 else x  # adds singleton dim for single-channel wavs

            if resample and fs_audio != fs_model:
                logging.info(f"   Resampling. Audio rate is {fs_audio}Hz but model was trained on data with {fs_model}Hz.")
                x = utils.resample(x, fs_audio, fs_model)

            logging.info(f"   Annotating using model at {model_save_name}.")
            # TODO: load model once, provide as direct arg
            events, segments, class_probabilities, class_names = predict(x, None, verbose, batch_size,
                                                                         model, params,
                                                                         event_thres, event_dist, event_dist_min, event_dist_max,
                                                                         segment_thres, segment_use_optimized, segment_minlen, segment_fillgap)

            if 'event' in params["class_types"]:
                logging.info(f"   found {len(events['seconds'])} instances of events '{list(set(events['sequence']))}'.")
            if 'segment' in params["class_types"]:
                logging.info(f"   found {len(segments['onsets_seconds'])} instances of segments '{list(set(segments['sequence']))}'.")

            if save_format == 'h5':
                # turn events and segments into df!
                d = {'events': events,
                     'segments': segments,
                     'class_probabilities': class_probabilities,
                     'class_names': class_names}
                if save_filename is None:
                    save_filename = os.path.splitext(recording_filename)[0] + '_das.h5'
                logging.info(f"   Saving results to {save_filename}.")
                flammkuchen.save(save_filename, d)
                logging.info(f"Done.")
            elif save_format == 'csv':
                evt = annot.Events.from_predict(events, segments)
                if save_filename is None:
                    save_filename = os.path.splitext(recording_filename)[0] + '_annotations.csv'
                logging.info(f"   Saving results to {save_filename}.")
                evt.to_df().to_csv(save_filename)
                logging.info(f"Done.")

            # reset
            if os.path.isdir(path):
                save_filename = None
        except Exception:
            logging.exception(f'Error processing file {recording_filename}.')
