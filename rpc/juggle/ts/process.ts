import {Imodule} from "./Imodule"

export class juggle_process{
    private module_set = new Map<number, Imodule>();

    public reg_module(_module:Imodule){
        this.module_set.set(_module.module_index, _module);
    }

    public process_event(_ch:any, _event:any){
        this.module_set.get(_event[0]).process_event(_ch, _event);
    }
}