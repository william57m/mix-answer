// Lib imports
import React from 'react';

// App imports
import NavBar from './common/NavBar';


class App extends React.Component {
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
