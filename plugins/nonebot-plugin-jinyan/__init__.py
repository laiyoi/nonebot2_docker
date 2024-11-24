from nonebot import get_plugin_config

from .config import Config

from nonebot import on_message, logger

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, GROUP, MessageSegment

import re

config = get_plugin_config(Config)

async def rule_checker(event: GroupMessageEvent) -> bool:
    return str(event.group_id) in config.jinyan_group 

ban_message = on_message(priority=1, block=False, permission=GROUP, rule=rule_checker)

groups = {}

@ban_message.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    uid = event.user_id
    """    msg = event.message
    urls = [
        seg.data["file"]
        for seg in msg
        if (seg.type == "image")
    ]"""
    msg = ""
    for seg in event.message:
        if seg.type == "text":
            msg += seg.data['text']
            pattern = re.compile(r'(.)\1+')
            msg = pattern.sub(r'\1', msg)
            
        elif seg.type == "at":
            msg += "@" + seg.data['qq']

        elif seg.type == "face":
            msg += "face_id: " + seg.data["id"]
            
        else:
            try:
                msg += seg.data["file"]
            except KeyError:
                msg += str(seg.data)
            
    
    time = event.time
    
    # 如果群组id不在groups中，添加一个新的键值对，值为一个空字典
    if group_id not in groups:
        groups[group_id] = {}
    # 定义一个变量，用字典存储当前消息的信息
    message = {"msg": msg} # 删除"uid": uid
    # 定义两个常量，表示次数和时间的上限
    MAX_COUNT = config.jinyan_max_count # 你可以根据需要修改这个数值
    MAX_TIME = config.jinyan_max_time # 你可以根据需要修改这个数值，单位为秒
    # 检查groups中该群组是否有该用户的记录
    if uid in groups[group_id]:
        # 获取该用户上一次发送的消息
        last_message = groups[group_id][uid]
        # 如果内容相同，增加次数
        if last_message["msg"] == msg:
            message["count"] = last_message["count"] + 1
            message["first_time"] = last_message["first_time"] # 保持第一次发送的时间不变
            # 如果次数超过上限，打印用户id和群组id
            if message["count"] > MAX_COUNT:
                print(f"User {uid} in Group {group_id} exceeded message count limit.")
                try:
                    await bot.set_group_ban(group_id=group_id, user_id=uid, duration=74)
                    await ban_message.send(message["msg"])
                except Exception:
                    await ban_message.send("闭嘴" + MessageSegment.at(uid))
                    
                message["count"] = 1
        # 否则，重置次数为1，并更新第一次发送的时间为当前时间
        else:
            message["count"] = 1
            message["first_time"] = time # 使用重置是那条消息的时间
    # 否则，初始化次数为1，并记录第一次发送的时间为当前时间
    else:
        message["count"] = 1
        message["first_time"] = time # 记录第一次发送消息的时间
    # 如果时间差超过上限，清除次数
    if time - message["first_time"] > MAX_TIME:
        message["count"] = 1
        message["first_time"] = time
    # 将message更新到groups中该群组该用户的记录中
    groups[group_id][uid] = message
    print_groups = {}
    for group_id, users in groups.items():
        print_groups[group_id] = {}
        for uid, user in users.items():
            message = user
            if len(user['msg']) > 6:
                message['msg'] = user['msg'][:2] + "..." + user['msg'][-2:] if user['msg'][-6:] != ".image" else user['msg'][:6] + ".image"
            else:
                message['msg'] = user['msg']
            print_groups[group_id][uid] = message

    logger.info(print_groups)