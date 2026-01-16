#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/14 17:28
# @Author  : wang ke
# @File    : config.py
# @Software: PyCharm

import os
import yaml
from dotenv import load_dotenv

from settings.nacos_client import NacosClient

load_dotenv()
nacos_keys = ["NACOS_USER", "NACOS_PASSWORD", "NACOS_SERVER_ADDRESSES", "NACOS_NAMESPACE", "NACOS_DATA_ID"]
nacos_values = {}

for nacos_key in nacos_keys:
    if (value := os.getenv(nacos_key)) is None:
        raise (f"Missing required environment variable: {nacos_key}")
    nacos_values[nacos_key] = value

# 使用收集到的值初始化Nacos客户端
nacos_client = NacosClient(
    server_addresses=nacos_values["NACOS_SERVER_ADDRESSES"],
    namespace=nacos_values["NACOS_NAMESPACE"],
    username=nacos_values["NACOS_USER"] or None,
    password=nacos_values["NACOS_PASSWORD"] or None
)

config = yaml.safe_load(nacos_client.get_config(nacos_values["NACOS_DATA_ID"]))

ollama_dict = config["ollama"]
local_ollama_dict = ollama_dict["local"]
OLLAMA_LOCAL_URL = local_ollama_dict["url"]
cloud_ollama_dict = ollama_dict["cloud"]
OLLAMA_KEY = cloud_ollama_dict["key"]
OLLAMA_CLOUD_URL = cloud_ollama_dict["url"]
OLLAMA_CLOUD_MODEL = cloud_ollama_dict["model"]