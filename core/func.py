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


def is_battle_end(input_pool):
    # 统计剩余阵营数目
    end_dict = {}
    cmp = 0
    for role in input_pool[::-1]:
        camp = role.camp
        if camp in end_dict.keys():
            end_dict[camp]+=1
        else:
            end_dict[camp]=1
    # 打印战局
    for key, value in end_dict.items():
        print("{0}阵营残余{1}人".format(key,value))
        cmp += 1
    # 跳出条件
    if (cmp==1):
        return True
    return False

def input_action_string():
    action_invalid = True
    # 循环要求输入
    while action_invalid:
        print("请输入你的行动")
        for ii in range(len(strategy_list)):
            print("##{0}={1}".format(strategy_list[ii],name_list[ii]))
        action_string = input()
        if action_string in strategy_list:
            action_invalid = False
    return action_string


def main_round(input_pool, round=0):

    """
    主结算函数
    input_pool: 递进来的结算池, 实际结算用排序池, 这个池子应该不会用
    
    """
    # 开始前阶段
    # 先按角色速度排序
    pool = sorted(input_pool,key=lambda x:x.status_current["basic"]["ROLE_SPD"])
    # 多余的东西,直接删了
    del input_pool
    gc.collect()
    
    
    # 获取本回合各人的行动
    for role in pool[::-1]:
        # 开始行动
        action = role.get_role_action()
        if not(action==None):
            
            # 存在ACT, 先检查ACT是否不满足发动条件
            # 这种情况理应当不会发生, 因为选择行动的时候就应该做这个判断了, 但是还没写这个
            # condition 是个字典
            if is_qualified_to_act(role=role, condition=action.act_condition):
                string = "{0} 满足条件, 开始行动: {1}".format(role.nickname, action.name)
                
            else:
                # 不满足发动条件, 有动作也不要了,直接给个None回去
                set_action_from_role(role=role,action=None)
                string = "{} 不满足 {} 的行动条件, 无法行动, 好逊哦".format(role.nickname, action.name)
        else:
            string = "{} 没有行动".format(role.nickname)
        print(string)
    
    # 起始阶段
    for role in pool[::-1]:
        # 获取该阶段step_list
        step_list = get_step_list_in_start_phase_from_role(role=role)
        if not(step_list==None):
            for step in step_list:
                # 首先确定行动条件
                step_condition = None
                step_content = None
                if "condition" in step.keys():
                    step_condition = step["condition"]
                if "content" in step.keys():
                    step_content = step["content"]
                # 先判断条件是否成立, 这里不成立的话, 本次step不进行
                if is_qualified_to_act(role=role, condition=step_condition):
                    # 施加效果
                    exert_effect(role=role, step_content=step_content)
        
    # 顺序阶段
    # 顺序阶段是有顺序的, 按照顺序来排
    is_order_phase_end = False
    order = 0
    # 大循环: 直到所有order都被结算完成
    while not(is_order_phase_end):
        print("-------------第{0}战斗轮-----------".format(order+1))
        
        # 为了防止结算的时候要再判断一次交锋生效性
        # 先进行一次快速判断
        for role in pool[::-1]:
            # 开始判断
            step = get_step_in_order_phase_from_role(role, order)
            # print("{0} - {1}".format(role.nickname,step))
            if not(step==None):
                # 首先确定行动条件
                step_condition = None
                if "condition" in step.keys():
                    step_condition = step["condition"]
                # 先判断条件是否成立, 这里不成立的话, 本次step的行动清空
                if not(is_qualified_to_act(role=role, condition=step_condition)):
                    # 清空
                    set_step_in_order_phase_from_role(role=role, order=order, step={})
        
        # 正式开始结算, 预设所有人都能动
        number_of_no_action_role = 0
        
        # 条件已经全部检查完毕, 正式操作 
        for role in pool[::-1]:
            # 开始行动
            action = role.get_role_action()
            # 判断当前遍历的角色能否在这个阶段行动
            if not(action==None) and (action.order_phase):
                # 如果有行动, 且行动有起始阶段, 继续
                # content_order_phase是个列表,列表里面有所有的行动
                if len(action.content_order_phase)>= order + 1:
                    
                    # 获取行动字典step
                    step = action.content_order_phase[order]
                    # print("{0} # {1}".format(role.nickname,step))
                    
                    # 首先看一眼行动字典是什么内容, 其中条件已经不用看了
                    # 略过step_condition=step["condition"]
                    if "harmful" in step.keys():
                        step_harmful = step["harmful"]
                    if "content" in step.keys():
                        step_content = step["content"]
                        # 有内容的前提下继续操作
                        if step_harmful:
                            # 本次动作涉及到伤害
                            # 调用函数damage_calculation
                            damage_result = cal_damage(role=role, content=step_content, order=order)
                        else:
                            # 本次行动不涉及到伤害
                            exert_effect(role=role, step_content=step_content)
                else:
                    # 对于一些处于等待触发的状态, 即使没有行动, 也不能断定下个回合没有行动
                    # 一个解决办法就是往等待触发的状态里面塞空字典
                    # 比如一个等待触发的防反, 前5次结算都被塞了空字典
                    # 结算的时候再塞一个行动就会在第6次结算的顺位上
                    # 但是这样随着结算顺序可能存在先被塞了额外行动
                    # 这样的话就是当场防反了
                    # 在结算函数里面要注意这一点, 要把轮次给代入进去
                    # 因为每个人的行动都不一样, 开始的时候每个人都得是各自实例化的行动, 不能是同一地址的行动
                    action.content_order_phase.append({})
                    
                    # 行动列表不够长的人, 当然也是行动完了
                    number_of_no_action_role += 1
            else:
                # 没行动的人, 或者顺序阶段没行动的人+1
                number_of_no_action_role += 1
        
        # 如果所有人都没得动了, 顺序阶段就结束
        # 否则的话, order+1, 继续
        if number_of_no_action_role == len(pool):
            is_order_phase_end = True
        else:
            print("********************")
            order += 1
        
    
    print("----------战斗阶段结束, 共{0}轮--------".format(order))   
        
        
    # 结束阶段
    for role in pool[::-1]:
        # 获取该阶段step_list
        step_list = get_step_list_in_ender_phase_from_role(role=role)
        if not(step_list==None):
            for step in step_list:
                # 首先确定行动条件
                step_condition = None
                step_content = None
                if "condition" in step.keys():
                    step_condition = step["condition"]
                if "content" in step.keys():
                    step_content = step["content"]
                # 先判断条件是否成立, 这里不成立的话, 本次step不进行
                if is_qualified_to_act(role=role, condition=step_condition):
                    # 施加效果
                    exert_effect(role=role, step_content=step_content)
            
    
    # buff循环阶段
    for role in pool[::-1]:
        role.iter_buff_status(pool)
        role.print_buff_status()
        
        
    # 死亡结算阶段
    for role in pool[::-1]:
        if not(role.is_role_alive()):
            pool.remove(role)
            print("{0}因为死亡, 已经被从战斗中移出".format(role.nickname))
    
    
    return pool