import optparse
import socket
from commands import getoutput as out
import time, sys, threading

result = []
logfile = ""
msg = "123456789" * 1000


class myThread(threading.Thread):
    def __init__(self, threadID, destination, port, packet):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.destination = destination
        self.port = port
        self.packet = packet

    def run(self):
        send(self.destination, self.port, self.packet)
        # cmd = "nping --udp --delay 0ms -c {} -p {} {} --data-string={} | tail -2 ".format(self.packet,
        #                                                                                   self.port,
        #                                                                                   self.destination, msg)
        # result.append(out(cmd))


def send(target, port, packet):
    i = 0
    while (i < int(packet)):
        i += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (target, int(port)))
        sock.close()


def getHitTime(start):
    start = int(start)
    diff = start % 60
    diff = 60 - diff
    end = start + diff
    return end


def main(args):
    threads = 5
    if args.threads != None:
        threads = int(args.threads)
    i = 0
    threadsObj = []

    print args
    while (i < threads):
        thisThread = myThread(i, args.destination, args.port, args.packet)
        threadsObj.append(thisThread)
        i += 1
    start = int(time.time())
    end = getHitTime(start)
    logfile = time.ctime(end).replace(" ", "-")
    print "Hit Time {0:1}".format(time.ctime(end))
    # while (int(time.time()) != end):
    #     pass
    print "Hitting"
    stime = time.time()
    for thread in threadsObj:
        thread.start()

    print "Initiallisation Completed ... \nWaiting for threds to complete ..."
    for th in threadsObj:
        th.join()
    etime = time.time()
    timetaken = etime - stime
    print "Time taken : {0:1}".format(timetaken)

    print "Process Complete\nSee {0:1} for details".format(logfile)
    out("mkdir log")
    for res in result:
        cmd = "echo  '{0:1}' >> log/{1:1}.log".format(res, logfile)
        print cmd
        out(cmd)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python UDPHitter.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The destination port to hit on.')
    parser.add_option('-d', '--destination', action='store', dest='destination', help='The destination IP to hit on.')
    parser.add_option('-t', '--threads', action='store', dest='threads', help='The destination IP to hit on.')
    parser.add_option('-n', '--packet', action='store', dest='packet', help='The Number of packet per thread')
    (args, _) = parser.parse_args()
    if args.port == None:
        print "Missing required argument: -p/--port"
        sys.exit(1)
    if args.packet == None:
        print "Missing required argument: -n/--packet"
        sys.exit(1)
    if args.destination == None:
        print "Missing required argument: -d/--destination"
        gateway = out("route -nee | grep '^0.0.0.0' | awk '{print $2}'")
        print "Using gateway IP {0:1}".format(gateway)
        args.destination = gateway
    main(args)
