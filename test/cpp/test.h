#ifndef _h_test_ae37a6c0_b1d3_11ea_97bf_a85e451255ad_
#define _h_test_ae37a6c0_b1d3_11ea_97bf_a85e451255ad_

#include <sole.hpp>
#include <rapidjson/rapidjson.h>

#include <signals.h>
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
        static rapidjson::Value test1_to_protcol(test1 _struct){
            rapidjson::Document _protocol;
            rapidjson::Document::AllocatorType& allocator = _protocol.GetAllocator();
            _protocol.SetArray();
            _protocol.PushBack(_struct.argv1, allocator);
            rapidjson::Value str_argv2(rapidjson::kStringType);
            str_argv2.SetString(_struct.argv2.c_str(), _struct.argv2.size());
            _protocol.PushBack(str_argv2, allocator);
            _protocol.PushBack(_struct.argv3, allocator);
            _protocol.PushBack(_struct.argv4, allocator);
            return _protocol.GetArray();
        }
        static test1 protcol_to_test1(rapidjson::Value& _protocol){
            auto _argv1 = _protocol[0].GetInt();
            std::string _argv2 = _protocol[1].GetString();
            auto _argv3 = _protocol[2].GetFloat();
            auto _argv4 = _protocol[3].GetDouble();
            test1 _struct(_argv1, _argv2, _argv3, _argv4);
            return _struct;
        }
    };

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
        static rapidjson::Value test2_to_protcol(test2 _struct){
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
    };

/*this caller code is codegen by abelkhan codegen for cpp*/
    class cb_test3
    {
    public:
        signals<void(test1 t1)> sig_test3_cb;
        signals<void(int32_t err)> sig_test3_err;

        void callBack(std::function<void(test1 t1)> cb, std::function<void(int32_t err)> err)
        {
            sig_test3_cb.connect(cb);
            sig_test3_err.connect(err);
        }

    };

/*this cb code is codegen by abelkhan for cpp*/
    class rsp_cb_test : public Imodule, public std::enable_shared_from_this<rsp_cb_test>{
    public:
        std::map<std::string, std::shared_ptr<cb_test3> > map_test3;
        rsp_cb_test() : Imodule("rsp_cb_test")
        {
        }

        void Init(std::shared_ptr<modulemng> modules){
            modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3_rsp", std::bind(&rsp_cb_test::test3_rsp, this, std::placeholders::_1));
            reg_method("test3_err", std::bind(&rsp_cb_test::test3_err, this, std::placeholders::_1));
        }
        void test3_rsp(rapidjson::Value& inArray){
            auto uuid = inArray[0].GetString();
            auto _t1 = test1::protcol_to_test1(inArray[1]);
            auto rsp = map_test3[uuid];
            if (rsp != nullptr){
                rsp->sig_test3_cb.emit(_t1);
                map_test3.erase(uuid);
            }
        }
        void test3_err(rapidjson::Value& inArray){
            auto uuid = inArray[0].GetString();
            auto _err = inArray[1].GetInt();
            auto rsp = map_test3[uuid];
            if (rsp != nullptr){
                rsp->sig_test3_err.emit(_err);
                map_test3.erase(uuid);
            }
        }

    };

    class test_caller : Icaller {
    public:
        static std::shared_ptr<rsp_cb_test> rsp_cb_test_handle;
        test_caller(std::shared_ptr<Ichannel> _ch, std::shared_ptr<modulemng> modules) : Icaller("test", _ch)
        {
            if (rsp_cb_test_handle == nullptr){
                rsp_cb_test_handle = std::make_shared<rsp_cb_test>();
                rsp_cb_test_handle->Init(modules);
            }
        }

        std::shared_ptr<cb_test3> test3(test2 t2){
            auto uuid_ae384300_b1d3_11ea_976f_a85e451255ad = sole::uuid0().str();
            rapidjson::Document _argv_ae384301_b1d3_11ea_a296_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_ae384301_b1d3_11ea_a296_a85e451255ad.GetAllocator();
            _argv_ae384301_b1d3_11ea_a296_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid_ae384300_b1d3_11ea_976f_a85e451255ad.c_str(), uuid_ae384300_b1d3_11ea_976f_a85e451255ad.size());
            _argv_ae384301_b1d3_11ea_a296_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_ae384301_b1d3_11ea_a296_a85e451255ad.PushBack(test2::test2_to_protcol(t2), allocator);
            call_module_method("test3", _argv_ae384301_b1d3_11ea_a296_a85e451255ad.GetArray());

            auto cb_test3_obj = std::make_shared<cb_test3>();
            rsp_cb_test_handle->map_test3.insert(std::make_pair(uuid_ae384300_b1d3_11ea_976f_a85e451255ad, cb_test3_obj));
            return cb_test3_obj;
        }

        void test4(std::vector<test2> argv){
            rapidjson::Document _argv_ae386a0f_b1d3_11ea_9e9c_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_ae386a0f_b1d3_11ea_9e9c_a85e451255ad.GetAllocator();
            _argv_ae386a0f_b1d3_11ea_9e9c_a85e451255ad.SetArray();
            rapidjson::Value _array_ae386a10_b1d3_11ea_8fd1_a85e451255ad(rapidjson::kArrayType);
            for(auto v_ae386a11_b1d3_11ea_816a_a85e451255ad : argv){
                _array_ae386a10_b1d3_11ea_8fd1_a85e451255ad.PushBack(test2::test2_to_protcol(v_ae386a11_b1d3_11ea_816a_a85e451255ad), allocator);
            }
            _argv_ae386a0f_b1d3_11ea_9e9c_a85e451255ad.PushBack(_array_ae386a10_b1d3_11ea_8fd1_a85e451255ad, allocator);
            call_module_method("test4", _argv_ae386a0f_b1d3_11ea_9e9c_a85e451255ad.GetArray());
        }

    };
/*this module code is codegen by abelkhan codegen for cpp*/
    class rsp_test3 : Response {
    private:
        std::string uuid;

    public:
        rsp_test3(std::shared_ptr<Ichannel> _ch, std::string _uuid) : Response("rsp_cb_test", _ch)
        {
            uuid = _uuid;
        }

        void rsp(test1 t1){
            rapidjson::Document _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad.GetAllocator();
            _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid.c_str(), uuid.size());
            _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad.PushBack(test1::test1_to_protcol(t1), allocator);
            call_module_method("test3_rsp", _argv_ae386a12_b1d3_11ea_bb03_a85e451255ad.GetArray());
        }

        void err(int32_t err){
            rapidjson::Document _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad.GetAllocator();
            _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid.c_str(), uuid.size());
            _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad.PushBack(err, allocator);
            call_module_method("test3_err", _argv_ae386a13_b1d3_11ea_9e1a_a85e451255ad.GetArray());
        }

    };

    class test_module : Imodule, public std::enable_shared_from_this<test_module>{
    public:
        test_module() : Imodule("test")
        {
        }

        void Init(std::shared_ptr<modulemng> _modules){
            _modules->reg_module(std::static_pointer_cast<Imodule>(shared_from_this()));

            reg_method("test3", std::bind(&test_module::test3, this, std::placeholders::_1));
            reg_method("test4", std::bind(&test_module::test4, this, std::placeholders::_1));
        }

        signals<void(test2 t2)> sig_test3;
        void test3(rapidjson::Value& inArray){
            auto _cb_uuid = inArray[0].GetString();
            auto _t2 = test2::protcol_to_test2(inArray[1]);
            rsp = std::make_shared<rsp_test3>(current_ch, _cb_uuid);
            sig_test3.emit(_t2);
            rsp = nullptr;
        }

        signals<void(std::vector<test2> argv)> sig_test4;
        void test4(rapidjson::Value& inArray){
            std::vector<test2> _argv;
            for(auto it_ae386a14_b1d3_11ea_88be_a85e451255ad = inArray[0].Begin(); it_ae386a14_b1d3_11ea_88be_a85e451255ad != inArray[0].End(); ++it_ae386a14_b1d3_11ea_88be_a85e451255ad){
                _argv.push_back(test2::protcol_to_test2(*it_ae386a14_b1d3_11ea_88be_a85e451255ad));
            }
            sig_test4.emit(_argv);
        }

    };

}

#endif //_h_test_ae37a6c0_b1d3_11ea_97bf_a85e451255ad_
