// Lib imports
import React from 'react';

// App imports
import RouteService from '../../services/RouteService';


class NavBar extends React.Component {
    render() {
        return (
            <div className="answer-header">
                <div className="header-wrapper">
                    <div className="header-logo" onClick={() => RouteService.goTo('/questions')}>
                        <img className="header-img" src="/resources/images/mix-logo.png"/>
                        <div className="header-title">answer</div>
                    </div>
                    <div className="header-input">
                        <input type="text" placeholder="Search..." />
                    </div>
                    <ul className="header-buttons-container header-buttons-container-right">
                        <li onClick={() => RouteService.goTo('/question/ask')}><a>Ask a Question</a></li>
                        <li><a><i className="fa fa-user"/> John</a></li>
                        <li><a><i className="fa fa-lock"/> Log in</a></li>
                    </ul>
                </div>
            </div>
        );
    }
}

export default NavBar
