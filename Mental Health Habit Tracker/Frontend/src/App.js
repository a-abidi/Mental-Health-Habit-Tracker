import React from "react";
import { Router, Switch, Link, Route, Redirect } from "react-router-dom";
import "./App.scss";
import MenuContainer from "./components/MenuContainer";
import Login from "./LoginScreen";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: false
    };
  }

  logIn = () => {
    this.setState({
      loggedIn: true
    });
  };

  render() {
    return (
      <div className="App">
        <Switch>
          <PrivateRoute
            path="/"
            component={MenuContainer}
            state={this.state.loggedIn}
            logIn={this.logIn}
          />
        </Switch>
      </div>
    );
  }
}

const PrivateRoute = ({ component, logIn, state, ...options }) => {
  const FinalComponent = state ? component : Login;

  return (<Route {...options} render={(props) => <FinalComponent logIn={logIn}/>} />);
}
