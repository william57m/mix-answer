// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class QuestionStore {
    @observable questions = [];
    @observable currentQuestion = undefined;
    @observable isLoaded = false;
    @observable isCurrentLoaded = false;

    loadAll(limit, offset, unanswered) {
        this.isLoaded = false;
        var promise = this._loadAll(limit, offset, unanswered);
        promise.then(result => {
            this.questions = result.data;
            this.isLoaded = true;
        });
        return promise;
    }
    setCurrent(id) {
        var promise = this._load(id);
        this.isCurrentLoaded = false;
        promise.then(result => {
            this.currentQuestion = result.question;
            this.isCurrentLoaded = true;
        });
        return promise;
    }
    get(id) {
        var question = null;
        this.questions.forEach(q => {
            if (q.id === id) {
                question = q;
            }
        });
        return question;
    }
    create(title, body, tags=[]) {
        var data = {
            title: title,
            body: body,
            tags: tags
        };
        var promise = this._create(data);
        promise.then(result => {
            this.questions.push(result.data);
        });
        return promise;
    }
    edit(id, data) {
        var promise = this._edit(id, data);
        promise.then(() => {
            var question = this.get(id);
            var indexQuestion = this.questions.indexOf(question);
            this.questions[indexQuestion] = data;
            this.currentQuestion = data;
        });
        return promise;
    }
    delete(id) {
        var promise = this._delete(id);
        promise.then(() => {
            var question = this.get(id);
            var indexQuestion = this.questions.indexOf(question);
            this.questions.splice(indexQuestion, 1);
        });
        return promise;
    }
    vote(id, upDown) {
        var data = {
            'up_down': upDown
        };
        var promise = this._vote(id, data);
        promise.then(result => {
            var question = this.get(id);
            var indexQuestion = this.questions.indexOf(question);
            this.questions[indexQuestion] = result.data;
            this.currentQuestion = result.data;
        });
        return promise;
    }
    search(value) {
        return this._search(value);
    }

    // Ajax requests
    _loadAll(limit, offset, unanswered) {
        var qp = $.param({
            limit: limit || 1000,
            offset: offset || 0,
            unanswered: unanswered || false
        });
        return $.get(URL.questions + '?' + qp);
    }
    _load(id) {
        return $.get(URL.question.replace(':questionId', id));
    }
    _create(data) {
        return $.ajax({
            method: 'POST',
            url: URL.questions,
            dataType: 'json',
            data: JSON.stringify(data)
        });
    }
    _edit(id, data) {
        return $.ajax({
            method: 'PUT',
            url: URL.question.replace(':questionId', id),
            dataType: 'json',
            data: JSON.stringify(data)
        });
    }
    _delete(id) {
        return $.ajax({
            method: 'DELETE',
            url: URL.question.replace(':questionId', id)
        });
    }
    _vote(id, data) {
        return $.ajax({
            method: 'POST',
            url: URL.voteQuestion.replace(':questionId', id),
            dataType: 'json',
            data: JSON.stringify(data)
        });
    }
    _search(value) {
        return $.get(URL.search.replace(':searchValue', value));
    }
}

export default new QuestionStore();
