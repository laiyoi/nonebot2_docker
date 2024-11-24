from nonebot import get_plugin_config, on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
import requests, time, os
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-gta5status",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

async def query_info(matcher, name: str):
    params = {'nickname': name}
    response = requests.get('https://www.hqshi.cn/api/status', params=params)
    if response.status_code != 200 or ('body' not in response.json().keys()):
        return f"查询{name}失败，请检查输入昵称是否正确"
    params['type']= 'detail'
    response = requests.get('https://www.hqshi.cn/api/recent', params=params)
    if response.status_code == 200:
        data = response.json()
        return data['body']  # 打印返回的数据
    elif response.status_code == 303:
        params = {'nickname': name}
        response = requests.get('https://www.hqshi.cn/api/post', params=params)
        await matcher.send(f'查询{name}中')
        for i in range(5):
            await matcher.send(f'等待查询结果({i}/5)')
            params['type']= 'detail'
            response = requests.get('https://www.hqshi.cn/api/recent', params=params)
            if response.status_code == 200:
                data = response.json()
                return data['body']
            time.sleep(10)
        return f"查询{name}失败，请等一会重试"
    else:
        return f"查询{name}失败，未知错误"

query = on_command("查询gta5", aliases={"gta5查询"}, priority=5, block=True)

@query.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().split(' ')
    for name in args:
        result = await query_info(query, name)
        if len(result) < 50:
            await query.finish(Message([MessageSegment.at(event.user_id), MessageSegment.text(result)]))
        else:
            result = text_to_image(result)
            await query.finish(Message([MessageSegment.at(event.user_id), MessageSegment.image(result)]))

def text_to_image(text: str):
    """文字转图片

    Args:
        text (str): 要转换的文字

    Returns:
        bytes: 图片
    """
    
    fontSize = 30
    liens = text.split('\n')
    max_len = 0
    for str in liens:
        max_len = max(len(str),max_len)
    image = Image.new("RGB", ((fontSize * max_len), len(liens) * (fontSize)), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    fontPath = os.path.join("C:\\Windows\\Fonts\\", "simhei.ttf")
    font = ImageFont.truetype(fontPath, fontSize)
    draw.text((0, 0), text, font=font, fill="#000000")
    img = image.convert("RGB")
    img_byte = BytesIO()
    img.save(img_byte,"PNG")
    return img_byte.getvalue()