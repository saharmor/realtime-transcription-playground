import React from "react";
import {Button} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import speechToTextUtils from "./utility_transcribe";
import TranscribeOutput from "./TranscribeOutput";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentData: [],
      recording: false,
    };
    this.onStart = this.onStart.bind(this);
    this.onStop = this.onStop.bind(this);
  }

  onStart() {
    this.setState({recording: true, currentData: ''});

    speechToTextUtils.initRecording((data) => {
      this.setState(prevState => ({
        currentData: [...prevState.currentData, data]
      }))
    }, (error) => {
      console.error('Error when recording', error);
      this.setState({recording: false});
      // No further action needed, as this already closes itself on error
    });
  }

  onStop() {
    this.setState({recording: false});
    speechToTextUtils.stopRecording();
  }


  render() {
    return (
      <div>
        <TranscribeOutput currentData={this.state.currentData}/>
        {!this.state.recording && <Button onClick={this.onStart} color="primary">Listen</Button>}
        {this.state.recording && <Button onClick={this.onStop} color="secondary">Stop</Button>}
      </div>
    );
  }
}

export default App;
