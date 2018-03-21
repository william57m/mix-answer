// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';

class TagStore {
    @observable tags = [];
    @observable isLoaded = false;

    init() {
        this.isLoaded = false;
        return $.get(URL.tags).then(result => {
            if (result.data) {
                this.tags = result.data;
            }
            this.isLoaded = true;
        });
    }
}

export default new TagStore();
