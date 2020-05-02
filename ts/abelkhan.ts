export class Icaller{
    private module_name : string;
    private ch : any;
    constructor(_module_name:string, _ch:any){
        this.module_name = _module_name;
        this.ch = _ch;
    }

    public call_module_method(method_name:number, argvs:any){
        var _event = [this.module_name, method_name, argvs];
        this.ch.push(_event); 
    }
}

export class Imodule{
    public module_name : string;
    constructor(_module_name:string){
        this.module_name = _module_name;
    }

    private methods = new Map<string, any>();
    public reg_method(method_name:string, method:any){
        this.methods.set(method_name, method);
    }
    
    public process_event(_event:any){
        this.methods.get(_event[1]).apply(this, [_event[2]]);
    }

}

export class modulemng{
    private module_set = new Map<string, Imodule>();

    public reg_module(_module:Imodule){
        this.module_set.set(_module.module_name, _module);
    }

    public current_ch:any = null;
    public rsp:any = null;
    public process_event(_ch:any, _event:any){
        this.current_ch = _ch;
        this.module_set.get(_event[0]).process_event(_event);
        this.current_ch = null;
    }
}