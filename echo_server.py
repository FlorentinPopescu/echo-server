# imports
import os
import io
import sys
# import time
import socket
import traceback
# --------------------------------------


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
        
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,\
                             socket.IPPROTO_TCP)
    except socket.error as err:
        print("server socket creation failed with error:", err)
    
    # TODO: You may find that if you repeatedly run the server script it fails,
    #       claiming that the port is already used.  You can set an option on
    #       your socket that will fix this problem. We DID NOT talk about this
    #       in class. Find the correct option by reading the very end of the
    #       socket library documentation:
    #       http://docs.python.org/3/library/socket.html#example
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # TODO: bind your new sock 'sock' to the address above and begin to listen
    #       for incoming connections
    try:
        sock.bind(address)
        sock.listen(1)
        print("Listening at {0}".format(sock.getsockname()))
    except OSError as err:
        print(err)
        sock.close()
        sock = None    
        
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)
            #time.sleep(5)
            
            # TODO: make a new socket when a client connects, call it 'conn',
            #       at the same time you should be able to get the address of
            #       the client so we can report it below.  Replace the
            #       following line with your code. It is only here to prevent
            #       syntax errors
            if sock is None:
                print("coud not open socket")
                sys.exit(1)
            else:
                conn, addr = sock.accept()
                addr = conn.getpeername()
            
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # TODO: receive 16 bytes of data from the client. Store
                    #       the data you receive as 'data'.  Replace the
                    #       following line with your code.  It's only here as
                    #       a placeholder to prevent an error in string
                    #       formatting
                    data = conn.recv(16)
                    if data:
                        print("received '{0}'".format(data.decode('utf8')))
                
                    # TODO: Send the data you received back to the client, log
                    # the fact using the print statement here.  It will help in
                    # debugging problems.
                    if data:
                       try:
                           conn.sendall(data)
                           print("sent '{0}'".format(data.decode('utf8')))
                       except socket.error:
                           print("cannot send data back to client")
                            
                    # TODO: Check here to see whether you have received the end
                    # of the message. If you have, then break from the
                    # `while True` loop.
                    # 
                    # Figuring out whether or not you have received the end of
                    # the message is a trick we learned in the lesson: if you 
                    # don't remember then ask your classmates or instructor 
                    # for a clue. :)
                          
                    binary_stream = io.BytesIO()
                    binary_stream.write(data)
                    binary_stream.seek(0)
                    count, total = 0, 0
                    try:
                        while count < 10:
                            digits = binary_stream.read(2)
                            total += len(digits)
                            if len(digits) < 2 and total < 16:
                                print("reached the end of message")
                                raise ValueError()
                                break
                            count += 1
                    except ValueError:
                        break
                    
            except Exception as e:
                print("exception occured: {}".format(e))
                traceback.print_exc()
                sys.exit(1)
                
            finally:
                # TODO: When the inner loop exits, this 'finally' clause will
                #       be hit. Use that opportunity to close the socket you
                #       created above when a client connected.
                conn.shutdown(2)
                conn.close()
                print('echo complete, client connection closed', \
                      file=log_buffer)
                # break
        
    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        try:
            print("You pressed Ctrl+C")
            sock.close()
            print('quitting echo server', file=log_buffer)
            sys.exit(0)
        except SystemExit:
            os._exit(1)
# --------------------------------------


if __name__ == '__main__':
    server()
    sys.exit(0)
