// Lib imports
import React from 'react';
import { Col, Row, Button } from 'react-bootstrap';
import { WithContext as ReactTags } from 'react-tag-input';
import EditorText from '../EditorText';

class TagInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tags: [{ id: 1, text: 'Thailand' }, { id: 2, text: 'India' }],
            suggestions: ['USA', 'Germany', 'Austria', 'Costa Rica', 'Sri Lanka', 'Thailand']
        };

        // Bind functions
        this.handleDelete = this.handleDelete.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.handleDrag = this.handleDrag.bind(this);
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
    handleDrag(tag, currPos, newPos) {
        let tags = this.state.tags;

        // mutate array
        tags.splice(currPos, 1);
        tags.splice(newPos, 0, tag);

        // re-render
        this.setState({ tags: tags });
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
                handleAddition={this.handleAddition}
                handleDrag={this.handleDrag} />
        );
    }
}

class AskQuestionView extends React.Component {
    render() {
        return (
            <div className="question-ask-container">
                <Row>
                    <Col xs={1} md={2} lg={3} />

                    <Col className="question-ask-title" xs={10} md={8} lg={6}>
                        <span className="question-ask-label">Title</span>
                        <input placeholder="What is your question? Please be specific."/>
                    </Col>

                    <Col xs={1} md={2} lg={3}/>
                </Row>
                <Row>
                    <Col xs={1} md={2} lg={3} />

                    <Col className="question-ask-body" xs={10} md={8} lg={6}>
                        <EditorText />
                    </Col>

                    <Col xs={1} md={2} lg={3} />
                </Row>
                <Row>
                    <Col xs={1} md={2} lg={3} />

                    <Col className="question-ask-tag" xs={10} md={8} lg={6}>
                        <TagInput />
                    </Col>

                    <Col xs={1} md={2} lg={3} />
                </Row>
                <Row>
                    <Col xs={1} md={2} lg={3} />

                    <Col className="question-ask-tag" xs={10} md={8} lg={6}>
                        <Button bsStyle="primary">Post Your Question</Button>
                    </Col>

                    <Col xs={1} md={2} lg={3} />
                </Row>
            </div>
        );
    }
}

export default AskQuestionView;
