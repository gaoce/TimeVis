FROM continuumio/miniconda
MAINTAINER gaoce
RUN apt-get update && apt-get install -yq git build-essential
RUN conda install -yq numpy scipy pandas
RUN pip install --upgrade pip
RUN pip install git+https://github.com/gaoce/TimeVis
