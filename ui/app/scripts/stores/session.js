// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class SessionStore {
    @observable user = null;
    @observable isLoaded = false;

    init() {
        return $.get(URL.init).then(result => {
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
        return $.ajax({
            method: 'POST',
            url: URL.login,
            dataType: 'json',
            data: JSON.stringify({email: email, password: password})
        }).then(result => {
            this.user = result;
            this.isLoaded = true;
        }, () => {
            this.isLoaded = true;
        });
    }

    logout() {
        return $.ajax({
            method: 'POST',
            url: URL.logout
        }).then(() => {
            this.user = null;
        });
    }
}

export default new SessionStore();
