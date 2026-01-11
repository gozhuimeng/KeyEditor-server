import zipfile
import os
import logging


# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


class Zipper:
    """
    压缩工具类
    """

    @staticmethod
    def unzip(file_path: str, output_path: str) -> None:
        """
        解压

        :param file_path: 压缩文件的路径（需要包括名称）
        :param output_path: 输出路径

        :return: None
        """
        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(output_path)
        except Exception as e:
            logging.warning(f"配置文件解压错误：{e}")

    @staticmethod
    def zip(file_path: str, output_name: str) -> None:
        """
        压缩

        :param file_path: 压缩目录路径
        :param output_name: 输出文件路径（需要包括文件名称）

        :return: None
        """
        try:
            with zipfile.ZipFile(output_name, "w", zipfile.ZIP_DEFLATED) as zipf:
                for folder_name, subfolders, filenames in os.walk(file_path):
                    for filename in filenames:
                        path = os.path.join(folder_name, filename)
                        zipf.write(path, arcname=os.path.relpath(path, file_path))
        except Exception as e:
            logging.warning(f"配置文件压缩错误：{e}")


# if __name__ == "__main__":
#     # example
#     file_path = "./data/bds/1.bds"
#     output_path = "./data/output/"
#     output_filename = "./data/bds/output.bds"
#     print("解压文件")
#     Zipper.unzip(file_path, output_path)
#     print("压缩文件")
#     Zipper.zip(output_path, output_filename)
