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
import gc,os,sys
from db.db_role.rolefunc import *
from db import *


def init_action_dict(path="."):
    """
    整局游戏开始时, 用来根据特定文件命名规范寻找action类文件, 创建一个实例化字典
    """
    action_dict = {}
    
    for root, dirs, files in os.walk(path):
        for file_name in files:
            #print(file_name)
            if  file_name.startswith("a") and file_name.endswith(".py"):
                action_string = ""
                try:
                    action_string = "a" + str(int(file_name.replace(".py","").replace("a",""))).zfill(4)
                except Exception as e:
                    pass
                if action_string != "":
                    action_dict[action_string] = eval("db_act.{0}.ACTION_{0}()".format(action_string))
    return action_dict


def init_role_feature(pool):
    """
    整局游戏开始时, 角色被动初始化
    """
    
    for role in pool[::-1]:
        exert_effect(role, step_content=role.feature)
    return


def choose_player_target(pool):
    """
    测试用, 用来让玩家输入本回合行动
    循环询问所有玩家的行动
    目的是获得本回合目标和本回合行动
    """
    for role in pool[::-1]:
         
        # 创建一个目标目录, 包含敌对目标
        target_list_tmp = []
        target_string = None
        target_true = None
        for target in pool:
            if target!=role:
                target_list_tmp.append(target)
        if not(role.ai):
            # -----------这个循环是给玩家的----------
            # 循环要求输入目标, 完成目标输入后循环完成
            target_invalid = True
            while target_invalid:
                # 先让玩家从pool里选目标
                print("请选择本轮的锁定目标")
                kk = 0
                print("0: 无锁定目标")
                for target in target_list_tmp[::-1]:
                    kk+=1
                    print("{0}: 锁定-{1}".format(kk,target.nickname))
                input_string = input()
                try:
                    target_string = int(input_string)-1
                except :
                    pass
                if target_string != None:
                    if target_string < 0:
                        target_true = []
                    elif target_string < len(target_list_tmp):
                        target_true = [target_list_tmp[target_string]]
                    else:
                        print("ERROR-错误输入")
                # 确定目标, 可以跳出了
                if target_true != None:
                    #print(target_true)
                    target_invalid = False
                    role.set_round_target(target_true)
        else:
            # -----------这个是给电脑的逻辑------------
            # 随便写个AI, 电脑耐力为0的时候只会无锁定
            if role.get_role_dur()!=0:
                if random.randint(1,1000)%2==0:
                    target = []
                else:
                    target = [random.choice(target_list_tmp)]
            else:
                target = []
            role.set_round_target(target)
        
        del target_list_tmp
        gc.collect()


def get_player_target_status(pool):
    num_be_targeted = 0
    for role in pool[::-1]:
        if not(role.ai):
            for target in pool[::-1]:
                if (role!=target) and (role in target.get_round_target()):
                    num_be_targeted +=1
            if num_be_targeted==0:
                print("灵感: 本回合未被锁定")
            else:
                print("灵感: 本回合共有{0}人锁定你".format(num_be_targeted))

            
def choose_player_action(pool=[],action_dict={}):
    
    for role in pool[::-1]:
        # 根据这个目标开始挑选行动
        action_list_tmp = []
        action = None
        for key, value in action_dict.items():
            # 查询列表里面的行动符不符合当前角色的条件
            if is_qualified_to_act(role=role, condition=value.act_condition):
                # 把可以使用的加入列表
                action_list_tmp.append(value)
                
        if action_list_tmp != []:
            if not(role.ai):
                # -----------这个循环是给玩家的----------
                # 循环要求输入目标, 完成目标输入后循环完成
                # 循环要求输入
                action_invalid = True
                while action_invalid:
                    kk = 0
                    for action in action_list_tmp:
                        kk += 1
                        print("{0}: {1}".format(kk, action.name))
                    input_string = input("{}的行动是: ".format(role.nickname))
                    try:
                        action = action_list_tmp[int(input_string)-1]
                    except Exception as e:
                        pass
                    if action != None:
                        action_invalid = False
                # ---------------------------------------
            else:
                action = random.choice(action_list_tmp)   
        else:
            print("本回合{}无可用行动".format(role.nickname))
        
        # 设置
        # -----------------------------------------------------------------
        if action != None:
            action_string = action.code
            action_tmp = eval("db_act.{0}.ACTION_{0}()".format(action_string))
            role.set_round_action(action_tmp)
        else:
            role.set_round_action(None)
            role.set_round_target([])
            
        # 用完了list_tmp删掉
        del action_list_tmp
        gc.collect()


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
    
    print("--------------第{0}回合-------------".format(round+1))
    
    # 获取本回合各人的行动
    for role in pool[::-1]:
        # 开始行动
        action = role.get_role_action()
        if not(action==None):
            
            # 存在ACT, 先检查ACT是否不满足发动条件
            # 这种情况理应当不会发生, 因为选择行动的时候就应该做这个判断了, 但是还没写这个
            # condition 是个字典
            if is_qualified_to_act(role=role, condition=action.act_condition):
                target = role.get_round_target()
                if target == []:
                    string = "{0} 进行行动: {1}".format(role.nickname, action.name)
                else:
                    string = "{0} 锁定{2} 进行行动: {1}".format(role.nickname, action.name, target[0].nickname)
            else:
                # 不满足发动条件, 有动作也不要了,直接给个None回去
                set_action_from_role(role=role,action=None)
                string = "{} 不满足 {} 的行动条件, 无法行动".format(role.nickname, action.name)
        else:
            string = "{} 没有行动".format(role.nickname)
        print(string)
    
    # 这里再来一遍循环是为了让判断和结算独立(不会出现判断+结算导致另外一个判断失效的情况)
    # 结算行动COST, 未来将上面的部分移出之后, 这个部分是整个的开头
    for role in pool[::-1]:
        action = role.get_role_action()
        if not(action==None):
            # 现在结算流程单独处理
            trig_action_cost(role=role,condition=action.act_condition)
    
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

    