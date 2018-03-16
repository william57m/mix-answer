// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class AnswerStore {
    @observable answers = [];
    @observable isLoaded = false;

    loadAll(questionId) {
        this.isLoaded = false;
        var promise = $.get(URL.answers.replace(':questionId', questionId));
        promise.then(result => {
            this.answers = result.data;
            this.isLoaded = true;
        });
        return promise;
    }
}

export default new AnswerStore();
