import logging
import select
import socket


class SocketProxy(object):
    
    def __init__(self, server_host, server_port, proxy_host='localhost', proxy_port='8080'):

        self.server_host = server_host
        self.server_port = int(server_port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.proxy_host = proxy_host
        self.proxy_port = int(proxy_port)
        self.proxy_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.pipes = []

    def connect(self):
        "Connects to the server"
        self.server.connect((self.server_host, self.server_port))

    def listen(self):
        "Waits for a connection"
        self.proxy_conn.bind((self.proxy_host, self.proxy_port))
        self.proxy_conn.listen(1)
        self.proxy_conn.accept()
        logging.info('{} connected'.format(addr))

    def proxy_data(self, sender, receiver):
        receiver.send(sender.recv(4096))

    def run(self):
        "Waits for a connection to the proxy, then connects to the server, then proxies data"

        self.listen()
        self.connect()

        while True:
            # Wait for one of the sockets to be readable
            sockets = (self.server, self.proxy)
            readables, _, errors = select.select(sockets, (), sockets, 30)

            for readable in readables:
                if readable is self.server:
                    self.proxy_data(self.server, self.proxy)
                else:
                    self.proxy_data(self.proxy, self.server)


def main(proxy_class):

    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description='Proxy a socket connection')
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()

    # Setup logging to stdout
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # Start proxy
    logging.info('Starting proxy to connect to {} on port {}'.format(args.host, args.port))
    proxy = proxy_class(args.host, args.port)
    proxy.run()

if __name__ == '__main__':
    main(SocketProxy)
