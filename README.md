# learn_networking

Simple server and client to send messages using TCP connections. 

Could be runned as
python server.py
# in another console:
python client.py

or using Docker:
Build images:
docker build -f server.Dockerfile -t echo-server:N .
docker build -f client.Dockerfile -t echo-client:N .

N - is the version. 

Running using the host network:
docker run --rm -p 9000:9000 --name echo-server echo-server:N
docker run --rm --network host echo-client:N

Running using a separate network:
docker network create echo-net
docker run --rm --name echo-server --network echo-net echo-server:N
docker run -it --rm --network echo-net -e ECHO_HOST=echo-server echo-client:N

