// Lib imports
import React from 'react';


class TagRow extends React.Component {
    render() {
        const tags = this.props.tags.map(tag => {
            return (
                <li key={tag}>{tag}</li>
            );
        });
        return (
            <div className="description-tags">
                <ul>
                    {tags}
                </ul>
            </div>
        );
    }
}

export default TagRow;
