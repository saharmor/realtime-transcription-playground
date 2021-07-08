<p align="center">
  <img width="60px" src="https://user-images.githubusercontent.com/6180201/124313197-cc93f200-db70-11eb-864a-fc65765fc038.png" alt="giant microphone"/><br/>
  <h2 align="center">Real-time Transcription Playground</h2>
</p>

A real-time transcription project using React and a socketio python server. The goal of this project is to enable developers to create web demos and speech2text prototypes with just a few lines of code. Examples can be medical dictation apps, a note-taking CRM for entrepreneurs, etc.

*Currently only supports real-time transcription using Google Cloud Speech*

# Demo
https://user-images.githubusercontent.com/6180201/124362454-370e6600-dc35-11eb-8374-77da5aec25b2.mp4


# Installation
* Python 3 [instructions](https://realpython.com/installing-python/)
* `yarn` [instructions](https://classic.yarnpkg.com/en/docs/install/#mac-stable)

## Google Speech API
The code assumes an environment variable `GOOGLE_SERVICE_JSON_FILE` that points to a valid GCP service account file.

If you need to get a service account:
  - Within your Google Cloud console, create or select a project
  - Enable the Cloud Speech API for that project
  - Create a service account
  - Download a private key as JSON

More info in Google Cloud's docs [here](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin) and [here](https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3#0).<br/>

Then, set the environment variable `GOOGLE_SERVICE_JSON_FILE` to the path of the JSON file containing your service account key, e.g. `/users/sahar/documents/sample-project-3c1a5892b00e.json`. Further details can be found in this [Medium article](https://medium.com/geekculture/how-to-build-a-full-stack-transcription-app-with-google-cloud-react-and-python-2dfdcb5e556f).

# Setup
1. Clone or fork this repository
2. Create a virtual environment in the root directory: `python -m venv $ENV_NAME`
3. Activate the virtual environment: ` source $ENV_NAME/bin/activate` (for MacOS, Unix, or Linux users) or ` .\ENV_NAME\Scripts\activate` (for Windows users)
4. Install requirements: `pip install -r backend/requirements.txt`
5. Set your environment variable `GOOGLE_SERVICE_JSON_FILE` to point to your file path
6. Run `yarn install` in the root directory
7. Run `yarn start` to start the frontend and `start-backend` to run the backend
