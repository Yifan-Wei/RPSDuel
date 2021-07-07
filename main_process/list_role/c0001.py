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
import sys
sys.path.append("..")

# from gambase import RoleBase
from gamebase import *

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
    pool = []
    a = ROLE_c0001("114514")
    #print(a.id)
    #print(type(a))
    b = ROLE_c0001("5201314")
    pool.append(a)
    pool.append(b)
    member = role_from_id("114514", pool)
    member.add_buff_status("TOXIC",100,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_NEGATIVE":1})
    member.add_buff_status("REGENERATION",20,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_NEGATIVE":1})
    member.add_buff_status("BURNING",3,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_NEGATIVE":1})
    member.add_buff_status("PIERCING",1,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_POSITIVE":1})
    member.add_buff_status("PIERCING",4,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_POSITIVE":1})
    member.add_buff_status("PIERCING",4,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_POSITIVE":1}, add_mode="refresh")
    member.add_buff_status("PIERCING",4,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["114514"],"BUFF_IS_POSITIVE":1}, add_mode="anyway")
    member.add_buff_status("PIERCING",2,add_buff={"BUFF_SOURCE":["114514"],"BUFF_TARGET":["5201314"],"BUFF_IS_POSITIVE":1})
    member.add_buff_status("PIERCING",1,add_buff={"BUFF_SOURCE":["5201314"],"BUFF_TARGET":["5201314"],"BUFF_IS_POSITIVE":1})
    member.add_buff_status("PIERCING",2,add_buff={"BUFF_SOURCE":["5201314"],"BUFF_TARGET":["114514"],"BUFF_IS_POSITIVE":1})
    #print(member.get_buff_status("PIERCING"))
    #member.add_buff_status("TOXIC",3,["114514"],["114514"])
    #print(member.get_buff_status("TOXIC"))
    #result = member.rm_buff_status("TOXIC",3, pool,["114514"],["114514"],billmode="BILL")
    #print(result)
    #print(member.get_buff_status("TOXIC"))
    member.print_buff_status()
    member.iter_buff_status(pool)
    #print(result)
    #print(member.get_buff_status("BEHEAD"))
    #print(member.get_role_hp())
    #print(member.get_role_dur())
    #member.set_role_dur(-4)
    #print(member.get_role_dur())
    member.print_buff_status()
    