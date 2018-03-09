FROM python:3.6.4

# Home directory
ENV HOME /home/server
WORKDIR $HOME

# Copy files for installation
COPY ./ $HOME

# Install dependencies
USER root
RUN pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        -r requirements.txt

# Setup
RUN python setup.py develop

# Run server
CMD ["python", "webserver.py", "--config", "config/dev.conf"]
