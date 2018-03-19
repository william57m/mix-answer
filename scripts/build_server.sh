set -e

GIT_REVISION=`git describe --long --tags --dirty`
SERVER_IMAGE=william57m/mix-answer-server
docker build -t $SERVER_IMAGE:$GIT_REVISION -f ./server/Dockerfile server
docker push $SERVER_IMAGE:$GIT_REVISION