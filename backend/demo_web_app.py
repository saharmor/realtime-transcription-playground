import asyncio

import socketio
from aiohttp import web

from gspeech_utils import GSpeechUtils

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins=[])  # * is bad

# Binds our Socket.IO server to our Web App instance
sio.attach(app)


@asyncio.coroutine
@sio.on('startGoogleCloudStream')
async def start_google_stream(sid, config):
    print(f'Starting streaming audio data from client {sid}')
    await GSpeechUtils.start_recognition_stream(sio, sid, config)


@sio.on('binaryAudioData')
async def receive_binary_audio_data(sid, message):
    GSpeechUtils.receive_data(sid, message)


@sio.on('endGoogleCloudStream')
async def close_google_stream(sid):
    print(f'Closing streaming data from client {sid}')
    await GSpeechUtils.stop_recognition_stream(sid)


web.run_app(app, port=10000)
