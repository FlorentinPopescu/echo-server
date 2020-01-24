# imports
import socket
import sys
import traceback
# --------------------------------------


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,\
                             socket.IPPROTO_TCP)
        print('connecting to {0} port {1}'.format(*server_address),\
              file=log_buffer)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as err:
        print("client socket creation failed with error:", err)
    
    # TODO: connect your socket to the server here.
    try:
        sock.connect(server_address)
    except ConnectionRefusedError:
        print("connection refused, server is closing")
        sock.close()
        sys.exit(1)

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''
      
    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        
        # TODO: send your message to the server here.
        try:
            sock.sendall(str.encode(msg))
        except OSError as err:
            print(err)
        
        # TODO: the server should be sending you back your message as a series
        #       of 16-byte chunks. Accumulate the chunks you get to build the
        #       entire reply from the server. Make sure that you have received
        #       the entire message and then you can break the loop.
        #
        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        
        # =============================================       
        # OPTION (A)
        MSGLEN = len(msg)
        while len(received_message) < MSGLEN:
            try:
                chunk = sock.recv(min(MSGLEN - len(received_message), 16))
                if chunk == b'': break
                print('received: "{0}"'.format(chunk.decode('utf8')), \
                      file=log_buffer)
                received_message += chunk.decode("utf-8")
                # print("expected %d bytes, received %d bytes cumulative" \
                #                   %(MSGLEN, len(received_message)))
            except (ConnectionResetError, EOFError, OSError) as err:
                print(err)
                break
        
        # OPTION (B)
        # MSGLEN = len(msg)
        # while len(received_message) < MSGLEN:
        #     try:
        #         chunk = sock.recv(16)
        #         if chunk.find(b'\036') != -1 and not chunk:
        #             print("expected %d bytes, received %d bytes" \
        #                            %(MSGLEN, len(received_message)))
        #             break
        #         print('received: "{0}"'.format(chunk.decode('utf8')), \
        #               file=log_buffer)
        #         received_message.append(chunk.decode("utf-8"))   
        #     except (ConnectionResetError, EOFError, OSError) as err:
        #         print(err)
        #         break
        # =============================================
                
        print("received message = {0}".format(received_message))
                    
    except Exception as e:
        print("exception occured: {0}".format(e))
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        try:
            sock.shutdown(1)
            sock.close()
            print('closing socket', file=log_buffer)
        except OSError:
            print("requested socket shutdown not possible; socket not active")
        
        # TODO: when all is said and done, you should return the entire reply
        # you received from the server as the return value of this function.
        return received_message
# --------------------------------------


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    try:
        client(msg)
    except ConnectionRefusedError as err:
        print(err)
    