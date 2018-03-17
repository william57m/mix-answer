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
    create(questionId, message) {
        var data = {
            message: message
        };
        var promise = $.ajax({
            method: 'POST',
            url: URL.answers.replace(':questionId', questionId),
            dataType: 'json',
            data: JSON.stringify(data)
        });
        promise.then(result => {
            this.answers.push(result.data);
        });
        return promise;
    }
    delete(id) {
        var promise = $.ajax({
            method: 'DELETE',
            url: URL.answer.replace(':answerId', id)
        });
        return promise;
    }
}

export default new AnswerStore();
