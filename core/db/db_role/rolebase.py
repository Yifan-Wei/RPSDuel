#!/usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------
# type action defination
# log
#       author: Iric
#       version: 0.01 
#       uptime: 2021/07/03
#       content: create this file
# -------------------------------------------------
import gc, math
from copy import deepcopy

# 调用独立出去的role函数, 包括字段的预留和结算
from db.db_role.rolefunc import *

class RoleBase(object):

    def __init__(self):
    
        # 角色二维码, 整局游戏唯一的身份标识
        self.id = ""
        # 角色昵称
        self.nickname = ""
        # 角色编号
        self.code = ""
        # 所属职业
        self.job = ""
        # 所属流派
        self.stream = ""
        # 稀有度
        self.rarity = ""
        
        # 角色默认状态
        self.status_default = {}
        self.status_default["basic"] = {}
        self.status_default["buff"] = {}
        self.status_default["round"] = {}
        # 角色当前状态
        self.status_current = self.status_default.copy()
        # 角色被动(不知道有没有用)
        self.feature = {}
        # 角色说明
        self.introduction = ""
        
    
    def is_role_exist(self):
        # 检查角色是否真的存在
        if self.id != "":
            return True
        return False
        
    def is_role_alive(self):
        # 检查角色是否存活
        if self.status_current["basic"]["ROLE_HP"]>0:
            return True
        else:
            return False
    
    
    def init_current_status(self):
        # 初始化当前状态为默认状态
        # 用深拷贝deepcopy实现
        self.status_current = deepcopy(self.status_default)
        
        
    def init_basic_status(self):
        
        # 初始化基础属性
        basic_list = []
        # 按顺序: 生命, 魔力, 耐力, 灵聚核心, 力量, 智力, 速度, 护甲
        basic_list.append("ROLE_HP")
        basic_list.append("ROLE_MP")
        basic_list.append("ROLE_DUR")
        basic_list.append("ROLE_CORE")
        basic_list.append("ROLE_STR")
        basic_list.append("ROLE_INT")
        basic_list.append("ROLE_SPD")
        basic_list.append("ROLE_ARM")
        # 按顺序: 最大生命, 最大魔力, 最大耐力, 最大灵聚核心, 最大护甲
        basic_list.append("ROLE_MAX_HP")
        basic_list.append("ROLE_MAX_MP")
        basic_list.append("ROLE_MAX_DUR")
        basic_list.append("ROLE_MAX_CORE")
        basic_list.append("ROLE_MAX_ARM")
        
        for basic in basic_list:
            self.status_default["basic"][basic] = 0
        
    def init_buff_status(self):
    
        # 初始化所有buff状态
        # 虽然感觉读一个表会更好,但目前暂时用手写的吧
        buff_list = []
        # 通用增益
        # 按顺序: 格挡, 格挡反击, 闪避, 闪避反击, 穿甲, 必中, 暴击, 流失, 坚韧, 再生, 隐匿, 消隐
        buff_list.append("DEFENDING")
        buff_list.append("DEFENDING_BEATBACK")
        buff_list.append("EVADING")
        buff_list.append("EVADING_BEATBACK")
        buff_list.append("PIERCING")
        buff_list.append("MUSTHIT")
        buff_list.append("CRITICAL")
        buff_list.append("HPLOSS")
        buff_list.append("LASTAND")
        buff_list.append("REGENERATION")
        buff_list.append("CONCEALED")
        buff_list.append("BLANKING")
        
        debuff_list = []
        # 通用减益
        # 按顺序: 致盲, 虚弱, 重创, 灼烧, 中毒, 诅咒, 幻惑, 缴械, 沉默, 眩晕
        debuff_list.append("BLIND")
        debuff_list.append("WEAK")
        debuff_list.append("FRAGILE")
        debuff_list.append("BURNING")
        debuff_list.append("TOXIC")
        debuff_list.append("CURSED")
        debuff_list.append("CONFUSED")
        debuff_list.append("DISARMED")
        debuff_list.append("SILENT")
        debuff_list.append("STUNNED")
        
        # buff的结构为dict["BUFF_STRING"]->list[]->dict[]
        # 先debuff后buff, 让结算的时候能先结算debuff
        for debuff in debuff_list:
            self.status_default["buff"][debuff] = []
        for buff in buff_list:
            self.status_default["buff"][buff] = []

    def init_round_status(self):
        
        # 初始化基础属性
        round_list = []
        # 按顺序: 回合目标, 回合行动, 回合交过锋, 回合受到伤害, 回合施加过伤害
        round_list.append("ROUND_TARGET")
        round_list.append("ROUND_ACTION")
        round_list.append("ROUND_HAS_CONFRONTED")
        round_list.append("ROUND_GET_HURT")
        round_list.append("ROUND_DO_HARM")
        
        for string in round_list:
            self.status_default["round"][string] = None
           
    
    def get_role_str(self):
        """
        获取角色力量
        """        
        # 当前血量和生命上限
        str = self.status_current["basic"]["ROLE_STR"]
        return(str)
    
    def set_role_str(self, value):      
        
        # 当前力量
        str = self.status_current["basic"]["ROLE_STR"]
        
        # 修改角色当前耐力
        if value >= 0:
            # 增强力量,判断会不会超出上限,之后向上取整
            self.status_current["basic"]["ROLE_STR"] = math.ceil(str + value)
        elif value < 0:
            # 削弱力量,力量可以为负数,但结算伤害的时候伤害不能
            self.status_current["basic"]["ROLE_DUR"] = math.ceil(str + value)
    
    
    def get_role_hp(self,mode="now"):
        """
        获取角色生命值
        输入参数 mode="now"/"max",分别返还status_current["basic"]里面的ROLE_HP和ROLE_HP_MAX
        """
        
        # 当前血量和生命上限
        hp = self.status_current["basic"]["ROLE_HP"]
        max_hp = self.status_current["basic"]["ROLE_MAX_HP"]
        
        if mode == "max":
            return(max_hp)
        return(hp)
    
    def set_role_hp(self,value,mode="now",bl_recover=False):
        
        # 当前血量和生命上限
        hp = self.status_current["basic"]["ROLE_HP"]
        max_hp = self.status_current["basic"]["ROLE_MAX_HP"]
        
        if mode== "now":
            # 修改角色当前生命值
            if value >= 0:
                # print("1")
                # 回血,判断会不会超出上限,之后向上取整
                self.status_current["basic"]["ROLE_HP"] = math.ceil(min(max_hp, hp+value))
            elif value < 0:
                # 扣血,不设下限, 但向上取整
                # 允许超杀, 允许debuff先扣下去再奶回来
                self.status_current["basic"]["ROLE_HP"] = math.ceil(hp+value)
            
        elif mode=="max":
            # 修改角色生命上限
            if value >= 0:
                # print("3")
                # 增加上限
                self.status_current["basic"]["ROLE_MAX_HP"] = max_hp + value
                # 增加上限之后,当前血量也增加比例上涨值
                add_value = math.ceil(((max_hp+value)/max_hp-1)*hp)
                if bl_recover:
                    add_value = max(value,add_value)
                self.set_role_hp(add_value)
            elif value < 0:
                # print("4")
                # 降低上限,判断会不会超出下限0,之后向上取整
                self.status_current["basic"]["ROLE_MAX_HP"] = math.ceil(max(0, max_hp+value))
                # 如果当前生命值大于上限, 则降低到上限
                if hp>self.status_current["basic"]["ROLE_MAX_HP"]:
                    self.status_current["basic"]["ROLE_HP"]=self.status_current["basic"]["ROLE_MAX_HP"]
                # 降低上限不会影响
        
        print("{4}的生命值从{0}/{1}变更为{2}/{3}".format(hp,max_hp,self.status_current["basic"]["ROLE_HP"],self.status_current["basic"]["ROLE_MAX_HP"],self.nickname))
    
    def get_role_dur(self,mode="now"):
        """
        获取角色耐力值
        输入参数 mode="now"/"max",分别返还status_current["basic"]里面的ROLE_DUR和ROLE_DUR_MAX
        """
        # 当前血量和生命上限
        dur = self.status_current["basic"]["ROLE_DUR"]
        max_dur = self.status_current["basic"]["ROLE_MAX_DUR"]
        
        if mode == "max":
            return(max_dur)
        return(dur)
    
    
    def set_role_dur(self,value,mode="now",bl_recover=False):
        
        
        # 当前耐力和耐力上限
        dur = self.status_current["basic"]["ROLE_DUR"]
        max_dur = self.status_current["basic"]["ROLE_MAX_DUR"]
        
        if mode== "now":
            # 修改角色当前耐力
            if value >= 0:
                # 回耐,判断会不会超出上限,之后向上取整
                self.status_current["basic"]["ROLE_DUR"] = math.ceil(min(max_dur, dur+value))
            elif value < 0:
                # 扣耐,判断会不会超出下限0,之后向上取整
                # 和生命不同, 耐力就是不会下降到0以下的
                self.status_current["basic"]["ROLE_DUR"] = math.ceil(max(0, dur+value))
            
            
        elif mode=="max":
            # 修改角色耐力上限
            if value >= 0:
                # 增加耐力上限
                self.status_current["basic"]["ROLE_MAX_DUR"] = max_dur + value
                # 增加耐力上限之后,当前耐力也增加比例上涨值, 从生命那边复制过来, 理论没卵用
                add_value = math.ceil(((max_dur+value)/max_dur-1)*dur)
                if bl_recover:
                    add_value = max(value,add_value)
                self.set_role_dur(value)
            elif value < 0:
                # 降低耐力上限,判断会不会超出下限0,之后向上取整
                self.status_current["basic"]["ROLE_MAX_DUR"] = math.ceil(max(0, max_dur+value))
                # 如果当前耐力大于上限, 则降低到上限
                if hp>self.status_current["basic"]["ROLE_MAX_DUR"]:
                    self.status_current["basic"]["ROLE_DUR"]=self.status_current["basic"]["ROLE_MAX_DUR"]
        
        print("{0}的耐力值从{1}/{2}变更为{3}/{4}".format(self.nickname, dur, max_dur, self.status_current["basic"]["ROLE_DUR"],self.status_current["basic"]["ROLE_MAX_DUR"]))
    
    
    def get_round_target(self):
        # -----------------------
        # 获取角色当前回合的目标, 省事的小函数
        # -----------------------
        target = self.status_current["round"]["ROUND_TARGET"]
        return target
    
    
    def set_round_target(self, target_list):
        # -----------------------
        # 设置角色当前回合的目标, 省事的小函数
        # -----------------------
        self.status_current["round"]["ROUND_TARGET"] = target_list
        return
        
    
    def get_buff_status(self, buff_string):
        """
        buff_string = 要操作的buff字段, 因为挂了self可以直接从buff字典里面找
        """
        if buff_string in self.status_current["buff"]:
            # 查找的buff可能是没有的, 只讨论有buff的情况, 避免报错
            list = self.status_current["buff"][buff_string]
            return list
        else:
            return
     
    
    def add_buff_status(self, buff_string, add_layer, add_buff={}, add_mode="layer"):
        """
        这个函数是一个通用add_buff函数,所有buff都应该调用这个函数来实现buff的挂载
        其中：
        buff_string = 要操作的buff字段, 因为挂了self可以直接从buff字典里面找
        add_layer = 要增加的buff层数
        add_buff = 要给加的buff
        add_mode = "layer":层数叠加, "refresh":重置层数为较大值, "anyway":独立计算
        注意, 不要让一个buff同时layer和anyway, 这样每次只会往第1个上面叠加
        """

        # 叠加模式3选1,不然报错
        if not(add_mode=="layer" or add_mode=="refresh" or add_mode=="anyway"):
            print("add_mode error")
            return -1
        
        # 默认给add_buff一个空字典,如果不输入,就置为默认值, 有值就不管了
        full_empty_buff(add_buff)
        
        if buff_string in self.status_current["buff"]:
            list = self.status_current["buff"][buff_string]
        else:
            list = []
            self.status_current["buff"][buff_string] = list
        
        if add_mode != "anyway":
            # 模式不是独立叠加
            for item in list[::-1]:
                # 如果当前列表中存在某个buff,其buff的属性完全一致,则视模式叠加
                # 这个地方暂时没有考虑叠加的时候触发buff效果的buff
                # 未来如果有这个需求,建议在给buff的时候判断,别在叠的时候判断
                if is_buff_the_same(dut_buff=item,cmp_buff=add_buff):
                    # 获取层数、最大层数
                    layer = item["BUFF_LAYER"]                
                    max_layer = item["BUFF_MAX_LAYER"]
                    
                    if add_mode == "layer":
                        # 叠加, 碰到最大层数则返回最大层数
                        item["BUFF_LAYER"] = min(max_layer, layer + add_layer)
                        print("{3} - {0} BUFF 从{1}层 叠加到 {2}层".format(buff_string, layer, item["BUFF_LAYER"], self.nickname))
                    elif add_mode == "refresh":
                        # 刷新, 重置为两者中的较大值
                        item["BUFF_LAYER"] = max(layer, add_layer)
                        print("{3} - {0} BUFF 从{1}层 刷新到 {2}层".format(buff_string, layer, item["BUFF_LAYER"], self.nickname))
                        
                    # 跳出
                    del add_buff
                    gc.collect()
                    return 0
        
        # 无论如何都叠加
        
        # 新增加
        max_layer = add_buff["BUFF_MAX_LAYER"]
        add_buff["BUFF_LAYER"]=min(max_layer, add_layer)
        list.append(add_buff)
        print("{2} - 新增 {0} BUFF: {1}层".format(buff_string, add_buff["BUFF_LAYER"], self.nickname))
        return 1
         
    def rm_buff_status(self, buff_string, rm_layer, pool, rm_buff={}, rm_mode="SPECIFIC", bill_mode="BILL"):
        
        """
        这个函数是一个通用rm_buff函数,所有buff都应该调用这个函数来实现buff的卸载
        其中:
        rm_buff = 待卸载函数的细节(默认为空,用来精细比对的)
        rm_mode = "SPECIFIC" 移除字段下一致的所有buff/"ANYWAY"完全移除字段下所有buff
        bill_mode = "BILL"结算/"GATES"不结算
        
        """
        # 初始化一个状态值
        remover = False
        
        # 默认给add_buff一个空字典,如果不输入, 就置为默认值, 有值就不管了
        full_empty_buff(rm_buff)
        
        # 开始搜索
        list = self.status_current["buff"][buff_string]
        for item in list[::-1]:
            # 选择移除模式
            if rm_mode =="SPECIFIC":
                # 默认特殊移出模式,当所有参数一致时才移除
                # 如果当前列表中存在某个buff,其buff的属性完全一致,则进行操作
                if is_buff_the_same(dut_buff=item, cmp_buff=rm_buff):
                    # 找到了, 调用一个在func里面的函数, 因为具体拿的过程和人物无关,且涉及复杂处理
                    rm_buff_status_from_dict(buff_string=buff_string, buff_list=list, buff=item, rm_layer=rm_layer, pool=pool, bill_mode=bill_mode)
                    # 不跳出,记录当前移除
                    remover = True
                    
            elif rm_mode == "ANYWAY":
                # 强力清扫模式,不讨论是否一致,直接移除
                rm_buff_status_from_dict(buff_string=buff_string, buff_list=list, buff=item, rm_layer=rm_layer, pool=pool, bill_mode=bill_mode)
                # 不跳出,记录当前移除
                remover = True
                
        # 如果没找到,可能不太对,也可能是没找到东西,返回一个打印来提醒一下
        if remover:
            print("remove at least one buff")
            del rm_buff
            gc.collect()
            return 1
        else:
            print("BUFF NOT FOUND")
            del rm_buff
            gc.collect()
            return 0
    
        
    def iter_buff_status(self, pool):
        
        # 首先搞清楚里面大概是个这样的状态:
        # 第一层是字典, 所有buff的字段在这里
        # 第二层是列表, 同一个类型的buff可能有不同来源,用列表来排列
        # 第三层是字典, 字典键带有buff来源, buff对象, buff正面标识符, buff负面标识符, buff脱落标识符, buff层数, buff数值, buff优先级, buff预留字段
        # 关键字是 BUFF_SOURCE=[], BUFF_TARGET=[], BUFF_IS_POSITIVE=0/1, BUFF_IS_NEGATIVE=0/1, BUFF_IS_SHEDDING=0/1, BUFF_LAYER=INTEGER, BUFF_VALUE=FLOAT, BUFF_PRIORITY=INTEGER, BUFF_PRESERVE=None
        # 在叠加buff的是时候,只有buff来源、对象一致的buff才会叠加/重置
        
        # 获取需要操作的列表
        buff_dict = self.status_current["buff"]
        # 循环遍历
        for buff_key, buff_value_list in buff_dict.items():
            #print(buff_key)
            # 如果这个状态列表里有一个以上状态
            if len(buff_value_list)>0:
                #print(buff_key)
                #print(len(buff_value_list))
                for value_list_dict in buff_value_list[::-1]:
                    # 如果这个状态有层数,层数=(0和层数-1)的最大值
                    if value_list_dict["BUFF_IS_SHEDDING"] == 1:
                        # 只拿可脱落的buff
                        print("# {} 在随时间减弱".format(buff_key))
                        # 这里用底层的buff移除, 是希望能够移除同时结算的buff, 如果不这样会逮着一个buff薅
                        rm_buff_status_from_dict(buff_string=buff_key, buff_list=buff_value_list, buff=value_list_dict, rm_layer=1, pool=pool, billmode="BILL")
    
    def print_buff_status(self):
        
        # 获取需要操作的列表
        buff_dict = self.status_current["buff"]
        print("#------------{}的BUFF状态--------------".format(self.nickname))
        for buff_key, buff_value_list in buff_dict.items():
            #print(buff_key)
            #print(len(buff_value_list))
            # 如果这个状态列表里有一个以上状态
            if len(buff_value_list)>0:
                for buff in buff_value_list:
                    name = buff_key
                    source = buff["BUFF_SOURCE"]
                    target = buff["BUFF_TARGET"]
                    layer = buff["BUFF_LAYER"]
                    max_layer = buff["BUFF_MAX_LAYER"]
                    count = buff["BUFF_COUNT"]
                    value = buff["BUFF_VALUE"]
                    is_positive = buff["BUFF_IS_POSITIVE"]
                    is_negative = buff["BUFF_IS_NEGATIVE"]
                    is_shedding = buff["BUFF_IS_SHEDDING"]
                    string = "你拥有 {0} 的".format(name)
                    if is_positive:
                        string+="正面"
                    if is_negative:
                        string+="负面"
                    string +="BUFF,层数为{0},".format(layer)
                    string +="来自{0},目标{1}".format(source,target)
                    if count>0:
                        string +=",计数为{0}".format(count)
                    if value>0:
                        string +=",值为{0}".format(value)
                    if is_shedding:
                        string += ",它会随时间减弱"
                    print(string)
        print("#---------------------------------------------")
    
    
    def is_buffed(self,buff_string):
        """
        判断角色是否处于特定buff状态
        粗略判断, 只要有一个buff在,就算在状态
        """
        if buff_string in self.status_current["buff"]:
            if len(self.status_current["buff"][buff_string])>0:
                return True
        return False
    
    def is_meeting_cost_condition(self):
        """
        需要满足: 1.角色存活
        return True/False
        """
        if not(self.is_role_alive()):
            print("{}已经濒死".format(self.nickname))
            return False
        return True
        
    def is_meeting_act_condition(self):
        """
        需要满足: 1.角色存活
        需要满足: 2.没有晕眩类的buff在身上
        return True/False
        """
        if not(self.is_role_alive()):
            print("{}已经濒死".format(self.nickname))
            return False
        if self.is_buffed("STUNNED"):
            print("{}晕眩中".format(self.nickname))
            return False
        return True
        
    
    def is_meeting_atk_condition(self):
        """
        为条件判断做的函数, 是否当前能攻击, 写成函数是为了固化判断
        需要满足: 1.角色存活
        需要满足: 2.没有晕眩和缴械类的buff在身上
        return: True/False
        """
        if not(self.is_role_alive()):
            print("{}已经濒死".format(self.nickname))
            return False
        if self.is_buffed("DISARMED") or self.is_buffed("STUNNED"):
            print("{}晕眩或者缴械".format(self.nickname))
            return False
        return True
    
    
    def is_affected(self):
        """
        为伤害结算做的函数, 是否角色正处于战场
        需要满足 不是消隐状态或者隐匿状态
        """
        if self.is_buffed("BLANKING") or self.is_buffed("CONCEALED"):
            return False
        return True
        
    
    def is_unavoidable(self):
        """
        能够影响到不在战场上人物的状态
        目前并不存在, 直接return False
        """
        return False
    
    
    def is_evading(self):
        """
        判断单位是否处于闪避状态, 未来可能会有复数个该类状态, 因此需要单独判断
        """
        if self.is_buffed("EVADING"):
            return True
        return False
    
    
    def is_evading_beatback(self):
        """
        判断单位是否处于闪避反击状态, 未来可能会有复数个该类状态, 因此需要单独判断
        """
        if self.is_buffed("EVADING_BEATBACK"):
            return True
        return False
    

    def is_defending(self):
        """
        判断单位是否处于防御状态, 未来可能会有复数个该类状态, 因此需要单独判断
        """
        if self.is_buffed("DEFENDING"):
            return True
        return False
    
    
    def is_defending_beatback(self):
        """
        判断单位是否处于防御反击状态, 未来可能会有复数个该类状态, 因此需要单独判断
        """
        if self.is_buffed("DEFENDING_BEATBACK"):
            return True
        return False
    
    
    def js_print(self):
        
        import json as js
        
        dict_print = {}
        dict_print["id"] = self.id
        dict_print["code"] = self.code
        dict_print["job"] = self.job
        dict_print["stream"] = self.stream
        dict_print["status_default"] = self.status_default
        dict_print["status_current"] = self.status_current
        str_print = js.dumps(dict_print)
        print(str_print)

# ---------------------------------------------------
# FOR TEST 
# ---------------------------------------------------

if __name__ =="__main__":
    pass