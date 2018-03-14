// Lib imports
import React from 'react';
import { Editor } from 'react-draft-wysiwyg';
import { EditorState } from 'draft-js';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';

class EditorText extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            editorState: EditorState.createEmpty()
        };

        // Bind functions
        this.onEditorStateChange = this.onEditorStateChange.bind(this);
    }
    onEditorStateChange(editorState) {
        this.setState({ editorState });
    }
    render() {
        return (
            <Editor editorState={this.state.editorState}
                toolbarClassName="editor-toolbar"
                wrapperClassName="editor-wrapper"
                editorClassName="editor"
                // toolbar={{
                //     blockType: {
                //     inDropdown: true,
                //     options: ['Normal', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Blockquote', 'Code'],
                //     className: undefined,
                //     component: undefined,
                //     dropdownClassName: undefined
                //     }
                // }}
                onEditorStateChange={this.onEditorStateChange} />
        );
    }
}

export default EditorText;
