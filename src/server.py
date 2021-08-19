import threading
import socket

host = input("IP to host (Press Enter to use localhost (127.0.0.1) as default): ")
if host == "":
    host = "127.0.0.1"
port = input("Port to host (Press Enter to use 55555 as default): ")
if port == "":
    port = 55555
else:
    try:
        port = int(port)
    except:
        print("Sorry, wrong input. Please try again.")
        exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            print(f'the client nicknamed as {nickname} has disconnected.')
            broadcast(f'[SERVER]: {nickname} has left.\nOnline Users: {nicknames}'.encode('utf-8'))
            break

def receive():
    while True:
        client, adress = server.accept()
        print(f'{str(adress)} connected.')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'nickname of the client is {nickname}.')
        broadcast(f'[SERVER]: {nickname} has joined.\nOnline Users: {nicknames}'.encode('utf-8'))
        #client.send("connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is starting...")
receive()