import socket


def main():

    server_socket=socket.create_server(("localhost", 4221), reuse_port=True)
    connection,address=server_socket.accept()

    print(f"connected successfully with {address}")

    data=connection.recv(1024)

    request_line=data.split(b"\r\n")[0]
    parts=request_line.split(b" ")
    path=parts[1]
    


    if path==b"/user-agent":
        lines=data.split(b"\r\n")
        body=b""

        for line in lines:
            if line.lower().startswith(b"user-agent"):
                body=line[len(b"user-agent: "):]
                break

        response=(
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            +b"Content-Length: "+str(len(body)).encode()
            +b"\r\n"
            +b"\r\n"

            +body

        )

    elif path.startswith(b"/echo/"):
        body=path[6:]
        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            + b"Content-Length: "
            + str(len(body)).encode()
            + b"\r\n"
            + b"\r\n"
            + body
        )    

        
    elif path == (b"/"):
         response=b"HTTP/1.1 200 OK\r\n\r\n"

    else:
        response=b"HTTP/1.1 404 Not Found\r\n\r\n"
  

    connection.sendall(response)
    connection.close()   




if __name__ =="__main__":
    main()    