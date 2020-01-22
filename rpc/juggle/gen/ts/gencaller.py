#coding:utf-8
# 2020-1-21
# build by qianqians
# gencaller

import uuid
import tools

def gen_module_caller(module_name, module_index, funcs, dependent_struct, dependent_enum):
        code = "export class " + module_name + "_caller extends Icaller {\n"
        code += "    constructor(_ch:any){\n"
        code += "        super(" + module_name + ", " + str(module_index) + ", _ch);\n"
        code += "    }\n\n"

        func_index = 1
        for i in funcs:
                func_name = i[1]
                code += "    " + func_name + "("
                count = 0
                for _type, _name in i[2]:
                        code += _name + ":" + tools.convert_type(_type)
                        count = count + 1
                        if count < len(i[2]):
                                code += ", "
                code += "){\n"
                _argv_uuid = uuid.uuid1()
                _argv_uuid = '_'.join(_argv_uuid.split('-'))
                code += "        let _argv_" + _argv_uuid + " = [];\n"
                for _type, _name in i[2]:
                        type_ = tools.check_type(_type)
                        if type_ == tools.TypeType.Original:
                                code += "        _argv_" + _argv_uuid + ".push(" + _name + ");\n"
                        elif type_ == tools.TypeType.Custom:
                                code += "        _argv_" + _argv_uuid + ".push(" + _type + "_to_protcol(" + _name + "));\n"
                        elif type_ == tools.TypeType.Array:
                                _array_uuid = uuid.uuid1()
                                _array_uuid = '_'.join(_array_uuid.split('-'))
                                code += "        let _array_" + _array_uuid + "":any[] = [];"
                                _v_uuid = uuid.uuid1()
                                _v_uuid = '_'.join(_v_uuid.split('-'))
                                code += "        for(let v_" + _v_uuid + " of _name){\n"
                                array_type = _type[:-2]
                                array_type_ = tools.check_type(array_type)
                                if array_type_ == tools.TypeType.Original:
                                        code += "            _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
                                elif array_type_ == tools.TypeType.Custom:
                                        code += "            _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                                elif array_type_ == tools.TypeType.Array:
                                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                                code += "        }\n"                                                     
                                code += "        _argv_" + _argv_uuid + ".push(_array_" + _array_uuid + ");\n"
                code += "        this.call_module_method(" + str(func_index) + ", _argv_" + _argv_uuid + ");\n"
                code += "    }\n\n"
                func_index += 1

        code += "}\n"

        return code

def gencaller(pretreatment, modules_index):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
    
    code = "/*this caller code is codegen by abelkhan codegen for typescript*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_caller(module_name, modules_index[module_name], funcs, dependent_struct, dependent_enum)
        
    return code