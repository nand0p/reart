#!/bin/sh -ex

docker build -t reart-dev \
	     -f Dockerfile \
	     --build-arg "DATE=$(date)" \
	     --build-arg "REVISION=$(git rev-parse HEAD)" \
	     .

docker kill reart-dev 2> /dev/null || true
sleep 2

docker run --rm \
	   --name reart-dev \
	   -d \
	   -p 5000:5000 \
	   reart-dev
sleep 5
docker ps

docker logs reart-dev
echo "docker run --rm --name reart-dev -ti -p 5000:8000 reart-dev bash"
