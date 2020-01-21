#coding:utf-8
# 2019-12-26
# build by qianqians
# genenum

def genenum(pretreatment):
    enum = pretreatment.enum
    
    code = "/*this enum code is codegen by abelkhan codegen for ts*/\n\n"
    for enum_name, enums in enum.items():
        code += "export enum " + enum_name + "{\n"
        names = []
        for key, value in enums:
            if key in names:
                raise Exception("repeat enum elem:%s in enum:%s" % (key, enum_name))
            code += "    " + key + " = " + str(value)
            names.append(key)
        code += "\n}\n"

    return code

