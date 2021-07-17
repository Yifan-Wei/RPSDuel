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
    a = db_role.c0002.ROLE_c0002(r"001")
    b = db_role.c0001.ROLE_c0001(r"002")
    pool.append(a)
    pool.append(b)
    
    a.nickname = r"织田信长"
    a.status_current["basic"]["ROLE_SPD"]=4
    a.camp = r"幕府"

    b.nickname = r"明智光秀"
    b.status_current["basic"]["ROLE_SPD"]=6
    b.camp = r"叛徒"
    round = 0
    
    strategy_list = ["a0003","a0004","a0009","a0012","a0066","a0154"]
    name_list = [r"修整",r"重振旗鼓",r"防御反击",r"攻击",r"枭首",r"手里剑"]
    
    init_role_feature(pool)
    
    # 循环战斗，直到耗尽
    while (end_flag==False):
    
        # 循环池中人物状态, 这一步不在main_round里面是因为会把target给洗了
        for role in pool[::-1]:
            role.suc_round_status()
            role.print_basic_status()
        
        # a是玩家自己输入的
        # action_string = random.choice(strategy_list)
        # -----------------------------------------------------------------
        action_invalid = True
        # 循环要求输入
        while action_invalid:
            print("请输入{}的行动".format(a.nickname))
            for ii in range(len(strategy_list)):
                print("#{0} :{1}".format(ii+1,name_list[ii]))
            choice = int(input().replace("#",""))-1
            if choice<len(strategy_list):
                action_string = strategy_list[choice]
            else:
                action_string = ""
            if action_string in strategy_list:
                action_invalid = False
        # -----------------------------------------------------------------
        
        print(action_string)
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
        
        
        # 主结算
        pool = main_round(pool, round)
        
        
        # 跳出判断
        end_flag = is_battle_end(input_pool=pool)
        # 循环
        round +=1