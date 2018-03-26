// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import RouteService from '../../services/RouteService';
import SessionStore from '../../stores/session';


class UserDropdown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showDropdown: false
        };

        // Bind functions
        this.goToProfile = this.goToProfile.bind(this);
        this.toggleDropdown = this.toggleDropdown.bind(this);
        this.logout = this.logout.bind(this);
        this.onBodyClick = this.onBodyClick.bind(this);
    }

    componentDidMount() {
        document.body.addEventListener('click', this.onBodyClick);
    }
    componentWillUnmount() {
        document.body.removeEventListener('click', this.onBodyClick);
    }
    onBodyClick(e) {
        if (this.state.showDropdown && !this.refs.list.contains(e.target)) {
            this.setState({ showDropdown: false });
        }
    }

    // Actions
    goToProfile() {
        RouteService.goTo('/profile')
    }
    logout() {
        SessionStore.logout();
        RouteService.goTo('/questions');
    }
    toggleDropdown() {
        this.setState({ showDropdown: !this.state.showDropdown });
    }
    render() {
        var username = `${this.props.user.firstname} ${this.props.user.lastname}`;
        return (
            <li className="user-dropdown-li" onClick={this.toggleDropdown} ref="list">
                <span>
                    <img className="user-img" src="resources/images/default_avatar.png" />
                    <i className="fa fa-chevron-down" />
                </span>
                <ul style={{ display: this.state.showDropdown ? 'block': 'none' }} className="dropdown-menu user-dropdown-menu">
                    <li onClick={this.goToProfile}><i className="fa fa-user"/> {username}</li>
                    <li onClick={this.logout}><i className="fa fa-lock" /> Logout</li>
                </ul>
            </li>
        );
    }
}

@observer
class NavBar extends React.Component {
    constructor(props) {
        super(props);
        this.onKeyUp = this.onKeyUp.bind(this);
    }
    onKeyUp(event) {
        if (event.which === 13) {
            var value = this.refs.searchInput.value;
            RouteService.goTo(`/search?q=${value}`);
        }
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
                        <li onClick={() => RouteService.goTo('/question/ask')}>Ask Question</li>
                        {user ?
                            <UserDropdown user={user} /> :
                            <li onClick={() => RouteService.goTo('/login')}>Log In</li>
                        }
                    </ul>
                </div>
            </div>
        );
    }
}

export default NavBar
