# Copyright (C) 2019  MixBytes, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND (express or implied).

import json

# import httplib2 as httplib2
from requests.exceptions import RequestException
import requests
from prometheus_client import Counter


class iconRPCError( RuntimeError ):
    pass


class iconRPC:
    """
    Class interacts with a icon node via RPC and takes care of errors.
    """

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url
        self._next_id = 1
        self._counter_rpc_calls = Counter('icon_exporter_rpc_calls','------Total number of RPC calls made by metric exporter')


    def request_nothrow(self, request_data):
        self._next_id += 1
        self._counter_rpc_calls.inc()
        try:
            result = requests.post(self.rpc_url, data=json.dumps(request_data))
            # print(result)
        except RequestException:
            # TODO more fine-grained error handling
            # self._counter_network_error.inc()
            return

        if result.status_code != 200:
            # self._counter_unexpected_status.inc()
            return

        result_json = result.json()
        if result_json.get( 'error' ):
            # self._counter_request_error.inc()
            return
        return result_json

    def request(self, request_data, params=None):
        result = self.request_nothrow(request_data)
        if result is None:
            raise iconRPCError()
        return result


def get_block_num(rpc_block):
    pass
#     return int( rpc_block['block']['header']['number'],16)
