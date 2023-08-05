# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.100.6
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import printnanny_api_client
from printnanny_api_client.models.paginated_pi_list import PaginatedPiList  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestPaginatedPiList(unittest.TestCase):
    """PaginatedPiList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedPiList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.paginated_pi_list.PaginatedPiList()  # noqa: E501
        if include_optional :
            return PaginatedPiList(
                count = 123, 
                next = 'http://api.example.org/accounts/?page=4', 
                previous = 'http://api.example.org/accounts/?page=2', 
                results = [
                    printnanny_api_client.models.pi.Pi(
                        id = 56, 
                        last_boot = '', 
                        settings = null, 
                        cloudiot_device = null, 
                        user = null, 
                        system_info = null, 
                        public_key = null, 
                        webrtc_edge = null, 
                        webrtc_cloud = null, 
                        octoprint_server = null, 
                        urls = printnanny_api_client.models.pi_urls.Pi_urls(
                            swupdate = '', 
                            octoprint = '', ), 
                        sbc = 'rpi_4', 
                        edition = 'octoprint_lite', 
                        created_dt = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        hostname = '', 
                        fqdn = '', 
                        favorite = True, 
                        setup_finished = True, )
                    ]
            )
        else :
            return PaginatedPiList(
        )

    def testPaginatedPiList(self):
        """Test PaginatedPiList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
