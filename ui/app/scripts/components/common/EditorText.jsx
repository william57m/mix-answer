// Lib imports
import React from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

class EditorText extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            html: props.value ? props.value : ''
        };

        this.modules = {
            toolbar: [
                ['bold', 'italic', 'underline', 'strike'],
                ['blockquote', 'code-block'],

                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'script': 'sub'}, { 'script': 'super' }],
                [{ 'indent': '-1'}, { 'indent': '+1' }],
                [{ 'direction': 'rtl' }],

                [{ 'size': ['small', false, 'large', 'huge'] }],
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

                [{ 'color': [] }, { 'background': [] }],
                [{ 'font': [] }],
                [{ 'align': [] }],

                ['clean']
            ]
        };

        // Bind functions
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(html) {
        this.setState({ html: html });
    }
    clearForm() {
        this.setState({ html: '' });
    }
    render() {
        return (
            <div className={this.props.className}>
                <ReactQuill value={this.state.html}
                    modules={this.modules}
                    theme={'snow'}
                    onChange={this.handleChange} />
            </div>
        );
    }
}

export default EditorText;
