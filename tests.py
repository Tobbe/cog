import unittest

def run_tests():
    tests = unittest.defaultTestLoader.discover('cog_tool/test')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    run_tests()
