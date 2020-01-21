#coding:utf-8
# 2019-12-27
# build by qianqians
# genstruct

import tools
import uuid

def genmainstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "export class " + struct_name + "\n{\n"
    names = []
    for key, value in elems:
        if key in names:
            raise Exception("repeat struct elem:%s in struct:%s" % (key, struct_name))
        names.append(key)
        code += "    public " + value + " : " + tools.convert_type(key, dependent_struct, dependent_enum) + ";\n"
    code += "\n    constructor(){\n"
    count = 0
    for key, value in elems:
        code += "_" + value + " : " + tools.convert_type(key, dependent_struct, dependent_enum)
        count = count + 1
        if count < len(elems):
            code += ", "
    code += "){\n"
    for key, value in elems:
        code += "        this." + value + " = _" + value + ";\n"
    code += "    }\n" 
    code += "}\n"
    return code

def genstructprotocol(struct_name, elems, dependent_struct, dependent_enum):
    code = "export function " + struct_name + "_to_protcol(_struct:" + struct_name + "){\n"
    code += "    let _protocol:any[] = [];\n"
    for key, value in elems:
        type_ = tools.check_type(key)
        if type_ == tools.TypeType.Original:
            code += "    _protocol.push(_struct." + value + ");\n"
        elif type_ == tools.TypeType.Custom:
            code += "    _protocol.push(" + key + "_to_protcol(_struct." + value + "));\n"
        elif type_ == tools.TypeType.Array:
            _array_uuid = uuid.uuid1()
            _array_uuid = '_'.join(_array_uuid.split('-'))
            code += "    let _array_" + _array_uuid + "":any[] = [];"
            _v_uuid = uuid.uuid1()
            _v_uuid = '_'.join(_v_uuid.split('-'))
            code += "    for(let v_" + _v_uuid + " of _struct." + value + "){\n"
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type)
            if array_type_ == tools.TypeType.Original:
                code += "        _array_" + _array_uuid + ".push(v_" + _v_uuid + ");\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "        _array_" + _array_uuid + ".push(" + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "    }\n"
            code += "    _protocol.push(_array_" + _array_uuid + ");\n"
    code += "    return _protocol;\n"
    code += "}\n"

def genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum):
    code = "export function protcol_to_" + struct_name + "(_protocol:any[]){\n"
    count = 0
    for key, value in elems:
        type_ = tools.check_type(key)
        if type_ == tools.TypeType.Original:
            code += "    let _" + value + " = _protocol[" + str(count) + "] as " + key + ";\n"
        elif type_ == tools.TypeType.Custom:
            code += "    let _" + value + " = protcol_to_" + key + "(_protocol[" + str(count) + "]);\n"
        elif type_ == tools.TypeType.Array:
            array_type = key[:-2]
            array_type_ = tools.check_type(array_type)
            code += "    let _" + value + ":" + array_type + "[] = [];\n"
            _v_uuid = uuid.uuid1()
            _v_uuid = '_'.join(_v_uuid.split('-'))
            code += "    for(let v_" + _v_uuid + " of _protocol[" + str(count) + "]){\n"
            if array_type_ == tools.TypeType.Original:
                code += "        _" + value + ".push(v_" + _v_uuid + ");\n"
            elif array_type_ == tools.TypeType.Custom:
                code += "        _" + value + ".push(protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
            elif array_type_ == tools.TypeType.Array:
                raise Exception("not support nested array:%s in struct:%s" % (key, struct_name))
            code += "    }\n"
        code += "    "
    code += "    let _struct : new " + struct_name + "(\n
    count = 0
    for key, value in elems:
        code += "        _" + value
        count = count + 1
        if count < len(elems):
            code += ",\n"
    code += ");\n"
    code += "    return _struct;\n"
    code += "}\n"
    pass

def genstruct(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    struct = pretreatment.struct
    
    code = "/*this struct code is codegen by abelkhan codegen for typescript*/\n"
    for struct_name, elems in struct.items():
        code += genmainstruct(struct_name, elems, dependent_struct, dependent_enum);
        code += genstructprotocol(struct_name, elems, dependent_struct, dependent_enum);
        code += genprotocolstruct(struct_name, elems, dependent_struct, dependent_enum);

    return code
