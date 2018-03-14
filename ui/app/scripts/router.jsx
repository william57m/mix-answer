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
import LoginView from './components/LoginView';


class ParentRoute extends React.Component {
    // In the future, add login logic here
    render() {
        return <Route {...this.props} />;
    }
}

const PrivateAppRoutes = () => (
    <App>
        <Switch>
            <Route path="/questions" component={QuestionsViews} />
            <Route path="/question/ask" component={AskQuestionView} />
            <Route path="/question/:id" component={QuestionView} />
            <Redirect to={'/questions'} />
        </Switch>
    </App>
);

class MainComponent extends React.Component {
    render() {
        return (
            <HashRouter>
                <App>
                    <Switch>
                        <Route path="/login" component={LoginView} />
                        <Route path="/questions" component={QuestionsViews} />
                        <Route path="/question/ask" component={AskQuestionView} />
                        <Route path="/question/:id" component={QuestionView} />
                        <Redirect to={'/questions'} />
                    </Switch>
                </App>
            </HashRouter>
        );
    }
}

export default MainComponent;
