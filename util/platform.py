#coding=utf-8
import platform

platform.platform()
platform.system() #获取操作系统名称，'Linux' platform.version() #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
platform.architecture() #获取操作系统的位数，('32bit', 'ELF') platform.machine() #计算机类型，'i686' platform.node() #计算机的网络名称，'XF654'
platform.processor() #计算机处理器信息，''i686'
platform.uname() #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
# import sys
# import platform

# # python判断当前的操作系统
# print(sys.platform)
# # print(platform.system)
# print(platform.system())
# print(platform.machine)
# print(platform.uname)

# 那如果我们想要知道更详细的信息呢？想要更详细的区分？这时候就要用到 platform 库了。
# platform.system 方法会返回当前操作系统的类型，Windows？Linux？OS X？Unix？FreeBSD？它能比较详细的区分。（其他的一般只能识别Windows和非Windwos）
# platform.release 方法会返回当前操作系统的版本。笔者的测试环境是Windows 10 64位，它返回的结果是 10 。（Python2和Python3都一样）。相应的，如果是Windows 7，则会返回 7 ；Windows XP则返回 XP。有点特殊的是对于Linux发行版，它返回的是内核（kernel）的版本号。 这点要注意。
# platform.version 方法返回的则是当前系统的版本号，这个就不细说了。
# platform.machine 方法返回的是系统的结构，64位or32位。
# platform.uname 方法返回一个 元组 ，里面包含了当前操作系统的更详细的信息，方便调用。


# if(platform.system()=='Windows'):
#     print('Windows系统')
# else if(platform.system()=='Linux'):
#     print('Linux系统')
# else:
#     print('其他')
