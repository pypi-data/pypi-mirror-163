"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import unittest

import lakefs_client
from lakefs_client.api.tags_api import TagsApi  # noqa: E501


class TestTagsApi(unittest.TestCase):
    """TagsApi unit test stubs"""

    def setUp(self):
        self.api = TagsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_tag(self):
        """Test case for create_tag

        create tag  # noqa: E501
        """
        pass

    def test_delete_tag(self):
        """Test case for delete_tag

        delete tag  # noqa: E501
        """
        pass

    def test_get_tag(self):
        """Test case for get_tag

        get tag  # noqa: E501
        """
        pass

    def test_list_tags(self):
        """Test case for list_tags

        list tags  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
