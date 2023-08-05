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


class V1NetworkImmutable(object):
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
        'destinationprefixes': 'list[str]',
        'nat': 'bool',
        'parentnetworkid': 'str',
        'prefixes': 'list[str]',
        'privatesuper': 'bool',
        'underlay': 'bool',
        'vrf': 'int',
        'vrfshared': 'bool'
    }

    attribute_map = {
        'destinationprefixes': 'destinationprefixes',
        'nat': 'nat',
        'parentnetworkid': 'parentnetworkid',
        'prefixes': 'prefixes',
        'privatesuper': 'privatesuper',
        'underlay': 'underlay',
        'vrf': 'vrf',
        'vrfshared': 'vrfshared'
    }

    def __init__(self, destinationprefixes=None, nat=None, parentnetworkid=None, prefixes=None, privatesuper=None, underlay=None, vrf=None, vrfshared=None):  # noqa: E501
        """V1NetworkImmutable - a model defined in Swagger"""  # noqa: E501

        self._destinationprefixes = None
        self._nat = None
        self._parentnetworkid = None
        self._prefixes = None
        self._privatesuper = None
        self._underlay = None
        self._vrf = None
        self._vrfshared = None
        self.discriminator = None

        self.destinationprefixes = destinationprefixes
        self.nat = nat
        if parentnetworkid is not None:
            self.parentnetworkid = parentnetworkid
        self.prefixes = prefixes
        self.privatesuper = privatesuper
        self.underlay = underlay
        if vrf is not None:
            self.vrf = vrf
        if vrfshared is not None:
            self.vrfshared = vrfshared

    @property
    def destinationprefixes(self):
        """Gets the destinationprefixes of this V1NetworkImmutable.  # noqa: E501

        the destination prefixes of this network  # noqa: E501

        :return: The destinationprefixes of this V1NetworkImmutable.  # noqa: E501
        :rtype: list[str]
        """
        return self._destinationprefixes

    @destinationprefixes.setter
    def destinationprefixes(self, destinationprefixes):
        """Sets the destinationprefixes of this V1NetworkImmutable.

        the destination prefixes of this network  # noqa: E501

        :param destinationprefixes: The destinationprefixes of this V1NetworkImmutable.  # noqa: E501
        :type: list[str]
        """
        if destinationprefixes is None:
            raise ValueError("Invalid value for `destinationprefixes`, must not be `None`")  # noqa: E501

        self._destinationprefixes = destinationprefixes

    @property
    def nat(self):
        """Gets the nat of this V1NetworkImmutable.  # noqa: E501

        if set to true, packets leaving this network get masqueraded behind interface ip  # noqa: E501

        :return: The nat of this V1NetworkImmutable.  # noqa: E501
        :rtype: bool
        """
        return self._nat

    @nat.setter
    def nat(self, nat):
        """Sets the nat of this V1NetworkImmutable.

        if set to true, packets leaving this network get masqueraded behind interface ip  # noqa: E501

        :param nat: The nat of this V1NetworkImmutable.  # noqa: E501
        :type: bool
        """
        if nat is None:
            raise ValueError("Invalid value for `nat`, must not be `None`")  # noqa: E501

        self._nat = nat

    @property
    def parentnetworkid(self):
        """Gets the parentnetworkid of this V1NetworkImmutable.  # noqa: E501

        the id of the parent network  # noqa: E501

        :return: The parentnetworkid of this V1NetworkImmutable.  # noqa: E501
        :rtype: str
        """
        return self._parentnetworkid

    @parentnetworkid.setter
    def parentnetworkid(self, parentnetworkid):
        """Sets the parentnetworkid of this V1NetworkImmutable.

        the id of the parent network  # noqa: E501

        :param parentnetworkid: The parentnetworkid of this V1NetworkImmutable.  # noqa: E501
        :type: str
        """

        self._parentnetworkid = parentnetworkid

    @property
    def prefixes(self):
        """Gets the prefixes of this V1NetworkImmutable.  # noqa: E501

        the prefixes of this network  # noqa: E501

        :return: The prefixes of this V1NetworkImmutable.  # noqa: E501
        :rtype: list[str]
        """
        return self._prefixes

    @prefixes.setter
    def prefixes(self, prefixes):
        """Sets the prefixes of this V1NetworkImmutable.

        the prefixes of this network  # noqa: E501

        :param prefixes: The prefixes of this V1NetworkImmutable.  # noqa: E501
        :type: list[str]
        """
        if prefixes is None:
            raise ValueError("Invalid value for `prefixes`, must not be `None`")  # noqa: E501

        self._prefixes = prefixes

    @property
    def privatesuper(self):
        """Gets the privatesuper of this V1NetworkImmutable.  # noqa: E501

        if set to true, this network will serve as a partition's super network for the internal machine networks,there can only be one privatesuper network per partition  # noqa: E501

        :return: The privatesuper of this V1NetworkImmutable.  # noqa: E501
        :rtype: bool
        """
        return self._privatesuper

    @privatesuper.setter
    def privatesuper(self, privatesuper):
        """Sets the privatesuper of this V1NetworkImmutable.

        if set to true, this network will serve as a partition's super network for the internal machine networks,there can only be one privatesuper network per partition  # noqa: E501

        :param privatesuper: The privatesuper of this V1NetworkImmutable.  # noqa: E501
        :type: bool
        """
        if privatesuper is None:
            raise ValueError("Invalid value for `privatesuper`, must not be `None`")  # noqa: E501

        self._privatesuper = privatesuper

    @property
    def underlay(self):
        """Gets the underlay of this V1NetworkImmutable.  # noqa: E501

        if set to true, this network can be used for underlay communication  # noqa: E501

        :return: The underlay of this V1NetworkImmutable.  # noqa: E501
        :rtype: bool
        """
        return self._underlay

    @underlay.setter
    def underlay(self, underlay):
        """Sets the underlay of this V1NetworkImmutable.

        if set to true, this network can be used for underlay communication  # noqa: E501

        :param underlay: The underlay of this V1NetworkImmutable.  # noqa: E501
        :type: bool
        """
        if underlay is None:
            raise ValueError("Invalid value for `underlay`, must not be `None`")  # noqa: E501

        self._underlay = underlay

    @property
    def vrf(self):
        """Gets the vrf of this V1NetworkImmutable.  # noqa: E501

        the vrf this network is associated with  # noqa: E501

        :return: The vrf of this V1NetworkImmutable.  # noqa: E501
        :rtype: int
        """
        return self._vrf

    @vrf.setter
    def vrf(self, vrf):
        """Sets the vrf of this V1NetworkImmutable.

        the vrf this network is associated with  # noqa: E501

        :param vrf: The vrf of this V1NetworkImmutable.  # noqa: E501
        :type: int
        """

        self._vrf = vrf

    @property
    def vrfshared(self):
        """Gets the vrfshared of this V1NetworkImmutable.  # noqa: E501

        if set to true, given vrf can be used by multiple networks, which is sometimes useful for network partioning (default: false)  # noqa: E501

        :return: The vrfshared of this V1NetworkImmutable.  # noqa: E501
        :rtype: bool
        """
        return self._vrfshared

    @vrfshared.setter
    def vrfshared(self, vrfshared):
        """Sets the vrfshared of this V1NetworkImmutable.

        if set to true, given vrf can be used by multiple networks, which is sometimes useful for network partioning (default: false)  # noqa: E501

        :param vrfshared: The vrfshared of this V1NetworkImmutable.  # noqa: E501
        :type: bool
        """

        self._vrfshared = vrfshared

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
        if issubclass(V1NetworkImmutable, dict):
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
        if not isinstance(other, V1NetworkImmutable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
