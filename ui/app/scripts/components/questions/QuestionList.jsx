// Lib imports
import React from 'react';
import ReactPaginate from 'react-paginate';

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
            <React.Fragment>
                <div className="question-list">
                   {questions}
                </div>
                {this.props.total > this.props.limit ?
                    <ReactPaginate
                        breakLabel={<a href="">...</a>}
                        breakClassName={"break-me"}
                        forcePage={this.props.currentPage}
                        pageCount={this.props.nbPage}
                        onPageChange={this.props.onPageChange}
                        containerClassName={"pagination"}
                        subContainerClassName={"pages pagination"}
                        activeClassName={"active"} /> : null
                }
            </React.Fragment>
        );
    }
}

export default QuestionList;
