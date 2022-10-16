import unittest
from pathlib import Path
import project1
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
    def test_situation_object(self):
        """Test for the function of situation."""
        inst = project1.situation('CANCEL', 'Trouble')
        self.assertEqual(inst.type, 'CANCEL')
        self.assertEqual(inst.msg, 'Trouble')
    def test_DEVICE(self):
        """Test device instance created as expected."""
        device_1 = project1.DEVICE(1)
        self.assertEqual(device_1.show_id(), 1)
        self.assertEqual(device_1.situation, [])
    def test_PRO(self):
        """Test the propagate instance created."""
        pro = project1.PROPAGATE(0, 'ALERT', 1, 2)
        self.assertEqual(pro.type, 'ALERT')
        self.assertEqual(pro.time, 0)
        self.assertEqual(pro.from_ID, 1)
        self.assertEqual(pro.to_ID, 2)
    def test_alert_cancel(self):
        """Testing the device can handle the instructions"""
        pro = project1.DEVICE(1)
        alert = project1.situation('ALERT', 'HELP')
        pro.add_situation(alert)
        self.assertEqual(pro.situation[0].type, 'ALERT')
        self.assertEqual(pro.situation[0].msg, 'HELP')
        pro.handle_cancel('HELP')
        self.assertEqual(pro.situation, [])
        pro.handle_cancel('ANOTHER HELP')
        #Testing if program can store the cancel instruction
        self.assertEqual(pro.situation[0].type, 'CANCEL')
        self.assertEqual(pro.situation[0].msg, 'ANOTHER HELP')
    def test_creation_devices(self):
        text_input=[
            'DEVICE 1',
            'DEVICE 22'
        ]
        out = project1.create_DEVICE(text_input)
        self.assertEqual(2, out[-1])
        self.assertEqual(1, out[0][0]._ID)
        self.assertEqual(22, out[0][1]._ID)




if __name__ == '__main__':
    unittest.main()