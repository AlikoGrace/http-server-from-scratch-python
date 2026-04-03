import socket


def main():

    server_socket=socket.create_server(("localhost", 4221), reuse_port=True)
    connection,address=server_socket.accept()

    print(f"connected successfully with {address}")

    data=connection.recv(1024)

    request_line=data.split(b"\r\n")[0]
    parts=request_line.split(b" ")
    path=parts[1]

    if path == (b"/"):
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
  


    connection.close()   




if __name__ =="__main__":
    main()    