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


class CouponFreeItemAndShippingWithSubtotal(object):
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
        'currency_code': 'str',
        'items': 'list[str]',
        'limit': 'int',
        'shipping_methods': 'list[str]',
        'subtotal_amount': 'float'
    }

    attribute_map = {
        'currency_code': 'currency_code',
        'items': 'items',
        'limit': 'limit',
        'shipping_methods': 'shipping_methods',
        'subtotal_amount': 'subtotal_amount'
    }

    def __init__(self, currency_code=None, items=None, limit=None, shipping_methods=None, subtotal_amount=None):  # noqa: E501
        """CouponFreeItemAndShippingWithSubtotal - a model defined in Swagger"""  # noqa: E501

        self._currency_code = None
        self._items = None
        self._limit = None
        self._shipping_methods = None
        self._subtotal_amount = None
        self.discriminator = None

        if currency_code is not None:
            self.currency_code = currency_code
        if items is not None:
            self.items = items
        if limit is not None:
            self.limit = limit
        if shipping_methods is not None:
            self.shipping_methods = shipping_methods
        if subtotal_amount is not None:
            self.subtotal_amount = subtotal_amount

    @property
    def currency_code(self):
        """Gets the currency_code of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501

        The ISO-4217 three letter currency code the customer is viewing prices in  # noqa: E501

        :return: The currency_code of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """Sets the currency_code of this CouponFreeItemAndShippingWithSubtotal.

        The ISO-4217 three letter currency code the customer is viewing prices in  # noqa: E501

        :param currency_code: The currency_code of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :type: str
        """
        if currency_code is not None and len(currency_code) > 3:
            raise ValueError("Invalid value for `currency_code`, length must be less than or equal to `3`")  # noqa: E501

        self._currency_code = currency_code

    @property
    def items(self):
        """Gets the items of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501

        A list of items that are eligible for this discount_price.  # noqa: E501

        :return: The items of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :rtype: list[str]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this CouponFreeItemAndShippingWithSubtotal.

        A list of items that are eligible for this discount_price.  # noqa: E501

        :param items: The items of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :type: list[str]
        """

        self._items = items

    @property
    def limit(self):
        """Gets the limit of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501

        The limit of free items that may be received when purchasing multiple items  # noqa: E501

        :return: The limit of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this CouponFreeItemAndShippingWithSubtotal.

        The limit of free items that may be received when purchasing multiple items  # noqa: E501

        :param limit: The limit of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :type: int
        """

        self._limit = limit

    @property
    def shipping_methods(self):
        """Gets the shipping_methods of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501

        One or more shipping methods that may be free  # noqa: E501

        :return: The shipping_methods of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :rtype: list[str]
        """
        return self._shipping_methods

    @shipping_methods.setter
    def shipping_methods(self, shipping_methods):
        """Sets the shipping_methods of this CouponFreeItemAndShippingWithSubtotal.

        One or more shipping methods that may be free  # noqa: E501

        :param shipping_methods: The shipping_methods of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :type: list[str]
        """

        self._shipping_methods = shipping_methods

    @property
    def subtotal_amount(self):
        """Gets the subtotal_amount of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501

        The amount of subtotal required to receive the discount percent  # noqa: E501

        :return: The subtotal_amount of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :rtype: float
        """
        return self._subtotal_amount

    @subtotal_amount.setter
    def subtotal_amount(self, subtotal_amount):
        """Sets the subtotal_amount of this CouponFreeItemAndShippingWithSubtotal.

        The amount of subtotal required to receive the discount percent  # noqa: E501

        :param subtotal_amount: The subtotal_amount of this CouponFreeItemAndShippingWithSubtotal.  # noqa: E501
        :type: float
        """

        self._subtotal_amount = subtotal_amount

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
        if issubclass(CouponFreeItemAndShippingWithSubtotal, dict):
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
        if not isinstance(other, CouponFreeItemAndShippingWithSubtotal):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
