from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    jinyan_max_count: int = 5
    jinyan_max_time: int = 20
    jinyan_group: list = ["563484241"]