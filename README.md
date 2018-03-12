# Mix Answer


## Overview
Mix Answer is a Question & Answer platform, a StackOverflow like tool.


## Technologies
Mix Answer uses modern tools
* [Docker](https://www.docker.com/) #containers
* [Python 3.6](http://www.python.org/) #server
* [PostgreSQL](http://www.postgresql.org/) #database
* [Tornado](http://www.tornadoweb.org/en/stable/) #server
* [ReactJS](https://reactjs.org/) #frontend


## Development
```
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Init database
docker-compose run --rm --no-deps mix-answer-server python scripts/init_db.py --config config/dev.conf --data_test true
```


## Tests
```
cd server/tests

# Build and tag the test image
docker build -t mix-answer-test \
             -f server/tests/Dockerfile \
             server

# Start the test DB container
docker run -d \
           -e POSTGRES_USER=mixuser \
           -e POSTGRES_PASSWORD=mixuser \
           -e POSTGRES_DB=mixanswer \
           --name mix-answer-test-db \
           postgres:9.4

# Initialize the test DB
docker run -t --rm \
           -v /$PWD/server:/home/server \
           --link mix-answer-test-db:db \
           mix-answer-test \
           python scripts/init_db.py --config=config/dev.conf

# Run test
docker run --rm -it \
           -v /$PWD/server:/home/server \
           --link mix-answer-test-db:db \
           mix-answer-test \
           pytest -v
```


## Deployment
TO WRITE


## Future Features
- Add ability to validate a response
- Badge for users (to distinguish reliable users)


## Contribution
- Please use flake8 as syntax linter
- Please write tests
- Please open a pull request for review