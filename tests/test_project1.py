import unittest
from pathlib import Path
from IO_file import read_instructions_from_file
from conflicts import find_conflict



class MyTestCase(unittest.TestCase):
    def test_file(self):
        """Test the opening and reading of the given files."""
        path = Path('test.txt')
        self.assertEqual(read_instructions_from_file(path), ['PROPAGATE 1 2 750','PROPAGATE 2 3 1250'])
        path = Path('nothing.txt')
        self.assertEqual(read_instructions_from_file(path),None)
    def test_the_conflicts(self):
        """Test the function of finding conflicts instructions."""
        text_input = [
            'ALERT 2 Trouble 100',
            'ALERT 3 Trouble 100',
            'CANCEL 1 OH 10'
        ]
        text_output = {
            '100': ['ALERT 2 Trouble 100','ALERT 3 Trouble 100'],
            '10':['CANCEL 1 OH 10']
        }
        self.assertEqual(find_conflict(text_input), text_output)


if __name__ == '__main__':
    unittest.main()