# ╔══════════════════════════════════════════════════════════════════════════╗
# ║ Copyright 2022. quinn.7@foxmail.com All rights reserved.                 ║
# ║                                                                          ║
# ║ Licensed under the Apache License, Version 2.0 (the "License");          ║
# ║ you may not use this file except in compliance with the License.         ║
# ║ You may obtain a copy of the License at                                  ║
# ║                                                                          ║
# ║ http://www.apache.org/licenses/LICENSE-2.0                               ║
# ║                                                                          ║
# ║ Unless required by applicable law or agreed to in writing, software      ║
# ║ distributed under the License is distributed on an "AS IS" BASIS,        ║
# ║ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. ║
# ║ See the License for the specific language governing permissions and      ║
# ║ limitations under the License.                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
"""
@ 模块     : 自定义异常
@ 作者     : chenjiancheng
@ 邮箱     : quinn.7@foxmail.com
@ 编写时间 : 2022-08-10

@ 模块描述 :
    NULL

"""
import re

from .decorator import singleton_pattern


class AwakenErrorRecorder: ...


@singleton_pattern
class AwakenErrorRecorder:
    """
    [ 错误记录器 ]

    ---
    描述:
        NULL

    """

    _error_warehouse: list
    """ 错误信息仓库 """

    def __init__(self) -> None:
        self._error_warehouse = []


    def record(self, error_string: str) -> None:
        """
        [ 记录 ]

        ---
        描述:
            NULL

        """
        self._error_warehouse.append(error_string)


    def read(self) -> None:
        """
        [ 读取 ]

        ---
        描述:
            NULL

        """
        return self._error_warehouse


    def template_print(self) -> None:
        """
        [ 模板打印 ]

        ---
        描述:
            NULL

        """
        sym1 = '━'
        sym2 = '┃'
        sym3 = '┏'
        sym4 = '┗'
        sym5 = '┓'
        sym6 = '┛'
        tab_max_len = 50
        error_list = ['ERROR LIST', '       ']
        error_number = 0

        # 处理初始错误信息
        for error in self._error_warehouse:
            error_list.append(f'error {error_number} ::')
            if len(error) > tab_max_len:
                while 1:
                    error_list.append(error[0: tab_max_len-3])
                    error = error[tab_max_len-3:]
                    error_list.append(error)
                    if len(error) >= tab_max_len:
                        continue
                    else:
                        error_list.append(error[tab_max_len-3:])
                        error_number += 1
                        break
            else:
                error_list.append(error)
                error_number += 1
            
            error_list.append('       ')

        # 消除空字符
        error_list = [error.replace(' ', '') for error in error_list if error != '']

        # # 计算打印表字符长度
        # error_max_len = 0
        # for error in error_list:
        #     if len(error) > error_max_len:
        #         error_max_len = len(error)
        #         for s in error:
        #             if not u'\u4e00' <= s <= u'\u9fff':
        #                 error_max_len += 0.1
        # error_max_len = int(error_max_len)

        # 制表
        print(sym3 + sym1*(tab_max_len*2 + 3 - 20) + sym5)
        for error in error_list:
            offset = 0
            for s in error:
                if not u'\u4e00' <= s <= u'\u9fff':
                    offset += 1
            n = ' '*((tab_max_len*2 - len(error)*2 - 20) + offset)
            print(f'{sym2} {error} {n} {sym2}')
        print(sym4 + sym1*(tab_max_len*2 + 3 - 20) + sym6)


ERROR_RECORDER = AwakenErrorRecorder()
""" 错误记录器实例 """


class _AwakenBaseError(Exception):
    """ 
    [ 自定义异常基类 ]
    
    """

    def __init__(self, error: BaseException | str):
        self.err_name = re.findall(r'\[ (.*) \]', self.__doc__)[0]
        self.message = ''.join([self.err_name, ' :: ', str(error)])
        ERROR_RECORDER.record(self.message)

    def __str__(self) -> str:
        return self.message


class AwakenLogCreationError(_AwakenBaseError):
    """
    [ 日志创建异常 ]
    
    """


class AwakenLogOutputError(_AwakenBaseError):
    """
    [ 日志输出异常 ]
    
    """


class AwakenWebEngineError(_AwakenBaseError):
    """
    [ WEB引擎异常 ]
    
    """


class AwakenApiEngineError(_AwakenBaseError):
    """
    [ API引擎异常 ]
    
    """


class AwakenConvertCodelinError(_AwakenBaseError):
    """
    [ 转换代码行异常 ]
    
    """


class AwakenAnalysisBaseCodeError(_AwakenBaseError):
    """
    [ 解读底层编码异常 ]
    
    """


class AwakenTaskPretreatmentError(_AwakenBaseError):
    """
    [ 任务预处理异常 ]
    
    """

class AwakenWebApiServerError(_AwakenBaseError):
    """
    [ WebApi服务器异常 ]
    
    """


class AwakenDataBaseError(_AwakenBaseError):
    """
    [ 数据库异常 ]
    
    """


class AwakenWebEngineRunError(_AwakenBaseError):
    """
    [ WEB引擎运行异常 ]
    
    """

