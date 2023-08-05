# coding: utf-8

"""
    metal-api

    API to manage and control plane resources like machines, switches, operating system images, machine sizes, networks, IP addresses and more  # noqa: E501

    OpenAPI spec version: v0.19.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import metal_python
from metal_python.api.network_api import NetworkApi  # noqa: E501
from metal_python.rest import ApiException


class TestNetworkApi(unittest.TestCase):
    """NetworkApi unit test stubs"""

    def setUp(self):
        self.api = metal_python.api.network_api.NetworkApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_allocate_network(self):
        """Test case for allocate_network

        allocates a child network from a partition's private super network  # noqa: E501
        """
        pass

    def test_create_network(self):
        """Test case for create_network

        create a network. if the given ID already exists a conflict is returned  # noqa: E501
        """
        pass

    def test_delete_network(self):
        """Test case for delete_network

        deletes a network and returns the deleted entity  # noqa: E501
        """
        pass

    def test_find_network(self):
        """Test case for find_network

        get network by id  # noqa: E501
        """
        pass

    def test_find_networks(self):
        """Test case for find_networks

        get all networks that match given properties  # noqa: E501
        """
        pass

    def test_free_network(self):
        """Test case for free_network

        free a network  # noqa: E501
        """
        pass

    def test_free_network_deprecated(self):
        """Test case for free_network_deprecated

        free a network  # noqa: E501
        """
        pass

    def test_list_networks(self):
        """Test case for list_networks

        get all networks  # noqa: E501
        """
        pass

    def test_update_network(self):
        """Test case for update_network

        updates a network. if the network was changed since this one was read, a conflict is returned  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
