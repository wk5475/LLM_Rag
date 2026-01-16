#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/1/14 17:29
# @Author  : wang ke
# @File    : nacos_client.py
# @Software: PyCharm

import nacos
import requests
from urllib.parse import urljoin

class NacosClient:
    def __init__(self, server_addresses: str, namespace: str, service_name: str = None, ip: str = None,
                 port: int = None, cluster_name: str = None, group_name: str = None, username=None, password=None):
        self.service_name = service_name
        self.ip = ip
        self.port = port
        self.cluster_name = cluster_name
        self.group_name = group_name if group_name else nacos.DEFAULT_GROUP_NAME
        self.validate_namespace(server_addresses, namespace)
        self.client = nacos.NacosClient(server_addresses, namespace=namespace, username=username, password=password)

    @staticmethod
    def validate_namespace(server_addresses, namespace):
        url = urljoin(server_addresses, "/nacos/v1/console/namespaces")
        response = requests.get(url)

    def register_service(self):
        return self.client.add_naming_instance(self.service_name, self.ip, self.port, cluster_name=self.cluster_name,
                                               group_name=self.group_name)

    def deregister_service(self):
        return self.client.remove_naming_instance(self.service_name, self.ip, self.port,
                                                  cluster_name=self.cluster_name,
                                                  group_name=self.group_name)

    def send_heartbeat(self):
        status = self.client.send_heartbeat(self.service_name, self.ip, self.port, self.cluster_name)
        if status.get("code") == 10200:
            return True
        return False

    def get_config(self, data_id):
        return self.client.get_config(data_id, self.group_name, timeout=10, no_snapshot=True)
