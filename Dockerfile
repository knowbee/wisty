FROM python:3

WORKDIR /workspace/wisty
COPY ./ ./
RUN python setup.py install

WORKDIR /wvideos

ENTRYPOINT [ "wisty" ]
CMD [ "--help" ]
