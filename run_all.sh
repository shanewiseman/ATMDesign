which docker > /dev/null && docker ps > /dev/null

if [ $? != 0 ]; then
	echo "Ensure Docker is installed and properly working"
	exit 1
fi



docker build . -f Dockerfile.test -t atmtest
docker run atmtest

if [ $? == 0 ]; then
	docker build . -f Dockerfile -t atm
	docker run -it atm
else
	echo "Not Running ATM, Tests Failed"
	exit 1
fi
