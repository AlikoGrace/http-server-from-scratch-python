import socket

def main():

    server_socket=socket.create_server(("localhost", 4221), reuse_port=True)
    connection,address=server_socket.accept()

    print(f"connected successfully with {address}")






if __name__ =="__main__":
    main()    