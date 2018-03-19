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
    create(questionId, body) {
        var data = {
            body: body
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
    vote(id, upDown) {
        var data = {
            'up_down': upDown
        };
        var promise = this._vote(id, data);
        promise.then(result => {
            var answer = this.get(id);
            var indexAnswer = this.answers.indexOf(answer);
            this.answers[indexAnswer] = result.data;
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
    _vote(id, data) {
        return $.ajax({
            method: 'POST',
            url: URL.voteAnswer.replace(':answerId', id),
            dataType: 'json',
            data: JSON.stringify(data)
        });
    }
}

export default new AnswerStore();
