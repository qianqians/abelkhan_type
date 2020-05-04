#coding:utf-8
# 2019-12-26
# build by qianqians
# tools

class TypeType():
    Original = 0
    Custom = 1
    Array = 2

def check_type(typestr, dependent_struct, dependent_enum):
    if typestr == 'int32':
        return TypeType.Original
    elif typestr == 'int64':
        return TypeType.Original
    elif typestr == 'uint32':
        return TypeType.Original
    elif typestr == 'uint64':
        return TypeType.Original
    elif typestr == 'string':
        return TypeType.Original
    elif typestr == 'float':
        return TypeType.Original
    elif typestr == 'double':
        return TypeType.Original
    elif typestr == 'bool':
        return TypeType.Original
    elif typestr in dependent_struct:
	    return TypeType.Custom
    elif typestr in dependent_enum:
    	return TypeType.Original
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        return TypeType.Array

    raise Exception("non exist type:%s" % typestr)

def convert_type(typestr, dependent_struct, dependent_enum):
    if typestr == 'int32':
        return 'Int32'
    elif typestr == 'int64':
        return 'Int64'
    elif typestr == 'uint32':
        return 'UInt32'
    elif typestr == 'uint64':
        return 'UInt64'
    elif typestr == 'string':
        return 'String'
    elif typestr == 'float':
        return 'Single'
    elif typestr == 'double':
        return 'Double'
    elif typestr == 'bool':
        return 'Boolean'
    elif typestr in dependent_struct:
	    return typestr
    elif typestr in dependent_enum:
    	return typestr
    elif typestr[len(typestr)-2] == '[' and typestr[len(typestr)-1] == ']':
        array_type = typestr[:-2]
        array_type = convert_type(array_type, dependent_struct, dependent_enum)
        return 'List<' + array_type+'>'

    raise Exception("non exist type:%s" % typestr)
    
