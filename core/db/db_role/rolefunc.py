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

# 这个函数被独立出来, 是因为这里的东西基本与Buff有关,与Role不相关

import gc, math, random

def get_role_from_id(id, pool):
    # 遍历池子里的结构体
    for member in pool:
        if member.id == id:
            return member
    # 找不到返回空
    return None

def get_action_from_role(role):
    
    if "ROUND_ACTION" in role.status_current["round"].keys():
            action = role.status_current["round"]["ROUND_ACTION"]
            return action
    else:
        return None 

def get_step_in_order_phase_from_role(role, order):
    """
    获取目标在顺序阶段第order轮的行动
    没有返回None
    """
    # 初始化
    step = None
    
    # 获取action
    action = get_action_from_role(role)
    # 如果action存在
    if not(action==None):
        # 如果action的顺序阶段不是跳过的
        if action.order_phase:
            # 如果顺序阶段大于等于order个行动
            # order=0, len>=1
            if len(action.content_order_phase) >= order+1:
                step = action.content_order_phase[order]
        
    #返回结果
    return step


def set_action_from_role(role, action):
    
    if "ROUND_ACTION" in role.status_current["round"].keys():
        role.status_current["round"]["ROUND_ACTION"]=action
    else:
        role.status_current["round"]["ROUND_ACTION"]=None
    return

def full_empty_buff(buff):
    """
    把没有字段的buff填满,主要是用来把默认值填满
    BUFF_SOURCE, BUFF_TARGET, BUFF_IS_POSITIVE, BUFF_IS_NEGATIVE, BUFF_IS_SHEDDING
    BUFF_LAYER, BUFF_MAX_LAYER, BUFF_COUNT, BUFF_VALUE
    """
    
    # 默认无来源
    if not("BUFF_SOURCE" in buff.keys()):
        buff["BUFF_SOURCE"] = []
    # 默认无目标
    if not("BUFF_TARGET" in buff.keys()):
        buff["BUFF_TARGET"] = []  
    # 默认不是正面
    if not("BUFF_IS_POSITIVE" in buff.keys()):
        buff["BUFF_IS_POSITIVE"] = 0
    # 默认不是负面
    if not("BUFF_IS_NEGATIVE" in buff.keys()):
        buff["BUFF_IS_NEGATIVE"] = 0 
    # 默认可衰减
    if not("BUFF_IS_SHEDDING" in buff.keys()):
        buff["BUFF_IS_SHEDDING"] = 1
    # 默认可驱散
    if not("BUFF_IS_DISPELLABLE" in buff.keys()):
        buff["BUFF_IS_DISPELLABLE"] = 1
    # 默认可见
    if not("BUFF_IS_VISIBLE" in buff.keys()):
        buff["BUFF_IS_VISIBLE"] = 1 
    # 默认层数为0
    if not("BUFF_LAYER" in buff.keys()):
        buff["BUFF_LAYER"] = 0
    # 默认最大层数为65536
    if not("BUFF_MAX_LAYER" in buff.keys()):
        buff["BUFF_MAX_LAYER"] = 65536
    # 默认次数为0
    if not("BUFF_COUNT" in buff.keys()):
        buff["BUFF_COUNT"] = 0
    # 默认值为0
    if not("BUFF_VALUE" in buff.keys()):
        buff["BUFF_VALUE"] = 0 
    # 默认优先级为0
    if not("BUFF_PRIORITY" in buff.keys()):
        buff["BUFF_PRIORITY"] = 0
    # 默认保留字段为无
    if not("BUFF_PRESERVE" in buff.keys()):
        buff["BUFF_PRESERVE"] = None
    
    return


def is_buff_the_same(dut_buff={}, cmp_buff={}):
    """
    # 第三层是字典, 字典键带有buff来源, buff对象, buff正面标识符, buff负面标识符, buff脱落标识符, buff层数, buff最大层数, buff次数, buff数值, buff优先级, buff预留字段
    # 关键字是 BUFF_SOURCE=[], BUFF_TARGET=[], BUFF_IS_POSITIVE=0/1, BUFF_IS_NEGATIVE=0/1, BUFF_IS_SHEDDING=0/1, BUFF_IS_DISPELLABLE=0/1, BUFF_IS_VISIBLE=0/1, BUFF_LAYER=INTEGER, BUFF_MAX_LAYER = INTEGER, BUFF_COUNT=INTEGER, BUFF_VALUE=FLOAT, BUFF_PRIORITY=INTEGER, BUFF_PRESERVE=None
    # 比较来源、对象、正负面、衰减、可驱散、可见、最大层数、值、优先级
    """
    # 先把buff可能空置的地方填满
    full_empty_buff(dut_buff)
    full_empty_buff(cmp_buff)
    
    # 顺着比,有一个不满足就return False,跳过后面的
    if not dut_buff["BUFF_SOURCE"]==cmp_buff["BUFF_SOURCE"]:
        return False
    if not dut_buff["BUFF_TARGET"]==cmp_buff["BUFF_TARGET"]:
        return False
    if not dut_buff["BUFF_IS_POSITIVE"]==cmp_buff["BUFF_IS_POSITIVE"]:
        return False
    if not dut_buff["BUFF_IS_NEGATIVE"]==cmp_buff["BUFF_IS_NEGATIVE"]:
        return False
    if not dut_buff["BUFF_IS_SHEDDING"]==cmp_buff["BUFF_IS_SHEDDING"]:
        return False
    if not dut_buff["BUFF_IS_DISPELLABLE"]==cmp_buff["BUFF_IS_DISPELLABLE"]:
        return False
    if not dut_buff["BUFF_IS_VISIBLE"]==cmp_buff["BUFF_IS_VISIBLE"]:
        return False
    if not dut_buff["BUFF_MAX_LAYER"]==cmp_buff["BUFF_MAX_LAYER"]:
        return False
    if not dut_buff["BUFF_VALUE"]==cmp_buff["BUFF_VALUE"]:
        return False
    if not dut_buff["BUFF_PRIORITY"]==cmp_buff["BUFF_PRIORITY"]:
        return False
    
    return True

        
def rm_buff_status_from_dict(buff_string, buff_list, buff, rm_layer, pool, billmode="BILL"):
    
    """
    注意:
    这个函数如果在调用的时候, 外面有对buff_list的循环, 千万要倒序调用列表！
    千万要倒序!
    因为要删除列表内容, 正着遍历就会把后面那个跳过了
    
    
    拔除的时候需要处理的步骤比较多,单独分了个函数出来, 这个函数包含所有的特殊处理
    这个函数放在func而不是放在结构体的方法里面, 是因为里面的判断很多, 单独拿出来更好
    后续看看这个是否能移动到其他地方
    另一个rm_buff_status负责给这个函数指路(找buff)
    buff_string = 要操作的buff字段, 判断buff类型用的
    buff = 要操作的具体字典,具体操作用的
    rm_layer = 要拔除的buff层数,一般是1层
    pool = 做效果处理的时候需要联动环境做处理,需要当前池子
    mode = 默认BILL/ GATES, 如果是结算BILL模式就要计算每层buff的影响, 否则不结算, 后者用于净化类别
    """

    iter_layer = rm_layer
    print(" - {0} BUFF 有{1}层, 要减少{2}层".format(buff_string, buff["BUFF_LAYER"],iter_layer))
    
    # 涉及到伤害相关的,先拿ID_list
    id_source_list = buff["BUFF_SOURCE"]
    id_target_list = buff["BUFF_TARGET"]
    # 从ID返回结构体, 加入列表
    source_list = []
    for id_item in id_source_list:
        source_tmp = get_role_from_id(id_item,pool)
        if not(source_tmp is None):
            source_list.append(source_tmp)
    # 从ID返回结构体, 加入列表
    target_list = []
    for id_item in id_target_list:
        target_tmp = get_role_from_id(id_item,pool)
        if not(target_tmp is None):
            target_list.append(target_tmp)
    
    # 一起拿掉会出问题,直接进行一个循环的拿
    while iter_layer>0:
        # 每次循环开始都要获取
        layer = buff["BUFF_LAYER"]
        value = buff["BUFF_VALUE"]
        
        # 只有当结算模式是BILL的时候, 才进行细节结算
        if billmode=="BILL":
            
            # 拿掉层数的时候进行额外操作的buff
            # 按顺序是 再生
            if buff_string == "REGENERATION":
                # 再生时, 所有目标恢复层数生命
                for target in target_list:
                    target.set_role_hp(1.0*layer)
                    
            # 拿掉层数的时候进行额外操作的debuff
            # 按顺序是 灼烧 中毒 诅咒
            if buff_string == "BURNING":
                # 灼烧时, 所有目标生命值-5
                for target in target_list:
                    target.set_role_hp(-5.0)
                    
            elif buff_string == "TOXIC":
                # 中毒时, 所有目标失去层数生命
                for target in target_list:
                    target.set_role_hp(-1.0*layer)
            
            elif buff_string == "CURSED":
                # 诅咒时, 所有目标失去层数*10的生命上限
                for target in target_list:
                    target.set_role_hp(-10.0*layer, mode="default")
            
        # 结算完成, 拿掉层数
        buff["BUFF_LAYER"] = max(0, layer-1)
        
        # 如果层数归0, 且buff可脱落, 就拿掉buff, 省去另外处理
        if buff["BUFF_LAYER"]==0 and buff["BUFF_IS_SHEDDING"]==1:
            print(" - 移除0层 BUFF: {}".format(buff_string))
            buff_list.remove(buff)
            del buff
            gc.collect()
            # 归零了, 当然跳出循环
            break
        
        # 循环变量
        iter_layer -= 1
        
    
        
def is_qualified_to_act(role, condition={}):
    
    """
    role: 判断主体
    condition: 判断条件, 是个字典
    return True/False
    """
    
    # 这个函数放在这里是因为涉及多种条件罗列和判断,没办法写在role/action里面
    # 这个函数如果明确调用了函数,暂时都是rolebase里面的函数
    for key, value in condition.items():
        
        # -------------常规条件----------------
        # 通用消耗条件
        if key == "COMMON_COST_COND":
            if not role.is_meeting_cost_condition():
                return False
        # 通用战斗条件
        if key == "COMMON_ATK_COND":
            if not role.is_meeting_atk_condition():
                return False

        # 本回合受伤害情况=value, 包括受伤害和没受伤害的
        if key == "GET_HURT":
            if role.status_current["round"]["ROUND_GET_HURT"] != value:
                return False
        
        # 本回合施加伤害情况=value, 包括伤害过别人和没受过伤害的
        if key == "DO_HARM":
            if role.status_current["round"]["ROUND_DO_HARM"] != value:
                return False
        
        # 本回合交锋情况(应该不太可能存在正在交锋的情况)
        if key== "HAS_CONFRONTED":
            if role.status_current["round"]["ROUND_HAS_CONFRONTED"] != value:
                return False
        
        # 自身耐力-目标耐力>=value
        # 根据之前的结构, target也应该是个list, 不过这个判断条件默认单对单, 所以取[0]
        if key == "DUR_ABOVE_TARGET":
            target = role.status_current["round"]["ROUND_TARGET"][0]
            if ((role.get_role_dur() - target.get_role_dur()) < value):
                return False
                
        # 自身力量-目标力量>=value
        # 根据之前的结构, target也应该是个list, 不过这个判断条件默认单对单, 所以取[0]
        if key == "STR_ABOVE_TARGET":
            target = role.status_current["round"]["ROUND_TARGET"][0]
            if ((role.get_role_dur() - target.get_role_dur()) < value):
                return False
        
        # --------------------------------------
        #|#
        #|#
        #|#
        # --------------结算条件----------------
        # HP消耗, 要求当前HP严格大于消耗HP
        if key == "HP_COST":
            if role.get_role_hp() <= value:
                return False
        
        # DUR消耗, 要求当前DUR大于等于消耗DUR        
        if key == "DUR_COST":
            if role.get_role_dur() < value:
                return False
        # --------------------------------------
        #|#
        #|#
        #|#
        # -------------特殊条件-----------------
        # 暂时没有
        # --------------------------------------
        
    
    # 所有条件遍历完成之后, 开始处理结算条件
    for key, value in condition.items():
        
        # --------------结算条件----------------
        # HP消耗, 已要求当前HP严格大于消耗HP
        if key =="HP_COST":
            role.set_role_hp(-1*value)
        
        # DUR消耗, 已要求当前DUR大于等于消耗DUR        
        if key =="DUR_COST":
            role.set_role_dur(-1*value)
        # --------------------------------------
        
        
    # 最后return True
    return True 


def get_hit_result(role, target):
    
    """
    计算和闪避相关的结果
    顺序为：
        输出端-致盲
        伤害端-闪避类(目前只有闪避)
        输出端-必中
        输出端-不可避
    """
    # 结果初始化
    hit_result = False
    blind_result = False
    string = "%闪避%"
    # 致盲结算
    if role.is_buffed("BLIND"):
        # 获取随机数
        random_number_1 = random.random()
        # 50%概率致盲, 不致盲的话判断闪避
        if random_number_1 < 0.5:
            string += "致盲让{0}头晕目眩({1});".format(role.nickname,round(random_number_1,2))
            blind_result = True
        else:
            string += "{0}没有屈服给致盲({1});".format(role.nickname,round(random_number_1,2))
    
    # 闪避结算
    if not(blind_result):
        if target.is_evading():
            # 理论上未来可能有多种闪避, 但目前只有这一种, 因此只做这个结算
            # 75%概率闪避, 不闪避的话命中
            random_number_2 = random.random()
            if random_number_2 < 0.25:
                # 脸黑没闪掉
                string += "{0}闪得不够快({1});".format(target.nickname, round(random_number_2,2))
                hit_result = True
            else:
                string += "惊险! 还好{0}闪得够快({1});".format(target.nickname, round(random_number_2,2))
        else:
            hit_result = True
    
    # 必中结算
    if role.is_buffed("MUSTHIT"):
        # 即使闪避闪了, 必中还是会中
        hit_result = True
        string += "但{0}的攻击是必中的".format(role.nickname)
    
    # 不可抵挡的
    if role.is_unavoidable():
        # 即使闪避闪了, 不可抵挡的还是会中
        hit_result = True
        string += "但{0}的攻击是避无可避的".format(role.nickname)

    # 出结果
    print(string)
    return hit_result 

def get_harm_result(role, target, value):
    
    """
    计算防御作用后的伤害
    顺序为：
        伤害端-防御类(目前只有防御)
        输出端-穿甲
    """
    # 结果初始化
    harm_result = value
    is_defending = False
    defend_index = 0
    string = "%格挡%"
    
    # 格挡结算
    if target.is_defending():
        defend_buff_list = target.status_current["buff"]["DEFENDING"]
        for buff in defend_buff_list[::-1]:
            # 是否产生过至少一次抵挡:
            is_defending = True
            # 叠加格挡因素
            defend_index += buff["BUFF_VALUE"]
            # 如果累积的格挡已经超过了伤害值, 跳出
            if defend_index > harm_result:
                break
        string += "{0}累积格挡为{1},".format(target.nickname, defend_index)  
        
    # 穿甲结算
    if role.is_buffed("PIERCING"):
        # 即使累积了防御, 穿甲还是会造成全额伤害
        # 方法是把叠起来的加穿为0
        # 但是没作用上来的甲, 这里先不考虑
        defend_index = 0
        # 因为穿甲了, 等于没抵挡
        is_defending = False
        string += "但{0}的攻击穿透护甲,".format(role.nickname)
    
    # 出结果
    harm_result -= defend_index
    harm_result = max(0, harm_result)
    string += "{0}要对{1}造成{2}点税前伤害".format(role.nickname, target.nickname, harm_result)
    print(string)
    return harm_result, is_defending
    

def trig_harm(damager, victim, value, extra={}):
    
    """
    在这里触发伤害相关的行动
    可能不是最好的实现方法
    半成品
    """
    # 伤害端
    if damager.nickname== r"团长":
        print("团长: 什么嘛, 结果我打得还蛮准的嘛……")
    elif damager.nickname== r"夏亚":
        print("夏亚: 胜利是对死者最好的报答啊……")
            
    
    # 被伤害端
    victim.status_current["round"]["ROUND_GET_HURT"] = True
    if victim.nickname == r"夏亚":
        print("夏亚: 还没有结束呢！")
    elif victim.nickname == r"团长":
        print("团长: 我可是铁华团, 奥尔加·伊兹卡啊……")
  
  
def give_harm(role, target, value, extra={}):
    
    """
    首先进行与伤害相关的buff/debuff枚举
    按顺序: 暴击, 坚韧
    按顺序: 虚弱, 重创
    """
    string = ""
    role_multi_index = 1.0
    role_linear_index = 0.0
    target_multi_index = 1.0
    target_linear_index = 0.0
    # 先从攻击者开始
    # 虚弱*0.5 暴击*2.0 交锋*0.5
    
    if role.is_buffed("WEAK"):
        role_multi_index *= 0.5
        string += "虚弱的"
    if role.is_buffed("CRITICAL"):
        role_multi_index *= 2.0
        string += "暴击的"
    if "is_confronting" in extra:
        if extra["is_confronting"]:
            role_multi_index *= 0.5
            string += "交锋的"
    string += "{0}对".format(role.nickname)
    
    # 被攻击目标
    # 坚韧*0.5 重创*1.5
    if target.is_buffed("LASTAND"):
        target_multi_index *= 0.5
        string += "坚韧的"
    if target.is_buffed("FRAGILE"):
        target_multi_index *= 1.5
        string += "重创的"
        
    string += "{0}".format(target.nickname)
    # 伤害减免
    # 暂时没有, 先空着
    
    # 把进攻方和防守方的加权放在上面
    real_harm = (value + role_linear_index) * role_multi_index * target_multi_index + target_linear_index
    # 伤害的最小值为0
    real_harm = max(0, real_harm)
    
    string += "造成{0}伤害!".format(real_harm)
    print(string)
    
    # 改变血量
    target.set_role_hp(-1*real_harm)
    
    # 伤害触发器, 在两端触发操作
    trig_harm(damager=role, victim=target, value=real_harm)
       
  
def cal_damage(role, content={}, order=0):
    
    """
    damage伤害 = harm数值伤害 + buff伤害
    action = get_action_from_role()
    action.order_phase = True
    action.content_order_phase = [step1,step2,step3...]
    step1 = action.content_order_phase[order]
    step1 = {"harmful":True, "condition"={}, "content":{}}
    content = {"HARM_INFLICT":harm, "IF_HIT":None, "IF_HURT":None}
    """
    # --------------------------------------
    damage_result = {}
    # 顺序包含以下字段，先初始化:
    # 自身: 命中, 交锋, 造成伤害, 丢失了, 被格挡
    damage_result["SELF_HIT"] = False
    damage_result["SELF_CONFRONTING"] = False
    damage_result["SELF_DO_HARM"] = False
    damage_result["SELF_MISSED"] = False
    damage_result["SELF_BLOCKED"] = False
    # --------------------------------------
    #|#
    #|#
    #|#
    # --------------------------------------
    # 先获取要造成伤害的目标, 大部分情况是1个人, 但做了未来兼容多个的可能
    target_list = role.status_current["round"]["ROUND_TARGET"]
    # 获取伤害的基本情况
    if "HARM_INFLICT" in content.keys():
        harm = content["HARM_INFLICT"]
        # 算伤害
        harm_value = 0
        if "HARM_CONST" in harm:
            # 常数伤害
            harm_value += harm["HARM_CONST"]
        if "HARM_VARIANT" in harm:
            for v_key, v_value in harm["HARM_VARIANT"].items():
                # 根据字典里面的伤害结构来增加伤害
                if v_key == "ROLE_STR":
                    harm_value += role.get_role_str() * v_value
                if v_key == "ROLE_HP":
                    harm_value += role.get_role_hp() * v_value
        # 算完了
        # print(harm_value)
        
    # 如果命中的字典
    if_hit = None
    if "IF_HIT" in content.keys():
        if_hit = content["IF_HIT"]
    # 如果造成伤害的字典
    if_harm = None
    if "IF_HARM" in content.keys():
        if_harm = content["IF_HARM"]
    # 如果被防御的字典
    if_defend = None
    if "IF_DEFEND" in content.keys():
        if_defend = content["IF_DEFEND"]
    
    # --------------------------------------
    #|#
    #|#
    #|#
    # --------------------------------------
    # 一般来讲target就一个人, 先按只有一个人来考虑, 循环是预留的余裕
    for target in target_list:
        
        # 初始化判断
        is_harm_hit = False
        is_harm_hurt = False
        is_confronting = False
        
        print("{0}攻击{1}".format(role.nickname, target.nickname))
        
        # --------------------------------------
        # 先判断交锋
        # 这个和外面那个还不一样, 这个是用来算伤害的
        # 获取攻击目标顺序阶段第order轮的step
        target_step = get_step_in_order_phase_from_role(role=target, order=order)
        # 获取攻击目标当前的回合目标
        target_target_list = target.status_current["round"]["ROUND_TARGET"]
        # 因为正式结算之前已经判断过是否能满足攻击条件, 所以这里不是空的都是交锋
        # 现在这种结算交锋的方式, 不能判断实际miss掉的情况
        # 是否要把这种情况视为交锋, 可以再讨论
        if not(target_step==None):
            if "harmful" in target_step.keys():
                if (target_step["harmful"]) and (role in target_target_list):
                    # 交锋: 如果目标的锁定了我, 且要造成伤害
                    is_confronting = True
                    print("{0}与{1}交锋".format(role.nickname, target.nickname))
        # --------------------------------------
        

        # --------------------------------------
        # 对隐匿/消隐的判断
        if target.is_affected() or role.is_unavoidable():
            # True or False/ False or True/ True or True
            
            # 判断是否命中对方
            is_harm_hit = get_hit_result(role=role,target=target)
            # 判断是否伤害对方
            harm_value, is_defending = get_harm_result(role=role,target=target,value=harm_value)
            if harm_value >0:
                is_harm_hurt = True
        # --------------------------------------
        
        
        # 判断完成, 开始正式处理
        if is_harm_hit:
            # 命中了
            # 结算IF_HIT
            # IF_HIT
            if is_harm_hurt:
                # 有伤害
                print("******伤害阶段******")
                give_harm(role=role,target=target, value=harm_value, extra={"is_confronting":is_confronting})
                # 结算IF_HARM
                # IF_HARM
        else:
            # 没命中
            continue
        
        
        
        
        
        
    # --------------------------------------
    
    # 返回结果参数表
    return damage_result
        
        
        
        
        