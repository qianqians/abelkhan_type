#coding:utf-8
# 2019-12-26
# build by qianqians
# tools

class TypeType():
    Original = 0
    Custom = 1
    Array = 2

def check_type(typestr):
    if typestr == 'int':
        return TypeType.Original
    elif typestr == 'string':
        return TypeType.Original
    elif typestr == 'float':
        return TypeType.Original
    elif typestr == 'bool':
        return TypeType.Original
    elif typestr in dependent_struct:
	    return TypeType.Custom
    elif typestr in dependent_enum:
    	return TypeType.Original
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        return TypeType.Array

    raise Exception("non exist type:%s" % _type)

def convert_type(_type, dependent_struct, dependent_enum):
    if typestr == 'int':
        return 'number'
    elif typestr == 'string':
        return 'string'
    elif typestr == 'float':
        return 'number'
    elif typestr == 'bool':
        return 'boolean'
    elif typestr in dependent_struct:
	    return typestr
    elif typestr in dependent_enum:
    	return typestr
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        array_type = typestr[:-2]
        array_type = convert_type(array_type)
        return array_type+'[]'

    raise Exception("non exist type:%s" % _type)
    
