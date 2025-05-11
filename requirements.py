import os, tqdm
try:  # pragma: py-gte-311
    import tomllib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:  # pragma: py-lt-311
    import tomli as tomllib  # pyright: ignore[reportMissingImports]

with open("./pyproject.toml", "r", encoding="utf-8") as f:
        data = tomllib.loads(f.read())

nonebot_data = data.get("tool", {}).get("nonebot")
plugins = nonebot_data.get("plugins", [])
#创建tqdm进度条
pbar = tqdm.tqdm(total=len(plugins))
for plugin in plugins[::-1]:
#for plugin in plugins:
    command = f"pip install {plugin} -U -i https://pypi.tuna.tsinghua.edu.cn/simple"
    #os.system(f'powershell /c "conda activate nb"')
    os.system(command)

    pbar.update(1)
