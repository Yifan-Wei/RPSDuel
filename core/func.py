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
import gc
from db.db_role.rolefunc import *
    
def main_round(input_pool):

    """
    主结算函数
    input_pool: 递进来的结算池, 实际结算用排序池, 这个池子应该不会用
    
    """
    # 开始前阶段
    # 先按角色速度排序
    pool = sorted(input_pool,key=lambda x:x.status_current["basic"]["ROLE_SPD"])
    
    # 获取本回合各人的行动
    for role in pool[::-1]:
        # 开始行动
        action = get_action_from_role(role=role)
        if not(action==None):
            string = "{} 开始行动".format(role.id)
            
        else:
            string = "{} 没有行动".format(role.id)

    
    
        
        print(string)
    
    # 起始阶段
    for role in pool[::-1]:
        pass
        
        
        
    # 顺序阶段
    for role in pool[::-1]:
        pass
        
        
        
    # 结束阶段
    for role in pool:
        pass
        
        
        