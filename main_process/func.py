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
import gc, math

def role_from_id(id, pool):
    # 遍历池子里的结构体
    for member in pool:
        if member.id == id:
            return member
    # 找不到返回空
    return None


def full_empty_buff(buff):
    """
    把没有字段的buff填满，主要是用来把默认值填满
    BUFF_SOURCE, BUFF_TARGET, BUFF_IS_POSITIVE, BUFF_IS_NEGATIVE, BUFF_IS_SHEDDING
    BUFF_LAYER, BUFF_MAX_LAYER, BUFF_COUNT, BUFF_VALUE
    """
    
    if not("BUFF_SOURCE" in buff.keys()):
        buff["BUFF_SOURCE"] = []
    if not("BUFF_TARGET" in buff.keys()):
        buff["BUFF_TARGET"] = []  
    if not("BUFF_IS_POSITIVE" in buff.keys()):
        buff["BUFF_IS_POSITIVE"] = 0
    if not("BUFF_IS_NEGATIVE" in buff.keys()):
        buff["BUFF_IS_NEGATIVE"] = 0 
    if not("BUFF_IS_SHEDDING" in buff.keys()):
        buff["BUFF_IS_SHEDDING"] = 1
    if not("BUFF_LAYER" in buff.keys()):
        buff["BUFF_LAYER"] = 0
    if not("BUFF_MAX_LAYER" in buff.keys()):
        buff["BUFF_MAX_LAYER"] = 65536
    if not("BUFF_COUNT" in buff.keys()):
        buff["BUFF_COUNT"] = 0
    if not("BUFF_VALUE" in buff.keys()):
        buff["BUFF_VALUE"] = 0 
    if not("BUFF_PRIORITY" in buff.keys()):
        buff["BUFF_PRIORITY"] = 0
    if not("BUFF_PRESERVE" in buff.keys()):
        buff["BUFF_PRESERVE"] = None
    
    return

def is_buff_the_same(dut_buff={}, cmp_buff={}):
    """
    # 第三层是字典, 字典键带有buff来源, buff对象, buff正面标识符, buff负面标识符, buff脱落标识符, buff层数, buff最大层数, buff次数, buff数值, buff优先级, buff预留字段
    # 关键字是 BUFF_SOURCE=[], BUFF_TARGET=[], BUFF_IS_POSITIVE=0/1, BUFF_IS_NEGATIVE=0/1, BUFF_IS_SHEDDING=0/1, BUFF_LAYER=INTEGER, BUFF_MAX_LAYER = INTEGER, BUFF_COUNT=INTEGER, BUFF_VALUE=FLOAT, BUFF_PRIORITY=INTEGER, BUFF_PRESERVE=None
    # 只比较来源、对象、正负面、脱落、最大层数、值、优先级
    """
    # 先把buff可能空置的地方填满
    full_empty_buff(dut_buff)
    full_empty_buff(cmp_buff)
    
    # 顺着比，有一个不满足就return False，跳过后面的
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
        source_tmp = role_from_id(id_item,pool)
        if not(source_tmp is None):
            source_list.append(source_tmp)
    # 从ID返回结构体, 加入列表
    target_list = []
    for id_item in id_target_list:
        target_tmp = role_from_id(id_item,pool)
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
    