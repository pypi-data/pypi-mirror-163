"""
    lakeFS API

    lakeFS HTTP API  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: services@treeverse.io
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import lakefs_client
from lakefs_client.model.staging_location import StagingLocation
globals()['StagingLocation'] = StagingLocation
from lakefs_client.model.staging_metadata import StagingMetadata


class TestStagingMetadata(unittest.TestCase):
    """StagingMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStagingMetadata(self):
        """Test StagingMetadata"""
        # FIXME: construct object with mandatory attributes with example values
        # model = StagingMetadata()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
