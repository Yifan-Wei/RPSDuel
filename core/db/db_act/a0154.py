#!/usr/bin/python
# -*- coding:utf-8 -*-

# ------------------------------------------------
# type action
# log
#       author: Iric
#       version: 0.01 
#       uptime: 2021/07/03
#       content: create this file
# -------------------------------------------------
from db.db_act.actionbase import ActionBase

class ACTION_a0154(ActionBase):

    def __init__(self):
        
        # 继承父类构造
        ActionBase.__init__(self)
        # 行动编号,需要与文件名一致
        self.code = r"a0154"
        # 行动名,随便写,不是关键字
        self.name = r"手枪速射"
        # 所属职业
        self.job = r"战士"
        # 所属流派
        self.stream = r"忍者"
        # 具体类型：UNLOCK/LOCK锁定
        self.type = "LOCK"
        # 稀有度
        self.rarity = "RARE"

        # ---------------------------------------------
        # 通用技能消耗条件
        self.act_condition["COM_COST_COND"]= 1
        # 通用技能消耗条件
        self.act_condition["DUR_COST"] = 1
        # ......

        # ----------------------------------------------
        # 开始阶段
        # 是否有开始阶段(没有开始阶段的话,后面跳过)
        self.start_phase = False
        # 开始阶段执行内容(列表)
        ## self.content_start_phase = []
        # STEP 1
        step = {}
        step["harmful"] = False
        self.content_start_phase.append(step)
        # STEP 2 if there is
        # .......

        # ---------------------------------------------
        # 顺序阶段
        # 是否有顺序阶段步骤动作
        self.order_phase = True
        # 顺序阶段步骤内容
        # self.content_order_phase = []
        # STEP 1
        # STEP 1 TYPE
        if True:
            step = {}
            step["harmful"] = True
        # STEP 1 condition
        if True:
            step_condition = {}
            step_condition["COM_ATK_COND"]= 1
            step["condition"] = step_condition
        # STEP1 CONTENT
        if True:
            step_content = {}
            # STEP 1 harm
            if True:
                harm = {}
                harm["HARM_CONST"] = 0
                harm["HARM_VARIANT"] = {"ROLE_STR": 0.25}
                step_content["HARM_INFLICT"] = harm
            # STEP 1 if_hit
            if True:
                if_hit = {}
                if_hit["IF_HIT"] = if_hit
            # STEP 1 if_harm
            if True:
                if_harm = {}
                step_content["IF_HARM"] = if_harm
                
        step["content"] = step_content
        self.content_order_phase.append(step)
        # STEP 2
        # 手里剑的step2和step1完全一致
        self.content_order_phase.append(step)
        # ......

        # ----------------------------------------------
        # 结束阶段
        # 是否有开始阶段(没有开始阶段的话,后面跳过)
        self.ender_phase = False
        # 结束阶段执行内容(列表)
        # self.content_ender_phase = []
        # STEP 1
        step = {}
        step["harmful"]:False
        self.content_ender_phase.append(step)
        
        #print(self.content_order_phase)
        
if __name__ == "__main__":
    a = ACTION_a0154()
    a.js_print()