// Lib imports
import moment from 'moment';
import React from 'react';

// App imports
import CONSTANTS from '../../services/constants';
import QuestionStore from '../../stores/question';
import RouteService from '../../services/RouteService';


class ItemStat extends React.Component {
    render() {
        return (
            <span className="stat">
                <div className="stat-count">{this.props.count}</div>
                <div className="stat-label">{this.props.label}</div>
            </span>
        );
    }
}

class ItemDescription extends React.Component {
    render() {
        const tags = this.props.question.tags.map(tag => {
            return (
                <li key={tag}>{tag}</li>
            );
        });
        return (
            <span className="description">
                <div onClick={() => RouteService.goTo(`/question/${this.props.question.id}`)} className="description-title">{this.props.question.title}</div>
                <div className="description-tags">
                    <ul>
                        {tags}
                    </ul>
                </div>
                <div>
                    <span className="description-footer">
                        modified {moment(this.props.question.created_at).format(CONSTANTS.DATETIME_FORMAT)} <span className="description-user">{this.props.question.user.firstname + ' ' + this.props.question.user.lastname}</span>
                    </span>
                </div>
            </span>
        );
    }
}

class QuestionRow extends React.Component {
    render() {
        return (
            <div className="questions-row">
                <span className="questions-stats">
                    <ItemStat count={'N/A'} label={'votes'}/>
                    <ItemStat count={this.props.question.nb_answers} label={'answer'}/>
                    <ItemStat count={'N/A'} label={'views'}/>
                </span>
                <span className="questions-description">
                    <ItemDescription question={this.props.question} />
                </span>
            </div>
        );
    }
}

class QuestionList extends React.Component {
    render() {
        const questions = QuestionStore.questions.map(question => {
            return (
                <QuestionRow key={question.id} question={question} />
            );
        });
        return (
            <div className="question-list">
               {questions}
            </div>
        );
    }
}

export default QuestionList;
