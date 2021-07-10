#!/usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------
# type action defination
# log
#       author: Iric
#       version: 0.01 
#       uptime: 2021/07/03
#       content: create this file
# -------------------------------------------------


class ActionBase(object):

    def __init__(self):
        
        # 行动编号,需要与文件名一致
        self.code = ""
        # 行动名,随便写,不是关键字
        self.name = ""
        # 所属职业
        self.job = ""
        # 所属流派
        self.stream = ""
        # 具体类型：UNLOCK/LOCK锁定
        self.type = ""
        # 稀有度
        self.rarity = ""
        
        # 技能整体发动条件初始化
        self.act_condition = {}
        
        # 是否有开始阶段(没有开始阶段的话,后面跳过)
        self.start_phase = False
        # 开始阶段执行内容(列表)
        self.content_start_phase = []
        
        # 是否有顺序阶段(没有开始阶段的话,后面跳过)
        self.order_phase = False
        # 顺序阶段执行内容(列表)
        self.content_order_phase = []
        
        # 是否有结束阶段(没有开始阶段的话,后面跳过)
        self.ender_phase = False
        # 结束阶段执行内容(列表)
        self.content_ender_phase = []
    
    
    def js_print(self):
        
        import json as js
        
        dict_print = {}
        dict_print["code"] = self.code
        dict_print["name"] = self.name
        dict_print["job"] = self.job
        dict_print["stream"] = self.stream
        dict_print["act_condition"] = self.act_condition
        dict_print["start_phase"] = self.start_phase
        dict_print["content_start_phase"] = self.content_start_phase
        dict_print["order_phase"] = self.order_phase
        dict_print["content_order_phase"] = self.content_order_phase
        dict_print["ender_phase"] = self.ender_phase
        dict_print["content_ender_phase"] = self.content_ender_phase
        str_print = js.dumps(dict_print)
        print(str_print)

if __name__ =="__main__":
    pass