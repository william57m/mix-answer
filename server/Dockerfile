FROM        python:3.6.4

# Home directory
ENV HOME    /home/server
WORKDIR     $HOME

# Copy files for installation
COPY        ./requirements.txt      $HOME/requirements.txt

# Install dependencies
USER        root
RUN         pip install \
                --no-cache-dir \
                --disable-pip-version-check \
                -r requirements.txt

COPY        ./                      $HOME

# Setup
RUN         python setup.py develop

# Run server
CMD         ["python", "core/webserver.py", "--config", "config/dev.conf"]
