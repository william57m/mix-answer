FROM mixanswer_mix-answer-server

USER root

COPY ./tests/requirements-test.txt $HOME/

RUN pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        -r requirements-test.txt

RUN python setup.py develop

COPY ./tests $HOME/tests