// Lib imports
import React from 'react';

// App imports
import QuestionRow from './QuestionRow';


class QuestionList extends React.Component {
    render() {
        const questions = this.props.questions.map(question => {
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
