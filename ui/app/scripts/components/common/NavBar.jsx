// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import RouteService from '../../services/RouteService';
import SessionStore from '../../stores/session';


@observer
class NavBar extends React.Component {
    constructor(props) {
        super(props);
        this.logout = this.logout.bind(this);
    }
    logout() {
        SessionStore.logout();
    }
    render() {
        var user = SessionStore.user;
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
                        {user ?
                            <li><a><i className="fa fa-user"/> {user.firstname}</a></li> : null
                        }
                        {user ?
                            <li onClick={this.logout}><a><i className="fa fa-lock" /> Logout</a></li> :
                            <li onClick={() => RouteService.goTo('/login')}><a><i className="fa fa-lock" /> Log in</a></li>
                        }
                    </ul>
                </div>
            </div>
        );
    }
}

export default NavBar
