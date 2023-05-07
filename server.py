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
    # Jika ada request connection maka menerima koneksi dari klien
    client_socket, client_address = server_socket.accept()

    try:
        # Membaca request dari link browser client
        request = client_socket.recv(1024).decode()
        # Membaca nama file yang ada dari request
        filename = request.split()[1][1:]
        # Membuka file dan menyimpan ke dalam variabel file
        file = open(filename, "r")
        # Membaca dan menyimpan file yang telah dibuka ke variabel file_content lalu selanjutnya file ditutup
        file_contents = file.read()
        file.close()
        # Membuat header agar file dapat dibaca oleh browser
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + file_contents
        # Mengirimkan isi dari file pada browser client
        for i in range(0, len(response)):
            client_socket.send(response[i].encode())
        client_socket.send("\r\n".encode())
        client_socket.close()
    # Apabila file tidak terdapat pada data system maka lanjut ke except
    except IOError:
        # Sama seperti diatas tetapi file yang dibaca hanya file 404.html tidak menggunakan request message
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
