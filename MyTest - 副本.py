
#import psutil
import time

from threading import Lock

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


thread = None
thread_lock = Lock()




def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        t = time.strftime('%M:%S', time.localtime())
        cpus = [1,2,3,4] #
        print('sending')
        socketio.emit('server_response',
                      {'data': [t, cpus[0],cpus[1],cpus[2],cpus[3]], 'count': count})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/t1')
def index1():
    return "hello world"


@socketio.on('connect', namespace='/tt')
def test_connect():
    global thread
    print('conn')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

@socketio.on('sendMsg')
def myhandle(jsondata):
    print('recv message')
    print(jsondata)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,debug=True)