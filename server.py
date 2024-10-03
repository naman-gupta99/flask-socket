from flask import Flask, render_template
from flask_socketio import SocketIO

def Counter():
    def __init__(self):
        self.__count = 0
    
    def increment(self):
        self.__count += 1
    
    def getCount(self):
        return self.__count

app = Flask(__name__)
socketio = SocketIO(app)
counter = Counter()

@app.route("/")
def page1():
    return render_template("./page1.html")


@app.route("/page2")
def page2():
    return render_template("./page2.html")

@socketio.on("increment")
def handle_increment():
    print("Incrementing counter")
    counter.increment()

    print("Emitting update_counter event")
    # Broadcast the updated counter to both pages
    socketio.emit("update_counter", {"number": counter.getCount()})


if __name__ == "__main__":
    socketio.run(app)
