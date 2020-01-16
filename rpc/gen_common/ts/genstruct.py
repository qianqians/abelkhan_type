#coding:utf-8
# 2019-12-27
# build by qianqians
# genstruct

def genstruct(pretreatment):
    dependent_struct = pretreatment.dependent_struct
    dependent_enum = pretreatment.dependent_enum
    
    struct = pretreatment.struct
    
    code = "/*this struct code is codegen by abelkhan codegen for typescript*/\n\n"
    for struct_name, elems in struct.items():
        code += "export class " + struct_name + "\n{\n"
        for key, value in elems:
            
            pass
        code += "}\n\n"

    return code
