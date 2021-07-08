# 行动编号，需要与文件名一致
code_action: a0004
# 行动名，随便写，不是关键字
name_action: 重振旗鼓
# 所属职业
job: 战士
# 具体类型：UNLOCK/LOCK锁定
type: UNLOCK

# 开始步骤
# 是否有开始步骤动作
start_step: N
# 开始步骤发动条件
start_condition: []
# 开始步骤执行内容
start_content: []

# 顺序步骤
# 是否有顺序结算步骤动作
order_step: N
# 顺序步骤发动条件
order_condition: []
# 顺序步骤发动内容
order_content: []

# 结束步骤
# 是否有结束步骤动作
end_step: Y
# 结束步骤发动条件
end_condition: {"UNINJURED":"Y"}
# 结束步骤执行内容
end_content: [{"HARMFUL":"N", "DUR_REC":4}]
  