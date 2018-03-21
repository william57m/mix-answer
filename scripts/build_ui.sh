set -e

# Build builder image
CHECKSUM=`cat ui/Dockerfile ui/package.json ui/scripts/webpack.config.prod.js | md5sum | awk '{print $1}'`
BUILDER_IMAGE=william57m/mix-answer-builder:$CHECKSUM
docker pull $BUILDER_IMAGE || { 
    docker build -t $BUILDER_IMAGE -f ui/Dockerfile ui
    docker push $BUILDER_IMAGE;
}

# Compile files
chmod a+w $PWD/ui/app
docker run --rm \
           -v $PWD/ui/app:/home/webapp/app \
           $BUILDER_IMAGE \
           npm run build

# Build nginx image
GIT_REVISION=`git describe --long --tags --dirty`
UI_IMAGE=william57m/mix-answer-ui
docker build -t $UI_IMAGE:$GIT_REVISION -f ./nginx/Dockerfile-prod .
docker tag $UI_IMAGE:$GIT_REVISION $UI_IMAGE:latest
docker push $UI_IMAGE:$GIT_REVISION
docker push $UI_IMAGE:latest