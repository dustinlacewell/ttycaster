#!/bin/bash

namespace="${1:-dlacewell}"

# build docker images
for image in images/*/
do
    cd ./$image
    base_name=$(basename $image)
    image_name="$namespace/$base_name"
    echo "Building $image_name..."
    docker build -t $image_name . &> /dev/null &&  \
    echo "Pushing $image_name..." &&   \
    docker push $image_name &> /dev/null
    cd ../..
done
