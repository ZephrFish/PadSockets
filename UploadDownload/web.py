from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('upload')
def on_upload():
    filename = request.sid + '_' + request.values.get('filename')
    filesize = int(request.values.get('filesize'))
    filedata = request.values.get('filedata')
    with open(filename, 'wb') as f:
        f.write(filedata)
    print('File uploaded:', filename)
    emit('upload_success', {'filename': filename})

@socketio.on('download')
def on_download():
    filename = request.values.get('filename')
    if os.path.isfile(filename):
        filesize = os.path.getsize(filename)
        emit('filesize', str(filesize))
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                emit('filedata', data, binary=True)
        print('File sent:', filename)
    else:
        emit('download_error', 'File not found')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
