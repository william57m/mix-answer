// Lib imports
import React from 'react';
import RouteService from '../services/RouteService';

class NavBar extends React.Component {
    render() {
        const { pathname } = RouteService.getHistory().location;
        return (
            <div className="answer-header">
                <div className="mix-header-logo">
                    <img src="/resources/images/MixLogoHeader.png"/>
                </div>
                <div className="mix-title">.answer</div>
                <ul className="mix-buttons-container">
                    <li className={`${pathname === '/questions' ? 'active' : ''}`} onClick={() => RouteService.goTo('/questions')}><a>Answer Questions</a></li>
                    <li className={`${pathname === '/question/ask' ? 'active' : ''}`} onClick={() => RouteService.goTo('/question/ask')}><a>Ask a Question</a></li>
                </ul>
                <ul className="right mix-buttons-container">
                    <li><a><i className="fa fa-user"/> John</a></li>
                    <li><a><i className="fa fa-lock"/> Log out</a></li>
                </ul>
            </div>
        );
    }
}

class App extends React.Component {
    render() {
        return (
            <React.Fragment>
                <NavBar />

                {/* ======================== Content ======================== */}

                {this.props.children}
            </React.Fragment>
        );
    }
}

export default App;
