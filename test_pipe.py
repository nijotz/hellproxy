from socketproxy import Pipe, SocketPlumbing, main
from socketproxy import logging


class TestProxy(SocketPlumbing):
    def __init__(self, *args):
        SocketPlumbing.__init__(self, *args)
        self.pipes.append(TestPipe())

class TestPipe(Pipe):
    
    def recieve_inbound(self, data):
        if data.find('x') != -1:
            print "I FOUND AN 'e'! THIS IS SPECIAL!!"

if __name__ == '__main__':
    main(TestProxy)
