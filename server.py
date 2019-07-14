from flask import Flask, request
import Controller
import threading
import asyncio
# import RPi.GPIO as GPIO

# perform some setup
app = Flask(__name__)
controller = Controller.drink_controller()
loop = asyncio.get_event_loop()


@app.route("/")
def mainpage():
    return app.send_static_file('drinkPage.html')


@app.route("/config")
def get_config():
    return app.send_static_file('config.json')


@app.route("/order/<drinkId>", methods=['POST'])
def order_drink(drinkId):
    return controller.add_drink(drinkId)


@app.route("/ready", methods=['GET'])
def make_drink():
    if controller.is_busy:
        return 'I\'m currently making a drink, Please try again later.'
    if controller.drinkQueue.empty():
        return 'There are no drinks in the queue!'
    else:
        t = threading.Thread(target=controller.makeNext, args=(loop,))
        t.start()
        return 'Making next drink in queue.'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    # GPIO.cleanup()
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    app.run()
