# coding: utf-8

"""
    printnanny-api-client

    Official API client library for printnanny.ai  # noqa: E501

    The version of the OpenAPI document: 0.100.6
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class PiSoftwareUpdatePayload(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'wic_tarball_url': 'str',
        'wic_bmap_url': 'str',
        'manifest_url': 'str',
        'swu_url': 'str',
        'version_id': 'str',
        'version': 'str',
        'version_codename': 'str'
    }

    attribute_map = {
        'wic_tarball_url': 'wic_tarball_url',
        'wic_bmap_url': 'wic_bmap_url',
        'manifest_url': 'manifest_url',
        'swu_url': 'swu_url',
        'version_id': 'version_id',
        'version': 'version',
        'version_codename': 'version_codename'
    }

    def __init__(self, wic_tarball_url=None, wic_bmap_url=None, manifest_url=None, swu_url=None, version_id=None, version=None, version_codename=None, local_vars_configuration=None):  # noqa: E501
        """PiSoftwareUpdatePayload - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._wic_tarball_url = None
        self._wic_bmap_url = None
        self._manifest_url = None
        self._swu_url = None
        self._version_id = None
        self._version = None
        self._version_codename = None
        self.discriminator = None

        self.wic_tarball_url = wic_tarball_url
        self.wic_bmap_url = wic_bmap_url
        self.manifest_url = manifest_url
        self.swu_url = swu_url
        self.version_id = version_id
        self.version = version
        self.version_codename = version_codename

    @property
    def wic_tarball_url(self):
        """Gets the wic_tarball_url of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The wic_tarball_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._wic_tarball_url

    @wic_tarball_url.setter
    def wic_tarball_url(self, wic_tarball_url):
        """Sets the wic_tarball_url of this PiSoftwareUpdatePayload.


        :param wic_tarball_url: The wic_tarball_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :type wic_tarball_url: str
        """
        if self.local_vars_configuration.client_side_validation and wic_tarball_url is None:  # noqa: E501
            raise ValueError("Invalid value for `wic_tarball_url`, must not be `None`")  # noqa: E501

        self._wic_tarball_url = wic_tarball_url

    @property
    def wic_bmap_url(self):
        """Gets the wic_bmap_url of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The wic_bmap_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._wic_bmap_url

    @wic_bmap_url.setter
    def wic_bmap_url(self, wic_bmap_url):
        """Sets the wic_bmap_url of this PiSoftwareUpdatePayload.


        :param wic_bmap_url: The wic_bmap_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :type wic_bmap_url: str
        """
        if self.local_vars_configuration.client_side_validation and wic_bmap_url is None:  # noqa: E501
            raise ValueError("Invalid value for `wic_bmap_url`, must not be `None`")  # noqa: E501

        self._wic_bmap_url = wic_bmap_url

    @property
    def manifest_url(self):
        """Gets the manifest_url of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The manifest_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._manifest_url

    @manifest_url.setter
    def manifest_url(self, manifest_url):
        """Sets the manifest_url of this PiSoftwareUpdatePayload.


        :param manifest_url: The manifest_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :type manifest_url: str
        """
        if self.local_vars_configuration.client_side_validation and manifest_url is None:  # noqa: E501
            raise ValueError("Invalid value for `manifest_url`, must not be `None`")  # noqa: E501

        self._manifest_url = manifest_url

    @property
    def swu_url(self):
        """Gets the swu_url of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The swu_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._swu_url

    @swu_url.setter
    def swu_url(self, swu_url):
        """Sets the swu_url of this PiSoftwareUpdatePayload.


        :param swu_url: The swu_url of this PiSoftwareUpdatePayload.  # noqa: E501
        :type swu_url: str
        """
        if self.local_vars_configuration.client_side_validation and swu_url is None:  # noqa: E501
            raise ValueError("Invalid value for `swu_url`, must not be `None`")  # noqa: E501

        self._swu_url = swu_url

    @property
    def version_id(self):
        """Gets the version_id of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The version_id of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._version_id

    @version_id.setter
    def version_id(self, version_id):
        """Sets the version_id of this PiSoftwareUpdatePayload.


        :param version_id: The version_id of this PiSoftwareUpdatePayload.  # noqa: E501
        :type version_id: str
        """
        if self.local_vars_configuration.client_side_validation and version_id is None:  # noqa: E501
            raise ValueError("Invalid value for `version_id`, must not be `None`")  # noqa: E501

        self._version_id = version_id

    @property
    def version(self):
        """Gets the version of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The version of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this PiSoftwareUpdatePayload.


        :param version: The version of this PiSoftwareUpdatePayload.  # noqa: E501
        :type version: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def version_codename(self):
        """Gets the version_codename of this PiSoftwareUpdatePayload.  # noqa: E501


        :return: The version_codename of this PiSoftwareUpdatePayload.  # noqa: E501
        :rtype: str
        """
        return self._version_codename

    @version_codename.setter
    def version_codename(self, version_codename):
        """Sets the version_codename of this PiSoftwareUpdatePayload.


        :param version_codename: The version_codename of this PiSoftwareUpdatePayload.  # noqa: E501
        :type version_codename: str
        """
        if self.local_vars_configuration.client_side_validation and version_codename is None:  # noqa: E501
            raise ValueError("Invalid value for `version_codename`, must not be `None`")  # noqa: E501

        self._version_codename = version_codename

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PiSoftwareUpdatePayload):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PiSoftwareUpdatePayload):
            return True

        return self.to_dict() != other.to_dict()
