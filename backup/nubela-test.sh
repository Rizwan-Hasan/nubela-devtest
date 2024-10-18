#!/bin/bash

docker run \
    --rm \
    --network none \
    -v $(pwd)/sock:/var/run/dev-test/sock \
    nubelacorp/dev-test:stable \
    /var/run/dev-test/sock
