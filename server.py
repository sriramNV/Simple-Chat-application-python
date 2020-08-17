from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread


def acceptIncommingConnections():
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s has connected" %clientAddress )
        client.send(bytes("Greeting from the Engineers Cave! \nNow type your NAME and press ENTER","utf8"))
        addresses[client] = clientAddress
        Thread(target=handleClient, args=(client,)).start()


def handleClient(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'welcome %s! ' %name
    client.send(bytes(welcome,"utf8"))
    msg = "%s has joined the chat!" %name
    broadcast(bytes(msg,"utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}","utf8"):
            broadcast(msg, name+': ')
        else:
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat" %name, "utf8"))
            break

def broadcast(msg, prefix = ""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)



clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(7)
    print("waiting for connection")
    ACCEPT_THREAD = Thread(target=acceptIncommingConnections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

