FROM ubuntu:18.04

MAINTAINER Bey Hao Yun <beyhy@artc.a-star.edu.sg>

# Add user
RUN adduser --quiet --disabled-password qtuser \
    && mkdir /app \
    && chown -R qtuser /app

# Install dbs_autodoc dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pyqt5 \
    python3-pip \
    python3-pytest-cov \
    wget \
    curl \
    doxygen && \
    pip3 install pytest \
    pytest-qt \
    pycodestyle \
    pyside2 \
    sphinx-rtd-theme \
    breathe \
    sphinx-sitemap
