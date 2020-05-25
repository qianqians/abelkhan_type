#ifndef _h_test_42a3715e_9e63_11ea_ab3e_a85e451255ad_
#define _h_test_42a3715e_9e63_11ea_ab3e_a85e451255ad_

#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/signals2.hpp>

#include <abelkhan.h>

namespace abelkhan
{
/*this enum code is codegen by abelkhan codegen for cpp*/

/*this struct code is codegen by abelkhan codegen for cpp*/
    class test1 {
    public:
        int32_t argv1;
        std::string argv2;
        float argv3;
        double argv4;

    public:
        test1(int32_t _argv1, std::string _argv2, float _argv3, double _argv4){
            argv1 = _argv1;
            argv2 = _argv2;
            argv3 = _argv3;
            argv4 = _argv4;
        }

    public:
        static rapidjson::Value& test1_to_protcol(test1 _struct){
            rapidjson::Document _protocol;
            rapidjson::Document::AllocatorType& allocator = _protocol.GetAllocator();
            _protocol.SetArray();
            _protocol.PushBack(_struct.argv1, allocator);
            _protocol.PushBack(_struct.argv3, allocator);
            _protocol.PushBack(_struct.argv4, allocator);
            return _protocol.GetArray();
        }
        static test1 protcol_to_test1(rapidjson::Value& _protocol){
            auto _argv1 = _protocol[0].GetInt();
            auto _argv3 = _protocol[2].GetFloat();
            auto _argv4 = _protocol[3].GetDouble();
            test1 _struct(_argv1, _argv2, _argv3, _argv4);
            return _struct;
        }
    }

    class test2 {
    public:
        int32_t argv1;
        test1 argv2;

    public:
        test2(int32_t _argv1, test1 _argv2){
            argv1 = _argv1;
            argv2 = _argv2;
        }

    public:
        static rapidjson::Value& test2_to_protcol(test2 _struct){
            rapidjson::Document _protocol;
            rapidjson::Document::AllocatorType& allocator = _protocol.GetAllocator();
            _protocol.SetArray();
            _protocol.PushBack(_struct.argv1, allocator);
            _protocol.PushBack(test1::test1_to_protcol(_struct.argv2), allocator);
            return _protocol.GetArray();
        }
        static test2 protcol_to_test2(rapidjson::Value& _protocol){
            auto _argv1 = _protocol[0].GetInt();
            auto _argv2 = test1::protcol_to_test1(_protocol[1]);
            test2 _struct(_argv1, _argv2);
            return _struct;
        }
    }

/*this caller code is codegen by abelkhan codegen for cpp*/
    class cb_test3
    {
    public:
        boost::signals2::signal<void(test1 t1) sig_test3_cb;
        boost::signals2::signal<void(int32_t err) sig_test3_err;

        public void callBack(std::function<void(test1 t1)> cb, std::function<void(int32_t err) err)
        {
            sig_test3_cb.connect(cb);
            sig_test3_err.connect(err);
        }

    }

/*this cb code is codegen by abelkhan for cpp*/
    class rsp_cb_test : public Imodule, public std::enable_shared_from_this<rsp_cb_test>{
    public:
        std::map<std::string, std::shared_ptr<cb_test3> > map_test3;
        rsp_cb_test() : Imodule("rsp_cb_test")
        {
        }

        void Init(std::shared_ptr<modulemng> modules){
            modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3_rsp", test3_rsp);
            reg_method("test3_err", test3_err);
        }
        void test3_rsp(rapidjson::Value& inArray){
            auto uuid = inArray[0].GetString();
            var _t1 = test1::protcol_to_test1(inArray[1]);
            auto rsp = map_test3[uuid];
            if (rsp != nullptr){
                rsp->sig_test3_cb(_t1);
                map_test3.erase(uuid);
            }
        }
        void test3_err(rapidjson::Value& inArray){
            auto uuid = inArray[0].GetString();
            auto _err = inArray[1].GetInt();
            auto rsp = map_test3[uuid];
            if (rsp != nullptr){
                rsp->sig_test3_err(_err);
                map_test3.erase(uuid);
            }
        }

    }

    class test_caller : Icaller {
    public:
        std::shared_Ptr<rsp_cb_test> rsp_cb_test_handle;
        test_caller(std::shared_ptr<Ichannel> _ch, std::shared_ptr<modulemng> modules) : Icaller("test", _ch)
        {
            rsp_cb_test_handle = std::make_shared<rsp_cb_test>();
            rsp_cb_test_handle->Init(modules);
        }

        std::shared_ptr<cb_test3> test3(test2 t2){
            auto uuid = boost::lexical_cast<std::string>(boost::uuids::random_generator()());
            rapidjson::Document _argv_42a3e68f_9e63_11ea_853a_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_42a3e68f_9e63_11ea_853a_a85e451255ad.GetAllocator();
            _argv_42a3e68f_9e63_11ea_853a_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid.c_str(), uuid.size());
            _argv_42a3e68f_9e63_11ea_853a_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_42a3e68f_9e63_11ea_853a_a85e451255ad.PushBack(test2::test2_to_protcol(t2));
            call_module_method("test3", _argv_42a3e68f_9e63_11ea_853a_a85e451255ad.GetArray());

            var cb_test3_obj = std::make_shared<cb_test3>();
            rsp_cb_test_handle->map_test3.insert(std::make_pair(uuid, cb_test3_obj));
            return cb_test3_obj;
        }

        void test4(std::vector<test2> argv){
            rapidjson::Document _argv_42a3e690_9e63_11ea_8134_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_42a3e690_9e63_11ea_8134_a85e451255ad.GetAllocator();
            _argv_42a3e690_9e63_11ea_8134_a85e451255ad.SetArray();
            rapidjson::Value _array_42a3e691_9e63_11ea_953f_a85e451255ad(rapidjson::kArrayType);
            for(auto v_42a3e692_9e63_11ea_93b4_a85e451255ad : _name){
                _array_42a3e691_9e63_11ea_953f_a85e451255ad.PushBack(test2::test2_to_protcol(v_42a3e692_9e63_11ea_93b4_a85e451255ad), allocator);
            }
            _argv_42a3e690_9e63_11ea_8134_a85e451255ad.PushBack(_array_42a3e691_9e63_11ea_953f_a85e451255ad, allocator);
            call_module_method("test4", _argv_42a3e690_9e63_11ea_8134_a85e451255ad.GetArray());
        }

    }
/*this module code is codegen by abelkhan codegen for cpp*/
    class rsp_test3 : Response {
    private:
        std::string uuid;

    public:
        rsp_test3(std::shared_ptr<Ichannel> _ch, std::string _uuid) : Response("rsp_cb_test", _ch)
        {
            uuid = _uuid;
        }

        rsp(test1 t1){
            rapidjson::Document _argv_42a3e693_9e63_11ea_97ee_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_42a3e693_9e63_11ea_97ee_a85e451255ad.GetAllocator();
            _argv_42a3e693_9e63_11ea_97ee_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid.c_str(), uuid.size());
            _argv_42a3e693_9e63_11ea_97ee_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_42a3e693_9e63_11ea_97ee_a85e451255ad.PushBack(test1::test1_to_protcol(t1), allocator);
            call_module_method("test3_rsp", _argv_42a3e693_9e63_11ea_97ee_a85e451255ad.GetArray());
        }

        err(int32_t err){
            rapidjson::Document _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad.GetAllocator();
            _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid.c_str(), uuid.size());
            _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad.PushBack(err, allocator);
            call_module_method("test3_err", _argv_42a3e694_9e63_11ea_8f4f_a85e451255ad.GetArray());
        }

    }

    class test_module : Imodule, public std::enable_shared_from_this<test>{
    public:
        test_module() : Imodule("test")
        {
        }

        void Init(abelkhan.modulemng _modules){
            _modules.reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3", test3);
            reg_method("test4", test4);
        }

        boost::signals2::signal<void(test2 t2) sig_test3;

        public void test3(rapidjson::Value& inArray){
            auto _cb_uuid = inArray[0].GetString();
            auto _t2 = test2::protcol_to_test2(inArray[1]);
            rsp = std::make_shared<rsp_test3>(current_ch, _cb_uuid);
            sig_test3(_t2);
            rsp = nullptr;
        }

        boost::signals2::signal<void(std::vector<test2> argv) sig_test4;
        void test4(rapidjson::Value& inArray){
            std::vector<test2> _argv;
            for(auto it_42a3e695_9e63_11ea_81f7_a85e451255ad = inArray[0].Begin(); it42a3e695_9e63_11ea_81f7_a85e451255ad != inArray[0].End(); ++it42a3e695_9e63_11ea_81f7_a85e451255ad){
                _argv.push_back(test2::protcol_to_test2(it_42a3e695_9e63_11ea_81f7_a85e451255ad));
            }
            sig_test4(_argv);
        }

    }

}

#endif //_h_test_42a3715e_9e63_11ea_ab3e_a85e451255ad_
