import configparser


class CustomConfigParser(configparser.ConfigParser):
    """
    重写ConfigParser
    """

    def __init__(self, **kwargs):
        """
        修改传参，取消`%`的格式化指令
        """
        kwargs.setdefault("interpolation", None)
        super().__init__(**kwargs)

    def optionxform(self, optionstr: str) -> str:
        """
        原optionxform返回optionstr.lower()，重写函数禁用大小写转换
        """
        return optionstr

    def write(self, fp, space_around_delimiters: bool = False) -> None:
        """
        重新write，键值对等号左右不添加空格
        """
        return super().write(fp, space_around_delimiters)
