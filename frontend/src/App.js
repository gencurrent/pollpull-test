import React from "react";
import ReactDOM from 'react-dom';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';
import PollControl from './components/PollControl';
import PollGo from './components/PollGo';
import PollResult from './components/PollResult';

const App = () => (
    <Router>
        <div>
            <Route exact path='/' component={PollControl}></Route>
            <Route exact path='/poll-go/:id' component={PollGo}></Route>
            <Route exact path='/poll-result/:id' component={PollResult}></Route>
        </div>
    </Router>
);
export default App;

