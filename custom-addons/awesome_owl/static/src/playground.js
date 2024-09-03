/** @odoo-module **/

import { Component, useState, xml} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList};
    setup(){
        this.sum = useState({value:0});
        this.cards = useState([]);
    }

// COUNTER
    updateSum(delta){
        this.sum.value+=delta;
    }

// CARD
    addCard() {
        const newCard = {
            id: this.cards.length + 1,
            title: `Card ${this.cards.length + 1}`,
            state: true,
        };
        this.cards.push(newCard);
    }

    removeCard() {
        if (this.cards.length > 0) {
            this.cards.pop();
        }
    }
}
