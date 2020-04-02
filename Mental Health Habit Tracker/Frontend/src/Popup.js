import React from "react";
import "./Popup.scss";
import RadialGraphWorkSelfConfidence from "./components/RadialGraphWorkSelfConfidence";
import RadialGraphWorkMentalHealth from "./components/RadialGraphMentalHealth";
import LinearGraph from "./components/LinearGraph";
import { Row, Container, Col } from "react-bootstrap";

export default class Popup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selection: "learning"
    };
  }

  changeSelection = newSelection => {
    console.log(newSelection);
    this.setState({ selection: newSelection });
  };

  render() {
    let stats;

    console.log(this.props.questionaire);

    switch (this.props.questionaire) {
      case "Self-confidence":
        stats = (
          <Row>
            <Col>
              <RadialGraphWorkSelfConfidence
                changeSelection={this.changeSelection}
                style="position:float-left"
              />
            </Col>
            <Col>
              <LinearGraph
                selection={this.state.selection}
                style="position:float-right"
                questionaire="work-self-confidence"
              />
            </Col>
          </Row>
        );
        break;
      case "Mental Health":
        stats = (
          <Row>
            <Col>
              <RadialGraphWorkMentalHealth
                changeSelection={this.changeSelection}
                style="position:float-left"
              />
            </Col>
            <Col>
              <LinearGraph
                selection={this.state.selection}
                style="position:float-right"
                questionaire="mental-health"
              />
            </Col>
          </Row>
        );
    }

    return (
      <div className="popup">
        <div className="popup_inner">
          {this.props.questionaire}
          <Container>{stats}</Container>
          <button onClick={this.props.closePopup}>Close</button>
        </div>
      </div>
    );
  }
}
