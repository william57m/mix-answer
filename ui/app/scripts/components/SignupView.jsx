// Lib import
import React from 'react';

// App imports
import CONSTANTS from '../services/constants';
import RouteService from '../services/RouteService';
import SessionStore from '../stores/session';


class SignupPage extends React.Component {
    constructor() {
        super();
        this.state = {
            // Data
            firstname: '',
            lastname: '',
            email: '',
            password: '',
            // Errors
            formErrorMessage: '',
            // State
            isSigningUp: false,
            isDisabledButton: true,
            hasSigned: true
        };

        // Bind functions
        this.onKeyUp = this.onKeyUp.bind(this);
        this.onChange = this.onChange.bind(this);
        this.signup = this.signup.bind(this);
    }

    // Actions
    goToLogin() {
        RouteService.goTo('/login');
    }
    signup() {
        this.setState({isSigningUp: true});
        SessionStore.signup(this.state.firstname, this.state.lastname, this.state.email, this.state.password).done(() => {
            this.setState({hasSigned: true});
        }).fail((error) => {
            this.setState({
                isSigningUp: false,
                formErrorMessage: error.responseJSON.error.message
            });
        });
    }

    // On change handlers
    onKeyUp(event) {
        if (event.which === 13 && !this.state.isDisabledButton) {
            this.signup();
        }
    }
    onChange(input) {
        switch (input) {
            case 'firstname': this.setState({firstname: this.firstnameInput.value}); break;
            case 'lastname': this.setState({lastname: this.lastnameInput.value}); break;
            case 'email': this.setState({email: this.emailInput.value}); break;
            case 'password': this.setState({password: this.passwordInput.value}); break;
        }
        this._toggleButton();
    }

    // Utils
    _toggleButton() {
        this.setState({
            isDisabledButton: this.firstnameInput.value === '' || this.lastnameInput.value === '' || this.emailInput.value === '' || this.passwordInput.value === ''
        });
    }

    render() {
        return (
            <div className="login-page">
                {!this.state.hasSigned ?
                    <div className="login-form" onKeyUp={this.onKeyUp}>
                        <div className="description">
                            Please enter your informations
                        </div>
                        <div className="form-group">
                            <input className="form-control" name="firstname" disabled={this.state.isSigningUp} type="text" onChange={this.onChange.bind(this, 'firstname')} ref={(c) => this.firstnameInput = c} placeholder="Firstname" autoFocus/>
                        </div>
                        <div className="form-group">
                            <input className="form-control" name="lastname" disabled={this.state.isSigningUp} type="text" onChange={this.onChange.bind(this, 'lastname')} ref={(c) => this.lastnameInput = c} placeholder="Lastname"/>
                        </div>
                        <div className="form-group">
                            <input className="form-control" name="email" disabled={this.state.isSigningUp} type="email" onChange={this.onChange.bind(this, 'email')} ref={(c) => this.emailInput = c} placeholder="Email"/>
                        </div>
                        <div className="form-group">
                            <input className="form-control" name="password" disabled={this.state.isSigningUp} type="password" onChange={this.onChange.bind(this, 'password')} ref={(c) => this.passwordInput = c} placeholder="Password"/>
                        </div>
                        {this.state.formErrorMessage ?
                            <div className="form-group has-error">
                                <span className="help-block">{this.state.formErrorMessage}</span>
                            </div> : null
                        }
                        <div className="login-actions">
                            <button className="btn btn-default" onClick={this.signup} disabled={this.state.isDisabledButton || this.state.isSigningUp}>Sign up</button>
                        </div>
                    </div> :
                    <div className="login-form">
                        <div>
                            Your account has been successfully created.
                        </div>
                        <button className="btn btn-default" onClick={this.goToLogin}>Log In</button>
                    </div>
                }
            </div>
        );
    }
}

export default SignupPage;
