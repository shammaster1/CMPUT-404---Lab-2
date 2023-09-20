import socket
BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #opened up the socket here. AF_INET tells to use IPV4
    # and SOCK_STREAM tells to use TCP (if a request fails, tells to send request again. Other is UDP and may fail but
    # is faster)
    s.connect((host,port)) #connect to google
    s.send(request) #send request
    s.shutdown(socket.SHUT_WR) #done sending
    result = s.recv(BYTES_TO_READ)  #keep reading incoming data
    while (len(result)>0):
        print(result)
        result =s.recv(BYTES_TO_READ)

    s.close() #garbage colllector does this anyways but its good programming to do this! Other languages
    # aren't as forgiving

#get("www.google.com", 8080)
get("localhost", 8080)