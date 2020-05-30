from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from argparse import ArgumentParser
from client_utility import *

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if "waiting" in msg:
                print("reverting the block")
                wallet.revert()
            verification = wallet.receive_broadcast(msg)
            if verification is not None:
                client_socket.send(bytes(verification, "utf8"))
            msg = '\n' + msg
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    parsed = msg.split(' ')
    if parsed[0] in cmd:
        param = []
        for i in range(1, len(parsed)):
            param.append(parsed[i])
        # Replace the msg with generated broadcast
        msg = str(cmd[parsed[0]](param))
    print(msg)
    if msg == "quit":
        client_socket.close()
        top.quit()
        return
    elif msg == "balance":
        my_msg.set(msg)
        return
    client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("quit")
    send()

def mine(event=None):
    mining_broadcast_message = wallet.mine()
    client_socket.send(bytes(mining_broadcast_message, "utf8"))

def balance(event=None):
    balance = wallet.get_balance()
    my_msg.set("My balance is " + str(balance))

if __name__ == "__main__":
    # Start Tinker Configuration
    top = tkinter.Tk()
    top.title("ECS 153 Babychain Simulator")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Text(messages_frame, height=25, width=75, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg, width=35)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    mine_button = tkinter.Button(top, text="Mine", command=mine)
    mine_button.pack()
    mine_button = tkinter.Button(top, text="Balance", command=balance)
    mine_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    # ----Now comes the sockets part----
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=23333, type=int, help='port to listen on')
    parser.add_argument('-ip', default='127.0.0.1', type=str)
    args = parser.parse_args()
    PORT = args.port
    HOST = args.ip
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()

    t = tkinter.Text(wrap=tkinter.WORD)
    t.pack()

    tkinter.mainloop()