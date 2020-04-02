import React, { Component } from "react";
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
  learning: "Learning",
  pressure: "Pressure",
  problem_solving: "Problem Solving",
  role_expectations: "Role Expectations",
  sensitivity: "Sensitivity",
  teamwork: "Teamwork",
  work_politics: "Work Politics"
};

class RadialGraphWorkSelfConfidence extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      withDateData: [],
      maxima: {
        learning: 5,
        pressure: 5,
        problem_solving: 5,
        role_expectations: 5,
        sensitivity: 5,
        teamwork: 5,
        work_politics: 5
      },
      ready: false
    };

    this.processData.bind(this);
  }

  componentDidMount() {
    fetch(
      "http://127.0.0.1:5000/work-self-confidence/overview?username=67611589",
      {
        mode: "cors"
      }
    )
      .then(response => {
        return response.json();
      })
      .then(data => {
        console.log(data);
        this.setState({
          data: this.processData(
            data.map(a => {
              delete a.date;
              return a;
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
      <VictoryChart
        polar
        theme={VictoryTheme.material}
        domain={{ y: [0, 1] }}
        animate={{ duration: 500 }}
      >
        <VictoryGroup
          colorScale={[myBlue]}
          style={{ data: { fillOpacity: 0.8, strokeWidth: 0 } }}
        >
          {this.state.data.map((data, i) => {
            if (i === 0) return <VictoryArea key={i} data={data} />;
          })}
        </VictoryGroup>
        {Object.keys(this.state.maxima).map((key, i) => {
          return (
            <VictoryPolarAxis
              key={i}
              dependentAxis
              style={{
                axisLabel: { padding: 10 },
                axis: { stroke: "none" },
                grid: {
                  stroke: myBlue,
                  strokeWidth: 0.25,
                  opacity: 0.5
                }
              }}
              tickLabelComponent={<VictoryLabel labelPlacement="vertical" />}
              labelPlacement="vertical"
              axisValue={i + 1}
              label={Titles[key]}
              tickFormat={t => Math.ceil(t * this.state.maxima[key])}
              tickValues={[0.25, 0.5, 0.75]}
              events={[
                {
                  target: "axisLabel",
                  eventHandlers: {
                    onClick: () => ({
                      target: "axisLabel",
                      mutation: () => {
                        console.log(key + " has been chosen");
                        this.props.changeSelection(key);
                        return null;
                      }
                    })
                  }
                }
              ]}
            />
          );
        })}
        <VictoryPolarAxis
          labelPlacement="parallel"
          tickFormat={() => ""}
          style={{
            axis: { stroke: "none" },
            grid: { stroke: myBlue, opacity: 1 }
          }}
        />
      </VictoryChart>
    );
  }
}
export default RadialGraphWorkSelfConfidence;
