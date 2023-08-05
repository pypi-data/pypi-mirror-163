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


class ItemContentMultimediaThumbnail(object):
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
        'height': 'int',
        'http_url': 'str',
        'https_url': 'str',
        'png_format': 'bool',
        'square': 'bool',
        'width': 'int'
    }

    attribute_map = {
        'height': 'height',
        'http_url': 'http_url',
        'https_url': 'https_url',
        'png_format': 'png_format',
        'square': 'square',
        'width': 'width'
    }

    def __init__(self, height=None, http_url=None, https_url=None, png_format=None, square=None, width=None):  # noqa: E501
        """ItemContentMultimediaThumbnail - a model defined in Swagger"""  # noqa: E501

        self._height = None
        self._http_url = None
        self._https_url = None
        self._png_format = None
        self._square = None
        self._width = None
        self.discriminator = None

        if height is not None:
            self.height = height
        if http_url is not None:
            self.http_url = http_url
        if https_url is not None:
            self.https_url = https_url
        if png_format is not None:
            self.png_format = png_format
        if square is not None:
            self.square = square
        if width is not None:
            self.width = width

    @property
    def height(self):
        """Gets the height of this ItemContentMultimediaThumbnail.  # noqa: E501

        Height of the thumbnail  # noqa: E501

        :return: The height of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this ItemContentMultimediaThumbnail.

        Height of the thumbnail  # noqa: E501

        :param height: The height of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def http_url(self):
        """Gets the http_url of this ItemContentMultimediaThumbnail.  # noqa: E501

        HTTP URL to view the thumbnail  # noqa: E501

        :return: The http_url of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: str
        """
        return self._http_url

    @http_url.setter
    def http_url(self, http_url):
        """Sets the http_url of this ItemContentMultimediaThumbnail.

        HTTP URL to view the thumbnail  # noqa: E501

        :param http_url: The http_url of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: str
        """

        self._http_url = http_url

    @property
    def https_url(self):
        """Gets the https_url of this ItemContentMultimediaThumbnail.  # noqa: E501

        HTTPS URL to view the thumbnail  # noqa: E501

        :return: The https_url of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: str
        """
        return self._https_url

    @https_url.setter
    def https_url(self, https_url):
        """Sets the https_url of this ItemContentMultimediaThumbnail.

        HTTPS URL to view the thumbnail  # noqa: E501

        :param https_url: The https_url of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: str
        """

        self._https_url = https_url

    @property
    def png_format(self):
        """Gets the png_format of this ItemContentMultimediaThumbnail.  # noqa: E501

        True if PNG, false if JPEG  # noqa: E501

        :return: The png_format of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: bool
        """
        return self._png_format

    @png_format.setter
    def png_format(self, png_format):
        """Sets the png_format of this ItemContentMultimediaThumbnail.

        True if PNG, false if JPEG  # noqa: E501

        :param png_format: The png_format of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: bool
        """

        self._png_format = png_format

    @property
    def square(self):
        """Gets the square of this ItemContentMultimediaThumbnail.  # noqa: E501

        True if the thumbnail is square  # noqa: E501

        :return: The square of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: bool
        """
        return self._square

    @square.setter
    def square(self, square):
        """Sets the square of this ItemContentMultimediaThumbnail.

        True if the thumbnail is square  # noqa: E501

        :param square: The square of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: bool
        """

        self._square = square

    @property
    def width(self):
        """Gets the width of this ItemContentMultimediaThumbnail.  # noqa: E501

        Width of the thumbnail  # noqa: E501

        :return: The width of this ItemContentMultimediaThumbnail.  # noqa: E501
        :rtype: int
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this ItemContentMultimediaThumbnail.

        Width of the thumbnail  # noqa: E501

        :param width: The width of this ItemContentMultimediaThumbnail.  # noqa: E501
        :type: int
        """

        self._width = width

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
        if issubclass(ItemContentMultimediaThumbnail, dict):
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
        if not isinstance(other, ItemContentMultimediaThumbnail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
