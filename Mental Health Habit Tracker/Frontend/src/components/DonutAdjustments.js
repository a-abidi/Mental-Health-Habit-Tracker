import React, { Component } from "react";
import ReactDOM from "react-dom";
import { VictoryBar } from "victory";
import {
  VictoryChart,
  VictoryTheme,
  VictoryLabel,
  VictoryPolarAxis,
  VictoryGroup,
  VictoryArea
} from "victory";

const myBlue = "#75b2ff";
var Titles;
Titles = {
  date: "Date",
  depression: "Depression",
  anxiety: "Anxiety",
  stress: "Stress"
};

class DonutAdjustments extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      withDateData: [],
      maxima: { depression: 36, stress: 42, anxiety: 42 },
      ready: false
    };
    this.processData.bind(this);
  }

  componentDidMount() {
    //Other endpoint
    fetch("http://127.0.0.1:5000/adjustments/overview?username=22222222", {
      mode: "cors"
    })
      .then(response => {
        return response.json();
      })
      .then(data => {
        console.log(data);
        this.setState({
          data: this.processData(
            data.map(a => {
              return {depression: a.depression, anxiety: a.anxiety, stress: a.stress};
            })
          ),
          ready: true,
          withDateData: data
        });
      });
  }

  processData(data) {
    const makeDataArray = d => {
      return Object.keys(d).map(key => {
        return { x: key, y: d[key] / this.state.maxima[key] };
      });
    };
    return data.map(datum => makeDataArray(datum));
  }

  render() {
    if (!this.state.ready) {
      return null;
    }

    return (
        <div>
        <svg viewBox="0 0 400 400" width="100%" height="100%">
          <VictoryPie
              standalone={false}
              animate={{ duration: 1000 }}
              width={400} height={400}
              data={this.state.data.polarity}
              innerRadius={120}
              cornerRadius={25}
              labels={() => null}
              style={{
                data: { fill: ({ datum }) => {
                    const color = datum.y > 30 ? "green" : "red";
                    return datum.x === 1 ? color : "transparent";
                  }
                }
              }}
          />
          <VictoryAnimation duration={1000} data={this.state}>
            {(newProps) => {
              return (
                  <VictoryLabel
                      textAnchor="middle" verticalAnchor="middle"
                      x={200} y={200}
                      text={`${Math.round(newProps.percent)}%`}
                      style={{ fontSize: 45 }}
                  />
              );
            }}
          </VictoryAnimation>
        </svg>
        </div>
    );
  }
}
export default DonutAdjustments;
