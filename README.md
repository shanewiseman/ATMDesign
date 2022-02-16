# ATMDesign

## Build App and Tests
docker build . -f Dockerfile -t atm
docker build . -f Dockerfile.test -t atmtest

## Run App
docker run -it atm

## Run Tests
docker run atmtest
