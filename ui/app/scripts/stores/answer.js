// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class AnswerStore {
    @observable answers = [];
    @observable isLoaded = false;

    loadAll(questionId) {
        this.isLoaded = false;
        $.get(URL.answers.replace(':questionId', questionId)).then(result => {
            this.answers = result.data;
            this.isLoaded = true;
        });
    }
}

export default new AnswerStore();
