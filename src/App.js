import React from "react";
import { Form, Button, Row, Col } from "react-bootstrap";
import ClipLoader from "react-spinners/ClipLoader";

import axios from "axios";
import { debounce } from "lodash";

import "bootstrap/dist/css/bootstrap.min.css";

const UI_PARAMS_API_URL = "/params";
const TRANSLATE_API_URL = "/translate";

const DEBOUNCE_INPUT = 250;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    };
    // Bind the event handlers
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    // Call API for the UI params
    axios
      .get(UI_PARAMS_API_URL)
      .then(
        ({
          data: { placeholder, button_text, description }
        }) => {
          this.setState({
            input: placeholder,
            buttonText: button_text,
            description: description,
          });
        }
      );
  }


  handleInputChange(e) {
    this.setState({ input: e.target.value });
  }

  handleClick(e) {
    e.preventDefault();
    let body = {
      prompt: this.state.input
    };
    this.setState({ inProgress: true });
    axios.post(TRANSLATE_API_URL, body).then(({ data: { text } }) => {
      this.setState({ output: text });
      this.setState({ inProgress: false });
    });
  }

  render() {
    return (
      <div >
      <div style={{ alignItems: "center", justifyContent: "center" }}>
          <div
            style={{
              margin: "auto",
              marginTop: "80px",
              display: "block",
              maxWidth: "500px",
              minWidth: "200px",
              width: "50%"
            }}
          >
            <Form onSubmit={this.handleClick}>
              <Form.Group controlId="formBasicEmail">
                <Form.Label>{this.state.description}</Form.Label>
                <Form.Control
                  type="text"
                  as="textarea"
                  placeholder="Enter text"
                  value={this.state.input}
                  onChange={this.handleInputChange}
                />
              </Form.Group>

              <Button variant="primary" type="submit" disabled={this.state.inProgress}>
                {this.state.inProgress && <span>
                <ClipLoader loading={this.state.inProgress} size={20}/>&nbsp; &nbsp;
                </span>}
                {this.state.buttonText}
              </Button>
            </Form>
            <div
              style={{
                textAlign: "center",
                margin: "20px",
                fontSize: "18pt"
              }}
            >
              {this.state.output}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
