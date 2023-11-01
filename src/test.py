import socket
import time
import re


def discover():
    """Discover UPNP capable routers in the local network
    Returns a lit of urls with service descriptions
    """
    REQ_ADDR = "192.168.11.1"
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900
    SSDP_MX = 2
    SSDP_ST = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"
    # SSDP_ST = "urn:schemas-upnp-org:service:WANIPConnection:1"

    WAIT = 1

    ssdpRequest = (
        "M-SEARCH * HTTP/1.1\r\n"
        + "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT)
        + 'MAN: "ssdp:discover"\r\n'
        + "MX: %d\r\n" % (SSDP_MX,)
        + "ST: %s\r\n" % (SSDP_ST,)
        + "\r\n"
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.sendto(ssdpRequest.encode(), (REQ_ADDR, SSDP_PORT))
    time.sleep(WAIT)
    paths = []
    try:
        data, fromaddr = sock.recvfrom(1024)
        # ip = fromaddr[0]
        # print "from ip: %s"%ip
        parsed = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", str(data, "utf-8"))

        # get the location header
        location = [x for x in parsed if x[0].lower() == "location"]

        # use the urlparse function to create an easy to use object to hold a URL
        router_path = location[0][1]
        paths.append(router_path)

    except socket.error:
        """no data yet"""
        print(socket.error)
    return paths


res = discover()
print(res)
