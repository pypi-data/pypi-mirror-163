# coding: utf-8

"""
    metal-api

    API to manage and control plane resources like machines, switches, operating system images, machine sizes, networks, IP addresses and more  # noqa: E501

    OpenAPI spec version: v0.19.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class V1IPIdentifiable(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'allocationuuid': 'str',
        'ipaddress': 'str'
    }

    attribute_map = {
        'allocationuuid': 'allocationuuid',
        'ipaddress': 'ipaddress'
    }

    def __init__(self, allocationuuid=None, ipaddress=None):  # noqa: E501
        """V1IPIdentifiable - a model defined in Swagger"""  # noqa: E501

        self._allocationuuid = None
        self._ipaddress = None
        self.discriminator = None

        self.allocationuuid = allocationuuid
        self.ipaddress = ipaddress

    @property
    def allocationuuid(self):
        """Gets the allocationuuid of this V1IPIdentifiable.  # noqa: E501

        a unique identifier for this ip address allocation, can be used to distinguish between ip address allocation over time.  # noqa: E501

        :return: The allocationuuid of this V1IPIdentifiable.  # noqa: E501
        :rtype: str
        """
        return self._allocationuuid

    @allocationuuid.setter
    def allocationuuid(self, allocationuuid):
        """Sets the allocationuuid of this V1IPIdentifiable.

        a unique identifier for this ip address allocation, can be used to distinguish between ip address allocation over time.  # noqa: E501

        :param allocationuuid: The allocationuuid of this V1IPIdentifiable.  # noqa: E501
        :type: str
        """
        if allocationuuid is None:
            raise ValueError("Invalid value for `allocationuuid`, must not be `None`")  # noqa: E501

        self._allocationuuid = allocationuuid

    @property
    def ipaddress(self):
        """Gets the ipaddress of this V1IPIdentifiable.  # noqa: E501

        the address (ipv4 or ipv6) of this ip  # noqa: E501

        :return: The ipaddress of this V1IPIdentifiable.  # noqa: E501
        :rtype: str
        """
        return self._ipaddress

    @ipaddress.setter
    def ipaddress(self, ipaddress):
        """Sets the ipaddress of this V1IPIdentifiable.

        the address (ipv4 or ipv6) of this ip  # noqa: E501

        :param ipaddress: The ipaddress of this V1IPIdentifiable.  # noqa: E501
        :type: str
        """
        if ipaddress is None:
            raise ValueError("Invalid value for `ipaddress`, must not be `None`")  # noqa: E501

        self._ipaddress = ipaddress

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1IPIdentifiable, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1IPIdentifiable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
