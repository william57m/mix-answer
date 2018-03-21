// Lib imports
import React from 'react';

class InlineInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: props.value ? props.value : ''
        };
        this.onChange = this.onChange.bind(this);
    }
    onChange() {
        this.setState({text: this.refs.inputTitle.value});
    }
    render() {
        return (
            <div className={this.props.className}>
                <span className="question-ask-label">Title</span>
                <input ref="inputTitle"
                    value={this.state.text}
                    onChange={this.onChange}
                    placeholder="What is your question? Please be specific."/>
            </div>
        );
    }
}

export default InlineInput;
