FROM alpine:latest

MAINTAINER Alessandro Tomasi <alessandro.tomasi@eitdigital.eu>

RUN apk update && apk upgrade && \
	apk add --virtual .build-deps \
	python \
	gfortran \
    musl-dev \
    g++ \
    python-dev \
    py-pip \
    python \
    make

COPY ./bin/get-pip.py /tmp

#RUN ln -sf `which python` /usr/bin/python && \
#	python /tmp/get-pip.py


#install dependencies
#RUN pip install --upgrade setuptools
#RUN pip install \
#	pyyaml \
#	xlsxwriter \
#	numpy \
#	setuptools \
#	python-dateutil \
#	pytz \
#	pandas

#clean up
RUN	rm -Rf /root/.cache && \
	rm -rf /var/cache/apk/* && \
	rm /tmp/get-pip.py && \
	apk del .build-deps






	