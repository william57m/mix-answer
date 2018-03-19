// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class AnswerStore {
    @observable answers = [];
    @observable isLoaded = false;

    loadAll(questionId) {
        this.isLoaded = false;
        var promise = this._loadAll(questionId);
        promise.then(result => {
            this.answers = result.data;
            this.isLoaded = true;
        });
        return promise;
    }
    get(id) {
        var answer = null;
        this.answers.forEach(q => {
            if (q.id === id) {
                answer = q;
            }
        });
        return answer;
    }
    create(questionId, message) {
        var data = {
            message: message
        };
        var promise = this._create(questionId, data);
        promise.then(result => {
            this.answers.push(result.data);
        });
        return promise;
    }
    delete(id) {
        var promise = this._delete(id);
        promise.then(() => {
            var answer = this.get(id);
            var indexAnswer = this.answers.indexOf(answer);
            this.answers.splice(indexAnswer, 1);
        });
        return promise;
    }

    // Ajax requests
    _loadAll(questionId) {
        return $.get(URL.answers.replace(':questionId', questionId));
    }
    _create(questionId, data) {
        return $.ajax({
            method: 'POST',
            url: URL.answers.replace(':questionId', questionId),
            dataType: 'json',
            data: JSON.stringify(data)
        });
    }
    _delete(id) {
        return $.ajax({
            method: 'DELETE',
            url: URL.answer.replace(':answerId', id)
        });
    }
}

export default new AnswerStore();
