<p align="center">
  <img width="60px" src="https://user-images.githubusercontent.com/6180201/124313197-cc93f200-db70-11eb-864a-fc65765fc038.png" alt="giant microphone"/><br/>
  <h2 align="center">Realtime Transcription Playground</h2>
</p>

A real-time transcription project using React and socketio. The goal of this project is to enable developers to create web demos or speech2text prototypes with just a few lines of code.

[Demo - FIX LINK]()


# Installation
* Google Speech API enabled for your project (see [below - FIX]())
* Python 3 [instructions](https://realpython.com/installing-python/)
* `yarn` ([instructions](https://classic.yarnpkg.com/en/docs/install/#mac-stable)) or `npm` ([instructions](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm))

## Enable Google Speech API
The `GOOGLE_SERVICE_JSON_FILE` environment file must be properly set and point to a valid service account file.

If you need to get a service account:
  - Within your Google Cloud console, create or select a project
  - Enable the Cloud Speech API for that project
  - Create a service account
  - Download a private key as JSON

More info here : https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#before-you-begin<br/>

Then, set the environment variable `GOOGLE_SERVICE_JSON_FILE` to the file path of the JSON file containing your service account key.

Further details can be found in this [Medium article - FIX]()

# Setup
1. Clone or fork this repository
2. Create a virtual environment in the root directory: `python -m venv $ENV_NAME`
3. Activate the virtual environment: ` source $ENV_NAME/bin/activate` (for MacOS, Unix, or Linux users) or ` .\ENV_NAME\Scripts\activate` (for Windows users)
4. Install requirements: `pip install -r api/requirements.txt`
5. Set your environment variable `GOOGLE_SERVICE_JSON_FILE` to point to your file path
6. Run `yarn install` or `npm install` in the root directory
