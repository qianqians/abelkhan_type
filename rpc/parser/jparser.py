#coding:utf-8
# 2016-6-10
# build by qianqians
# parser
import os
import statemachine
import deletenote
import postprocess

text = """
module name{
   void func1();
   void func2(int i);
   func3 ntf(int i, string str);
   func4 ntf(int i, array a, bool b, float f, string s);
}

struct kv{
    int k1;
}
"""

def parser(_str):
    machine = statemachine.statemachine()
    machine.syntaxanalysis(deletenote.deletenote(_str))
    return machine.getimport(), machine.getmodule(), machine.getenum(), machine.getstruct()

def batch(inputdir):
    pretreatmentdata = []
    for filename in os.listdir(inputdir):
        fname = os.path.splitext(filename)[0]
        fex = os.path.splitext(filename)[1]
        if fex == '.juggle':
            file = open(inputdir + '//' + filename, 'r')
            genfilestr = file.readlines()

            _import, module, enum, struct = parser(genfilestr)
            pretreatmentdata.append(postprocess.pretreatment(fname, _import, module, enum, struct))
            
    modules_index = postprocess.process(pretreatmentdata)
    return pretreatmentdata, modules_index
    
_import, module, enum, struct = parser(text)
print(_import)
print(module)
print(enum)
print(struct)