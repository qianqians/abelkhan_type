export class Icaller{
    private module_name : string;
    private module_index : number;
    private ch : any;
    constructor(_module_name:string, _module_index:number, _ch:any){
        this.module_name = _module_name;
        this.module_index = _module_index;
        this.ch = _ch;
    }

    public call_module_method(method_index:number, argvs:any){
        var _event = [this.module_index, method_index, argvs];
        this.ch.push(_event); 
    }
}

enum em_key{
    em1,
    em2
}

let key:Array<em_key> = [1, 2,3];