#coding:utf-8
import json
from robot.api import logger
class CustomKWs(object):
    def addTest(self,a,b):
        return a+b
    def convert_to_dictionary(self,str):
        return eval(str)

    def compareJson(self,actStr,expectStr):
        """比较两个json字符串，第一个参数是需要对比的字符串，第二个参数是我们预期的结果.
        支持如下几种匹配方式：

        1、完全匹配

        2、仅匹配部分key存在即表示验证通过，不严格校验对应key的value值是什么

        3、模糊匹配，校验key对应的value只要包含某些字符串即表示验证通过
        样例:
        | `Compare Json` | {'a':'b'} | {'a':'b'}  |
        | `Compare Json` | {'a0':{'a1':{'a2':'b2'}},'aa0':'bb0'} | {'a0':{'a1':{'a2':'b2'}},'aa0':'bb0'} |
        | `Compare Json` | {'a':'b','aa':'bb 其他字符串'}  | {'a':'b','aa':'@FMbb'} |
        | `Compare Json` | {'a':'b','aa':'aa这个key对应的value每次返回都比较随机，没有校验的基准，那么我们可以校验这个aa key是否存在'}  | {'a':'b','aa':'@CK'} |


        Examples:
        | `Compare Json` | {'a':'b'} | {'a':'b'}  |
        | `Compare Json` | {'a0':{'a1':{'a2':'b2'}},'aa0':'bb0'} | {'a0':{'a1':{'a2':'b2'}},'aa0':'bb0'} |
        | `Compare Json` | {'a':'b','aa':'bb Other String'}  | {'a':'b','aa':'@FMbb'} |
        | `Compare Json` | {'a':'b','aa':'something changes frequently,we can check whether the key '''aa''' exsits or not'}  | {'a':'b','aa':'@CK'} |

        """
        logger.info('预期的json字符串为：'+expectStr)
        logger.info('实际的json字符串为：'+actStr)
        expectStrDic = eval(expectStr)
        actStrDic = eval(actStr)

        expectStrDicKeys =  expectStrDic.keys()
        actStrDicKeys = actStrDic.keys()
        for k in expectStrDicKeys:
            if k not in actStrDicKeys:
                logger.error('预期的键'+k+'，在实际结果中并不存在')
                raise AssertionError("expect key :"+k+" ,but  doesnot found one " )

            elif (type(expectStrDic[k]).__name__ == 'dict'):
                self.compareJson(str(actStrDic[k]),str(expectStrDic[k]))
            elif "@FM" in str(expectStrDic[k]):
                # 模糊匹配逻辑
                if expectStrDic[k].replace("@FM","") in actStrDic[k]:
                    #模糊匹配ok
                    return
                else:
                    #模糊匹配失败
                    logger.error('模糊匹配的字符串：'+expectStrDic[k].replace("@FM","")+'，在实际结果找到的是：'+str(actStrDic[k]))
                    raise AssertionError(expectStrDic[k].replace("@FM","")+" is not in "+ actStrDic[k] )
            elif "@CK" in str(expectStrDic[k]):
                # 仅检查key存在即可
                return
            elif expectStrDic[k]!=actStrDic[k]:
                logger.error('预期的值'+str(expectStrDic[k])+'，在实际结果中找到的是：'+str(actStrDic[k]))
                raise AssertionError(str(expectStrDic[k])+" not match "+str(actStrDic[k]) )



