import unittest
from pathlib import Path
from IO_file import read_instructions_from_file
class MyTestCase(unittest.TestCase):
    def test_file(self):
        """Test the opening and reading of the given files."""
        path = Path('test.txt')
        self.assertEqual(read_instructions_from_file(path), ['PROPAGATE 1 2 750','PROPAGATE 2 3 1250'])
        path = Path('nothing.txt')
        self.assertEqual(read_instructions_from_file(path),None)
if __name__ == '__main__':
    unittest.main()