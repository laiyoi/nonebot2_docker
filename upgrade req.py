import tomli, os, tqdm
with open("./pyproject.toml", "r", encoding="utf-8") as f:
        data = tomli.loads(f.read())

nonebot_data = data.get("tool", {}).get("nonebot")
plugins = nonebot_data.get("plugins", [])
#创建tqdm进度条
#pbar = tqdm.tqdm(total=len(plugins))
for plugin in tqdm.tqdm(plugins):
    #command = f"pip install {plugin} -U"
    command = f"pip install {plugin} --force-reinstall"
    #os.system(f'powershell /c "conda activate nb"')
    os.system(command)
    #pbar.update(1)
