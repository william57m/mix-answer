// Lib imports
import React from 'react';

// App imports
import NavBar from './common/NavBar';
import SessionStore from '../stores/session';


class App extends React.Component {
    componentDidMount() {
        SessionStore.init();
    }
    render() {
        return (
            <React.Fragment>
                <NavBar />
                <div className="answer-page">
                    {this.props.children}
                </div>
            </React.Fragment>
        );
    }
}

export default App;
