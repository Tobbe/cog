"""This module tests the testing framework.
"""
import cog_tool.test.base as test

class TestTest(test.TC):
    def test_add_data(self):
        test.add_data(self.state,
                      a={'LINK': 123},
                      b={'ID': 'beta'},
                      c={'DESCRIPTION': ['qwe', 'asd']})

        self.assertHas('a', 'LINK', '123')
        self.assertHas('b', 'ID', 'beta')
        self.assertHas('c', 'DESCRIPTION', 'qwe')
        self.assertHas('c', 'DESCRIPTION', 'asd')
        self.assertCount(3)
