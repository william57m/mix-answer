# Mix Answer


## Overview
Mix Answer is a Question & Answer platform, a StackOverflow like tool.


## Development
```
# Build images
docker-compose build

# Run containers
docker-compose up -d

# Init database
docker-compose run --rm --no-deps mix-answer-server python scripts/init_db.py --config config/dev.conf --data_test true
```


## Deployment
TO WRITE


## Contribution
1. Please use flake8 as syntax linter
2. Please write tests
3. Please open a pull request for review