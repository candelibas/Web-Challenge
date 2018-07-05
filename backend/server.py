from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g
from flask_socketio import SocketIO, emit, send
import requests, json, datetime
from threading import Lock
from database import read_reviews_daily, save_review_daily

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

server = Flask(__name__)
server.config['SECRET_KEY'] = 'totallysecret'
socketio = SocketIO(server, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    while True:
        print("hiammına")
        socketio.emit('message', get_avg_rating())
        socketio.sleep(10) # 3600 in seconds = 1 hour

@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    # emit('message', "Connected!")


def get_avg_rating():
    uri = "https://www.udemy.com/api-2.0/courses/1178124?fields[course]=@min,avg_rating" # 1178124
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"  
    jResponse = uResponse.text
    courseData = json.loads(jResponse)
    avgRating = str(courseData['avg_rating'])
    courseTitle = str(courseData['title'])

    todayDate = datetime.datetime.today().strftime('%d.%m.%Y')
    nowTime = datetime.datetime.today().strftime('%H:%M')
    save_review_daily(avgRating, courseTitle, todayDate, nowTime)
    
    return avgRating + "," + courseTitle + "," + todayDate + "," + nowTime


if __name__ == "__main__":
    # socketio.run(host='0.0.0.0', port=9000, debug=True)
    socketio.run(server, host='0.0.0.0', port=9000, debug=True)