// Lib imports
import { createHashHistory } from 'history';

// Create history
const history = createHashHistory();

// Working variables
var LISTENER = {};


class RouteService {

    // Navigation
    static goTo(path) {
        history.push({ pathname: path });
    }
    // Getters
    static getHistory() {
        return history;
    }
    static getParams() {
        var location = window.location.href.split('?')[1];
        if (!location) return {};

        var searchString = location;
        var searchArray = searchString.split('&');
        var params = {};
        searchArray.map((string) => {
            var keyValue = string.split('=');
            params[keyValue[0]] = decodeURIComponent(keyValue[1]);
        });
        return params;
    }

    // Listener
    static subscribeOnRouteChange(callback) {
        var listener = history.listen(callback);
        LISTENER[callback] = listener;
    }
    static unsubscribeOnRouteChange(callback) {
        var unlisten = LISTENER[callback];
        if (unlisten) {
            unlisten();
            delete LISTENER[callback];
        }
    }
}

module.exports = RouteService;
