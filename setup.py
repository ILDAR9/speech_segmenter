# encoding: utf-8


import os
from setuptools import setup, find_packages


DESCRIPTION='CNN-based audio segmentation toolkit. Does voice activity detection, speech detection, music detection, noise detection, speaker gender recognition.'

setup(
    name = "speech_segmenter",
    version = "0.7",
    install_requires=['tensorflow', 'numpy', 'pandas', 'scikit-image', 'pyannote.algorithms', 'pyannote.core', 'pyannote.parser', 'matplotlib', 'Pyro4', 'pytextgrid', 'soundfile'],

    packages = find_packages(),
    package_data = {'speech_segmenter': ['*.hdf5']},
    include_package_data = True,
    scripts=[os.path.join('scripts', script) for script in \
             ['speech_segmenter.py', 'speech_segmenter_pyro_client.py', 'speech_segmenter_pyro_server.py', 'speech_segmenter_pyro_client_setjobs.py']],
    python_requires='>=3.6',
)
