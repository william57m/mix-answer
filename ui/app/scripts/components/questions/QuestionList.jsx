// Lib imports
import React from 'react';

// App imports
import QuestionRow from './QuestionRow';
import QuestionStore from '../../stores/question';


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
