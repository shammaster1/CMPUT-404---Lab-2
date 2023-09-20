import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "localhost" #127.0.0.1
PROXY_SERVER_PORT = 8080

#send some data(request) to host:port
def send_request(host, port, request):

    #create a new socket in with block to ensure it's closed once we're done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        #connect the socket to host:port
        client_socket.connect((host,port))
        #send the request through the connected socket.
        client_socket.send(request)
        #shut the socket to further writes. Tells server we're done sending.
        client_socket.shutdown(socket.SHUT_WR)

        #assemble response, be careful here, recall that recv(bytes) blockes until it receives data!
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: #keep reading data until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        #return response
        return result
    
#handle an incoming connection that has been accepted by the server
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True: #while the client is keeping the socket open
            data = conn.recv(BYTES_TO_READ) # read some data from the socket
            if not data: #if the coket has been closed to further writes, break.
                break
            print(data) #otherwise, print the data to the screen
            request += data
            response = send_request("www.google.com", 80, request) #and send it as a request to www.google.com
            conn.sendall(response) #return the response from www.google.com back to the client

#start single-threaded proxy server
def start_server():
    '''
    Create the socket in 'with' block to ensure it gets auto-closed once
    we're done.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        #bind the server to a specific host and port on this machine
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        '''
        Allow us to reuse this coket address during linger, as well as other
        implications.

        See: https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ
        '''
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) #allow queuing of up to 2 connections
        '''
        wait for an incoming connection, and when one arrives, accept it and
        create a new socket called 'conn' to interact with it
        '''
        conn, addr = server_socket.accept()

        #pass 'conn' off to handle_connection to do some logic
        handle_connection(conn, addr)

#start multi-threaded proxy server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) #allow queuing of up to 2 connections

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()

'''
see which ports are active:
losf -nP | grep LISTEN

kill processes, in increasing order of danger:
pkill python

sudo kill <pid>

sudo kill -9 <pid>

'''