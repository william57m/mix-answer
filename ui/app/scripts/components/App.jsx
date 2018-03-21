// Lib imports
import React from 'react';

// App imports
import NavBar from './common/NavBar';
import SessionStore from '../stores/session';
import TagStore from '../stores/tag';

class App extends React.Component {
    componentDidMount() {
        Promise.all([
            SessionStore.init(),
            TagStore.init()
        ]);
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
