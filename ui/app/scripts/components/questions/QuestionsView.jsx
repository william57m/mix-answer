// Lib imports
import React from 'react';
import { Row, Col } from 'react-bootstrap';
import RouteService from '../../services/RouteService';

class Tabs extends React.Component {
    render() {
        return (
            <ul className="right tabs">
                <li className={this.props.activeTab === 'today' ? 'active' : ''} onClick={() => this.props.selectTab('today')}>today</li>
                <li className={this.props.activeTab === 'interesting' ? 'active' : ''} onClick={() => this.props.selectTab('interesting')}>interesting</li>
            </ul>
        );
    }
}

class RowStat extends React.Component {
    render() {
        return (
            <span className="stat">
                <div className="stat-count">{this.props.count}</div>
                <div className="stat-label">{this.props.label}</div>
            </span>
        );
    }
}

class RowDescription extends React.Component {
    render() {
        return (
            <span className="description">
                <div onClick={() => RouteService.goTo('/question/123')} className="description-title">{this.props.title}</div>
                <div className="description-tags">
                    <ul>
                        <li>swift</li>
                        <li>apple-watch</li>
                        <li>watch-os</li>
                        <li>wkinterfacecontroller</li>
                    </ul>
                </div>
                <div>
                    <span className="description-footer">
                        modified {this.props.date} <span className="description-user">{this.props.user}</span>
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
                    <RowStat count={3} label={'votes'}/>
                    <RowStat count={6} label={'answer'}/>
                    <RowStat count={500} label={'views'}/>
                </span>
                <span className="questions-description">
                    <RowDescription title={'analyzing crash dumps with debian kernel packages'}
                        date={'Mar 5 at 17:34'}
                        user={'glagolig'} />
                </span>
            </div>
        );
    }
}
class QuestionList extends React.Component {
    render() {
        return (
            <React.Fragment>
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
               <QuestionRow />
            </React.Fragment>
        );
    }
}
class QuestionsView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTab: 'interesting'
        };
    }
    render() {
        return (
            <div className="questions-view-container">
                <Row>
                    <Col xs={1} md={2} lg={2} />

                    <Col className="questions-header" xs={10} md={8} lg={8}>
                        <Col bsClass="left" md={4}>
                            <h4 className="left">Top Questions</h4>
                        </Col>
                        <Col bsClass="right" md={8}>
                            <Tabs activeTab={this.state.activeTab} selectTab={tab => this.setState({ activeTab: tab })}/>
                        </Col>
                    </Col>

                    <Col xs={1} md={2} lg={2}/>
                </Row>
                <Row>
                    <Col xs={1} md={2} lg={2} />

                    <Col className="questions-body" xs={10} md={8} lg={8}>
                        <QuestionList />
                    </Col>

                    <Col xs={1} md={2} lg={2} />
                </Row>
            </div>
        );
    }
}

export default QuestionsView;
