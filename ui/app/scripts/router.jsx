// Lib import
import React from 'react';
import { Route } from 'react-router';
import { Switch, Redirect } from 'react-router';
import { HashRouter } from 'react-router-dom';

// Views
import App from './components/App';
import AskQuestionView from './components/ask/AskQuestionView';
import QuestionView from './components/question/QuestionView';
import QuestionsViews from './components/questions/QuestionsView';
import ProfileView from './components/profile/ProfileView';
import LoginView from './components/LoginView';

// Store
import SessionStore from './stores/session';


class ParentRoute extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLogged: false,
            initialized: false
        };
    }
    componentDidMount() {
        // Init state
        this.checkLogin();
    }
    componentWillReceiveProps() {
        // When location change check user
        this.checkLogin();
    }
    checkLogin() {
        SessionStore.isAuthenticated().then(() => {
            this.setState({isLogged: true, initialized: true});
        }, () => {
            this.setState({isLogged: false, initialized: true});
        });
    }
    render() {
        var displayRoute = this.props.private ? this.state.isLogged : !this.state.isLogged;
        var redirect = this.props.private ? '/login' : '/';
        return (
            this.state.initialized ?
                (displayRoute ?
                    <Route {...this.props} /> :
                    <Redirect to={redirect} />
                ) :
                <span />
        );
    }
}

class MainComponent extends React.Component {
    render() {
        return (
            <HashRouter>
                <App>
                    <Switch>
                        <ParentRoute path="/login" component={LoginView} />
                        <Route path="/questions" component={QuestionsViews} />
                        <ParentRoute private path="/question/ask" component={AskQuestionView} />
                        <ParentRoute private path="/profile" component={ProfileView} />
                        <Route path="/question/:id" component={QuestionView} />
                        <Redirect to={'/questions'} />
                    </Switch>
                </App>
            </HashRouter>
        );
    }
}

export default MainComponent;
