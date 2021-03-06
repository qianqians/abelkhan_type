#coding:utf-8
# 2020-1-21
# build by qianqians
# gencaller

import uuid
import tools

def gen_module_caller(module_name, funcs, dependent_struct, dependent_enum):
    cb_func = ""

    cb_code = "/*this cb code is codegen by abelkhan for c#*/\n"
    cb_code += "    public class " + module_name + "_rsp_cb : abelkhan.Imodule {\n"
    cb_code_constructor = "        public " + module_name + "_rsp_cb(abelkhan.modulemng modules) : base(\"" + module_name + "_rsp_cb\")\n"
    cb_code_constructor += "        {\n"
    cb_code_constructor += "            modules.reg_module(this);\n\n"
    cb_code_section = ""

    code = "    public class " + module_name + "_caller : abelkhan.Icaller {\n"
    code += "        public static " + module_name + "_rsp_cb rsp_cb_" + module_name + "_handle = null;\n"
    code += "        public " + module_name + "_caller(abelkhan.Ichannel _ch, abelkhan.modulemng modules) : base(\"" + module_name + "\", _ch)\n"
    code += "        {\n"
    code += "            if (rsp_cb_" + module_name + "_handle == null)\n            {\n"
    code += "                rsp_cb_" + module_name + "_handle = new rsp_cb_" + module_name + "(modules);\n"
    code += "            }\n"
    code += "        }\n\n"

    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code += "        public void " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "            var _argv_" + _argv_uuid + " = new JArray();\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code += "            _argv_" + _argv_uuid + ".Add(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    code += "            _argv_" + _argv_uuid + ".Add(" + _type + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "            var _array_" + _array_uuid + " = new JArray();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "            foreach(var v_" + _v_uuid + " in " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code += "                _array_" + _array_uuid + ".Add(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                _array_" + _array_uuid + ".Add(" + array_type + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "            }\n"                                                     
                    code += "            _argv_" + _argv_uuid + ".Add(_array_" + _array_uuid + ");\n"
            code += "            call_module_method(\"" + func_name + "\", _argv_" + _argv_uuid + ");\n"
            code += "        }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            cb_func += "    public class " + module_name + "_" + func_name + "_cb\n    {\n"
            cb_func += "        public delegate void " + func_name + "_handle_cb("
            count = 0
            for _type, _name in i[4]:
                cb_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    cb_func += ", "
            cb_func += ");\n"
            cb_func += "        public event " + func_name + "_handle_cb on" + func_name + "_cb;\n\n"

            cb_func += "        public delegate void " + func_name + "_handle_err("
            count = 0
            for _type, _name in i[6]:
                cb_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count = count + 1
                if count < len(i[6]):
                    cb_func += ", "
            cb_func += ");\n"
            cb_func += "        public event " + func_name + "_handle_err on" + func_name + "_err;\n\n"

            cb_func += "        public void callBack(" + func_name + "_handle_cb cb, " + func_name + "_handle_err err)\n        {\n"
            cb_func += "            on" + func_name + "_cb += cb;\n"
            cb_func += "            on" + func_name + "_err += err;\n"
            cb_func += "        }\n\n"
            
            cb_func += "        public void call_cb("
            count = 0
            for _type, _name in i[4]:
                cb_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    cb_func += ", "
            cb_func += ")\n        {\n"
            cb_func += "            if (on" + func_name + "_cb != null)\n"
            cb_func += "            {\n"
            cb_func += "                on" + func_name + "_cb(" 
            count = 0
            for _type, _name in i[4]:
                cb_func += _name
                count = count + 1
                if count < len(i[4]):
                    cb_func += ", "
            cb_func += ");\n"
            cb_func += "            }\n"
            cb_func += "        }\n\n"
            
            cb_func += "        public void call_err("
            count = 0
            for _type, _name in i[6]:
                cb_func += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[6]):
                    cb_func += ", "
            cb_func += ")\n        {\n"
            cb_func += "            if (on" + func_name + "_err != null)\n"
            cb_func += "            {\n"
            cb_func += "                on" + func_name + "_err(" 
            count = 0
            for _type, _name in i[6]:
                cb_func += _name
                count = count + 1
                if count < len(i[6]):
                    cb_func += ", "
            cb_func += ");\n"
            cb_func += "            }\n"
            cb_func += "        }\n\n"

            cb_func += "    }\n\n"

            cb_code += "        public Dictionary<string, " + module_name + "_" + func_name + "_cb> map_" + func_name + ";\n"
            cb_code_constructor += "            map_" + func_name + " = new Dictionary<string, " + module_name + "_" + func_name + "_cb>();\n"
            cb_code_constructor += "            reg_method(\"" + func_name + "_rsp\", " + func_name + "_rsp);\n"
            cb_code_constructor += "            reg_method(\"" + func_name + "_err\", " + func_name + "_err);\n"

            cb_code_section += "        public void " + func_name + "_rsp(JArray inArray){\n"
            cb_code_section += "            var uuid = (String)inArray[0];\n"
            count = 1 
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    cb_code_section += "            var _" + _name + " = (" + _type_ + ")inArray[" + str(count) + "];\n"
                elif type_ == tools.TypeType.Custom:
                    cb_code_section += "            var _" + _name + " = " + _type + ".protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    cb_code_section += "            var _" + _name + " = new List<" + _array_type + ">();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    cb_code_section += "            foreach(var v_" + _v_uuid + " in inArray[" + str(count) + "]){\n"
                    if array_type_ == tools.TypeType.Original:
                        cb_code_section += "                _" + _name + ".Add((" + _array_type + ")v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        cb_code_section += "                _" + _name + ".Add(" + array_type + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    cb_code_section += "            }\n"
                count += 1
            cb_code_section += "            var rsp = map_" + func_name + "[uuid];\n"
            cb_code_section += "            rsp.call_cb("
            count = 0
            for _type, _name in i[4]:
                cb_code_section += "_" + _name
                count = count + 1
                if count < len(i[4]):
                    cb_code_section += ", "
            cb_code_section += ");\n"
            cb_code_section += "            map_" + func_name + ".Remove(uuid);\n"
            cb_code_section += "        }\n"

            cb_code_section += "        public void " + func_name + "_err(JArray inArray){\n"
            cb_code_section += "            var uuid = (String)inArray[0];\n"
            count = 1 
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    cb_code_section += "            var _" + _name + " = (" + _type_ + ")inArray[" + str(count) + "];\n"
                elif type_ == tools.TypeType.Custom:
                    cb_code_section += "            var _" + _name + " = " + _type + ".protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    cb_code_section += "            var _" + _name + " = new List<" + _array_type + ">();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    cb_code_section += "            foreach(var v_" + _v_uuid + " in inArray[" + str(count) + "]){\n"
                    if array_type_ == tools.TypeType.Original:
                        cb_code_section += "                _" + _name + ".Add((" + _array_type + ")v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        cb_code_section += "                _" + _name + ".Add(" + array_type + ".protcol_to_" + array_type + "(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    cb_code_section += "            }\n"
                count += 1
            cb_code_section += "            var rsp = map_" + func_name + "[uuid];\n"
            cb_code_section += "            rsp.call_err("
            count = 0
            for _type, _name in i[6]:
                cb_code_section += "_" + _name
                count = count + 1
                if count < len(i[6]):
                    cb_code_section += ", "
            cb_code_section += ");\n"
            cb_code_section += "            map_" + func_name + ".Remove(uuid);\n"
            cb_code_section += "        }\n"

            code += "        public " + module_name + "_" + func_name + "_cb " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _cb_uuid_uuid = str(uuid.uuid1())
            _cb_uuid_uuid = '_'.join(_cb_uuid_uuid.split('-'))
            code += "            var uuid_" + _cb_uuid_uuid + " = System.Guid.NewGuid().ToString(\"N\");\n\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "            var _argv_" + _argv_uuid + " = new JArray();\n"
            code += "            _argv_" + _argv_uuid + ".Add(uuid_" + _cb_uuid_uuid + ");\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Original:
                    code += "            _argv_" + _argv_uuid + ".Add(" + _name + ");\n"
                elif type_ == tools.TypeType.Custom:
                    code += "            _argv_" + _argv_uuid + ".Add(" + _type + "." + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "            var _array_" + _array_uuid + " = new JArray();\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "            foreach(var v_" + _v_uuid + " in " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Original:
                        code += "                _array_" + _array_uuid + ".Add(v_" + _v_uuid + ");\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                _array_" + _array_uuid + ".Add(" + array_type + "." + array_type + "_to_protcol(v_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "            }\n"                                                     
                    code += "            _argv_" + _argv_uuid + ".Add(_array_" + _array_uuid + ");\n"
            code += "            call_module_method(\"" + func_name + "\", _argv_" + _argv_uuid + ");\n\n"
            code += "            var cb_" + func_name + "_obj = new " + module_name + "_" + func_name + "_cb();\n"
            code += "            rsp_cb_" + module_name + "_handle.map_" + func_name + ".Add(uuid_" + _cb_uuid_uuid + ", cb_" + func_name + "_obj);\n"
            code += "            return cb_" + func_name + "_obj;\n"
            code += "        }\n\n"

        else:
            raise Exception("func:" + func_name + " wrong rpc type:" + i[1] + ", must req or ntf")

    cb_code_constructor += "        }\n"
    cb_code_section += "    }\n\n"
    code += "    }\n"

    return cb_func + cb_code + cb_code_constructor + cb_code_section + code

def gencaller(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
    
    code = "/*this caller code is codegen by abelkhan codegen for c#*/\n"
    for module_name, funcs in modules.items():
        code += gen_module_caller(module_name, funcs, dependent_struct, dependent_enum)
        
    return code