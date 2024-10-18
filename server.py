from counter import Counter
from flask import Flask, render_template
from flask_sock import Sock
import json
import os

app = Flask(__name__)

env = os.getenv("FLASK_ENV", "development")

if env == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

sock = Sock(app)
counter = Counter()
clients = set()

@app.route("/")
def home_page():
    return render_template("./index.html", websocket_url=app.config["WEBSOCKET_URL"])


@app.route("/admin")
def admin_page():
    print("counter.getCount() = ", counter.getCount())
    return render_template(
        "./admin.html",
        counter_value=counter.getCount(),
        websocket_url=app.config["WEBSOCKET_URL"],
    )

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
        new_clients = clients.copy()
        for client in clients:
            try:
                client.send(json.dumps({"number": counter.getCount()}))
                print("coutner.getCount() = ", counter.getCount())
            except Exception as e:
                print(f"Error sending message to client: {e}")
                new_clients.remove(client)
        clients = new_clients
