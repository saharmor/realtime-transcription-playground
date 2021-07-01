import asyncio
import queue
import re
import sys
import threading
import wave

from google.cloud import speech

clients = {}


class ClientData:
    def __init__(self, transcribe_thread, conn):
        self._buff = queue.Queue()
        self._thread = transcribe_thread
        self._closed = True
        self._conn = conn

    async def close(self):
        self._closed = True
        self._buff.put(None)
        self._thread.join()
        await self._conn.emit('endGoogleCloudStream', '')

    def start_transcribing(self):
        self._closed = False
        self._thread.start()

    def add_data(self, data):
        self._buff.put(data)

    def generator(self):
        print('generator')
        while not self._closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return

            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

    async def send_client_data(self, data):
        await self._conn.emit('speechData', data)


async def listen_print_loop(responses, client: ClientData):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)
        else:
            text = transcript + overwrite_chars
            # red.publish(text, u'[%s] %s: %s' % (datetime.now, 'user', 'message'))
            print(text)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            if client:
                await client.send_client_data(text)

            num_chars_printed = 0


class GSpeechUtils:
    recognizeStream = None
    config = None
    speech_client = None
    chunks = 0

    @staticmethod
    def _wrapper(gen):
        for m in gen:
            print("here", m)
            yield m

    @staticmethod
    async def start_listen(client_id):
        print('start_listen')
        language_code = "en-US"
        speech_client = speech.SpeechClient.from_service_account_json('json_file')
        config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                          sample_rate_hertz=16000, language_code=language_code,
                                          enable_automatic_punctuation=True)
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

        client = clients[client_id]
        audio_generator = client.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
        responses = speech_client.streaming_recognize(streaming_config, requests)
        await listen_print_loop(responses, client)

        # In case of ERROR
        # client.emit('googleCloudStreamError', err);

        # client._conn.emit('endGoogleCloudStream', '')
        print('done listening')

    @staticmethod
    async def start_recognition_stream(sio, client_id: str, config):
        if client_id not in clients:
            clients[client_id] = ClientData(threading.Thread(target=asyncio.run, args=(GSpeechUtils.start_listen(client_id),)), sio)
            clients[client_id].start_transcribing()
        else:
            print('Already running transcription for client')

    @staticmethod
    async def stop_recognition_stream(client):
        if client in clients:
            await clients[client].close()
            del clients[client]

    @staticmethod
    def receive_data_to_file(client, data):
        if GSpeechUtils.chunks > 200:
            frames = []
            chunk = GSpeechUtils._buff.get()
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = GSpeechUtils._buff.get(block=False)
                    if chunk is None:
                        return
                    frames.append(chunk)
                except queue.Empty:
                    break

            # for i in range(0, int(16000 / 1024 * 10)):
            #     data = GSpeechUtils._buff.get(1024)
            #     frames.append(data)

            waveFile = wave.open('test.wav', 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(2)
            waveFile.setframerate(16000)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
        else:
            GSpeechUtils._buff.put(data)
            GSpeechUtils.chunks += 1

    @staticmethod
    def receive_data(client, data):
        if client not in clients:
            return

        clients[client].add_data(data)

        # if end of utterance, let's restart stream
        # this is a small hack. After 65 seconds of silence, the stream will still throw an error for speech length limit

        # if data.results[0] and data.results[0].isFinal:
        #     GSpeechUtils.stop_recognition_stream()
        #     GSpeechUtils.start_recognition_stream(client)
        # else:
        #     GSpeechUtils.recognizeStream = speech_client.streaming_recognize(config)
