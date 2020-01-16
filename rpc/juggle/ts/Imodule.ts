import {event_closure} from "event_closure"

export let current_ch = null;

export class Imodule extends event_closure{
    public module_name : string;
    public module_index : number;
    constructor(_module_name:string, _module_index:number){
        super();
        this.module_name = _module_name;
        this.module_index = _module_index;
    }

    private methods = new Map<number, any>();
    public reg_method(method_index:number, method:any){
        this.methods.set(method_index, method);
    }
    public process_event(_ch:any, _event:any){
        current_ch = _ch;
        this.methods.get(_event[1]).apply(this, _event[2]);
        current_ch = null;
    }
}