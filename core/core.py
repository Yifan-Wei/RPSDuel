#!/usr/bin/python
# -*- coding: UTF-8 -*-

# -------------------------------------------
# Author: weiyifan
# Build Time: 12th June
# Last Update: 12th June

# log
# v 0.1 12th June weiyifan: start to practice
# v 0.2 7th July weiyifan: add a lot things

# -------------------------------------------
import sys, gc, math
import os,sys,time,shutil,ast
import pandas as pd
import json as js
from ast import literal_eval


# self-designed
from db import *
from func import *

if __name__ == "__main__":
    print("铁华团的战斗开始了！")
    pool = []
    a = db_role.c0001.ROLE_c0001(r"001")
    b = db_role.c0001.ROLE_c0001(r"002")
    c = db_role.c0001.ROLE_c0001(r"003")
    a.set_role_str(value=50)
    b.set_role_str(value=50)
    a.set_role_dur(value=-3)
    b.set_role_dur(value=-3)
    a.nickname = r"夏亚"
    b.nickname = r"团长"
    c.nickname = r"杰哥"
    pool.append(a)
    pool.append(b)
    pool.append(c)
    
    a.add_buff_status("CRITICAL",1,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1})

    #b.add_buff_status("DEFENDING",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1,"BUFF_VALUE":25})
    #b.add_buff_status("DEFENDING_BEATBACK",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1})
    
    
    #b.add_buff_status("DEFENDING",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1,"BUFF_VALUE":10}, add_mode="anyway")
    #b.add_buff_status("DEFENDING",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1,"BUFF_VALUE":10}, add_mode="anyway")
    #b.add_buff_status("DEFENDING",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1,"BUFF_VALUE":10}, add_mode="anyway")
    #b.add_buff_status("PIERCING",2,add_buff={"BUFF_SOURCE":[r"001"],"BUFF_TARGET":[r"001"],"BUFF_IS_POSITIVE":1})
    
    b.add_buff_status("BLIND",2,add_buff={"BUFF_SOURCE":[r"002"],"BUFF_TARGET":[r"002"],"BUFF_IS_NEGATIVE":1})
    #b.add_buff_status("EVADING",2,add_buff={"BUFF_SOURCE":[r"002"],"BUFF_TARGET":[r"002"],"BUFF_IS_POSITIVE":1})
    #b.add_buff_status("MUSTHIT",2,add_buff={"BUFF_SOURCE":[r"002"],"BUFF_TARGET":[r"002"],"BUFF_IS_POSITIVE":1})
    
    a0009_1 = db_act.a0009.ACTION_a0009()
    a0066_1 = db_act.a0066.ACTION_a0066()
    a0154_1 = db_act.a0154.ACTION_a0154()
    
    a.status_current["round"]["ROUND_ACTION"]=a0154_1
    b.status_current["round"]["ROUND_ACTION"]=a0009_1
    c.status_current["round"]["ROUND_ACTION"]=a0066_1
    a.set_round_target([b])
    b.set_round_target([])
    c.set_round_target([a])
    exert_effect(role=c,step_content={"EXERT_BUFF_BEHEAD":1})
    a.status_current["basic"]["ROLE_SPD"]=154
    b.status_current["basic"]["ROLE_SPD"]=100
    c.status_current["basic"]["ROLE_SPD"]=174
    main_round(pool)
    
    """
    member = get_role_from_id("001", pool)
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
    """