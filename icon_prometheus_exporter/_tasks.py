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

from abc import abstractmethod
from icon_prometheus_exporter._utils import PeriodicTask, check
from icon_prometheus_exporter._rpc import iconRPCError, get_block_num
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import Gauge

#

class ExporterPeriodicTask( PeriodicTask ):
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
class prepsUpdater( ExporterPeriodicTask ):
    def __init__(self, rpc, request_data):
        super( prepsUpdater, self ).__init__( rpc, 1 )
        self.request_data = request_data
        self._gauge_preps_totalBlocks = Gauge( 'icon_preps_totalBlocks','------the total number of block chain',['p2pEndpoint'] )
        self._gauge_preps_validatedBlocks = Gauge( 'icon_preps_validatedBlocks','------the total number of validated block chain',['p2pEndpoint'] )
        self._gauge_preps_blockHeight = Gauge( 'icon_preps_blockHeight','------the hight of block chain',['p2pEndpoint'])
        iconlist = []
        blockHeight = {}
        self._allpreps = (self._rpc.request( self.request_data )["result"]["preps"])
        print (self._allpreps)


    def _perform_internal(self):
        print( "------------" )
        print( "internal Performer" )
        self.update_Blockhight()
        self._allpreps = (self._rpc.request( self.request_data )["result"]["preps"])
        for i in range( len( self._allpreps )):
            self._gauge_preps_totalBlocks.labels([self._allpreps[i]["p2pEndpoint"]]).set(int( self._allpreps[i]["totalBlocks"], 16 ))
            self._gauge_preps_validatedBlocks.labels([self._allpreps[i]["p2pEndpoint"]]).set(int( self._allpreps[i]["validatedBlocks"], 16 ))
            self._gauge_preps_blockHeight.labels([self._allpreps[i]["p2pEndpoint"]]).set(int( self._allpreps[i]["blockHeight"], 16 ))
            print (i)
            if(i==9): return
            # self._gauge_preps_validatedBlocks.add_metric( [ self._allpreps[i]["p2pEndpoint"]],
            #                                               int( self._allpreps[i]["validatedBlocks"], 16 ) )
            # self._gauge_preps_blockHeight.add_metric( [self._allpreps[i]["p2pEndpoint"]],
            #                                           int( self._allpreps[i]["blockHeight"], 16 ) )
        # yield self._gauge_preps_totalBlocks
        # yield self._gauge_preps_blockHeight
        # yield self._gauge_preps_validatedBlocks

    def update_Blockhight(self):
        pass

