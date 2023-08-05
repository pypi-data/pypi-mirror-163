"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import unittest

import lakefs_client
from lakefs_client.api.repositories_api import RepositoriesApi  # noqa: E501


class TestRepositoriesApi(unittest.TestCase):
    """RepositoriesApi unit test stubs"""

    def setUp(self):
        self.api = RepositoriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_branch_protection_rule(self):
        """Test case for create_branch_protection_rule

        """
        pass

    def test_create_repository(self):
        """Test case for create_repository

        create repository  # noqa: E501
        """
        pass

    def test_delete_branch_protection_rule(self):
        """Test case for delete_branch_protection_rule

        """
        pass

    def test_delete_repository(self):
        """Test case for delete_repository

        delete repository  # noqa: E501
        """
        pass

    def test_get_branch_protection_rules(self):
        """Test case for get_branch_protection_rules

        get branch protection rules  # noqa: E501
        """
        pass

    def test_get_repository(self):
        """Test case for get_repository

        get repository  # noqa: E501
        """
        pass

    def test_list_repositories(self):
        """Test case for list_repositories

        list repositories  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
