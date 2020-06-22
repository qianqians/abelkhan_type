#coding:utf-8
# 2020-1-21
# build by qianqians
# gencaller

import uuid
import tools

def gen_module_caller(module_name, funcs, dependent_struct, dependent_enum):
    code = "    class " + module_name + "_caller : Icaller {\n"
    code += "    private:\n"
    code += "        std::shared_ptr<modulemng> modules;\n\n"
    code += "    public:\n"
    code += "        " + module_name + "_caller(std::shared_ptr<Ichannel> _ch, std::shared_ptr<modulemng> _modules) : Icaller(\"" + module_name + "\", _ch)\n"
    code += "        {\n"
    code += "            modules = _modules;\n"
    code += "        }\n\n"
    
    for i in funcs:
        func_name = i[0]

        if i[1] == "ntf":
            code += "        void " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "            rapidjson::Document _argv_" + _argv_uuid + ";\n"
            code += "            rapidjson::Document::AllocatorType& allocator = _argv_" + _argv_uuid + ".GetAllocator();\n"
            code += "            _argv_" + _argv_uuid + ".SetArray();\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32 or type_ == tools.TypeType.Int64 or type_ == tools.TypeType.Uint32 or type_ == tools.TypeType.Uint64 or type_ == tools.TypeType.Float or type_ == tools.TypeType.Double or type_ == tools.TypeType.Bool:
                    code += "            _argv_" + _argv_uuid + ".PushBack(" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.String:
                    code += "            rapidjson::Value str_" + _name + "(rapidjson::kStringType);\n"
                    code += "            str_" + _name + ".SetString(" + _name + ".c_str(), " + _name + ".size());\n"
                    code += "            _argv_" + _argv_uuid + ".PushBack(str_" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.Custom:
                    code += "            _argv_" + _argv_uuid + ".PushBack(" + _type + "::" + _type + "_to_protcol(" + _name + "));\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "            rapidjson::Value _array_" + _array_uuid + "(rapidjson::kArrayType);\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "            for(auto v_" + _v_uuid + " : " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Int32 or array_type_ == tools.TypeType.Int64 or array_type_ == tools.TypeType.Uint32 or array_type_ == tools.TypeType.Uint64 or array_type_ == tools.TypeType.Float or array_type_ == tools.TypeType.Double or array_type_ == tools.TypeType.Bool:
                        code += "                _array_" + _array_uuid + ".PushBack(v_" + _v_uuid + ", allocator);\n"
                    elif type_ == tools.TypeType.String:
                        code += "            rapidjson::Value str_" + _v_uuid + "(rapidjson::kStringType);\n"
                        code += "            str_" + _v_uuid + ".SetString(v_" + _v_uuid + ".c_str(), v_" + _v_uuid + ".size());\n"
                        code += "            _array_" + _array_uuid + ".PushBack(str_" + _v_uuid + ", allocator);\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                _array_" + _array_uuid + ".PushBack(" + array_type + "::" + array_type + "_to_protcol(v_" + _v_uuid + "), allocator);\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "            }\n"                                                     
                    code += "            _argv_" + _argv_uuid + ".PushBack(_array_" + _array_uuid + ", allocator);\n"
            code += "            call_module_method(emRpcType::EM_RPC_TYPE_NTF, \"" + func_name + "\", _argv_" + _argv_uuid + ".GetArray());\n"
            code += "        }\n\n"
        elif i[1] == "req" and i[3] == "rsp" and i[5] == "err":
            code += "        class " + module_name + "_" + func_name + "_cb{\n"
            code += "        public:\n"
            code += "            signals<void("
            count = 0
            for _type, _name in i[4]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    code += ", "
            code += ")> sig_" + func_name + "_cb;\n"
            
            code += "            signals<void("
            count = 0
            for _type, _name in i[6]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count = count + 1
                if count < len(i[6]):
                    code += ", "
            code += ")> sig_" + func_name + "_err;\n\n"
            
            code += "            void callBack(std::function<void("
            count = 0
            for _type, _name in i[4]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[4]):
                    code += ", "
            code += ")> cb, std::function<void("
            count = 0
            for _type, _name in i[6]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name
                count = count + 1
                if count < len(i[6]):
                    code += ", "
            code += ")> err){\n"
            code += "                sig_" + func_name + "_cb.connect(cb);\n"
            code += "                sig_" + func_name + "_err.connect(err);\n"
            code += "            }\n\n"

            code += "            static void rsp(std::shared_ptr<" + module_name + "_" + func_name + "_cb> self, rapidjson::Value& inArray){\n"
            count = 0
            for _type, _name in i[4]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetInt();\n"
                elif type_ == tools.TypeType.Int64:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetInt64();\n"
                elif type_ == tools.TypeType.Uint32:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetUint();\n"
                elif type_ == tools.TypeType.Uint64:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetUint64();\n"
                elif type_ == tools.TypeType.Float:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetFloat();\n"
                elif type_ == tools.TypeType.Double:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetDouble();\n"
                elif type_ == tools.TypeType.Bool:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetBool();\n"
                elif type_ == tools.TypeType.String:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetString();\n"
                elif type_ == tools.TypeType.Custom:
                    code += "                auto _" + _name + " = " + _type + "::protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code += "                std::vector<" + _array_type + "> _" + _name + ";\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "                for(auto it_" + _v_uuid + " = inArray[" + str(count) + "].Begin(); it_" + _v_uuid + " != inArray[" + str(count) + "].End(); ++it_" + _v_uuid + "){\n"
                    if array_type_ == tools.TypeType.Int32:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetInt());\n"
                    elif array_type_ == tools.TypeType.Int64:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetInt64());\n"
                    elif array_type_ == tools.TypeType.Uint32:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetUint());\n"
                    elif array_type_ == tools.TypeType.Uint64:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetUint64());\n"
                    elif array_type_ == tools.TypeType.Float:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetFloat());\n"
                    elif array_type_ == tools.TypeType.Double:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetDouble());\n"
                    elif array_type_ == tools.TypeType.Bool:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetBool());\n"
                    elif array_type_ == tools.TypeType.String:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetString());\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                    _" + _name + ".push_back(" + array_type + "::protcol_to_" + array_type + "(it_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "                }\n"
                count += 1
            code += "                if (self == nullptr){\n"
            code += "                    return;\n"
            code += "                }\n"
            code += "                if (self->sig_" + func_name + "_cb.empty()){\n"
            code += "                    return;\n"
            code += "                }\n"
            code += "                self->sig_" + func_name + "_cb.emit("
            count = 0
            for _type, _name in i[4]:
                code += "_" + _name
                count = count + 1
                if count < len(i[4]):
                    code += ", "
            code += ");\n"
            code += "            }\n"

            code += "            static void err(std::shared_ptr<" + module_name + "_" + func_name + "_cb> self, rapidjson::Value& inArray){\n"
            count = 0
            for _type, _name in i[6]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                _type_ = tools.convert_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetInt();\n"
                elif type_ == tools.TypeType.Int64:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetInt64();\n"
                elif type_ == tools.TypeType.Uint32:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetUint();\n"
                elif type_ == tools.TypeType.Uint64:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetUint64();\n"
                elif type_ == tools.TypeType.Float:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetFloat();\n"
                elif type_ == tools.TypeType.Double:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetDouble();\n"
                elif type_ == tools.TypeType.Bool:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetBool();\n"
                elif type_ == tools.TypeType.String:
                    code += "                auto _" + _name + " = inArray[" + str(count) + "].GetString();\n"
                elif type_ == tools.TypeType.Custom:
                    code += "                auto _" + _name + " = " + _type + "::protcol_to_" + _type + "(inArray[" + str(count) + "]);\n"
                elif type_ == tools.TypeType.Array:
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    _array_type = tools.convert_type(array_type, dependent_struct, dependent_enum)
                    code += "                std::vector<" + _array_type + "> _" + _name + ";\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "                for(auto it_" + _v_uuid + " = inArray[" + str(count) + "].Begin(); it_" + _v_uuid + " != inArray[" + str(count) + "].End(); ++it_" + _v_uuid + "){\n"
                    if array_type_ == tools.TypeType.Int32:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetInt());\n"
                    elif array_type_ == tools.TypeType.Int64:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetInt64());\n"
                    elif array_type_ == tools.TypeType.Uint32:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetUint());\n"
                    elif array_type_ == tools.TypeType.Uint64:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetUint64());\n"
                    elif array_type_ == tools.TypeType.Float:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetFloat());\n"
                    elif array_type_ == tools.TypeType.Double:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetDouble());\n"
                    elif array_type_ == tools.TypeType.Bool:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetBool());\n"
                    elif array_type_ == tools.TypeType.String:
                        code += "                    _" + _name + ".push_back(it_" + _v_uuid + "->GetString());\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                    _" + _name + ".push_back(" + array_type + "::protcol_to_" + array_type + "(it_" + _v_uuid + "));\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "                }\n"
                count += 1
            code += "                if (self == nullptr){\n"
            code += "                    return;\n"
            code += "                }\n"
            code += "                if (self->sig_" + func_name + "_err.empty()){\n"
            code += "                    return;\n"
            code += "                }\n"
            code += "                self->sig_" + func_name + "_err.emit("
            count = 0
            for _type, _name in i[6]:
                code += "_" + _name
                count = count + 1
                if count < len(i[6]):
                    code += ", "
            code += ");\n"
            code += "            }\n"

            code += "        };\n\n"

            code += "        std::shared_ptr<" + module_name + "_" + func_name + "_cb> " + func_name + "("
            count = 0
            for _type, _name in i[2]:
                code += tools.convert_type(_type, dependent_struct, dependent_enum) + " " + _name 
                count = count + 1
                if count < len(i[2]):
                    code += ", "
            code += "){\n"
            _cb_uuid_uuid = str(uuid.uuid1())
            _cb_uuid_uuid = '_'.join(_cb_uuid_uuid.split('-'))
            code += "            auto uuid_" + _cb_uuid_uuid + " = sole::uuid0().str();\n"
            _argv_uuid = str(uuid.uuid1())
            _argv_uuid = '_'.join(_argv_uuid.split('-'))
            code += "            rapidjson::Document _argv_" + _argv_uuid + ";\n"
            code += "            rapidjson::Document::AllocatorType& allocator = _argv_" + _argv_uuid + ".GetAllocator();\n"
            code += "            _argv_" + _argv_uuid + ".SetArray();\n"
            code += "            rapidjson::Value str_uuid(rapidjson::kStringType);\n"
            code += "            str_uuid.SetString(uuid_" + _cb_uuid_uuid + ".c_str(), uuid_" + _cb_uuid_uuid + ".size());\n"
            code += "            _argv_" + _argv_uuid + ".PushBack(str_uuid, allocator);\n"
            for _type, _name in i[2]:
                type_ = tools.check_type(_type, dependent_struct, dependent_enum)
                if type_ == tools.TypeType.Int32 or type_ == tools.TypeType.Int64 or type_ == tools.TypeType.Uint32 or type_ == tools.TypeType.Uint64 or type_ == tools.TypeType.Float or type_ == tools.TypeType.Double or type_ == tools.TypeType.Bool:
                    code += "            _argv_" + _argv_uuid + ".PushBack(" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.String:
                    code += "            rapidjson::Value str_" + _name + "(rapidjson::kStringType);\n"
                    code += "            str_" + _name + ".SetString(" + _name + ".c_str(), " + _name + ".size());\n"
                    code += "            _argv_" + _argv_uuid + ".PushBack(str_" + _name + ", allocator);\n"
                elif type_ == tools.TypeType.Custom:
                    code += "            _argv_" + _argv_uuid + ".PushBack(" + _type + "::" + _type + "_to_protcol(" + _name + "), allocator);\n"
                elif type_ == tools.TypeType.Array:
                    _array_uuid = str(uuid.uuid1())
                    _array_uuid = '_'.join(_array_uuid.split('-'))
                    code += "            rapidjson::Value _array_" + _array_uuid + "(rapidjson::kArrayType);\n"
                    _v_uuid = str(uuid.uuid1())
                    _v_uuid = '_'.join(_v_uuid.split('-'))
                    code += "            for(auto v_" + _v_uuid + " : " + _name + "){\n"
                    array_type = _type[:-2]
                    array_type_ = tools.check_type(array_type, dependent_struct, dependent_enum)
                    if array_type_ == tools.TypeType.Int32 or array_type_ == tools.TypeType.Int64 or array_type_ == tools.TypeType.Uint32 or array_type_ == tools.TypeType.Uint64 or array_type_ == tools.TypeType.Float or array_type_ == tools.TypeType.Double or array_type_ == tools.TypeType.Bool:
                        code += "                _array_" + _array_uuid + ".PushBack(v_" + _v_uuid + ", allocator);\n"
                    elif type_ == tools.TypeType.String:
                        code += "            rapidjson::Value str_" + _v_uuid + "(rapidjson::kStringType);\n"
                        code += "            str_" + _v_uuid + ".SetString(v_" + _v_uuid + ".c_str(), v_" + _v_uuid + ".size());\n"
                        code += "            _array_" + _array_uuid + ".PushBack(str_" + _v_uuid + ", allocator);\n"
                    elif array_type_ == tools.TypeType.Custom:
                        code += "                _array_" + _array_uuid + ".PushBack(" + array_type + "::" + array_type + "_to_protcol(v_" + _v_uuid + "), allocator);\n"
                    elif array_type_ == tools.TypeType.Array:
                        raise Exception("not support nested array:%s in func:%s" % (_type, func_name))
                    code += "            }\n"                                                     
                    code += "            _argv_" + _argv_uuid + ".PushBack(_array_" + _array_uuid + ", allocator);\n"
            code += "            call_module_method(emRpcType::EM_RPC_TYPE_REQ, \"" + func_name + "\", _argv_" + _argv_uuid + ".GetArray());\n\n"

            code += "            auto cb_" + func_name + "_obj = std::make_shared<" + module_name + "_" + func_name + "_cb>();\n"
            code += "            modules->reg_callback_method(uuid_" + _cb_uuid_uuid + ", std::bind(&" + module_name + "_" + func_name + "_cb::rsp, cb_" + func_name + "_obj, std::placeholders::_1), std::bind(&" + module_name + "_" + func_name + "_cb::err, cb_" + func_name + "_obj, std::placeholders::_1));\n"
            code += "            return cb_" + func_name + "_obj;\n"
            
            code += "        }\n\n"
        else:
            raise Exception("func:" + func_name + " wrong rpc type:" + i[1] + ", must req or ntf")

    code += "    };\n"

    return code

def gencaller(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    modules = pretreatment.module
    
    h_code = "/*this caller code is codegen by abelkhan codegen for cpp*/\n"
    for module_name, funcs in modules.items():
        h_code += gen_module_caller(module_name, funcs, dependent_struct, dependent_enum)
        
    return h_code