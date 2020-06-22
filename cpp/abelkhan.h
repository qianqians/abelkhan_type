/*
 * abelkhan type 
 * qianqians
 * 2020/5/21
 */
#ifndef abelkhan_type_h_
#define abelkhan_type_h_

#include <stdarg.h>

#include <exception>
#include <string>
#include <memory>
#include <map>
#include <functional>
#include <vector>

#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

namespace abelkhan{

    std::string format(const char* pszFmt, ...)
    {
        std::string str;
        va_list args;
        va_start(args, pszFmt);
        {
            int nLength = _vscprintf(pszFmt, args);
            nLength += 1;
            std::vector<char> vectorChars(nLength);
            _vsnprintf(vectorChars.data(), nLength, pszFmt, args);
            str.assign(vectorChars.data());
        }
        va_end(args);
        return str;
    }

    enum class emRpcType
    {
        EM_RPC_TYPE_NTF = 1,
        EM_RPC_TYPE_REQ = 2,
        EM_RPC_TYPE_RSP = 3,
        EM_RPC_TYPE_ERR = 4,
    };


    class Exception : public std::exception {
    public:
        Exception(std::string _err) : std::exception() {
            err = _err;
        }

    public:
        std::string err;
    };

    class Ichannel {
    public:
        virtual void push(rapidjson::Document & doc) = 0;
    };

    class Icaller {
    public:
        Icaller(std::string _module_name, std::shared_ptr<Ichannel> _ch) {
            module_name = _module_name;
            ch = _ch;
        }

        void call_module_method(emRpcType rpctype, std::string methodname, rapidjson::Value argvs){
            rapidjson::Document _event;
            _event.SetArray();
            rapidjson::Document::AllocatorType& allocator = _event.GetAllocator();
            rapidjson::Value num_rpctype(rapidjson::kNumberType);
            num_rpctype.SetInt((int)rpctype);
            _event.PushBack(num_rpctype, allocator);
            rapidjson::Value str_methodname(rapidjson::kStringType);
            str_methodname.SetString(methodname.c_str(), methodname.size());
            _event.PushBack(str_methodname, allocator);
            rapidjson::Value str_methodname(rapidjson::kStringType);
            str_methodname.SetString(methodname.c_str(), methodname.size());
            _event.PushBack(str_methodname, allocator);
            _event.PushBack(argvs, allocator);
            
            try
            {
                ch->push(_event);
            }
            catch (std::exception err)
            {
                throw new Exception(err.what());
            }
        }
        
    protected:
        std::string module_name;
    private:
        std::shared_ptr<Ichannel> ch;
    };

    class Response{
    public:
        Response(std::shared_ptr<Ichannel> _ch) {
            ch = _ch;
        }

        void call_module_method(emRpcType rpctype, std::string uuid, rapidjson::Value argvs){
            rapidjson::Document _event;
            _event.SetArray();
            rapidjson::Document::AllocatorType& allocator = _event.GetAllocator();
            rapidjson::Value num_rpctype(rapidjson::kNumberType);
            num_rpctype.SetInt((int)rpctype);
            _event.PushBack(num_rpctype, allocator);
            rapidjson::Value str_methodname(rapidjson::kStringType);
            str_methodname.SetString(uuid.c_str(), uuid.size());
            _event.PushBack(str_methodname, allocator);
            _event.PushBack(argvs, allocator);
            
            try
            {
                ch->push(_event);
            }
            catch (std::exception err)
            {
                throw new Exception(err.what());
            }
        }

    private:
        std::shared_ptr<Ichannel> ch;
    };

    class Imodule
    {
    protected:
        std::map<std::string, std::function<void(rapidjson::Value& doc)> > events;

    public:
        Imodule(std::string _module_name) {
            module_name = _module_name;
            current_ch = nullptr;
            rsp = nullptr;
        }

        void reg_method(std::string method_name, std::function<void(rapidjson::Value& doc)> method) {
            events.insert(std::make_pair(method_name, method));
        }

        void process_event(std::shared_ptr<Ichannel> _ch, rapidjson::Document& _event)
        {
            current_ch = _ch;
            try
            {
                std::string func_name = _event[2].GetString();
                auto it_func = events.find(func_name);
                if (it_func != events.end())
                {
                    try
                    {
                        it_func->second(_event[3]);
                    }
                    catch (std::exception e)
                    {
                        throw new Exception(format("function name:%s System.Exception:%s", func_name, e.what()));
                    }
                }
                else
                {
                    throw new Exception(format("do not have a function named:%s", func_name));
                }
            }
            catch (std::exception e)
            {
                throw new Exception(format("System.Exception:%s", e.what()));
            }
            current_ch = nullptr;
        }

    public:
        std::shared_ptr<Ichannel> current_ch;
        std::shared_ptr<Response> rsp;
        std::string module_name;
    };

    class modulemng
    {
    public:
        modulemng(){
        }

        void reg_module(std::shared_ptr<Imodule> _module){
            ntf_req_module_set.insert(std::make_pair(_module->module_name, _module));
        }

        void unreg_module(std::shared_ptr<Imodule> _module){
            ntf_req_module_set.erase(_module->module_name);
        }

        void reg_callback_method(std::string cb_uuid, std::function<void(rapidjson::Value& doc)> rsp, std::function<void(rapidjson::Value& doc)> err){
            rsp_method_set.insert(std::make_pair(cb_uuid, rsp));
            err_method_set.insert(std::make_pair(cb_uuid, err));
        }

        void process_event(std::shared_ptr<Ichannel> _ch, rapidjson::Document& _event) {
            try {
                emRpcType rpctype = (emRpcType)_event[0].GetInt();

                if (rpctype == emRpcType::EM_RPC_TYPE_NTF || rpctype == emRpcType::EM_RPC_TYPE_REQ){
                    std::string module_name = _event[1].GetString();
                    auto it_module = ntf_req_module_set.find(module_name);
                    if (it_module != ntf_req_module_set.end()) {
                        it_module->second->process_event(_ch, _event);
                    }
                    else {
                        throw new Exception(format("do not have a module named:%s", module_name));
                    }
                }
                else if (rpctype == emRpcType::EM_RPC_TYPE_RSP){
                    std::string uuid = _event[1].GetString();
                    auto it_func = rsp_method_set.find(uuid);
                    if (it_func != rsp_method_set.end())
                    {
                        try
                        {
                            it_func->second(_event[2]);
                            rsp_method_set.erase(uuid);
                            err_method_set.erase(uuid);
                        }
                        catch (std::exception e)
                        {
                            throw new Exception(format("rsp callback uuid:%s System.Exception:%s", uuid, e.what()));
                        }
                    }
                    else
                    {
                        throw new Exception(format("do not have a rsp callback function:%s", uuid));
                    }
                }
                else if (rpctype == emRpcType::EM_RPC_TYPE_ERR){
                    std::string uuid = _event[1].GetString();
                    auto it_func = err_method_set.find(uuid);
                    if (it_func != err_method_set.end())
                    {
                        try
                        {
                            it_func->second(_event[2]);
                            rsp_method_set.erase(uuid);
                            err_method_set.erase(uuid);
                        }
                        catch (std::exception e)
                        {
                            throw new Exception(format("err callback uuid:%s System.Exception:%s", uuid, e.what()));
                        }
                    }
                    else
                    {
                        throw new Exception(format("do not have a err callback function:%s", uuid));
                    }
                }
            }
            catch (std::exception e)
            {
                throw Exception(format("System.Exception:%s", e.what()));
            }
        }

    private:
        std::map<std::string, std::shared_ptr<Imodule> > ntf_req_module_set;
        std::map<std::string, std::function<void(rapidjson::Value& doc)> > rsp_method_set;
        std::map<std::string, std::function<void(rapidjson::Value& doc)> > err_method_set;
    };
}

#endif //abelkhan_type_h_