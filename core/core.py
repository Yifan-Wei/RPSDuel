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
import sys, gc, math, os, time, shutil, ast, random
import pandas as pd
import json as js

# self-designed
from db import *
from func import *

if __name__ == "__main__":
    
    end_flag = False
    pool = []
    a = db_role.c0001.ROLE_c0001(r"001")
    b = db_role.c0001.ROLE_c0001(r"002")
    pool.append(a)
    pool.append(b)
    
    a.nickname = r"织田信长"
    a.status_current["basic"]["ROLE_SPD"]=154
    a.camp = r"幕府"

    b.nickname = r"明智光秀"
    b.status_current["basic"]["ROLE_SPD"]=100
    b.camp = r"叛徒"
    round = 0
    
    strategy_list = ["a0003","a0004","a0009","a0012","a0066","a0154"]
    name_list = [r"修整",r"重振旗鼓",r"防御反击",r"攻击",r"枭首",r"手里剑"]
    
    # 循环战斗，直到耗尽
    while (end_flag==False):
        # 循环回合状态:
        for role in pool[::-1]:
            role.suc_round_status()
        
        # a是玩家自己输入的
        action_string = random.choice(strategy_list)
        action_tmp = eval("db_act.{0}.ACTION_{0}()".format(action_string))
        a.set_round_action(action_tmp)
        if action_tmp.type == "UNLOCK":
            a.set_round_target([])
        else:
            a.set_round_target([b])
            
        # b是随机控制的
        action_string = random.choice(strategy_list)
        print(action_string)
        action_tmp = eval("db_act.{0}.ACTION_{0}()".format(action_string))
        b.set_round_action(action_tmp)
        if action_tmp.type == "UNLOCK":
            b.set_round_target([])
        else:
            b.set_round_target([a])
        pool = main_round(pool)
        
        
        # 跳出判断
        end_flag = is_battle_end(input_pool=pool)
        # 循环
        round +=1