import configparser
from os import initgroups
from module.zipper import Zipper
from module.CustomConfigParser import CustomConfigParser


class Packer:
    """
    解包、读取、修改、写入、打包bds文件
    """

    def __init__(
        self, filename: str, output_path: str, save_filename: str | None = None
    ):
        """
        初始化

        :param filename: 加载bds文件名称
        :param output_path: 存放解包文件路径
        :param save_filename: 打包文件名称，若为空则与filename一致
        """
        self.filename: str = filename
        self.output_path: str = output_path
        self.save_filename: str = save_filename if save_filename else filename
        self.key_map: dict[str | int, dict[str, str | None]] = {}
        self.key_layout: list[list] = []
        self.ini_filename: str = ""

    @staticmethod
    def get_char_num(char: str | None) -> str:
        """
        功能函数：获取字母在26字母中的排序

        :param char: 字母

        :return: -2(非法字符) -1(字符属于26个字母) other(字母在26个字母中的排序)
        """
        if char is None:
            return "-2"
        elif len(char) != 1:
            return "-2"
        else:
            char = char.lower()
            if "a" <= char <= "z":
                return str(ord(char) - ord("a") + 1)
            return "-1"

    def loader(self, ini_file: str) -> None:
        """
        加载ini文件内容

        :param init_file: ini文件路径（需要包括文件名称）

        :return: None
        """
        config = CustomConfigParser()
        config.read(ini_file)
        self.ini_filename = ini_file
        layout = []
        for section in config.sections():
            value = config.get(section, "CENTER", fallback=None)
            char_num = self.get_char_num(value)
            if char_num not in ["-1", "-2"]:
                up = config.get(section, "UP", fallback=None)
                left = config.get(section, "LEFT", fallback=None)
                right = config.get(section, "RIGHT", fallback=None)
                down = config.get(section, "DOWN", fallback=None)
                self.key_map.update(
                    {
                        char_num: {
                            "body": value,
                            "up": up,
                            "left": left,
                            "right": right,
                            "down": down,
                        }
                    }
                )
                layout.append(char_num)
        self.key_layout = [layout[0:10], layout[10:19], layout[19:26]]

    def reloader(self, ini_file: str) -> None:
        """
        重新加载ini文件

        :param init_file: ini文件路径（需要包括文件名称）

        :return: None
        """
        self.key_layout = []
        self.key_map = {}
        self.loader(ini_file)

    def dumper(self, ini_file: str | None = None) -> None:
        """
        写入内容到ini文件

        :param ini_file: ini文件路径（需要包括文件名称）

        :return: None
        """
        ini_file = ini_file if ini_file else self.ini_filename
        config = CustomConfigParser()
        config.read(ini_file)
        for section in config.sections():
            value = config.get(section, "CENTER", fallback=None)
            char_num = self.get_char_num(value)
            if char_num not in ["-1", "-2"]:
                try:
                    up = self.key_map[char_num]["up"]
                    left = self.key_map[char_num]["left"]
                    right = self.key_map[char_num]["right"]
                    down = self.key_map[char_num]["down"]
                    config.set(section, "UP", up) if up else None
                    config.set(section, "LEFT", left) if left else None
                    config.set(section, "RIGHT", right) if right else None
                    config.set(section, "DOWN", down) if down else None
                except Exception as e:
                    print("error: ", e)

        with open(ini_file, "w") as configfile:
            config.write(configfile)

    def unpacker(self):
        """
        解包内容
        """
        Zipper.unzip(self.filename, self.output_path)

    def packer(self):
        """
        打包内容
        """
        Zipper.zip(self.output_path, self.save_filename)


# if __name__ == "__main__":
