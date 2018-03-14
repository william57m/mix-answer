FROM node:9.5.0

# Add standard user so that npm is not run as root.
RUN useradd --create-home --comment "Default User" webapp
USER webapp
ENV HOME /home/webapp
WORKDIR $HOME

# This will reuse the cache and save a significant amout of time
# Unless package.json has changed. In that case all the commands
# after this one will be re-run
ADD ./package.json      $HOME/
RUN npm install --loglevel warn

# Now we're free to add any additional files, they won't trigger the
# npm install when they change.
ADD ./.babelrc          $HOME/
ADD ./scripts           $HOME/scripts/

# Run
CMD ["npm", "run", "dev"]
