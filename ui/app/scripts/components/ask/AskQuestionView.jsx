// Lib imports
import React from 'react';
import { observer } from 'mobx-react';
import { WithContext as ReactTags } from 'react-tag-input';

// App imports
import EditorText from '../common/EditorText';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';
import SessionStore from '../../stores/session';


class TagInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tags: [],
            suggestions: ['USA', 'Germany', 'Austria', 'Costa Rica', 'Sri Lanka', 'Thailand']
        };

        // Bind functions
        this.handleDelete = this.handleDelete.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
    }
    handleDelete(i) {
        let tags = this.state.tags;
        tags.splice(i, 1);
        this.setState({tags: tags});
    }
    handleAddition(tag) {
        let tags = this.state.tags;
        tags.push({
            text: tag
        });
        this.setState({tags: tags});
    }
    getTags() {
        return this.state.tags.map(tag => tag.text);
    }
    render() {
        return (
            <ReactTags
                classNames={{
                    tags: 'tags',
                    tagInput: 'tag-input',
                    tagInputField: 'tag-input-field',
                    selected: 'tag-selected',
                    tag: 'tag',
                    remove: 'tag-remove',
                    suggestions: 'tags-suggestions',
                    activeSuggestion: 'tag-active'
                }}
                tags={this.state.tags}
                suggestions={this.state.suggestions}
                handleDelete={this.handleDelete}
                handleAddition={this.handleAddition} />
        );
    }
}

@observer
class AskQuestionView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: '',
            body: ''
        };
        this.onBodyChange = this.onBodyChange.bind(this);
        this.onTitleChange = this.onTitleChange.bind(this);
        this.postQuestion = this.postQuestion.bind(this);
    }
    componentDidMount() {
        if (SessionStore.isLoaded && !SessionStore.user) {
            RouteService.goTo('/login');
        }
    }

    // On change handlers
    onBodyChange(state) {
        this.setState({body: state.blocks[0].text});
    }
    onTitleChange() {
        this.setState({title: this.refs.inputTitle.value});
    }
    postQuestion() {
        var title = this.state.title;
        var body = this.state.body;
        var tags = this.refs.inputTag.getTags();
        QuestionStore.create(title, body, tags).then((result) => {
            RouteService.goTo(`/question/${result.data.id}`);
        });
    }
    render() {
        return (
            <div className="question-ask-container">
                <div className="question-ask-title">
                    <span className="question-ask-label">Title</span>
                    <input ref="inputTitle" value={this.state.title} onChange={this.onTitleChange} placeholder="What is your question? Please be specific."/>
                </div>
                <div className="question-ask-body">
                    <EditorText onChange={this.onBodyChange} />
                </div>
                <div className="question-ask-tag">
                    <TagInput ref="inputTag" />
                </div>
                <div className="question-ask-tag">
                    <button className="btn btn-primary" onClick={this.postQuestion}>Post Your Question</button>
                </div>
            </div>
        );
    }
}

export default AskQuestionView;
