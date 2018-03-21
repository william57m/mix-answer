// Lib imports
import React from 'react';
import { observer } from 'mobx-react';


// App imports
import InlineInput from '../common/InlineInput';
import TagInput from '../common/TagInput';
import EditorText from '../common/EditorText';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';
import SessionStore from '../../stores/session';


@observer
class AskQuestionView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            errors: []
        };
        this.postQuestion = this.postQuestion.bind(this);
    }
    componentDidMount() {
        if (SessionStore.isLoaded && !SessionStore.user) {
            RouteService.goTo('/login');
        }
    }

    postQuestion() {
        const title = this.refs.inputTitle.state.text;
        const body = this.refs.inputBody.state.html;
        const tags = this.refs.inputTag.getTags();
        const errors = [];
        if (title.length < 6) {
            errors.push('Title has to have at least 6 characters');
        }
        if (body.length < 6) {
            errors.push('Message body has to have at least 6 characters');
        }
        if (tags < 1) {
            errors.push('You must select at least one tag');
        }
        if (errors.length === 0) {
            QuestionStore.create(title, body, tags).then((result) => {
                RouteService.goTo(`/question/${result.data.id}`);
            });
        }
        this.setState({ errors: errors });
    }
    render() {
        return (
            <div className="question-ask-container">
                { this.state.errors.length > 0 ?
                    <ul className="error-box">
                        { this.state.errors.map((error, i) => <li key={i}>{error}</li>) }
                    </ul> : null
                }
                <InlineInput className="question-ask-title" ref="inputTitle" />
                <EditorText className="question-ask-body" ref="inputBody" />
                <TagInput className="question-ask-tag" ref="inputTag" />
                <div className="question-ask-tag">
                    <button className="btn btn-primary" onClick={this.postQuestion}>Post Your Question</button>
                </div>
            </div>
        );
    }
}

export default AskQuestionView;
