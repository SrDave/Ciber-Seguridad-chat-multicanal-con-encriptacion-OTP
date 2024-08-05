import socket
import threading
import secrets

host = 'localhost'
port = 12345

#socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
print(f"Conectado al servidor en {host}:{port}")

contador_claves = 0

def generar_flujo_claves(key):
    return ''.join([secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(key)])

def xor_bytes(key_stream, message):
    length = min(len(key_stream), len(message))
    return bytes([key_stream[i] ^ message[i] for i in range(length)])

key_stream = b'HBBOOGRHGBBYPIRQMQSESAQCFKJYCSCULNNFOVMWJMAQAJNULQEZXVOLSNEYUNPOPDMRPTXDBYJFSRLQUQOGQVYVICKHZKKVSZDO'
# Función para manejar la recepción de mensajes
def recibir_mensajes():
    global contador_claves
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                #texto = data.decode()
                clave = key_stream[contador_claves:contador_claves+len(data)]
                mensaje_descifrado = xor_bytes(clave, data)
                contador_claves += len(data)
                print(f"\nMensaje recibido: {mensaje_descifrado.decode('utf-8')}")
            else:
                print("El servidor ha cerrado la conexión.")
                break
        except Exception as e:
            print(f"Error al recibir mensajes: {e}")
            break



# Iniciar el hilo para la recepción de mensajes
thread_recepcion = threading.Thread(target=recibir_mensajes)
thread_recepcion.start()

# Bucle principal para enviar mensajes
while True:
    message = input("Ingrese un mensaje ('exit' para salir): ")
    if message.lower() == 'exit':
        break
    else:
        clave = key_stream[contador_claves:contador_claves+len(message)]
        mensaje_cifrado = xor_bytes(clave, message.encode('utf-8'))
        client_socket.sendall(mensaje_cifrado)
        contador_claves += len(message)
# Esperar a que el hilo de recepción termine
thread_recepcion.join()

# Cerrar el socket
client_socket.close()


