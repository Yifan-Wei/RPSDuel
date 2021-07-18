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
    
    # 在开始的时候先初始化一个全局的全行动字典, 用来查询
    # 这个字典不会用在查询以外的地方
    ACTION_DICT = init_action_dict()
    
    # 初始化人物与战斗池
    pool = []
    a = db_role.c0002.ROLE_c0002(r"001")
    b = db_role.c0001.ROLE_c0001(r"002")
    c = db_role.c0001.ROLE_c0001(r"003")
    pool.append(a)
    pool.append(b)
    #pool.append(c)
    
    a.nickname = r"织田信长"
    a.status_current["basic"]["ROLE_SPD"]=4
    a.camp = r"织田家"

    b.nickname = r"明智光秀"
    b.status_current["basic"]["ROLE_SPD"]=6
    b.camp = r"叛徒"
    b.ai = True
    
    c.nickname = r"杂鱼小兵"
    c.status_current["basic"]["ROLE_SPD"]=5
    c.camp = r"叛徒"
    c.ai = True
    
    # 初始化人物特性
    init_role_feature(pool)
    
    round = 0
    end_flag = False
    # 循环战斗，直到耗尽
    while (end_flag==False):
    
        # 循环池中人物状态, 这一步不在main_round里面是因为会把target给洗了
        for role in pool[::-1]:
            role.suc_round_status()
            role.print_basic_status()
        
        # 锁定阶段
        choose_player_target(pool)
        # 灵感阶段
        get_player_target_status(pool)
        # 行动阶段
        choose_player_action(pool,action_dict=ACTION_DICT)
        # 结算行动
        pool = main_round(pool, round)
        # 跳出判断
        end_flag = is_battle_end(input_pool=pool)
        # 循环
        round +=1
    
    if a.is_role_alive():
        print("恭喜您获得胜利")
    else:
        print("敌 在 本 能 寺！")