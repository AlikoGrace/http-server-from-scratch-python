import socket
import threading
import  sys
import os

print(sys.argv)


def handle_client(connection):
    try:
        data = connection.recv(1024)
        request_line = data.split(b"\r\n")[0]
        parts = request_line.split(b" ")
        path = parts[1]

        if path == b"/user-agent":
            lines = data.split(b"\r\n")
            body = b""

            for line in lines:
                if line.lower().startswith(b"user-agent"):
                    body = line[len(b"user-agent: "):]
                    break

            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                + b"Content-Length: " + str(len(body)).encode()
                + b"\r\n"
                + b"\r\n"
                + body
            )
        elif path.startswith(b"/files/"):
             filename=path[len(b"/files/"):]
             directory=sys.argv[2]
            #  tester from codecrafter had a temp in main in app so [2] targetted temp
             full_path=os.path.join(directory,filename.decode())

             try:
                 with open(full_path,"rb")as f:
                     body=f.read
                     response=(

                      b"HTTP/1.1 200 OK\r\n"
                      b"Content-Type: application/octet-stream\r\n"
                      + b"Content-Length: " + str(len(body)).encode()
                      + b"\r\n"
                      + b"\r\n"
                      + body
                 )
                
                     
             except FileNotFoundError:
                 response=b"HTTP/1.1 404 Not Found\r\n\r\n"         
                 


        elif path.startswith(b"/echo/"):
            body = path[6:]
            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                + b"Content-Length: "
                + str(len(body)).encode()
                + b"\r\n"
                + b"\r\n"
                + body
            )

        elif path == b"/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

        connection.sendall(response)

    finally:
        connection.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(connection,))
        thread.start()


if __name__ == "__main__":
    main()




    # def handle_client(connection):
    # read request
    # extract path/header info
    # decide response
    # send response
    # all the code is doing 