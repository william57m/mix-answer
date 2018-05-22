// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class SessionStore {
    @observable features = {};
    @observable user = null;
    @observable isLoaded = false;

    init() {
        return $.get(URL.init).then(result => {
            if (result.features) {
                this.features = result.features;
            }
            if (result.user) {
                this.user = result.user;
            }
        });
    }

    isAuthenticated() {
        return $.get(URL.authenticated);
    }

    login(email, password) {
        this.isLoaded = false;
        var promise = $.ajax({
            method: 'POST',
            url: URL.login,
            dataType: 'json',
            data: JSON.stringify({email: email, password: password})
        });
        promise.then(result => {
            this.user = result;
            this.isLoaded = true;
        }, () => {
            this.isLoaded = true;
        });
        return promise;
    }

    logout() {
        return $.ajax({
            method: 'POST',
            url: URL.logout
        }).then(() => {
            this.user = null;
        });
    }

    signup(firstname, lastname, email, password) {
        return $.ajax({
            method: 'POST',
            url: URL.signup,
            dataType: 'json',
            data: JSON.stringify({firstname: firstname, lastname: lastname, email: email, password: password})
        });
    }
}

export default new SessionStore();
