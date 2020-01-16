#coding:utf-8
# 2019-12-26
# build by qianqians
# genenum

def genenum(pretreatment):
    enum = pretreatment.enum
    
    code = "/*this enum code is codegen by abelkhan codegen for ts*/\n\n"
    for enum_name, enums in enum.items():
        code += "export enum " + enum_name + "{\n"
        for key, value in enums:
            code += "    " + key + " = " + str(value)
        code += "    " + enum_name + "_total"
        code += "\n}\n"

    return code

