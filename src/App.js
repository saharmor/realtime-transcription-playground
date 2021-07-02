import React, {useState} from "react";
import {Button} from "react-bootstrap";
import withStyles from "@material-ui/core/styles/withStyles";
import Typography from "@material-ui/core/Typography";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import speechToTextUtils from "./utility_transcribe";
import TranscribeOutput from "./TranscribeOutput";
import SettingsSections from "./SettingsSection";

const useStyles = () => ({
  root: {
    display: 'flex',
    flex: '1',
    margin: '100px 0px 100px 0px',
    alignItems: 'center',
    textAlign: 'center',
    flexDirection: 'column',
  },
  title: {
    marginBottom: '20px',
  },
  settingsSection: {
    marginBottom: '20px',
  },
  buttonsSection: {
    marginBottom: '40px',
  },
});

const App = ({classes}) => {
  const [transcribedData, setTranscribedData] = useState([]);
  const [interimTranscribedData, setInterimTranscribedData] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en-US');

  const supportedLanguages = {'en-US': 'English', 'de-DE': 'German', 'fr-FR': 'French', 'es-ES': 'Spanish'}

  function flushInterimData() {
    if (interimTranscribedData !== '') {
      setInterimTranscribedData('')
      setTranscribedData(oldData => [...oldData, interimTranscribedData])
    }
  }

  function handleDataReceived(data, isFinal) {
    if (isFinal) {
      setInterimTranscribedData('')
      setTranscribedData(oldData => [...oldData, data])
    } else {
      setInterimTranscribedData(data)
    }
  }

  function getTranscriptionConfig() {
    return {
      audio: {
        encoding: 'LINEAR16',
        sampleRateHertz: 16000,
        languageCode: selectedLanguage,
      },
      interimResults: true
    }
  }

  function onStart() {
    setTranscribedData([])
    setIsRecording(true)

    speechToTextUtils.initRecording(
      getTranscriptionConfig(),
      handleDataReceived,
      (error) => {
        console.error('Error when transcribing', error);
        setIsRecording(false)
        // No further action needed, as stream already closes itself on error
      });
  }

  function onStop() {
    setIsRecording(false)
    flushInterimData() // A safety net if Google's Speech API doesn't work as expected, i.e. always sends the final result
    speechToTextUtils.stopRecording();
  }

  return (
    <div className={classes.root}>
      <div className={classes.title}>
        <Typography variant="h3">
          Your Transcription App <span role="img" aria-label="microphone-emoji">🎤</span>
        </Typography>
      </div>
      <div className={classes.settingsSection}>
        <SettingsSections possibleLanguages={supportedLanguages} selectedLanguage={selectedLanguage}
                          onLanguageChanged={setSelectedLanguage}/>
      </div>
      <div className={classes.buttonsSection}>
        {!isRecording && <Button onClick={onStart} variant="primary">Start transcribing</Button>}
        {isRecording && <Button onClick={onStop} variant="danger">Stop</Button>}
      </div>
      <div>
        <TranscribeOutput transcribedText={transcribedData} interimTranscribedText={interimTranscribedData}/>
      </div>
    </div>
  );
}

export default withStyles(useStyles)(App);
