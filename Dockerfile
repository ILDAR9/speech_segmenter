FROM tensorflow/tensorflow:2.7.0-cpu-jupyter

RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /inaSpeechSegmenter
COPY . ./

RUN pip install --upgrade pip && pip install . && pip cache purge
