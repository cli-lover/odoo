/** @odoo-module **/
import { Component } from "@odoo/owl";

export class Todoitem extends Component {
    static template = "todoitem.row";
    static props = {
        todo : {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean },
        },
        toggleState: Function,
        removeState: Function,
    };
    onChange() {
        this.props.toggleState(this.props.todo.id);
    }
    onRemove() {
        this.props.removeState(this.props.todo.id);
    }
}