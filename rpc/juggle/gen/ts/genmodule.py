#coding:utf-8
# 2020-1-21
# build by qianqians
# genmodule

import uuid
import tools

def gen_module_module(module_name, module_index, funcs, dependent_struct, dependent_enum):
        code_constructor = "export class " + module_name + "_module extends Imodule {\n"
        code_constructor += "    constructor(){\n"
        code_constructor += "        super(" + module_name + ", " + str(module_index) + ");\n"
        
        code_constructor_cb = ""
        code_func = ""
        func_index = 1
        for i in funcs:
                func_name = i[1]
                code_constructor += "        this.reg_method(" + str(func_index) + ", " + func_name + ");\n"
                code_constructor_cb += "        cb_" + func_name + " = null;\n"
                
                code_func += "    public cb_" + func_name + " : ("
                count = 0
                for _type, _name in i[2]:
                        code_func += _name + ":" + tools.convert_type(_type)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code_func += ")=>void | null;"
                code_func += "    " + func_name + "(inArray:any[]){\n"
                _argv_uuid = uuid.uuid1()
                _argv_uuid = '_'.join(_argv_uuid.split('-'))
                code_func += "        let _argv_" + _argv_uuid + " = [];\n"
                count = 0
                for _type, _name in i[2]:
                        type_ = tools.check_type(_type)
                        if type_ == tools.TypeType.Original:
                                code += "        _argv_" + _argv_uuid + ".push(inArray[" + str(count) + "]);\n"
                        elif type_ == tools.TypeType.Custom:
                                code += "        _argv_" + _argv_uuid + ".push(protcol_to_" + _type + "(inArray[" + str(count) + "]));\n"
                        elif type_ == tools.TypeType.Array:
                                _array_uuid = uuid.uuid1()
                                _array_uuid = '_'.join(_array_uuid.split('-'))
                                code += "        let _array_" + _array_uuid + "":any[] = [];"
                                _v_uuid = uuid.uuid1()
                                _v_uuid = '_'.join(_v_uuid.split('-'))
                                code += "        for(let v_" + _v_uuid + " of inArray[" + str(count) + "]){\n"
                                array_type = _type[:-2]
                                array_type_ = tools.check_type(array_type)
                                if array_type_ == tools.TypeType.Original:
                                        code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                                elif array_type_ == tools.TypeType.Custom:
                                        code += "            _array_" + _array_uuid + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                                elif array_type_ == tools.TypeType.Array:
                                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                                code += "        }\n"                                                     
                                code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                        count += 1
                code_func += "        if (cb_" + func_name + "){\n"
                code_func += "            cb_" + func_name + ".apply(null, _argv_" + _argv_uuid + ");\n"
                code_func += "        }\n"
                code_func += "    }\n\n"
                func_index += 1
        
        code_constructor_end = "    }\n\n"
        code = "}\n"
        
        return code_constructor + code_constructor_cb + code_constructor_end + code_func + code
        

def genmodule(pretreatment, modules_index):
        dependent_struct = pretreatment.dependent_struct
        dependent_enum = pretreatment.dependent_enum
    
        modules = pretreatment.module
        
        code = "/*this module code is codegen by abelkhan codegen for typescript*/\n"
        for module_name, funcs in modules.items():
                code += gen_module_caller(module_name, modules_index[module_name], funcs, dependent_struct, dependent_enum)
                
        return code