// Lib import
import React from 'react';
import { observer } from 'mobx-react';

// App imports
import SessionStore from '../../stores/session';


@observer
class ProfilePage extends React.Component {
    render() {
        var user = SessionStore.user || {};
        return (
            <div>
                <h3>Profile View</h3>
                <div className="form-group">
                    <input type="text" className="form-control" value={user.firstname} disabled />
                </div>
                <div className="form-group">
                    <input type="text" className="form-control" value={user.lastname} disabled />
                </div>
                <div className="form-group">
                    <input type="text" className="form-control" value={user.email} disabled />
                </div>
            </div>
        );
    }
}

export default ProfilePage;
