from flask import Flask, render_template
from flask_sock import Sock
import json

class Counter():
    def __init__(self):
        self.__count = 0
    
    def increment(self):
        self.__count += 1
    
    def getCount(self):
        return self.__count

app = Flask(__name__)
sock = Sock(app)
counter = Counter()
clients = set()

@app.route("/")
def page1():
    return render_template("./page1.html")


@app.route("/page2")
def page2():
    return render_template("./page2.html", counter_value=counter.getCount())

@sock.route("/increment")
def handle_increment(ws):
    global clients
    clients.add(ws)
    while True:
        ws.receive()
        print("Incrementing counter")
        counter.increment()

        print("Emitting update_counter event")
        # Broadcast the updated counter to both pages
        for client in clients:
            new_clients = clients.copy()
            try:
                client.send(json.dumps({"number": counter.getCount()}))
            except Exception as e:
                print(f"Error sending message to client: {e}")
                new_clients.remove(client)
        clients = new_clients
