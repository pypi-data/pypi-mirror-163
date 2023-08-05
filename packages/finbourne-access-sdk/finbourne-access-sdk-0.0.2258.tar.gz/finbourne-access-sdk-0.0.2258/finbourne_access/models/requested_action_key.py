# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.2258
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_access.configuration import Configuration


class RequestedActionKey(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'entity_code': 'str',
        'scope': 'str',
        'activity': 'str'
    }

    attribute_map = {
        'entity_code': 'entityCode',
        'scope': 'scope',
        'activity': 'activity'
    }

    required_map = {
        'entity_code': 'required',
        'scope': 'required',
        'activity': 'required'
    }

    def __init__(self, entity_code=None, scope=None, activity=None, local_vars_configuration=None):  # noqa: E501
        """RequestedActionKey - a model defined in OpenAPI"
        
        :param entity_code:  The type of the resource on which the activity would be performed (required)
        :type entity_code: str
        :param scope:  The scope/provider/vendor of the activity (required)
        :type scope: str
        :param activity:  The identifier of the action to be performed on the resource (required)
        :type activity: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._entity_code = None
        self._scope = None
        self._activity = None
        self.discriminator = None

        self.entity_code = entity_code
        self.scope = scope
        self.activity = activity

    @property
    def entity_code(self):
        """Gets the entity_code of this RequestedActionKey.  # noqa: E501

        The type of the resource on which the activity would be performed  # noqa: E501

        :return: The entity_code of this RequestedActionKey.  # noqa: E501
        :rtype: str
        """
        return self._entity_code

    @entity_code.setter
    def entity_code(self, entity_code):
        """Sets the entity_code of this RequestedActionKey.

        The type of the resource on which the activity would be performed  # noqa: E501

        :param entity_code: The entity_code of this RequestedActionKey.  # noqa: E501
        :type entity_code: str
        """
        if self.local_vars_configuration.client_side_validation and entity_code is None:  # noqa: E501
            raise ValueError("Invalid value for `entity_code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                entity_code is not None and len(entity_code) > 100):
            raise ValueError("Invalid value for `entity_code`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                entity_code is not None and len(entity_code) < 3):
            raise ValueError("Invalid value for `entity_code`, length must be greater than or equal to `3`")  # noqa: E501

        self._entity_code = entity_code

    @property
    def scope(self):
        """Gets the scope of this RequestedActionKey.  # noqa: E501

        The scope/provider/vendor of the activity  # noqa: E501

        :return: The scope of this RequestedActionKey.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this RequestedActionKey.

        The scope/provider/vendor of the activity  # noqa: E501

        :param scope: The scope of this RequestedActionKey.  # noqa: E501
        :type scope: str
        """
        if self.local_vars_configuration.client_side_validation and scope is None:  # noqa: E501
            raise ValueError("Invalid value for `scope`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) > 100):
            raise ValueError("Invalid value for `scope`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                scope is not None and len(scope) < 3):
            raise ValueError("Invalid value for `scope`, length must be greater than or equal to `3`")  # noqa: E501

        self._scope = scope

    @property
    def activity(self):
        """Gets the activity of this RequestedActionKey.  # noqa: E501

        The identifier of the action to be performed on the resource  # noqa: E501

        :return: The activity of this RequestedActionKey.  # noqa: E501
        :rtype: str
        """
        return self._activity

    @activity.setter
    def activity(self, activity):
        """Sets the activity of this RequestedActionKey.

        The identifier of the action to be performed on the resource  # noqa: E501

        :param activity: The activity of this RequestedActionKey.  # noqa: E501
        :type activity: str
        """
        if self.local_vars_configuration.client_side_validation and activity is None:  # noqa: E501
            raise ValueError("Invalid value for `activity`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                activity is not None and len(activity) > 100):
            raise ValueError("Invalid value for `activity`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                activity is not None and len(activity) < 3):
            raise ValueError("Invalid value for `activity`, length must be greater than or equal to `3`")  # noqa: E501

        self._activity = activity

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
        if not isinstance(other, RequestedActionKey):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RequestedActionKey):
            return True

        return self.to_dict() != other.to_dict()
