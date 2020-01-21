#coding:utf-8
# 2019-12-24
# build by qianqians
# postprocess

class pretreatment(object):
    def __init__(self, fname, _import, module, enum, struct):
        self.name = fname
        self._import = _import
        self.module = module
        self.enum = enum
        self.struct = struct
        
        self.def_struct = []
        self.dependent_struct = []
        
        self.def_enum = []
        self.dependent_enum = []
        
def getImportElem(_import, pretreatmentdata):
    for e in pretreatmentdata:
        if _import != e.name:
            continue
        return e
        
def process(pretreatmentdata):
    names = []
    modules = []
    for elem in pretreatmentdata:
        for k, v in elem.module.items():
            if k in names:
                raise Exception("repeat module key:%s in file:%s" % (k, elem.name))
            names.append(k)
            modules.append(k)
        for k, v in elem.enum.items():
            if k in names:
                raise Exception("repeat enum key:%s in file:%s" % (k, elem.name))
            names.append(k)
        for k, v in elem.struct.items():
            if k in names:
                raise Exception("repeat struct key:%s in file:%s" % (k, elem.name))
            names.append(k)
    
    for elem in pretreatmentdata:
        for k, v in elem.enum.items():
            elem.def_enum.append(k)
        elem.dependent_enum.extend(elem.def_enum) 
        for k, v in elem.struct.items():
            elem.def_struct.append(k)   
        elem.dependent_struct.extend(elem.def_struct)   
    
    for elem in pretreatmentdata:
        for _import in elem._import:
            e = getImportElem(_import, pretreatmentdata)
            elem.dependent_struct.extend(e.def_struct)
            elem.dependent_enum.extend(e.def_enum)      
            
    modules_index = {}
    index = 1
    for m in modules:
        modules_index[m] = index
        index += 1
        
    return modules_index