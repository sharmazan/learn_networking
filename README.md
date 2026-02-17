# learn_networking

Simple server and client to send messages using TCP connections. 

Could be runned as
`python server.py`
in another console:
`python client.py`

## Run client and server using Docker:

### Build images:
```
docker build -f server.Dockerfile -t echo-server:N .
docker build -f client.Dockerfile -t echo-client:N .
```

N - is the version. 

### Running using the host network:
```
docker run --rm -p 9000:9000 --name echo-server echo-server:N
docker run --rm --network host echo-client:N
```

### Running using a separate network:
```
docker network create echo-net
docker run --rm --name echo-server --network echo-net echo-server:N
docker run -it --rm --network echo-net -e ECHO_HOST=echo-server echo-client:N
```

## How to sniff the traffic using tcpdump

### Find a bridge interface
ip link show type bridge | grep br-$(docker network inspect echo-net --format '{{.Id}}' | head -c 12)

### Use it for tcpdump command
sudo tcpdump -ni br-75afa930d574 -A tcp port 9000
or
sudo tcpdump -ni br-75afa930d574 -vv tcp port 9000
or
sudo tcpdump -ni br-$(docker network inspect echo-net --format '{{.Id}}' | head -c 12) tcp port 9000 -A

To record the traffic and review it later with Wireshark:
sudo tcpdump -ni br-75afa930d574 tcp port 9000 -w echo-net-9000.pcap

Use external container to connect to the server
docker run --rm -it --net container:echo-server --cap-add NET_ADMIN --cap-add NET_RAW nicolaka/netshoot tcpdump -ni eth0 tcp port 9000 -A

## Docker commands

Print containers that are running with their networks
docker ps --format "table {{.Names}}\t{{.Networks}}\t{{.Status}}"

Output containers connected to the echo-net network
docker network inspect echo-net --format '{{json .Containers}}'

Test DNS resolv for echo-server inside echo-net network
docker run --rm --network echo-net busybox nslookup echo-server

Review logs
docker logs echo-server


### How tcpdump works in netshoot container
--cap-add is Docker’s way to give a container specific Linux capabilities (fine-grained “root-like powers”) without giving it full --privileged.

In your command:
```
docker run --rm -it \
  --net container:echo-server \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  nicolaka/netshoot tcpdump -ni eth0 tcp port 9000 -vv
```

you’re doing two big things:

Sharing the server’s network namespace

--net container:echo-server means: this netshoot container does NOT get its own network stack.

Instead, it enters the exact same network namespace as echo-server.

So inside netshoot, eth0, IP, routes, ports… are the server’s.

That’s why tcpdump -ni eth0 there sees the server’s traffic “from inside”.

Granting the permissions needed to sniff packets
Linux protects packet sniffing. Even if you are root inside the container, Docker typically drops powerful capabilities.

What NET_RAW does

Allows creating raw sockets / packet sockets (AF_PACKET).

tcpdump needs this to capture packets from an interface.

Without NET_RAW, you usually get an error like “Operation not permitted”.

So: NET_RAW = “let me read raw packets.”

What NET_ADMIN does

Allows various network administration operations in that namespace:

put interface into promiscuous mode,

change interface settings,

add/remove routes, iptables rules, etc.

tcpdump often works with just NET_RAW, but in practice (and across kernels/configs) adding NET_ADMIN avoids failures when tcpdump tries to tweak capture settings.

So: NET_ADMIN = “let me manage the network settings.”

How it works under the hood (short + concrete)

Docker starts netshoot as a normal Linux process.

It puts that process into the same network namespace as echo-server (that’s --net container:...).

It also asks the kernel to allow that process extra powers via capabilities (capset), specifically CAP_NET_RAW and CAP_NET_ADMIN.

Now tcpdump can open a packet capture socket on eth0 inside that namespace.

