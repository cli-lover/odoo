/** @odoo-module **/
import { Component, useState, xml} from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.counter";
    static props = {
        onChange:  Function,
    }
    setup() {
        this.value = useState({ count: 0 });
    }
    increment() {
        this.value.count += 1;
        if (this.props.onChange) {
            this.props.onChange(1);
        }
    }
    decrement() {
        this.value.count -= 1;
        if (this.props.onChange) {
            this.props.onChange(-1);
        }
    }
}