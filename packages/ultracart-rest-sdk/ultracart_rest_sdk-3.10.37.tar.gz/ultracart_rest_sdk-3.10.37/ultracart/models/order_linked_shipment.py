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


class OrderLinkedShipment(object):
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
        'has_linked_shipment': 'bool',
        'linked_shipment': 'bool',
        'linked_shipment_channel_partner_order_ids': 'list[str]',
        'linked_shipment_order_ids': 'list[str]',
        'linked_shipment_to_order_id': 'str'
    }

    attribute_map = {
        'has_linked_shipment': 'has_linked_shipment',
        'linked_shipment': 'linked_shipment',
        'linked_shipment_channel_partner_order_ids': 'linked_shipment_channel_partner_order_ids',
        'linked_shipment_order_ids': 'linked_shipment_order_ids',
        'linked_shipment_to_order_id': 'linked_shipment_to_order_id'
    }

    def __init__(self, has_linked_shipment=None, linked_shipment=None, linked_shipment_channel_partner_order_ids=None, linked_shipment_order_ids=None, linked_shipment_to_order_id=None):  # noqa: E501
        """OrderLinkedShipment - a model defined in Swagger"""  # noqa: E501

        self._has_linked_shipment = None
        self._linked_shipment = None
        self._linked_shipment_channel_partner_order_ids = None
        self._linked_shipment_order_ids = None
        self._linked_shipment_to_order_id = None
        self.discriminator = None

        if has_linked_shipment is not None:
            self.has_linked_shipment = has_linked_shipment
        if linked_shipment is not None:
            self.linked_shipment = linked_shipment
        if linked_shipment_channel_partner_order_ids is not None:
            self.linked_shipment_channel_partner_order_ids = linked_shipment_channel_partner_order_ids
        if linked_shipment_order_ids is not None:
            self.linked_shipment_order_ids = linked_shipment_order_ids
        if linked_shipment_to_order_id is not None:
            self.linked_shipment_to_order_id = linked_shipment_to_order_id

    @property
    def has_linked_shipment(self):
        """Gets the has_linked_shipment of this OrderLinkedShipment.  # noqa: E501

        True if this order has child linked shipments  # noqa: E501

        :return: The has_linked_shipment of this OrderLinkedShipment.  # noqa: E501
        :rtype: bool
        """
        return self._has_linked_shipment

    @has_linked_shipment.setter
    def has_linked_shipment(self, has_linked_shipment):
        """Sets the has_linked_shipment of this OrderLinkedShipment.

        True if this order has child linked shipments  # noqa: E501

        :param has_linked_shipment: The has_linked_shipment of this OrderLinkedShipment.  # noqa: E501
        :type: bool
        """

        self._has_linked_shipment = has_linked_shipment

    @property
    def linked_shipment(self):
        """Gets the linked_shipment of this OrderLinkedShipment.  # noqa: E501

        True if this order is linked to another parent order  # noqa: E501

        :return: The linked_shipment of this OrderLinkedShipment.  # noqa: E501
        :rtype: bool
        """
        return self._linked_shipment

    @linked_shipment.setter
    def linked_shipment(self, linked_shipment):
        """Sets the linked_shipment of this OrderLinkedShipment.

        True if this order is linked to another parent order  # noqa: E501

        :param linked_shipment: The linked_shipment of this OrderLinkedShipment.  # noqa: E501
        :type: bool
        """

        self._linked_shipment = linked_shipment

    @property
    def linked_shipment_channel_partner_order_ids(self):
        """Gets the linked_shipment_channel_partner_order_ids of this OrderLinkedShipment.  # noqa: E501

        The child linked shipment channel partner order ids  # noqa: E501

        :return: The linked_shipment_channel_partner_order_ids of this OrderLinkedShipment.  # noqa: E501
        :rtype: list[str]
        """
        return self._linked_shipment_channel_partner_order_ids

    @linked_shipment_channel_partner_order_ids.setter
    def linked_shipment_channel_partner_order_ids(self, linked_shipment_channel_partner_order_ids):
        """Sets the linked_shipment_channel_partner_order_ids of this OrderLinkedShipment.

        The child linked shipment channel partner order ids  # noqa: E501

        :param linked_shipment_channel_partner_order_ids: The linked_shipment_channel_partner_order_ids of this OrderLinkedShipment.  # noqa: E501
        :type: list[str]
        """

        self._linked_shipment_channel_partner_order_ids = linked_shipment_channel_partner_order_ids

    @property
    def linked_shipment_order_ids(self):
        """Gets the linked_shipment_order_ids of this OrderLinkedShipment.  # noqa: E501

        The child linked shipment order ids  # noqa: E501

        :return: The linked_shipment_order_ids of this OrderLinkedShipment.  # noqa: E501
        :rtype: list[str]
        """
        return self._linked_shipment_order_ids

    @linked_shipment_order_ids.setter
    def linked_shipment_order_ids(self, linked_shipment_order_ids):
        """Sets the linked_shipment_order_ids of this OrderLinkedShipment.

        The child linked shipment order ids  # noqa: E501

        :param linked_shipment_order_ids: The linked_shipment_order_ids of this OrderLinkedShipment.  # noqa: E501
        :type: list[str]
        """

        self._linked_shipment_order_ids = linked_shipment_order_ids

    @property
    def linked_shipment_to_order_id(self):
        """Gets the linked_shipment_to_order_id of this OrderLinkedShipment.  # noqa: E501

        The parent order id that this one is linked to  # noqa: E501

        :return: The linked_shipment_to_order_id of this OrderLinkedShipment.  # noqa: E501
        :rtype: str
        """
        return self._linked_shipment_to_order_id

    @linked_shipment_to_order_id.setter
    def linked_shipment_to_order_id(self, linked_shipment_to_order_id):
        """Sets the linked_shipment_to_order_id of this OrderLinkedShipment.

        The parent order id that this one is linked to  # noqa: E501

        :param linked_shipment_to_order_id: The linked_shipment_to_order_id of this OrderLinkedShipment.  # noqa: E501
        :type: str
        """

        self._linked_shipment_to_order_id = linked_shipment_to_order_id

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
        if issubclass(OrderLinkedShipment, dict):
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
        if not isinstance(other, OrderLinkedShipment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
