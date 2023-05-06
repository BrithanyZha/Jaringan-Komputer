from socket import *
import sys

# Mendefinisikan host dan port yang akan digunakan
HOST = '192.168.56.1'
PORT = 80

# Membuat objek socket TCP
server_socket = socket(AF_INET, SOCK_STREAM)

# Mengikat socket ke host dan port yang telah ditentukan
server_socket.bind((HOST, PORT))

# Mendengarkan koneksi masuk dari klien
server_socket.listen(1)

print(f"Server berjalan di {HOST}:{PORT}")

while True:
    # Menerima koneksi dari klien
    client_socket, client_address = server_socket.accept()
    print(f"Terhubung dari {client_address[0]}:{client_address[1]}")

    try:
        # Menerima data dari klien
        request = client_socket.recv(1024).decode()
        # Memproses permintaan klien
        filename = request.split()[1][1:]
        file = open(filename, "r")
        file_contents = file.read()
        file.close()
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_contents
        for i in range(0, len(response)):
            client_socket.send(response[i].encode())
        client_socket.send("\r\n".encode())
        client_socket.close()
    except IOError:
        file = open("404.html", "r")
        file_404 = file.read()
        file.close()
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"+ file_404
        for i in range(0, len(response)):
            client_socket.send(response[i].encode())
        client_socket.send("\r\n".encode())
        client_socket.close()
    # Menutup koneksi dengan klien
    client_socket.close()

server_socket.close()
sys.exit()