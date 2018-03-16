// Lib imports
import React from 'react';
import { Col, Row, Button } from 'react-bootstrap';
import { WithContext as ReactTags } from 'react-tag-input';

// App imports
import EditorText from '../common/EditorText';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';


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
            id: tags.length + 1,
            text: tag
        });
        this.setState({tags: tags});
    }
    render() {
        return (
            <ReactTags classNames={{
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
        QuestionStore.create(title, body).then((result) => {
            RouteService.goTo(`/question/${result.data.id}`);
        });
    }
    render() {
        return (
            <div className="question-ask-container">
                <Row>
                    <Col className="question-ask-title">
                        <span className="question-ask-label">Title</span>
                        <input ref="inputTitle" value={this.state.title} onChange={this.onTitleChange} placeholder="What is your question? Please be specific."/>
                    </Col>
                </Row>
                <Row>
                    <Col className="question-ask-body">
                        <EditorText onChange={this.onBodyChange} />
                    </Col>
                </Row>
                <Row>
                    <Col className="question-ask-tag">
                        <TagInput />
                    </Col>
                </Row>
                <Row>
                    <Col className="question-ask-tag">
                        <Button bsStyle="primary" onClick={this.postQuestion}>Post Your Question</Button>
                    </Col>
                </Row>
            </div>
        );
    }
}

export default AskQuestionView;
