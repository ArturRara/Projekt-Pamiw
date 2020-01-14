import React, {Component} from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom'
import './App.css';
//import {render} from "react-dom";


import login from './components/login'
import register from './components/register'
import Navbar  from './components/navbar'
import profile from './components/profile'
import upload from "./components/upload";


class App extends Component{
  render()
  {
    return (
        <div className="App">
          <Router>
            <div className="App">
              <Navbar />
              <Route exact path="/" component={login} />
              <div className="container">
                <Route exact path="/register" component={register} />
                <Route exact path="/profile" component={profile} />
                <Route exact path="/upload" component={upload} />
              </div>
            </div>
          </Router>
        </div>
    );
  }
}
export default App;
