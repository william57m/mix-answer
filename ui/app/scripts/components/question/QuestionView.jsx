// Lib imports
import { observer } from 'mobx-react';
import moment from 'moment';
import React from 'react';

// App imports
import AnswerStore from '../../stores/answer';
import CONSTANTS from '../../services/constants';
import EditorText from '../common/EditorText';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';
import SessionStore from '../../stores/session';
import TagRow from '../common/TagRow';


class Answer extends React.Component {
    constructor(props) {
        super(props);
        this.delete = this.delete.bind(this);
    }
    vote(upDown) {
        if (this.props.type === 'question') {
            QuestionStore.vote(this.props.question.id, upDown);
        } else {
            AnswerStore.vote(this.props.answer.id, upDown);
        }
    }
    delete() {
        if (this.props.type === 'question') {
            QuestionStore.delete(this.props.question.id).then(() => {
                RouteService.goTo('/questions');
            });
        } else {
            AnswerStore.delete(this.props.answer.id);
        }
    }
    render() {
        var canEdit;
        var canDelete;
        const type = this.props.type;
        var user;
        var date;
        var vote;
        if (type === 'question') {
            canEdit = SessionStore.user && SessionStore.user.id === this.props.question.creator_id;
            canDelete = SessionStore.user && SessionStore.user.id === this.props.question.creator_id;
            date = moment(this.props.question.created_at).format(CONSTANTS.DATETIME_FORMAT);
            user = this.props.question.user.firstname + ' ' + this.props.question.user.lastname;
            vote = this.props.question.votes;
        } else {
            canEdit = SessionStore.user && SessionStore.user.id === this.props.answer.creator_id;
            canDelete = SessionStore.user && SessionStore.user.id === this.props.answer.creator_id;
            date = moment(this.props.answer.created_at).format(CONSTANTS.DATETIME_FORMAT);
            user = this.props.answer.user.firstname + ' ' + this.props.answer.user.lastname;
            vote = this.props.answer.votes;
        }
        return (
            <div className={`content-format ${type === 'question' ? 'question-type' : 'answer-type'}`}>
                <div className="left-vote">
                    <div><i className={'fa fa-caret-up'} onClick={this.vote.bind(this, true)} /></div>
                    <div>{vote}</div>
                    <div><i className={'fa fa-caret-down'} onClick={this.vote.bind(this, false)} /></div>
                </div>
                <div className="right-content">
                    {type === 'question' ?
                        <div dangerouslySetInnerHTML={{__html: this.props.question.body}} /> :
                        <div dangerouslySetInnerHTML={{__html: this.props.answer.body}} />
                    }
                    {type === 'question' ?
                        <TagRow tags={this.props.question.tags} /> : null
                    }
                    <div>
                        <span className="description-footer">
                            {`${type === 'question' ? 'asked' : 'answered'}`} {date} <span className="description-user">{user}</span>
                        </span>
                    </div>
                    <div>
                        {canEdit ?
                            <span className="user-action">edit</span> : null
                        }
                        {canDelete ?
                            <span className="user-action" onClick={this.delete}>delete</span> : null
                        }
                    </div>
                </div>
            </div>
        );
    }
}

@observer
class Answers extends React.Component {
    render() {
        const answers = this.props.answers.map(answer => {
            return (
                <Answer key={answer.id} answer={answer} />
            );
        });
        return (
            answers.length > 0 ?
                <React.Fragment>
                    <div className="separator">
                        {answers.length} Answers
                    </div>
                    {answers}
                </React.Fragment> : null
        );
    }
}

class Question extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="question-title">
                    {this.props.question.title}
                </div>
                <Answer type="question" question={this.props.question} />
            </React.Fragment>
        );
    }
}

class Reply extends React.Component {
    constructor(props) {
        super(props);
        this.postAnswer = this.postAnswer.bind(this);
    }
    postAnswer() {
        var questionId = this.props.question.id;
        var body = this.refs.inputAnswer.state.text;
        AnswerStore.create(questionId, body);
    }
    render() {
        return (
            <React.Fragment>
                <div className="separator your-reply">
                    Your Answer
                </div>
                <EditorText ref="inputAnswer" />
                <div className="post-button">
                    <button className="btn btn-primary" onClick={this.postAnswer}>Post Your Answer</button>
                </div>
            </React.Fragment>
        );
    }
}

@observer
class QuestionView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questionId: this.props.match.params.id
        };
    }
    componentDidMount() {
        QuestionStore.setCurrent(this.state.questionId);
        AnswerStore.loadAll(this.state.questionId);
    }
    render() {
        var canReply = SessionStore.user ? true : false;
        var currentQuestion = QuestionStore.currentQuestion;
        var answers = AnswerStore.answers;
        return (
            <div className="question-view">
                <div className="question-content-container">
                    {currentQuestion ?
                        <React.Fragment>
                            <Question question={currentQuestion} />
                            <Answers answers={answers} />
                        </React.Fragment> : null
                    }
                    {currentQuestion && canReply ?
                        <Reply question={currentQuestion} /> : null
                    }
                </div>
            </div>
        );
    }
}

export default QuestionView;
