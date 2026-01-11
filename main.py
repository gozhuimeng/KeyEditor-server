import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from module.packer import Packer


# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        bds_filepath: str = "./data/bds/1.bds"
        output_path: str = "./data/output/"
        save_filepath: str = "./data/bds/output.bds"
        ini_filename: str = "./data/output/dark/land/en_26.ini"
        app.state.packer = Packer(bds_filepath, output_path, save_filepath)
        app.state.packer.unpacker()
        app.state.packer.loader(ini_filename)
    except Exception as e:
        logging.warning("配置文件加载错误，退出程序")
        logging.warning("exception: ", e)
        exit()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/getMap")
async def get_map():
    return app.state.packer.key_map


@app.get("/getLayout")
async def get_layout():
    return app.state.packer.key_layout


class pushMap(BaseModel):
    key_map: dict[str, dict]


class pushLayout(BaseModel):
    key_layout: list


@app.post("/pushMap")
async def push_map(push_map: pushMap):
    # print(push_map.key_map["1"])
    app.state.packer.key_map = push_map.key_map
    return {"message": "ok"}


@app.post("/pushLayout")
async def push_layout(push_layout: pushLayout):
    # 为后续自定义布局预留接口
    print(push_layout.key_layout)
    return {"message": "ok"}


@app.get("/endEdit")
async def endEdit():
    app.state.packer.dumper()
    app.state.packer.packer()
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
