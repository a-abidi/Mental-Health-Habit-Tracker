import React, { Component } from "react";
import { VictoryChart, VictoryLine, VictoryAxis } from "victory";

const myBlue = "#75b2ff";

class LinearGraph extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wholeData: [],
      ready: false,
      selection: props.selection
    };
  }

  componentDidMount() {
    fetch(
      "http://127.0.0.1:5000/" +
        this.props.questionaire +
        "/overview?username=67611589",
      {
        mode: "cors"
      }
    )
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState({
          wholeData: data,
          ready: true
        });
      });
  }

  render() {
    if (!this.state.ready) {
      return null;
    }

    var currentData = this.state.wholeData.map(a => {
      console.log(this.props.selection);
      console.log({ x: new Date(a.date), y: a[this.props.selection] });
      return { x: new Date(a.date), y: a[this.props.selection] };
    });

    return (
      <VictoryChart scale={{ x: "time" }}
                    animate={{ duration: 500 }}
      >
        <VictoryLine
          style={{
            data: { stroke: "#75b2ff" },
            parent: { border: "1px solid #ccc" }
          }}
          data={currentData}
          maxDomain={{ y: 4 }}
          minDomain={{ y: 0 }}
        />
        <VictoryAxis
          dependentAxis
          width={400}
          height={400}
          domain={[0, 4]}
          standalone={false}
        />
        <VictoryAxis
          independentAxis
          width={400}
          height={400}
          standalone={false}
        />
      </VictoryChart>
    );
  }
}
export default LinearGraph;
