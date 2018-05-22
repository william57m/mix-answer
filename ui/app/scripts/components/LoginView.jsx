// Lib import
import React from 'react';

// App imports
import CONSTANTS from '../services/constants';
import RouteService from '../services/RouteService';
import SessionStore from '../stores/session';


class LoginPage extends React.Component {
    constructor() {
        super();
        this.state = {
            // Credentials
            username: '',
            password: '',
            // Errors
            formErrorMessage: '',
            // State
            isLoggingIn: false,
            isDisabledButton: true
        };

        // Bind functions
        this.login = this.login.bind(this);
        this.onKeyUp = this.onKeyUp.bind(this);
        this.onChange = this.onChange.bind(this);
        this.goToSignup = this.goToSignup.bind(this);
    }

    // Actions
    login() {
        var formErrorMessage = this._validateForm();
        if (formErrorMessage) {
            this.setState({formErrorMessage: formErrorMessage});
            return;
        }

        this.setState({isLoggingIn: true});
        SessionStore.login(this.state.username, this.state.password).done((result) => {
            RouteService.goTo(CONSTANTS.defaultRoute);
        }).fail(() => {
            this.setState({
                isLoggingIn: false,
                formErrorMessage: 'Wrong email/password. Try again.'
            });
        });
    }
    goToSignup() {
        RouteService.goTo('/signup');
    }

    // On change handlers
    onKeyUp(event) {
        if (event.which === 13 && !this.state.isDisabledButton) {
            this.login();
        }
    }
    onChange(input) {
        switch (input) {
            case 'email': this.setState({username: this.emailInput.value}); break;
            case 'password': this.setState({password: this.passwordInput.value}); break;
        }
        this._toggleButton();
    }

    // Utils
    _toggleButton() {
        this.setState({
            isDisabledButton: this.emailInput.value === '' || this.passwordInput.value === ''
        });
    }
    _validateForm() {
        // Values
        var email = this.state.username;
        var password = this.state.password;
        // Check value
        if (!email || (CONSTANTS.regex.email.test(email) === false && CONSTANTS.regex.username.test(email) === false)) {
            return 'You need to supply an email address or a username.';
        } else if (!password) {
            return 'You need to supply a password.';
        } else {
            return '';
        }
    }

    render() {
        return (
            <div className="login-page">
                <div className="login-form" onKeyUp={this.onKeyUp}>
                    <div className="description">
                        Please enter your email address and password
                    </div>
                    <div className="form-group">
                        <input className="form-control" name="username" disabled={this.state.isLoggingIn} type="email" onChange={this.onChange.bind(this, 'email')} ref={(c) => this.emailInput = c} placeholder="Email" autoComplete="on" autoFocus/>
                    </div>
                    <div className="form-group">
                        <input className="form-control" name="password" disabled={this.state.isLoggingIn} type="password" onChange={this.onChange.bind(this, 'password')} ref={(c) => this.passwordInput = c} placeholder="Password" autoComplete="on"/>
                    </div>
                    {this.state.formErrorMessage ?
                        <div className="form-group has-error">
                            <span className="help-block">{this.state.formErrorMessage}</span>
                        </div> : null
                    }
                    <div className="login-actions">
                        <button className="btn btn-default" onClick={this.login} disabled={this.state.isDisabledButton || this.state.isLoggingIn}>Log In</button>
                        {SessionStore.features.ldap_enabled ? null :
                            <span className="btn-action-signup" onClick={this.goToSignup}>
                                <a>Sign up</a>
                            </span>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

export default LoginPage;
