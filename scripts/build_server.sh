set -e

GIT_REVISION=`git describe --long --tags --dirty`
SERVER_IMAGE=william57m/mix-answer-server
docker build -t $SERVER_IMAGE:$GIT_REVISION -f ./server/Dockerfile-prod server
docker tag $SERVER_IMAGE:$GIT_REVISION $SERVER_IMAGE:latest
docker push $SERVER_IMAGE:$GIT_REVISION
docker push $SERVER_IMAGE:latest