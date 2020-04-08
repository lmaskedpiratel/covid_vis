FROM python:3.7-alpine
COPY requirements.txt /
RUN apk update \
    && apk add -virtual build-dependencies \
        build-base \
        gcc
RUN pip install -r /requirements.txt
COPY scraper.py /
WORKDIR /
CMD ["python3", "scraper.py"]
