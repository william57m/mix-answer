// Lib imports
import { observer } from 'mobx-react';
import React from 'react';

// App imports
import QuestionList from './QuestionList';
import QuestionStore from '../../stores/question';
import Spinner from '../common/Spinner';


@observer
class QuestionsView extends React.Component {
    componentDidMount() {
        if (!QuestionStore.isLoaded) {
            QuestionStore.loadAll();
        }
    }
    render() {
        return (
            <div className="questions-container">
                {QuestionStore.isLoaded ?
                    <QuestionList /> :
                    <Spinner />
                }
            </div>
        );
    }
}

export default QuestionsView;
