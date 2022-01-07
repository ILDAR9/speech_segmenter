# -*- coding: utf-8 -*-

import argparse
import glob
import os
import distutils.util
import warnings
from argparse import ArgumentTypeError


# TODO
# * allow to use external activity or speech music segmentatio

description = """Do Speech/Music(/Noise) and Male/Female segmentation and store segmentations into CSV files. Segments labelled 'noEnergy' are discarded from music, noise, speech and gender analysis. 'speech', 'male' and 'female' labels include speech over music and speech over noise. 'music' and 'noise' labels are pure segments that are not supposed to contain speech.
"""
epilog=""

def str2bool(v) -> bool:
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')

# Configure command line parsing
parser = argparse.ArgumentParser(description=description, epilog=epilog)
parser.add_argument('-i', '--input', nargs='+', help='Input media to analyse. May be a full path to a media (/home/david/test.mp3), a list of full paths (/home/david/test.mp3 /tmp/mymedia.avi), a regex input pattern ("/home/david/myaudiobooks/*.mp3"), an url with http protocol (http://url_of_the_file)', required=True)
parser.add_argument('-o', '--output_directory', help='Directory used to store segmentations. Resulting segmentations have same base name as the corresponding input media, with csv extension. Ex: mymedia.MPG will result in mymedia.csv', required=True)
parser.add_argument('-d', '--vad_engine', choices=['sm', 'smn'], default='smn', help="Voice activity detection (VAD) engine to be used (default: 'smn'). 'smn' split signal into 'speech', 'music' and 'noise' (better). 'sm' split signal into 'speech' and 'music' and do not take noise into account, which is either classified as music or speech. Results presented in ICASSP were obtained using 'sm' option")
parser.add_argument('-g', '--detect_gender', choices = ['true', 'false'], default='True', help="(default: 'true'). If set to 'true', segments detected as speech will be splitted into 'male' and 'female' segments. If set to 'false', segments corresponding to speech will be labelled as 'speech' (faster)")
parser.add_argument('-b', '--ffmpeg_binary', default='ffmpeg', help='Your custom binary of ffmpeg', required=False)
parser.add_argument('--audioconvert', default=False, type = str2bool, help="If True the firstly we convert a media file to wav (8k)")
parser.add_argument('-e', '--export_format', choices = ['csv', 'textgrid'], default='csv', help="(default: 'csv'). If set to 'csv', result will be exported in csv. If set to 'textgrid', results will be exported to praat Textgrid")
parser.add_argument('-r', '--energy_ratio', default=0.03, type=float, help="(default: 0.03). Energetic threshold used to detect activity (percentage of mean energy of the signal)")
parser.add_argument('--verbose', default=False, type=str2bool)

args = parser.parse_args()

# Preprocess arguments and check their consistency
input_files = []
for e in args.input:
    if e.startswith("http"):
        input_files += [e]
    else:
        input_files += glob.glob(e)
assert len(input_files) > 0, 'No existing media selected for analysis! Bad values provided to -i (%s)' % args.input

odir = args.output_directory.strip(" \t\n\r").rstrip('/')
os.makedirs(odir, exist_ok=True)
assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir

# Do processings
from speech_segmenter import Segmenter, seg2csv

# load neural network into memory, may last few seconds
detect_gender = bool(distutils.util.strtobool(args.detect_gender))
ffmpeg = args.ffmpeg if args.audioconvert else None
seg = Segmenter(vad_engine=args.vad_engine, detect_gender=detect_gender,
                ffmpeg=ffmpeg, energy_ratio=args.energy_ratio)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    base = [os.path.splitext(os.path.basename(e))[0] for e in input_files]
    output_files = [os.path.join(odir, e + '.' + args.export_format) for e in base]
    seg.batch_process(input_files, output_files, verbose=args.verbose, output_format=args.export_format, skipifexist=False)

