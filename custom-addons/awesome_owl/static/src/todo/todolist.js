/** @odoo-module **/
import { Component, useState, xml } from "@odoo/owl";
import { Todoitem} from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "todolist.list";
    static components = { Todoitem };
    setup(){
        this.todos = useState([]);
        this.inputRef = useAutofocus('inputRef');
    }
    addtodo(ev){
        if (ev.keyCode === 13){
            const value = ev.target.value;
            if(value.trim() !== '') {
                const newId = this.todos.length;
                this.todos.push(
                    {
                        id: newId+1,
                        description: value,
                        isCompleted: false, 
                    }
                );
                ev.target.value = '';
            }
        }
    }
    toggleTodo(todoId){
        const todo = this.todos.find(todo => todo.id ===todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {
        const index = this.todos.findIndex(todo => todo.id===todoId);
        if (index>=0){
            this.todos.splice(index, 1);
            for (let i = index; i < this.todos.length; i++) {
                this.todos[i].id = i + 1;
            }
        }
    }

    // addtodo() {
    //     const newId = this.todos.length;
    //     this.todos.push({
    //         id: newId + 1,
    //         description: `Hello ${newId + 1}`,
    //         isCompleted : (newId%2 == 0) ? true : false,
    //     });
    // }
    poptodo() {
        if (this.todos){
            this.todos.pop();
        }
    }
    // completetodo(delta) {
    //     for ( todo of this.todos) {
    //         if (todo.id == delta){
    //             todo.isCompleted = true;
    //             todo.description = "<t style='text-decoration:line-through' >"+todo.description+"</t>";
    //         }
    //     }
    // }
}