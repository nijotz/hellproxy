import logging
import select
import socket


class SocketProxy(object):
    
    def __init__(self, server_host, server_port, listener_host='localhost', listener_port='8080'):

        self.server_host = server_host
        self.server_port = int(server_port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listener_host = listener_host
        self.listener_port = int(listener_port)
        self.listener_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        "Connects to the server"
        self.server.connect((self.server_host, self.server_port))

    def listen(self):
        "Waits for a connection"
        self.listener_conn.bind((self.listener_host, self.listener_port))
        self.listener_conn.listen(1)
        self.listener, addr = self.listener_conn.accept()
        logging.info('{} connected'.format(addr))

    def run(self):
        "Waits for a connection to the proxy, then connects to the server, then proxies data"

        self.listen()
        self.connect()

        while True:
            # Wait for one of the sockets to be readable
            sockets = (self.server, self.listener)
            readables, writeables, errors = select.select(sockets, (), sockets, 60)

            # Proxy data
            for readable in readables:
                if readable is self.server:
                    self.listener.send(self.server.recv(4096))
                else:
                    self.server.send(self.listener.recv(4096))


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Proxy a socket connection')
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()

    logging.info('Start proxy to connect to {} on port {}'.format(args.host, args.port))

    proxy = SocketProxy(args.host, args.port)
    proxy.run()

if __name__ == '__main__':
    main()
