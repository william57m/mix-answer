// Lib imports
import $ from 'jquery';
import { observable } from 'mobx';
import URL from './_url';


class QuestionStore {
    @observable questions = [];
    @observable isLoaded = false;

    loadAll() {
        this.isLoaded = false;
        $.get(URL.questions).then(result => {
            this.questions = result.data;
            this.isLoaded = true;
        });
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
}

export default new QuestionStore();
