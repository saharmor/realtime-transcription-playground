import asyncio

import socketio
from aiohttp import web

from backend.gspeech_utils import GSpeechUtils

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins=[])  # * is bad

# Binds our Socket.IO server to our Web App instance
sio.attach(app)


@asyncio.coroutine
@sio.on('startGoogleCloudStream')
async def startGoogleCloudStream(sid, config):
    print('startGoogleCloudStream')
    await GSpeechUtils.start_recognition_stream(sio, sid, config)


@sio.on('binaryAudioData')
async def binaryAudioData(sid, message):
    GSpeechUtils.receive_data(sid, message)


@sio.on('endGoogleCloudStream')
async def endGoogleCloudStream(sid, message):
    print('endGoogleCloudStream')
    await GSpeechUtils.stop_recognition_stream(sid)


## We bind our aiohttp endpoint to our app router
# app.router.add_get('startGoogleCloudStream',startGoogleCloudStream)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app, port=10000)
