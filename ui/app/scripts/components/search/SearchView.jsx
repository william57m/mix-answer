// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import QuestionRow from '../questions/QuestionRow';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';


@observer
class SearchView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: []
        };

        // Bind functions
        this.onRouteChange = this.onRouteChange.bind(this);
    }
    componentDidMount() {
        var params = RouteService.getParams();
        var value = params.q;
        this.search(value);
        this.setState({value: value});

        RouteService.subscribeOnRouteChange(this.onRouteChange);
    }
    componentWillUnmount() {
        RouteService.unsubscribeOnRouteChange(this.onRouteChange);
    }

    search(value) {
        if (value) {
            QuestionStore.search(value).then((result) => {
                this.setState({questions: result.data});
            });
        }
    }

    // Listener
    onRouteChange() {
        var params = RouteService.getParams();
        var value = params.q;
        this.search(value);
        this.setState({value: value});
    }

    render() {
        const questions = this.state.questions.map(question => {
            return (
                <QuestionRow key={question.id} question={question} />
            );
        });
        return (
            <div className="questions-container">
                <h4>Results for "{this.state.value}"</h4>
                {questions ?
                    questions :
                    'No results'
                }
            </div>
        );
    }
}

export default SearchView;
