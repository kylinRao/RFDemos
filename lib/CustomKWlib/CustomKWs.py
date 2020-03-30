# coding:utf-8

import json
import execjs
import  os




class CustomKWs():
    cur = None

    def toStr(self, strOrBytes):
        if type(strOrBytes).__name__ == "bytes":
            return strOrBytes.decode("UTF-8")
        else:
            return strOrBytes
    def not_empty(self,msg):
        if msg:
            return True;
        else:
            return False;
    def convert_doublecomma_to_singlecomma(self, inputstr):
        return inputstr.replace('"', "'")

    def to_dictionary(self, inputstr):
        inputstr= inputstr.replace("false","False")
        inputstr= inputstr.replace("true","True")
        return eval(inputstr)

    def number_to_fixed_length_string(self, number, fixed=5):
        str = "{number}".format(number=number)
        for egg in range(0, fixed - len(str)):
            str = "0" + str
        return str

    def string_contains(self, full_string, part_of_string):
        if str(part_of_string) in str(full_string):
            return True
        else:
            raise AssertionError(
                "{part_of_string} not in {full_string}".format(part_of_string=part_of_string, full_string=full_string))
    def list_contains(self, full_list, sublist):
        if not sublist:
            return True
        if eval(sublist) in eval(full_list):
            return True
        else:
            raise AssertionError(
                "{sublist} not in {full_list}".format(sublist=sublist, full_list=full_list))

    def compareJson(self, realStr, expectStr):
        """用于比较两个json串是否一致，支持模糊匹配@FM，仅校验key是否存在@CK，校验json内部的列表内部的json串，支持递归
         Compare Json    realStr=${res.content}    expectStr=${expectResponse}

         Examples:
         | Compare Json| realStr={"a":"a1"} | expectStr={"a":"a1"} |
         | Compare Json| realStr={"a":[{"innerA":"A"},{"innerB":"B"}]} | expectStr={"a":[{"innerA":"A"},{"innerB":"B"}]} |
         | Compare Json| realStr={"first":{"second":"something"}} | expectStr={"first":{"second":"something"}} |
         | Compare Json| realStr={"a":"abcdefg"} | expectStr={"a":"@FMabc"} |
         | Compare Json| realStr={"a":""} | expectStr={"a":"@CK"} |


        """

        expectStr = self.toStr(expectStr)
        realStr = self.toStr(realStr)
        if (not '{' in realStr) and (not '[' in realStr):
            if ((realStr) != (expectStr)):
                print("expect:", expectStr)
                print("in fact:", realStr)
                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=realStr,
                                                                                    expectStrDic=expectStr))
            else:
                return;

        if "false" in expectStr or "true" in expectStr:
            expectStr = expectStr.replace("false", "False").replace("true", "True")
        if "false" in realStr or "true" in realStr:
            realStr = realStr.replace("false", "False").replace("true", "True")
        if (expectStr == "NC"):
            return;

        expectStrDic = eval(expectStr)
        realStrDic = eval(realStr)
        print(type(expectStrDic))
        if (type(expectStrDic).__name__ == 'str'):
            if ((realStrDic) != (expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)
                raise AssertionError(
                    "{realStrDic} not match {expectStrDic}".format(realStrDic=realStrDic, expectStrDic=expectStrDic))
            else:
                return True;
        if (type(expectStrDic).__name__ == 'int'):
            if ((realStrDic) != (expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)
                raise AssertionError(
                    "{realStrDic} not match {expectStrDic}".format(realStrDic=realStrDic, expectStrDic=expectStrDic))
            else:
                return True;
        if (type(expectStrDic).__name__ == 'list'):
            if (len(realStrDic) != len(expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)

                raise AssertionError("list length not match")
            for (item1, item2) in zip(realStrDic, expectStrDic):
                print(item1, item2)
                self.compareJson(str(item1), str(item2))
            return
        expectStrDicKeys = expectStrDic.keys()
        realStrDicKeys = realStrDic.keys()

        for k in expectStrDicKeys:
            print(k, expectStrDic[k])
            if k not in realStrDicKeys:
                raise AssertionError("expect key :" + k + " ,but  doesnot found one ")
            elif (type(expectStrDic[k]).__name__ == 'list'):

                if len(realStrDic[k]) != len(expectStrDic[k]):
                    print("expect:", expectStrDic[k])
                    print("in fact:", realStrDic[k])

                    raise AssertionError("list length not match")
                for (item1, item2) in zip(realStrDic[k], expectStrDic[k]):
                    print(item1, item2)
                    print(type(item1))
                    if (type(item1).__name__ == 'str'):
                        if not (('{' in item1) or ('[' in item1)):
                            if ((item1) != (item2)):
                                print("expect:", item2)
                                print("in fact:", item1)
                                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=item1,
                                                                                                    expectStrDic=item2))

                    self.compareJson(str(item1), str(item2))

            elif (type(expectStrDic[k]).__name__ == 'dict'):
                self.compareJson(str(realStrDic[k]), str(expectStrDic[k]))
            elif "@FM" in str(expectStrDic[k]):
                # 模糊匹配逻辑
                if expectStrDic[k].replace("@FM", "") in realStr:
                    # 模糊匹配ok
                    continue
                else:
                    # 模糊匹配失败
                    raise AssertionError(expectStrDic[k].replace("@FM", "") + " is not in " + realStrDic[k])
            elif "@CK" in str(expectStrDic[k]):
                # 仅检查key存在即可
                continue
            elif expectStrDic[k] != realStrDic[k]:

                raise AssertionError(str(expectStrDic[k]) + " not match " + str(realStrDic[k]))
    def uworker_encrypt_des_ecb(self, text):
        """用于比较两个json串是否一致，支持模糊匹配@FM，仅校验key是否存在@CK，校验json内部的列表内部的json串，支持递归
         Compare Json    realStr=${res.content}    expectStr=${expectResponse}

         Examples:
         | Compare Json| realStr={"a":"a1"} | expectStr={"a":"a1"} |
         | Compare Json| realStr={"a":[{"innerA":"A"},{"innerB":"B"}]} | expectStr={"a":[{"innerA":"A"},{"innerB":"B"}]} |
         | Compare Json| realStr={"first":{"second":"something"}} | expectStr={"first":{"second":"something"}} |
         | Compare Json| realStr={"a":"abcdefg"} | expectStr={"a":"@FMabc"} |
         | Compare Json| realStr={"a":""} | expectStr={"a":"@CK"} |


        """
        current_dir = os.path.dirname(__file__)
        js_dir = os.path.join(current_dir,"js")
        os.chdir(js_dir)
        with open(os.path.join(js_dir,"crypto-func.js"),encoding="utf-8") as f:
            js = f.read()
            ctx = execjs.compile(js)
            res = ctx.call('encryptByDes',"9588888888880288",text)
            return res

if __name__ == '__main__':
    cw = CustomKWs()
    r = """{"code":"200","msg":"","data":{"total":8,"rows":[{"id":34,"code":"permission","name":"权限中心","status":true,"appKey":"c5c06985-6e3f-4dd5-991e-d4b4cf22e5c9","appSecret":"590eced4-c6b0-445e-942b-9efd38c1ad49"},{"id":36,"code":"auth","name":"认证中心","status":true,"appKey":"81fc01d2-6b4f-4eda-b8f1-aeb71c139696","appSecret":"f89cc1ee-bc30-44e8-afd4-2ba6e3e796c3"},{"id":37,"code":"dictionary","name":"数据字典","status":true,"appKey":"61df9851-dd0f-4b06-a3b9-9b89f9fa0a88","appSecret":"52251467-a37b-4799-abc8-98116003ff9c"},{"id":64,"code":"uworker-personal","name":"人事模块","status":true,"appKey":"cd956e38-6784-4b70-8151-cdd418db0b4e","appSecret":"5b0fed5d-75fa-4a01-bde8-23db37f4a922"},{"id":65,"code":"uworker-assets","name":"资产模块","status":true,"appKey":"7bb1419e-6467-4427-a6da-654f712e68dc","appSecret":"fd89ba8e-2af6-49fa-ab78-a95d1f6e005d"},{"id":70,"code":"bpm-server","name":"流程引擎","status":true,"appKey":"asdad","appSecret":"adsadadasd"},{"id":71,"code":"file","name":"文件服务器","status":true,"appKey":"asdsad","appSecret":"asdasdasdasd"},{"id":72,"code":"uworker-meeting","name":"会议系统","status":true,"appKey":"asdasd","appSecret":"asdasdasd"}]}}"""
    e  =  """{"code":"200","msg":"","data":{"total":8,"rows":[{"id":34,"code":"permission","name":"权限中心","status":True,"appKey":"c5c06985-6e3f-4dd5-991e-d4b4cf22e5c9","appSecret":"590eced4-c6b0-445e-942b-9efd38c1ad49"},{"id":36,"code":"auth","name":"认证中心","status":True,"appKey":"81fc01d2-6b4f-4eda-b8f1-aeb71c139696","appSecret":"f89cc1ee-bc30-44e8-afd4-2ba6e3e796c3"},{"id":37,"code":"dictionary","name":"数据字典","status":True,"appKey":"61df9851-dd0f-4b06-a3b9-9b89f9fa0a88","appSecret":"52251467-a37b-4799-abc8-98116003ff9c"},{"id":64,"code":"uworker-personal","name":"人事模块","status":True,"appKey":"cd956e38-6784-4b70-8151-cdd418db0b4e","appSecret":"5b0fed5d-75fa-4a01-bde8-23db37f4a922"},{"id":65,"code":"uworker-assets","name":"资产模块","status":True,"appKey":"7bb1419e-6467-4427-a6da-654f712e68dc","appSecret":"fd89ba8e-2af6-49fa-ab78-a95d1f6e005d"},{"id":70,"code":"bpm-server","name":"流程引擎","status":True,"appKey":"asdad","appSecret":"adsadadasd"},{"id":71,"code":"file","name":"文件服务器","status":True,"appKey":"asdsad","appSecret":"asdasdasdasd"},{"id":72,"code":"uworker-meeting","name":"会议系统","status":True,"appKey":"asdasd","appSecret":"asdasdasd"}]}}"""
    cw.compareJson(r,e)
