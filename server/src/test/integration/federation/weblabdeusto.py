#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
# 

import time
import unittest

import voodoo.gen.loader.ServerLoader as ServerLoader

from weblab.data.command import Command
from weblab.data.experiments import ExperimentId
from weblab.core.coordinator.clients.weblabdeusto import WebLabDeustoClient
from weblab.core.reservations import Reservation

FEDERATED_DEPLOYMENTS = 'test/deployments/federated_basic'

CONSUMER_CONFIG_PATH  = FEDERATED_DEPLOYMENTS + '/consumer/'
PROVIDER1_CONFIG_PATH = FEDERATED_DEPLOYMENTS + '/provider1/'
PROVIDER2_CONFIG_PATH = FEDERATED_DEPLOYMENTS + '/provider2/'

class FederatedWebLabDeustoTestCase(unittest.TestCase):
    def setUp(self):
        self.server_loader     = ServerLoader.ServerLoader()

        self.consumer_handler  = self.server_loader.load_instance( CONSUMER_CONFIG_PATH,   'consumer_machine', 'main_instance' )
        self.provider1_handler = self.server_loader.load_instance( PROVIDER1_CONFIG_PATH,  'provider1_machine', 'main_instance' )
        self.provider2_handler = self.server_loader.load_instance( PROVIDER2_CONFIG_PATH,  'provider2_machine', 'main_instance' )

        self.consumer_login_client = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 18645 )
        self.consumer_core_client  = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 18345 )

        self.provider1_login_client = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 28645 )
        self.provider1_core_client  = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 28345 )

        self.provider2_login_client = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 38645 )
        self.provider2_core_client  = WebLabDeustoClient("http://127.0.0.1:%s/weblab/" % 38345 )

        self.dummy1 = ExperimentId("dummy1", "Dummy experiments")
        self.dummy2 = ExperimentId("dummy2", "Dummy experiments")
        self.dummy3 = ExperimentId("dummy3", "Dummy experiments")
        self.dummy4 = ExperimentId("dummy4", "Dummy experiments")

    def tearDown(self):
        self.consumer_handler.stop()
        self.provider1_handler.stop()
        self.provider2_handler.stop()

    def test_local_experiment(self):
        #######################################################
        # 
        #   Local testing  (to check that everything is right)
        # 
        #   We enter as a student of Consumer, and we ask for an
        #   experiment that only the Consumer university has.
        # 
        session_id = self.consumer_login_client.login('fedstudent1', 'password')

        self._test_reservation(session_id, self.dummy2, 'Consumer', True, True)
        
        #######################################################
        # 
        #   Simple federation
        # 
        #   Now we ask for an experiment that only Provider 1
        #   has. There is no load balance, neither 
        #   subcontracting
        #
        #self._test_reservation(session_id, self.dummy3, 'Provider 1', True, True)

    def _test_reservation(self, session_id, experiment_id, expected_server_info, wait, finish):
        reservation_status = self.consumer_core_client.reserve_experiment(session_id, experiment_id, "{}", "{}")
        
        reservation_id = reservation_status.reservation_id

        if not wait:
            if finish:
                self.consumer_core_client.finished_experiment(reservation_id)
            return reservation_id

        max_timeout = 10
        initial_time = time.time()

        while reservation_status.status in (Reservation.WAITING, Reservation.WAITING_CONFIRMATION):
            if time.time() - initial_time > max_timeout:
                self.fail("Waiting too long in the queue for %s in %s" % (experiment_id, expected_server_info))
            time.sleep(0.1)
            reservation_status = self.consumer_core_client.get_reservation_status(reservation_id)
        
        self.assertEquals(Reservation.CONFIRMED, reservation_status.status)

        experiment_reservation_id = reservation_status.remote_reservation_id
        if experiment_reservation_id.id == '':
            experiment_reservation_id = reservation_id
            
        client = WebLabDeustoClient( reservation_status.url )

        response = client.send_command(experiment_reservation_id, Command("server_info"))
        self.assertEquals(expected_server_info, response.get_command_string())

        if finish:
            self.consumer_core_client.finished_experiment(reservation_id)

        return reservation_id


def suite():
    suites = (unittest.makeSuite(FederatedWebLabDeustoTestCase), )
    return unittest.TestSuite( suites )

if __name__ == '__main__':
    unittest.main()


