// Lib imports
import React from 'react';


class Tabs extends React.Component {
    render() {
        return (
            <ul className="tabs">
                <li className={this.props.activeTab === 'unanswered' ? 'active' : ''} onClick={() => this.props.selectTab('unanswered')}>Unanswered</li>
                <li className={this.props.activeTab === 'all' ? 'active' : ''} onClick={() => this.props.selectTab('all')}>All</li>
            </ul>
        );
    }
}

class QuestionHeader extends React.Component {
    render() {
        var title = this.props.activeTab === 'all' ? 'All Questions' :
                    this.props.activeTab === 'unanswered' ? 'Unanswered Questions' : 'Questions'
        return (
            <div className="questions-header">
                <div className="title">
                    <h4>{title}</h4>
                </div>
                <div className="filter">
                    <Tabs activeTab={this.props.activeTab} selectTab={this.props.selectTab} />
                </div>
            </div>
        );
    }
}

export default QuestionHeader;
