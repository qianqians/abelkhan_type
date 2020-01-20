#coding:utf-8
# 2019-12-26
# build by qianqians
# tools

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
    
