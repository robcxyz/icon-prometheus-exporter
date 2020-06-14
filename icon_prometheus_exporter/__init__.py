# Prometheus exporter for icon relay chain node

# TODO WebSocket subscriptions

import sys
import os
sys.path.append("..")
from time import sleep, time
from signal import signal, SIGINT, SIGTERM
import argparse
import random
import time
# import psutil

from icon_prometheus_exporter import _tasks
from icon_prometheus_exporter._tasks import prepsUpdater
from prometheus_client import start_http_server, Counter, Gauge, Summary,Info

if __name__ == '__main__':
    # have to make sure we'll be able to find submodules
    sys.path.append( os.path.realpath( os.path.dirname( os.path.dirname( __file__ ) ) ) )

from icon_prometheus_exporter._utils import check
from icon_prometheus_exporter._rpc import iconRPC, iconRPCError, get_block_num
# from icon_prometheus_exporter._blockchain import BlockCache
# from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily


class Exporter:
    POLL_INTERVAL = 0.5

    def __init__(self, exporter_port, exporter_address='', rpc_url='', request_data=''):
        self.exporter_port = exporter_port
        self.exporter_address = exporter_address
        self._rpc = iconRPC(rpc_url)
        # Exporter.request_data = request_data
        # initialize a _block_cache as a dictionary of all hashes
        # self._block_cache = BlockCache(self._rpc)
        self.request_data = request_data
    #     #
        self._info_updaters = [prepsUpdater( self._rpc, self.request_data )]
        # REGISTRY.register(prepsUpdater(self._rpc, self.request_data))

    # SYSTEM_USAGE = Gauge('system_usage', 'Hold current system resource usage',['resource_type'])



    def serve_forever(self):
        # start_http_server(self.exporter_port, self.exporter_address)
        start_http_server(6100)
        stop = [False]
        # i = Info('my_build_version', 'Description of info')
        # for x in self._rpc.request(self.request_data)["result"]["preps"]:

        while not stop[0]:
            try:
                self._step()
            except iconRPCError:
                pass
            except iconRPCError:
                pass


    def _step(self):
        self._run_updaters()
#             else:
#                 block_hash = self._rpc.request('chain_getBlockHash', [self._last_processed_block_num + 1])['result']
#                 check(block_hash is not None, 'hash of {} must not be none'.format(self._last_processed_block_num + 1))
#
#                 # optimization
#                 self._last_processed_block_hash = block_hash
#
#                 block = self._block_cache.get(block_hash)
#                 check(block is not None, 'block {} must not be none'.format(self._last_processed_block_num + 1))
#
#             self._counter_blocks_seen.inc()
#             self._last_processed_block_num = get_block_num(block)
#
#             self._counter_extrinsics_seen.inc(len(block['block']['extrinsics']))
# # self._run_updaters()
#
    def _run_updaters(self):
        for updater in self._info_updaters:
            updater.run()


def main():
    ap = argparse.ArgumentParser( description='Prometheus python exporter for icon node' )
    ap.add_argument( "--exporter_port", type=int, default=6100, help='expose metrics on this port' )
    ap.add_argument( "--exporter_address", type=str, help='expose metrics on this address' )
    ap.add_argument( "--rpc_url", type=str, default='https://ctz.solidwallet.io/api/v3',
                     help='icon node rpc address' )
    # ap.add_argument( "--blackbox_rpc_url", type=str, default='http://35.174.249.15:9000/api/v3',
    #                  help='icon node black_rpc address' )

    # ap.add_argument("--request_data", type=str, default='{"jsonrpc": "2.0",'
    #                                                     '"id": 1234,'
    #                                                     '"method": "icx_call",'
    #                                                     '"params": {'
    #                                                     '"to":"cx0000000000000000000000000000000000000000",'
    #                                                     '"dataType": "call",'
    #                                                     '"data": {'
    #                                                     '"method": "getPReps",'
    #                                                     '"params": {"startRanking": "0x1","endRanking": "0xa"}}}}', help='icon node rpc address')
    args = ap.parse_args()
    request_data = {
            "jsonrpc": "2.0",
            "id": 1234,
            "method": "icx_call",
            "params": {
                "to": "cx0000000000000000000000000000000000000000",
                "dataType": "call",
                "data": {
                    "method": "getPReps",
                    "params": {
                        "startRanking": "0x1",
                        "endRanking": "0xa"
                    }
                }
            }
        }
    print(args)
    Exporter(args.exporter_port, args.exporter_address if args.exporter_address else '', args.rpc_url, request_data).serve_forever()


if __name__ == '__main__':
    main()
