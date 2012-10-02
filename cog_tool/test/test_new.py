import cog_tool.test.base as test

class TestNew(test.TC):
    def test_create_new(self):
        test.run_cmd(self.state, 'new', 'a')
        self.assertCount(1)

        data = self.state.get_all()[0]
        for key in ['ID', 'NAME', 'DESCRIPTION']:
            self.assertTrue(data.get(key))

    def test_create_new_all(self):
        test.run_cmd(self.state, 'new', '--all', 'a')
        self.assertCount(1)

        data = self.state.get_all()[0]
        for key in ['ID', 'NAME', 'DESCRIPTION', 'STATUS', 'ASSIGNED',
                    'PRIORITY', 'LINK', 'PARENT']:
            self.assertTrue(data.get(key))

    def test_create_new_multiple(self):
        test.run_cmd(self.state, 'new', 'a', 'b', 'c')
        self.assertCount(3)
