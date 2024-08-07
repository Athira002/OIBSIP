# -*- coding: utf-8 -*-
"""chat_server.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m5n8nLCyYwlp2xvHwW8G3Iwlao-u7eoo
"""

import socket
import threading

def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                print(f"[{addr}] disconnected")
                break
            print(f"[{addr}] {msg}")
            # Broadcast message to all clients
            broadcast(msg)
        except Exception as e:
            print(f"Exception: {e}")
            break
    client_socket.close()

def broadcast(msg):
    for client in clients:
        try:
            client.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Exception: {e}")
            clients.remove(client)

def start_server():
    global clients
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    clients = []

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()

