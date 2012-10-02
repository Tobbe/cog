import cog_tool.test.base as test

class TestLink(test.TC):
    def test_link_link(self):
        test.add_data(self.state, a={}, b={'ID': 'beta'})

        test.run_cmd(self.state, 'link', '-t', 'link', 'a', 'b')
        self.assertHas('a', 'LINK', 'beta b')

    def test_link_parent(self):
        test.add_data(self.state, a={}, b={'ID': 'beta'})

        test.run_cmd(self.state, 'link', '-t', 'parent', 'a', 'b')
        self.assertHas('a', 'PARENT', 'beta b')

    def test_link_multiple(self):
        test.add_data(self.state, a={}, b={'ID': 'beta'}, c={'ID': 'gamma'})

        test.run_cmd(self.state, 'link', '-t', 'link', 'a', 'b', 'c')
        self.assertHas('a', 'LINK', 'beta b')
        self.assertHas('a', 'LINK', 'gamma c')
