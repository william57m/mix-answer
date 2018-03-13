// Lib imports
import React from 'react';
import { Row, Col, Button } from 'react-bootstrap';
import EditorText from '../EditorText';

class ContentFormat extends React.Component {
    render() {
        const { type } = this.props;
        return (
            <div className={`content-format ${type === 'question' ? 'question-type' : 'answer-type'}`}>
                <div className="left-vote">
                    <div><i className={'fa fa-caret-up'} /></div>
                    <div>218</div>
                    <div><i className={'fa fa-caret-down'} /></div>
                </div>
                <div className="right-content">
                    <div>
                        help, not enough brains to solve the problem. The search does not give results when entering information about a category (an example of a search in the code, only in categories: heroes), you need to enter an appropriate value in the field and display the table for one element, depending on the category, heroes, ship or planet. In addition, it is desirable to enter a letter, display the necessary objects, ships or planets (for example: enter the letter d, and in the field I see: Darth Vader, dart sirius, etc.)
                        help, not enough brains to solve the problem. The search does not give results when entering information about a category (an example of a search in the code, only in categories: heroes), you need to enter an appropriate value in the field and display the table for one element, depending on the category, heroes, ship or planet. In addition, it is desirable to enter a letter, display the necessary objects, ships or planets (for example: enter the letter d, and in the field I see: Darth Vader, dart sirius, etc.)
                    </div>
                    {type === 'question' ?
                        <div className="description-tags">
                            <ul>
                                <li>swift</li>
                                <li>apple-watch</li>
                                <li>watch-os</li>
                                <li>wkinterfacecontroller</li>
                            </ul>
                        </div> : null
                    }
                    <div>
                        <span className="description-footer">
                            {`${type === 'question' ? 'asked' : 'answered'}`} 4 hours ago <span className="description-user">someuser</span>
                        </span>
                    </div>
                    <div>
                        <span className="user-action">edit</span>
                    </div>
                </div>
            </div>
        );
    }
}

class Answers extends React.Component {
    render() {
        const answers = [1, 2, 3, 4, 5];
        return (
            answers.length > 0 ?
                <React.Fragment>
                    <div className="separator">
                        {answers.length} Answers
                    </div>
                    <ContentFormat type="answer"/>
                    <ContentFormat type="answer"/>
                    <ContentFormat type="answer"/>
                    <ContentFormat type="answer"/>
                </React.Fragment> : null
        );
    }
}

class Question extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="question-title">
                    how to output the information entered into the search with a XMLHttpRequest
                </div>
                <ContentFormat type="question" />
            </React.Fragment>
        );
    }
}

class Reply extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="separator your-reply">
                    Your Answer
                </div>
                <EditorText />
                <div className="post-button">
                    <Button bsStyle="primary">Post Your Answer</Button>
                </div>
            </React.Fragment>
        );
    }
}

class QuestionView extends React.Component {
    render() {
        return (
            <div className="question-view">
                <Row>
                    <Col xs={1} md={2} lg={3} />

                    <Col className="question-content-container" xs={10} md={8} lg={6}>
                        <Question />
                        <Answers />
                        <Reply />
                    </Col>

                    <Col xs={1} md={2} lg={3}/>
                </Row>
            </div>
        );
    }
}

export default QuestionView;

