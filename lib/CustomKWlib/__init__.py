from .CustomKWs import CustomKWs


_version_ = '0.0.1'


class CustomKWlib(CustomKWs):
    """ CustomKWlib 可供关键字开发人员做样例参考，可以用来存放自定义的关键字，与系统第三方库分离开来

        关键字使用举例:
        | Compare Json | {'a':'b'} | {'a':'b'} |
        | ${sum} | Add Test | 1 | 2 |

    """
# （1）ROBOT_LIBRARY_SCOPE为ROBOT库范围，这个范围有三个等级，分别是TEST CASE、TEST SUITE、GLOBAL三个等级，默认是TEST CASE；而刚开始学习自定义库，所看到的基本都是GLOBAL这个等级。
# （2）在测试库中申明等级的作用是，在调用这个类的方法，就会实例化这个类
#         --TEST CASE：在每个test case中引用都会实例化一次
#         --TEST SUITE：在suite中引用，只会实例化一次，也就是说10个test case都引用了这个类的方法，但是只有第一个test case是调用的时候实例化，后续的共用
#         --GLOBAL：在全局只实例化一次，调用一次后，在所有suite中引用、test case中引用都不会再实例化
# （3）global的缺点如果只在一个test case中用到自定义类方法，这时候用GLOBAL是不是有点浪费啊；或者说多人共同开发的时候，你在运行的时候，自定义类被改了，你使用GLOBAL，之后的test case都不会再实例化，这就会造成你的test case都以旧方法跑，当然这情况出现的比较少。
# （4）每个项目组都是有自己的工程目录的，同一个项目组内部使用的关键字组内通用的情况居多，所以建议大家直接使用GLOBAL即可
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
