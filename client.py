#!/usr/bin/python2
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import socket
import sys
import subprocess as sp
# from Peer1 import peer1


class ClientProtocol(DatagramProtocol):
    """
    The clients registers with the rendezvous server.
    The rendezvous server returns connection details for the other peer.
    The client Initializes a connection with the other peer and sends a
    message.
    """

    def startProtocol(self):
        """Register with the server."""
        self.server_connect = False
        self.peer_init = False
        self.peer_connect = False
        self.peer_address = None
        self.transport.write('0', (sys.argv[1], int(sys.argv[2])))

    def toAddress(self, data):
        """Return a tuple containing IPv4 address."""
        ip, port = data.split(':')
        return (ip, int(port))

    def datagramReceived(self, datagram, host):
        """Handle incoming datagram messages."""
        if not self.server_connect:
            self.server_connect = True
            self.transport.write('ok', (sys.argv[1], int(sys.argv[2])))
            print 'Connected to server, waiting for peer...'

        elif not self.peer_init:
            self.peer_init = True
            self.peer_address = self.toAddress(datagram)
            self.transport.write('init', self.peer_address)
            print 'Sent initialization message to %s:%d' % self.peer_address

        elif not self.peer_connect:
            self.peer_connect = True
            # host = self.transport.getHost().host
            # port = self.transport.getHost().port
            #Added two initialization messages because for peers under different level of NAT, the first packet gets rejected by the router and not forwarded to the destination port.
            self.transport.write("Initialization", self.peer_address)
            self.transport.write("Initialization", self.peer_address)
           

        else:

            print 'Received from the peer: ', datagram        
            msg = raw_input("Enter the message to send to peer: ")
            # print self.peer_address[1], self.peer_address[0]
            self.transport.write(msg, self.peer_address)
            #
            


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./client RENDEZVOUS_IP RENDEZVOUS_PORT"
        sys.exit(1)

    protocol = ClientProtocol()
    t = reactor.listenUDP(0, protocol)
    reactor.run()
