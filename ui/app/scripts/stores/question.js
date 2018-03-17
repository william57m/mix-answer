// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class QuestionStore {
    @observable questions = [];
    @observable currentQuestion = undefined;
    @observable isLoaded = false;

    loadAll() {
        this.isLoaded = false;
        var promise = $.get(URL.questions);
        promise.then(result => {
            this.questions = result.data;
            this.isLoaded = true;
        });
        return promise;
    }
    load(id) {
        var promise = $.get(URL.question.replace(':questionId', id));
        promise.then(result => {
            this.currentQuestion = result;
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
        var promise = $.ajax({
            method: 'POST',
            url: URL.questions,
            dataType: 'json',
            data: JSON.stringify(data)
        });
        promise.then(result => {
            this.questions.push(result.data);
        });
        return promise;
    }
    delete(id) {
        var promise = $.ajax({
            method: 'DELETE',
            url: URL.question.replace(':questionId', id)
        });
        promise.then(() => {
            var question = this.get(id);
            var indexQuestion = this.questions.indexOf(question);
            this.questions.splice(indexQuestion, 1);
        });
        return promise;
    }
}

export default new QuestionStore();
