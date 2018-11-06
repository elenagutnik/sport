
from .Race import EventDefiner

from .. import socketio
from .. import celery
import json
from celery import shared_task
import redis

import eventlet

eventlet.monkey_patch()

def send_message(EVENT_NAME, DATA):
    print('Socket')
    socketio.emit(EVENT_NAME, json.dumps(DATA))

@celery.task
def dataHandler(data):
    # have_lock = False
    # my_lock = redis.Redis().lock("dataIn")
    # try:
    #     have_lock = my_lock.acquire(blocking=False)
    from manage import app
    with app.app_context(), app.test_request_context():
        racehandler = EventDefiner(data)
        racehandler.HandleData()
        print(racehandler.EVENT_NAME)
        print('racehandler.isDataForSend ', racehandler.isDataForSend)
        if racehandler.isDataForSend:
            print('socket data ', racehandler.EVENT_NAME, json.dumps(racehandler.resultView()))
            socketio.emit(racehandler.EVENT_NAME, json.dumps(racehandler.resultView()))
    return None, None
    # finally:
    #     if have_lock:
    #         my_lock.release()
