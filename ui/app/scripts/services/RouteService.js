// Lib imports
import { createHashHistory } from 'history';

// Create history
const history = createHashHistory();

// Working variables
class RouteService {

    // Navigation
    static goTo(path) {
        history.push({ pathname: path });
    }
    // Getters
    static getHistory() {
        return history;
    }
}

module.exports = RouteService;
