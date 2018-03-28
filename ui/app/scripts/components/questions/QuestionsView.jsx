// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import QuestionHeader from './QuestionHeader';
import QuestionList from './QuestionList';
import QuestionStore from '../../stores/question';
import Spinner from '../common/Spinner';


@observer
class QuestionsView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // Tab
            activeTab: 'all',
            // Pagination
            limit: 25,
            page: 0,
            total: 0,
            nbPage: 0
        };
        this.onPageChange = this.onPageChange.bind(this);
        this.selectTab = this.selectTab.bind(this);
    }
    componentDidMount() {
        if (!QuestionStore.isLoaded) {
            this.loadQuestions();
        }
    }

    // Actions
    onPageChange(page) {
        this.setState({page: page.selected}, () => {
            this.loadQuestions()
        });
    }
    selectTab(tab) {
        this.setState({activeTab: tab, page: 0}, () => {
            this.loadQuestions();
        });
    }

    // Request
    loadQuestions() {
        QuestionStore.loadAll(this.state.limit, this.state.page*this.state.limit, this.state.activeTab === 'unanswered').then((result) => {
            this.setState({
                total: result.metadata.total,
                nbPage: Math.ceil(result.metadata.total / this.state.limit)
            });
        });
    }

    render() {
        return (
            <div className="questions-container">
                <QuestionHeader activeTab={this.state.activeTab} selectTab={this.selectTab} />
                {QuestionStore.isLoaded ?
                    QuestionStore.questions.length ?
                        <QuestionList
                            questions={QuestionStore.questions}
                            total={this.state.total}
                            limit={this.state.limit}
                            currentPage={this.state.page}
                            nbPage={this.state.nbPage}
                            onPageChange={this.onPageChange} />  :
                        <div className="empty-view">
                            <h4>No results</h4>
                        </div> :
                    <Spinner />
                }
            </div>
        );
    }
}

export default QuestionsView;
