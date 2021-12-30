# encoding: utf-8

import os
import tempfile
import warnings
from subprocess import Popen, PIPE
import numpy as np

#os.environ['SIDEKIT'] = 'theano=false,libsvm=false,cuda=false'
#from sidekit.frontend.io import read_wav
#from sidekit.frontend.features import mfcc
from .sidekit_mfcc import read_wav, mfcc


def _wav2feats(wavname):
    """
    Extract features for wav 16k mono
    """
    ext = os.path.splitext(wavname)[-1]
    assert ext.lower() == '.wav' or ext.lower() == '.wave'
    sig, read_framerate, sampwidth = read_wav(wavname)
    shp = sig.shape
    # wav should contain a single channel
    assert len(shp) == 1 or (len(shp) == 2 and shp[1] == 1)
    # wav sample rate should be 16000 Hz
    assert read_framerate == 16000
    # current version of readwav is supposed to return 4
    # whatever encoding is detected within the wav file
    assert sampwidth == 4
    #sig *= (2**(15-sampwidth))

    with warnings.catch_warnings() as w:
        # ignore warnings resulting from empty signals parts
        warnings.filterwarnings('ignore', message='divide by zero encountered in log', category=RuntimeWarning)
        _, loge, _, mspec = mfcc(sig.astype(np.float32), get_mspec=True)
        
    # Management of short duration segments
    difflen = 0
    if len(loge) < 68:
        difflen = 68 - len(loge)
        warnings.warn("media %s duration is short. Robust results require length of at least 720 milliseconds" %wavname)
        mspec = np.concatenate((mspec, np.ones((difflen, 24)) * np.min(mspec)))
        #loge = np.concatenate((loge, np.ones(difflen) * np.min(mspec)))

    return mspec, loge, difflen


def media2feats(medianame, tmpdir, start_sec, stop_sec, ffmpeg):
    """
    Convert media to temp wav 16k file and return features
    """
    
    base, _ = os.path.splitext(os.path.basename(medianame))

    with tempfile.TemporaryDirectory(dir=tmpdir) as tmpdirname:
        # build ffmpeg command line
        tmpwav = tmpdirname + '/' + base + '.wav'
        args = [ffmpeg, '-y', '-i', medianame, '-ar', '16000', '-ac', '1']
        if start_sec is None:
            start_sec = 0
        else:
            args += ['-ss', '%f' % start_sec]

        if stop_sec is not None:
            args += ['-to', '%f' % stop_sec]
        args += [tmpwav]

        # launch ffmpeg
        p = Popen(args, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        assert p.returncode == 0, error

        # Get Mel Power Spectrogram and Energy
        return _wav2feats(tmpwav)
