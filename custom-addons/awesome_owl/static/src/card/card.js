/** @odoo-module **/
import { markup, Component, useState, xml } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                content: true
            },
        }
    };
    setup() {
        this.isOpen = useState({ value: true});
    }
    toggleContent() {
        this.isOpen.value = !this.isOpen.value;
    }
}