# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class DataTablesServerSideResponse(object):
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
        'data': 'list[Customer]',
        'draw': 'int',
        'records_filtered': 'int',
        'records_total': 'int'
    }

    attribute_map = {
        'data': 'data',
        'draw': 'draw',
        'records_filtered': 'recordsFiltered',
        'records_total': 'recordsTotal'
    }

    def __init__(self, data=None, draw=None, records_filtered=None, records_total=None):  # noqa: E501
        """DataTablesServerSideResponse - a model defined in Swagger"""  # noqa: E501

        self._data = None
        self._draw = None
        self._records_filtered = None
        self._records_total = None
        self.discriminator = None

        if data is not None:
            self.data = data
        if draw is not None:
            self.draw = draw
        if records_filtered is not None:
            self.records_filtered = records_filtered
        if records_total is not None:
            self.records_total = records_total

    @property
    def data(self):
        """Gets the data of this DataTablesServerSideResponse.  # noqa: E501


        :return: The data of this DataTablesServerSideResponse.  # noqa: E501
        :rtype: list[Customer]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this DataTablesServerSideResponse.


        :param data: The data of this DataTablesServerSideResponse.  # noqa: E501
        :type: list[Customer]
        """

        self._data = data

    @property
    def draw(self):
        """Gets the draw of this DataTablesServerSideResponse.  # noqa: E501


        :return: The draw of this DataTablesServerSideResponse.  # noqa: E501
        :rtype: int
        """
        return self._draw

    @draw.setter
    def draw(self, draw):
        """Sets the draw of this DataTablesServerSideResponse.


        :param draw: The draw of this DataTablesServerSideResponse.  # noqa: E501
        :type: int
        """

        self._draw = draw

    @property
    def records_filtered(self):
        """Gets the records_filtered of this DataTablesServerSideResponse.  # noqa: E501


        :return: The records_filtered of this DataTablesServerSideResponse.  # noqa: E501
        :rtype: int
        """
        return self._records_filtered

    @records_filtered.setter
    def records_filtered(self, records_filtered):
        """Sets the records_filtered of this DataTablesServerSideResponse.


        :param records_filtered: The records_filtered of this DataTablesServerSideResponse.  # noqa: E501
        :type: int
        """

        self._records_filtered = records_filtered

    @property
    def records_total(self):
        """Gets the records_total of this DataTablesServerSideResponse.  # noqa: E501


        :return: The records_total of this DataTablesServerSideResponse.  # noqa: E501
        :rtype: int
        """
        return self._records_total

    @records_total.setter
    def records_total(self, records_total):
        """Sets the records_total of this DataTablesServerSideResponse.


        :param records_total: The records_total of this DataTablesServerSideResponse.  # noqa: E501
        :type: int
        """

        self._records_total = records_total

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
        if issubclass(DataTablesServerSideResponse, dict):
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
        if not isinstance(other, DataTablesServerSideResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
