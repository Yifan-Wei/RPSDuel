#!/usr/bin/python
# -*- coding:utf-8 -*-

# ------------------------------------------------
# type action
# log
#       author: Iric
#       version: 0.01 
#       uptime: 2021/07/04
#       content: create this file
# -------------------------------------------------
from db.db_role.rolebase import RoleBase

class ROLE_c0001(RoleBase):

    def __init__(self, id):
        
        # 继承父类构造
        RoleBase.__init__(self)
        # 角色二维码, 整局游戏唯一的身份标识
        self.id = id
        # 角色编号
        self.code = "c0001"
        # 所属职业
        self.job = r"战士"
        # 所属流派
        self.stream = r"大师"
        # 稀有度
        self.rarity = "Normal"
        
        # 角色默认状态
        # 基础属性
        basic = {}
        # ROLE_HP/MP/CORE/DUR/STR/INT/SPD/ARM
        if True:
            # HP/MP/CORE/DUR/ARM 这些参数要设置两个，一个当前值一个最大值
            basic["ROLE_HP"] = 100
            basic["ROLE_MAX_HP"] = 100
            basic["ROLE_DUR"] = 6
            basic["ROLE_MAX_DUR"] = 6
            
            # 参数STR/INT/SPD只用设置一个
            basic["ROLE_STR"] = 20
            basic["ROLE_INT"] = 20
            basic["ROLE_SPD"] = 6
        self.status_default["basic"]=basic
        
        # buff属性 直接初始化(调用函数初始化)
        self.init_buff_status()
        
        # 角色当前状态(调用函数初始化)
        self.init_current_status()
        # 角色被动(不知道有没有用)
        self.feature = {}
        # 角色说明
        self.introduction = r"自律带来力量"
        
if __name__ == "__main__":
    pass