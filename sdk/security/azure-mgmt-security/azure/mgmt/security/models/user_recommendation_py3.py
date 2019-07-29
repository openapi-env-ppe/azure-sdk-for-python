# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UserRecommendation(Model):
    """Represents a user that is recommended to be allowed for a certain rule.

    :param username: Represents a user that is recommended to be allowed for a
     certain rule
    :type username: str
    :param recommendation_action: Possible values include: 'Recommended',
     'Add', 'Remove'
    :type recommendation_action: str or ~azure.mgmt.security.models.enum
    """

    _attribute_map = {
        'username': {'key': 'username', 'type': 'str'},
        'recommendation_action': {'key': 'recommendationAction', 'type': 'str'},
    }

    def __init__(self, *, username: str=None, recommendation_action=None, **kwargs) -> None:
        super(UserRecommendation, self).__init__(**kwargs)
        self.username = username
        self.recommendation_action = recommendation_action