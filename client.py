from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
import tkinter

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msgList.insert(tkinter.END,msg)
        except OSError:
            break

def send(evemt = None):
    msg = myMsg.get()
    myMsg.set("")
    client_socket.send(bytes(msg,"utf8"))
#   if msg == "{quit}":
     #   client_socket.close()
      #  top.quit()

def onClosing(event = None):
    myMsg.set("{quit}")
    send()

def qt(event = None):
    
    client_socket.send(bytes("{quit}","utf8"))
    send()
    client_socket.close()
    top.quit()
    


top = tkinter.Tk()
top.title("Let's Chat!")
msgFrame = tkinter.Frame(top)
myMsg = tkinter.StringVar()
myMsg.set("type your message here")
scBar = tkinter.Scrollbar(msgFrame)

msgList = tkinter.Listbox(msgFrame, height = 15, width = 100, yscrollcommand = scBar.set)
scBar.pack(side = tkinter.RIGHT,fill=tkinter.Y)
msgList.pack(side = tkinter.LEFT, fill= tkinter.BOTH)
msgList.pack()
msgFrame.pack()

eField = tkinter.Entry(top, textvariable=myMsg)
eField.bind("<Return>",send)
eField.pack()
sBut = tkinter.Button(top, text="Send", command = send)
sBut.pack()
stBut = tkinter.Button(top, text = "Quit", command = qt)
stBut.pack()
top.protocol("WM_DELETE_WINDOW", onClosing)


HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST,PORT)
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)

recThread = Thread(target=receive)
recThread.start()
tkinter.mainloop()