import socket
import sys
from struct import unpack

ETH_ALL = 0x0003
ETH_LEN = 14
BUF_SIZE = 65565

# In linux socket.ntohs(0x0003) tells capture everything including ethernet frames.
# To capture TCP, UDP, or ICMP only, instead of socket.ntohs(0x0003) you will write
# socket.IPPROTO_TCP, socket.IPPROTO_UDP and socket.IPPROTO_ICMP respectively
# See socket method at: https://docs.python.org/3/library/socket.html
def create_socket():
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_ALL))
    except socket.error as msg:
        print("Socket could not be created. ERROR: " + str(msg[0]) + " " + msg[1])
        sys.exit()
    return s

def receive_packet(sock):
    while True:
        raw_data, addr  = sock.recvfrom(BUF_SIZE)
        ether_header = parse_ethernet_header(raw_data)
        
        # Check Ethernet Type for Internet Protocol version 4 (prototype value  = 8)
        # See at: https://en.wikipedia.org/wiki/EtherType
        if ether_header[3] == 8:
            # Parse IP header by taking first 20 characters of IP packet
            ipv4_data = raw_data[ETH_LEN:20+ETH_LEN]
            parse_ipv4_header(ipv4_data)
"""
+-----------------------------------------------------+ +----------------------+ +--------------+
|+------------------+-----------------+-------------+ | |+-----------------+   | | CRC Checksum |
|| Destination MAC  |    Source MAC   | Ether Type  | | ||      IP         |   | |   (4 bytes)  |
||   (6 bytes)      |     (6 bytes)   |  (2 bytes)  | | |+-----------------+   | |              |
|+------------------+-----------------+-------------+ | |       DATA           | +--------------+
|              MAC Header (14 bytes)                  | |   (46-1500 bytes)    | 
+-----------------------------------------------------+ +----------------------+

This function will unpack the first 14 bytes of data that we sniffed.
Here we use the unpack method in the struct module.
See more at: https://docs.python.org/3/library/struct.html
"""
def parse_ethernet_header(raw_data):
    mac_header = raw_data[:ETH_LEN]
    mac_addrs = unpack("!6s6sH", mac_header)
    dest = get_mac_addr(mac_addrs[0])
    source = get_mac_addr(mac_addrs[1])
    prototype = socket.htons(mac_addrs[2])

    print("  source MAC: " + source + " destination MAC: " + dest + " Prototype: " + str(prototype))
    
    return mac_header, dest, source, prototype

def get_mac_addr(a):
    mac_addr =  "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (a[0], a[1], a[2], a[3], a[4], a[5])
    return mac_addr
"""
An IP header looks like the following:


 0               1               2               3               4  bytes offset
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |Version|  IHL  |Type of Service|          Total Length         | 4   
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |         Identification        |Flags|      Fragment Offset    | 8 
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |  Time to Live |    Protocol   |         Header Checksum       | 12   
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |                       Source Address                          | 16   
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |                    Destination Address                        | 20   
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
 |                    Options                    |    Padding    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

If the IHL is 5 then total size is 20 bytes hence options+padding is absent.
For TCP packets the protocol is 6. Source address is the source IPv4 address in long format
"""
def parse_ipv4_header(ip_data):
    version_and_IHL = ip_data[0]
    # use bit-shift to take first 4 bits to get version value
    version = version_and_IHL >> 4
    # get the header length (last 4 bits of the first byte)
    ihl = (version_and_IHL & 0x0F) * 4 # 0x0F is 00001111 

    # 8x means 8 bytes padding, that means we do not get identification, flags and fragment offset. Simillar to 2x
    ttl, protocol, src, dest = unpack("! 8x B B 2x 4s 4s", ip_data)

    src_addr = ".".join(map(str,src))
    dest_addr = ".".join(map(str, dest))
    print( '\t - ' + 'IPv4 Packet:')
    print('\t\t - ' + 'Version: {}, Header Length: {}, TTL:{},'.format(version, ihl, ttl))
    print('\t\t - ' + 'Protocol: {}, Source: {}, Destination: {}'.format(protocol, src_addr, dest_addr))

    # Now that we have the internet layer unpacked, the next layer we have to unpack is the transport layer.
    # We can determine the protocol from the protocol ID in the IP header.
    # The following are the protocol IDs for some of the protocols:
    # TCP: 6, ICMP: 1, UDP: 17, RDP: 27, etc.
    data = ip_data[ihl:]
    if protocol == 1: # ICMP Packets (Internet Control Message Protocol)
        parse_icmp_packet(data)
    elif protocol == 6:
        parse_tcp_packet(data)
    elif protocol = 17:
        parse_udp_packet(data)
    else:
        print("Some other protocols !!! Waiting for updates later")



if __name__ == "__main__":
    s = create_socket()
    receive_packet(s)
