#ifndef _h_test_54547630_b456_11ea_97d7_a85e451255ad_
#define _h_test_54547630_b456_11ea_97d7_a85e451255ad_

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

        test1() = default;

        test1(test1& value) = default;

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

        test2() = default;

        test2(test2& value) = default;

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
    class test_caller : Icaller {
    private:
        std::shared_ptr<modulemng> modules;

    public:
        test_caller(std::shared_ptr<Ichannel> _ch, std::shared_ptr<modulemng> _modules) : Icaller("test", _ch)
        {
            modules = _modules;
        }

        class test_test3_cb{
        public:
            signals<void(test1 t1)> sig_test3_cb;
            signals<void(int32_t err)> sig_test3_err;

            void callBack(std::function<void(test1 t1)> cb, std::function<void(int32_t err)> err){
                sig_test3_cb.connect(cb);
                sig_test3_err.connect(err);
            }

            static void rsp(std::shared_ptr<test_test3_cb> self, rapidjson::Value& inArray){
                auto _t1 = test1::protcol_to_test1(inArray[0]);
                if (self == nullptr){
                    return;
                }
                if (self->sig_test3_cb.empty()){
                    return;
                }
                self->sig_test3_cb.emit(_t1);
            }
            static void err(std::shared_ptr<test_test3_cb> self, rapidjson::Value& inArray){
                auto _err = inArray[0].GetInt();
                if (self == nullptr){
                    return;
                }
                if (self->sig_test3_err.empty()){
                    return;
                }
                self->sig_test3_err.emit(_err);
            }
        };

        std::shared_ptr<test_test3_cb> test3(test2 t2){
            auto uuid_5455126e_b456_11ea_87e7_a85e451255ad = sole::uuid0().str();
            rapidjson::Document _argv_5455126f_b456_11ea_a25c_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_5455126f_b456_11ea_a25c_a85e451255ad.GetAllocator();
            _argv_5455126f_b456_11ea_a25c_a85e451255ad.SetArray();
            rapidjson::Value str_uuid(rapidjson::kStringType);
            str_uuid.SetString(uuid_5455126e_b456_11ea_87e7_a85e451255ad.c_str(), uuid_5455126e_b456_11ea_87e7_a85e451255ad.size());
            _argv_5455126f_b456_11ea_a25c_a85e451255ad.PushBack(str_uuid, allocator);
            _argv_5455126f_b456_11ea_a25c_a85e451255ad.PushBack(test2::test2_to_protcol(t2), allocator);
            call_module_method(emRpcType::EM_RPC_TYPE_REQ, "test3", _argv_5455126f_b456_11ea_a25c_a85e451255ad.GetArray());

            auto cb_test3_obj = std::make_shared<test_test3_cb>();
            modules->reg_callback_method(uuid_5455126e_b456_11ea_87e7_a85e451255ad, std::bind(&test_test3_cb::rsp, cb_test3_obj, std::placeholders::_1), std::bind(&test_test3_cb::err, cb_test3_obj, std::placeholders::_1));
            return cb_test3_obj;
        }

        void test4(std::vector<test2> argv){
            rapidjson::Document _argv_54551270_b456_11ea_a39d_a85e451255ad;
            rapidjson::Document::AllocatorType& allocator = _argv_54551270_b456_11ea_a39d_a85e451255ad.GetAllocator();
            _argv_54551270_b456_11ea_a39d_a85e451255ad.SetArray();
            rapidjson::Value _array_54551271_b456_11ea_9179_a85e451255ad(rapidjson::kArrayType);
            for(auto v_54551272_b456_11ea_a47c_a85e451255ad : argv){
                _array_54551271_b456_11ea_9179_a85e451255ad.PushBack(test2::test2_to_protcol(v_54551272_b456_11ea_a47c_a85e451255ad), allocator);
            }
            _argv_54551270_b456_11ea_a39d_a85e451255ad.PushBack(_array_54551271_b456_11ea_9179_a85e451255ad, allocator);
            call_module_method(emRpcType::EM_RPC_TYPE_NTF, "test4", _argv_54551270_b456_11ea_a39d_a85e451255ad.GetArray());
        }

    };
/*this module code is codegen by abelkhan codegen for cpp*/
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

        class test_test3_rsp : Response {
        private:
            std::string uuid;

        public:
            test_test3_rsp(std::shared_ptr<Ichannel> _ch, std::string _uuid) : Response(_ch){
                uuid = _uuid;
            }

            void rsp(test1 t1){
                rapidjson::Document _argv_54551273_b456_11ea_b8bb_a85e451255ad;
                rapidjson::Document::AllocatorType& allocator = _argv_54551273_b456_11ea_b8bb_a85e451255ad.GetAllocator();
                _argv_54551273_b456_11ea_b8bb_a85e451255ad.SetArray();
                _argv_54551273_b456_11ea_b8bb_a85e451255ad.PushBack(test1::test1_to_protcol(t1), allocator);
                call_module_method(emRpcType::EM_RPC_TYPE_RSP, uuid, _argv_54551273_b456_11ea_b8bb_a85e451255ad.GetArray());
            }

            void err(int32_t err){
                rapidjson::Document _argv_54551274_b456_11ea_ac83_a85e451255ad;
                rapidjson::Document::AllocatorType& allocator = _argv_54551274_b456_11ea_ac83_a85e451255ad.GetAllocator();
                _argv_54551274_b456_11ea_ac83_a85e451255ad.SetArray();
                _argv_54551274_b456_11ea_ac83_a85e451255ad.PushBack(err, allocator);
                call_module_method(emRpcType::EM_RPC_TYPE_ERR, uuid, _argv_54551274_b456_11ea_ac83_a85e451255ad.GetArray());
            }

        };

        signals<void(test2 t2)> sig_test3;
        void test3(rapidjson::Value& inArray){
            auto _cb_uuid = inArray[0].GetString();
            auto _t2 = test2::protcol_to_test2(inArray[1]);
            rsp = std::make_shared<test_test3_rsp>(current_ch, _cb_uuid);
            sig_test3.emit(_t2);
            rsp = nullptr;
        }

        signals<void(std::vector<test2> argv)> sig_test4;
        void test4(rapidjson::Value& inArray){
            std::vector<test2> _argv;
            for(auto it_54551275_b456_11ea_91e5_a85e451255ad = inArray[0].Begin(); it_54551275_b456_11ea_91e5_a85e451255ad != inArray[0].End(); ++it_54551275_b456_11ea_91e5_a85e451255ad){
                _argv.push_back(test2::protcol_to_test2(*it_54551275_b456_11ea_91e5_a85e451255ad));
            }
            sig_test4.emit(_argv);
        }

    };

}

#endif //_h_test_54547630_b456_11ea_97d7_a85e451255ad_
