#!/usr/bin/python
import optparse
import socket, threading

import sys

target = "10.113.56.177"
port = int("8090")
message = "123456789"*1000


def send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (target, port))


threads = []


def main(args):
    i = int(0)
    while (i < int(args.threads)):
        i+=1
        t = threading.Thread(target=send)
        threads.append(t)
        t.start()

    for i in threads:
        i.join()

    return 0


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python Udpsender.py -t <threads> ")
    parser.add_option('-t', '--threads', action='store', dest='threads', help='The number of threads')
    (args, _) = parser.parse_args()
    if args.threads == None:
        print "arguement -t/--threads not found"
        sys.exit(2)
    else:
        main(args)
