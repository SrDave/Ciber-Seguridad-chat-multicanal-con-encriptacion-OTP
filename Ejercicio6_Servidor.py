import socket
import select

host = 'localhost'
port = 12345

#TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port))
server_socket.listen(5)

lista_sockets = [server_socket]
clients = {}

print(f"Servidor escuchando en {host}:{port}")

while True:
    clientes, _, _ = select.select(lista_sockets, [], [])

    for sock in clientes:
        # Nueva conexión entrante
        if sock == server_socket:
            client_socket, client_address = server_socket.accept()
            lista_sockets.append(client_socket)
            clients[client_socket] = client_address
            print(f"Nueva conexión establecida desde {client_address}")

        # Datos recibidos de un cliente existente
        else:
            data = sock.recv(1024)
            mensaje = data.decode()
            if data:
                print(f"Datos recibidos de {clients[sock]}: {data.decode('utf-8')}")
                for client in clients:
                    if client != sock:  # Evitar enviar el mensaje de vuelta al remitente
                        try:
                            #client.sendall(f"{clients[client]}: {mensaje}".encode())
                            client.sendall(mensaje.encode())
                        except Exception as e:
                            print(f"Error al enviar mensaje a {clients[client]}: {e}")
                            client.close()
                            lista_sockets.remove(client)
                            del clients[client]
            else:
                # Cliente desconectado
                print(f"Cliente {clients[sock]} desconectado")
                sock.close()
                lista_sockets.remove(sock)
                del clients[sock]

