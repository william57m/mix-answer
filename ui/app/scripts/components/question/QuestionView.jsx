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
import TagInput from '../common/TagInput';
import InlineInput from '../common/InlineInput';
import Spinner from '../common/Spinner';

@observer
class Answer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isEditing: false,
            errors: []
        };
        this.delete = this.delete.bind(this);
        this.edit = this.edit.bind(this);
        this.save = this.save.bind(this);
    }
    edit() {
        this.setState({isEditing: this.props.type});
    }
    save() {
        if (this.props.type === 'answer') {
            const { answer } = this.props;
            const { editAnswer } = this.refs;
            AnswerStore.edit(answer.id, {
                ...answer,
                body: editAnswer.state.html
            }).then(() => {
                this.setState({isEditing: false});
            });
        } else {
            const { question } = this.props;
            const { inputTitle, editQuestion, inputTag } = this.refs;

            const title = inputTitle.state.text;
            const body = editQuestion.state.html;
            const tags = inputTag.getTags();

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
            this.setState({ errors: errors });
            if (errors.length === 0) {
                QuestionStore.edit(question.id, {
                    ...question,
                    title: title,
                    body: body,
                    tags: tags
                }).then(() => {
                    this.setState({isEditing: false});
                });
            }
        }
    }
    vote(upDown) {
        if (this.props.type === 'question') {
            QuestionStore.vote(this.props.question.id, upDown);
        } else {
            AnswerStore.vote(this.props.answer.id, upDown);
        }
    }
    delete() {
        if (confirm(`Are you sure you want to delete your ${this.props.type}?`)) {
            if (this.props.type === 'question') {
                QuestionStore.delete(this.props.question.id).then(() => {
                    RouteService.goTo('/questions');
                });
            } else {
                AnswerStore.delete(this.props.answer.id);
            }
        }
    }
    render() {
        var canEdit;
        var canDelete;
        const type = this.props.type;
        var user;
        var userName;
        var date;
        var vote;
        var imageUrl;
        if (type === 'question') {
            canEdit = SessionStore.user && SessionStore.user.id === this.props.question.creator_id;
            canDelete = SessionStore.user && SessionStore.user.id === this.props.question.creator_id;
            date = moment(this.props.question.created_at).fromNow();
            user = this.props.question.user;
            userName = this.props.question.user.firstname + ' ' + this.props.question.user.lastname;
            vote = this.props.question.votes;
            imageUrl = this.props.question.user.gravatar_url;
        } else {
            canEdit = SessionStore.user && SessionStore.user.id === this.props.answer.creator_id;
            canDelete = SessionStore.user && SessionStore.user.id === this.props.answer.creator_id;
            date = moment(this.props.answer.created_at).fromNow();
            user = this.props.answer.user;
            userName = this.props.answer.user.firstname + ' ' + this.props.answer.user.lastname;
            vote = this.props.answer.votes;
        }
        const editAnswer = (
            this.state.isEditing === 'answer' ?
                <div className="edit-answer">
                    <EditorText ref="editAnswer" value={this.props.answer.body} />
                    <button className="btn btn-primary" onClick={this.save}>
                        <i className="fa fa-edit"/>Save
                    </button>
                    <button className="btn" onClick={() => this.setState({isEditing: false})}>Cancel</button>
                </div> : null
        );
        const editQuestion = (
            this.state.isEditing === 'question' ?
                <div className="edit-question">
                    { this.state.errors.length > 0 ?
                        <ul className="error-box">
                            { this.state.errors.map((error, i) => <li key={i}>{error}</li>) }
                        </ul> : null
                    }
                    <InlineInput ref="inputTitle" value={this.props.question.title} />
                    <EditorText ref="editQuestion" value={this.props.question.body} />
                    <TagInput ref="inputTag" tags={this.props.question.tags} />
                    <button className="btn btn-primary" onClick={this.save}>
                        <i className="fa fa-edit"/>Save
                    </button>
                    <button className="btn" onClick={() => this.setState({isEditing: false})}>Cancel</button>
                </div> : null
        );
        const normal = (
            !this.state.isEditing ?
                <React.Fragment>
                    {type === 'question' ?
                        <div dangerouslySetInnerHTML={{__html: this.props.question.body}} /> :
                        <div className="content-body" dangerouslySetInnerHTML={{__html: this.props.answer.body}} />
                    }
                    {type === 'question' ?
                        <TagRow tags={this.props.question.tags} /> : null
                    }
                    <div className="description-footer">
                        <div className="description-img">
                            <img src={user.gravatar_url} />
                        </div>
                        <div className="description-content">
                            <div>{`${type === 'question' ? 'asked' : 'answered'}`} {date}</div>
                            <div className="description-user">{userName} ({user.nb_answers} <i className="fa fa-star"/>)</div>
                        </div>
                    </div>
                    <div>
                        {canEdit ?
                            <span onClick={this.edit} className="user-action">edit</span> : null
                        }
                        {canDelete ?
                            <span className="user-action" onClick={this.delete}>delete</span> : null
                        }
                    </div>
                </React.Fragment> : null
        );
        return (
            <div className={`content-format ${type === 'question' ? 'question-type' : 'answer-type'}`}>
                <div className="left-vote">
                    <div><i className={'fa fa-caret-up'} onClick={this.vote.bind(this, true)} /></div>
                    <div>{vote}</div>
                    <div><i className={'fa fa-caret-down'} onClick={this.vote.bind(this, false)} /></div>
                </div>
                <div className="right-content">
                    { editAnswer }
                    { editQuestion }
                    { normal }
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
                <Answer key={answer.id} answer={answer} type={'answer'} />
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
        var body = this.refs.inputAnswer.state.html;
        AnswerStore.create(questionId, body).then(() => {
            this.refs.inputAnswer.clearForm();
        });
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
                    { !currentQuestion || !AnswerStore.isLoaded || !QuestionStore.isCurrentLoaded ?
                        <Spinner /> :
                        <React.Fragment>
                            <Question question={currentQuestion} />
                            <Answers answers={answers} />
                        </React.Fragment>
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
