// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import QuestionList from '../questions/QuestionList';
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
        return (
            <div className="search-page">
                {this.state.questions.length ?
                    <h4>Results for "{this.state.value}"</h4> :
                    <h4>No result for "{this.state.value}"</h4>
                }
                {this.state.questions.length ?
                    <div className="questions-container">
                        <QuestionList questions={this.state.questions} />
                    </div> : null
                }
            </div>
        );
    }
}

export default SearchView;
