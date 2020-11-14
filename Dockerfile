FROM jupyter/minimal-notebook
LABEL author="samuelmignot"
USER root
RUN pip install pipdeptree==1.0.0 pytest==6.1.2 twine==3.2.0
USER $NB_UID
