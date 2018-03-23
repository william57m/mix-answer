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
        this.onKeyUp = this.onKeyUp.bind(this);
    }
    onKeyUp(event) {
        if (event.which === 13) {
            var value = this.refs.searchInput.value;
            RouteService.goTo(`/search?q=${value}`);
        }
    }
    logout() {
        SessionStore.logout();
        RouteService.goTo('/questions');
    }
    render() {
        var user = SessionStore.user;
        return (
            <div className="answer-header">
                <div className="header-wrapper">
                    <div className="header-logo" onClick={() => RouteService.goTo('/questions')}>
                        <img className="header-img" src="resources/images/mix-logo-black.png"/>
                        <div className="header-title">answer</div>
                    </div>
                    <div className="header-input">
                        <input type="text" ref="searchInput" placeholder="Search..." onKeyUp={this.onKeyUp} />
                    </div>
                    <ul className="header-buttons-container header-buttons-container-right">
                        <li onClick={() => RouteService.goTo('/question/ask')}><a>Ask a Question</a></li>
                        {user ?
                            <li onClick={() => RouteService.goTo('/profile')}><a><i className="fa fa-user"/></a></li> : null
                        }
                        {user ?
                            <li onClick={this.logout}><a><i className="fa fa-lock" /></a></li> :
                            <li onClick={() => RouteService.goTo('/login')}><a><i className="fa fa-lock" /> Log in</a></li>
                        }
                    </ul>
                </div>
            </div>
        );
    }
}

export default NavBar
