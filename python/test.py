import unittest
from python import main
from pprint import pprint

class TestConfigparser(unittest.TestCase):
    def test_integration(self):
        teststring = """
# this is a comment

# simple 
default:
    a = "test"
    b = "something"

somename = "something"
somenamespace:
    a = 42
    b = "test"
    c = 3.14159265
    d = [1,2,3]
    e = {"a": "b", "c": "d"} # discouraged but allowed.
    
    # preferred
    f:
        a = "b"
        c = "d"
    
    g = None
    h = False
    i = True
    
    tester:
        extends default
        a = "b"
        
    # hexadecimal also works!
    j = 0x15
    # prefixed zeros don't matter
    k = 0x015
    # even octal works!
    l = 0o123
    # and binary
    m = 0b1010
    
    # scientific notation
    n = 1e10

"""
        res = main.loads(teststring)
        pprint(res)

        self.assertEqual(res, {
            'default': {'a': 'test', 'b': 'something'},
            'somename': 'something',
            'somenamespace': {
                'a': 42,
                'b': 'test',
                'c': 3.14159265,
                'd': [1, 2, 3],
                'e': {'a': 'b', 'c': 'd'},
                'f': {'a': 'b', 'c': 'd'},
                'g': None,
                'h': False,
                'i': False,
                'j': 21,
                'k': 21,
                'l': 83,
                'm': 10,
                'n': 1e10,
                'tester': {'a': 'b', 'b': 'something'}
            }
        })


if __name__ == '__main__':
    unittest.main()
