import socket
import os


class HTTPHandler:
    # Define socket host and port
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 80

    def get(self, resource):
        current_dir = os.getcwd()
        if resource == '/':
            fin = open(current_dir + '\\html\\' + 'index.html')

        else:
            if resource.find("html") == -1:
                image_data = open(current_dir + '\\html\\' + resource, 'rb')
                bytes = image_data.read()

                # Content-Type: image/jpeg, image/png \n\n
                content = bytes
                image_data.close()
                return content

        # Read file contents
        content = fin.read()
        fin.close()
        return content

    def send_data(self, content, client_connection):
        if content:
            if str(content).find("html") > 0:
                client_connection.sendall('HTTP/1.0 200 OK\n\n'.encode())
                client_connection.sendall(content.encode())
            else:
                client_connection.sendall('HTTP/1.0 200 OK\r\n'.encode())
                client_connection.sendall("Content-Type: image/jpeg\r\n".encode())
                client_connection.sendall("Accept-Ranges: bytes\r\n\r\n".encode())
                client_connection.sendall(content)
        else:
            response = 'HTTP/1.0 404 NOT FOUND\r\nFile Not Found'
            client_connection.sendall(response.encode())
        client_connection.close()

    def init_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        server_socket.listen(1)
        print('Listening on port %s ...' % self.SERVER_PORT)

        while True:
            # Wait for client connections
            client_connection, client_address = server_socket.accept()
            # Handle client request
            request = client_connection.recv(1024).decode()
            if request:
                type_of_request = request.split("\n")[0]
                slash_data = type_of_request.split(" ")[1]
                content = self.get(slash_data)
            else:
                content = ""
            self.send_data(content, client_connection)
            # Send HTTP response

        server_socket.close()
