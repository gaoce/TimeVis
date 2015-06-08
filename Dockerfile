FROM continuumio/miniconda
MAINTAINER gaoce
RUN conda install -yq numpy scipy pandas flask sqlalchemy
COPY . /tmp/timevis
RUN pip install /tmp/timevis
