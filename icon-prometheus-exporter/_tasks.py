# # Copyright (C) 2019  MixBytes, LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License").
# # You may not use this file except in compliance with the License.
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND (express or implied).
#
# from abc import abstractmethod
#
from prometheus_client import Gauge, Info, Histogram


#
from abc import abstractmethod
from icon_prometheus_exporter._utils import PeriodicTask, check
from icon_prometheus_exporter._rpc import iconRPCError, get_block_num
#
#
class ExporterPeriodicTask(PeriodicTask):
    """
    PeriodicTask shim which handles some common logic.
    """

    def __init__(self, rpc, period_seconds):
        super( ExporterPeriodicTask, self ).__init__( period_seconds )
        self._rpc = rpc
    #
    def _perform(self):
        try:
            self._perform_internal()
        except:
            pass
    #
    @abstractmethod
    def _perform_internal(self):
        raise NotImplementedError()
#
class IconHightUpdater( ExporterPeriodicTask ):
    def __init__(self, rpc, request_data):
        super( IconHightUpdater, self ).__init__( rpc, 3)
        self.request_data = request_data
        self._cashed_block_height = int( self._rpc.request( self.request_data )["result"]["blockHeight"], 16 )
        self._gauge_delta_block_height = Gauge('icon_delta_height_block', '----------the varying in height of block chain' )
        self._gauge_change_block_height = Gauge('icon_change_height_block', 'xxxxxxxxxxxxxxxxxthe varying in height of block chain' )

        print("Initial Height")
        # print(self._cashed_block_height)
        self._delta_block_height = 0
    def _perform_internal(self):
        print("------------")
        print("internal Performer")
        current_block_height = int(self._rpc.request(self.request_data)["result"]["blockHeight"],16)
        print("current_block_height",current_block_height)
        print("_cashed_block_height",self._cashed_block_height)
        temp = current_block_height - self._cashed_block_height
        print("current pull change in height",temp)
        self._cashed_block_height = current_block_height
        # if temp > 0:
        print(type(temp))
        self._gauge_change_block_height.inc(temp)
        self._gauge_delta_block_height.set(temp)

# class SystemInfoUpdater(ExporterPeriodicTask):
#     def __init__(self, rpc):
#         super(SystemInfoUpdater, self).__init__(rpc, 5*60)
#         self._info = Info('icon_system', 'icon system information')
#         self._runtime_info = Info('icon_runtime', 'icon runtime information')
#
#     def _perform_internal(self):
#         self._info.info({ 'name': self._rpc.request('system_name')['result'],
#                           'version': self._rpc.request('system_version')['result'],
#                           'chain': self._rpc.request('system_chain')['result'],
#                           })
#
#         runtime = self._rpc.request('state_getRuntimeVersion')['result']
#         for key in list(runtime):
#             if key not in ("authoringVersion", "implName", "implVersion", "specName", "specVersion"):
#                 runtime.pop(key)
#             else:
#                 runtime[key] = str(runtime[key])
#
#         self._runtime_info.info(runtime)
#
#
# class HealthInfoUpdater(ExporterPeriodicTask):
#     def __init__(self, rpc):
#         super(HealthInfoUpdater, self).__init__(rpc, 1)
#         self._gauge_is_syncing = Gauge('icon_node_syncing', '1 if a Polkadot node is syncing, 0 otherwise')
#         self._gauge_should_have_peers = Gauge('polkadot_node_should_have_peers', '1 if a Polkadot node should have peers, 0 otherwise')
#         self._gauge_peers = Gauge('polkadot_node_peers', 'Number of peers')
#
#     def _perform_internal(self):
#         health = self._rpc.request('system_health')['result']


# class MemPoolUpdater(ExporterPeriodicTask):
#
#     def __init__(self, rpc):
#         super(MemPoolUpdater, self).__init__(rpc, 5*60)
#         # self._gauge = Gauge('polkadot_pending_extrinsics', 'Polkadot pending extrinsics count as seen by a node')
#
#     def _perform_internal(self):
#         # self._gauge.set(len(self._rpc.request('author_pendingExtrinsics')['result']))
#
#
# class FinalityInfoUpdater(ExporterPeriodicTask):
#
#     def __init__(self, rpc, cache):
#         super(FinalityInfoUpdater, self).__init__(rpc, 0.2)
#         self._cache = cache
#         # self._gauge_final_block = Gauge('polkadot_final_block',
#         #                                 'Number of last finalized block')
#         #
#         # self._gauge_finality_delay_blocks = Gauge('polkadot_finality_delay_blocks',
#         #                                           'Difference in blocks between head and finalized blocks')
#         # self._histogram_finality_delay_blocks = Histogram('polkadot_finality_delay_blocks_histogram',
#         #                                                   'Histogram of the difference in blocks between head and '
#         #                                                   'finalized blocks')
#     #
#     def _perform_internal(self):
#         final_block_hash = self._rpc.request('chain_getFinalizedHead')['result']
#         latest_block_hash = self._rpc.request('chain_getBlockHash')['result']
#         if final_block_hash is None:
#             return
#
#         block = self._cache.get(final_block_hash)
#         check(block is not None, 'finalized block {} must not be none'.format(final_block_hash))
#         final_block_num = get_block_num(block)
#         self._gauge_final_block.set(final_block_num)
#
#         check(latest_block_hash is not None, 'head block is absent but finalized block isn\'t')
#         block = self._cache.get(latest_block_hash)
#         check(block is not None, 'head block {} must not be none'.format(latest_block_hash))
#         latest_block_num = get_block_num(block)
#
#         self._gauge_finality_delay_blocks.set(latest_block_num - final_block_num)
#         self._histogram_finality_delay_blocks.observe(latest_block_num - final_block_num)
