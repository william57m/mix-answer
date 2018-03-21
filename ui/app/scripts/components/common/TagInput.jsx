// Lib imports
import React from 'react';
import { observer } from 'mobx-react';
import { WithContext as ReactTags } from 'react-tag-input';
import TagStore from '../../stores/tag';

@observer
class TagInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tags: props.tags ? props.tags.map(tag => { return { text: tag }; }) : [],
            suggestions: TagStore.tags.map(tag => tag.label)
        };

        // Bind functions
        this.handleDelete = this.handleDelete.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
    }
    handleDelete(i) {
        let tags = this.state.tags;
        tags.splice(i, 1);
        this.setState({tags: tags});
    }
    handleAddition(tag) {
        let tags = this.state.tags;
        tags.push({
            text: tag
        });
        this.setState({tags: tags});
    }
    getTags() {
        return this.state.tags.map(tag => tag.text);
    }
    render() {
        return (
            <div className={this.props.className}>
                <ReactTags
                    classNames={{
                        tags: 'tags',
                        tagInput: 'tag-input',
                        tagInputField: 'tag-input-field',
                        selected: 'tag-selected',
                        tag: 'tag',
                        remove: 'tag-remove',
                        suggestions: 'tags-suggestions',
                        activeSuggestion: 'tag-active'
                    }}
                    tags={this.state.tags}
                    suggestions={this.state.suggestions}
                    handleDelete={this.handleDelete}
                    handleAddition={this.handleAddition} />
            </div>
        );
    }
}

export default TagInput;
