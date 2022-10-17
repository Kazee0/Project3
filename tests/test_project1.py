import unittest
from pathlib import Path
import project1
from IO_file import read_instructions_from_file
from InstructionsProcess import *


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
        """Test for the function of Situation."""
        inst = project1.Situation('CANCEL', 'Trouble')
        self.assertEqual(inst.type, 'CANCEL')
        self.assertEqual(inst.msg, 'Trouble')

    def test_DEVICE(self):
        """Test device instance created as expected."""
        device_1 = project1.Device(1)
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
        pro = project1.Device(1)
        alert = project1.Situation('ALERT', 'HELP')
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
        """Testing the device created successfully"""
        text_input=[
            'DEVICE 1',
            'DEVICE 22'
        ]
        out = project1.create_device(text_input)
        self.assertEqual(2, out[-1])
        self.assertEqual(1, out[0][0]._ID)
        self.assertEqual(22, out[0][1]._ID)

    def test_propagate(self):
        """Testing for receiving propagate"""
        device_1 = project1.Device(1)
        can = project1.Situation('CANCEL', 'HELP')
        device_1.add_situation(can)
        device_input = [project1.Device(2), device_1]
        time_input = 10
        temp_input = [project1.PROPAGATE(10, [can], 1, 2)]
        with self.assertRaises(SystemExit) as c:
            out = project1.check_if_propagate(temp_input, time_input, device_input)
            self.assertEqual(out[0].Situation[0].msg, 'HELP')
            self.assertEqual(out[0].Situation[0].type, 'CANCEL')
        self.assertEqual(c.exception.code, None)

    def test_only_one(self):
        to_do_input = ['ALERT 1 ABC 100']
        device_1 = project1.Device(1)
        out = project1.only_one_instruction(to_do_input, [device_1])
        situation_out = out[0].situation[0]
        self.assertEqual(out[0].situation[0].msg, 'ABC')
        self.assertEqual(out[0].situation[0].type, 'ALERT')
        to_do_input = ['CANCEL 1 ABC 100']
        device_1 = project1.Device(1)
        out = project1.only_one_instruction(to_do_input, [device_1])
        situation_out = out[0].situation[0]
        self.assertEqual(out[0].situation[0].msg, 'ABC')
        self.assertEqual(out[0].situation[0].type, 'CANCEL')

    def test_single_alert_time(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
        ]
        with self.assertRaises(SystemExit) as c:
            project1.running_program(text_input)
        self.assertEqual(c.exception.code, None)

    def test_two_alerts(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'ALERT 2 AnotherOne 200',
        ]
        a,b = create_device(text_input)
        with self.assertRaises(SystemExit) as c:
            project1.running_program(text_input, a, b)
            self.assertEqual(a[0].situation[0].type, 'ALERT')
            self.assertEqual(a[0].situation[0].msg, 'Trouble')
            self.assertEqual(a[1].situation[0].type, 'ALERT')
            self.assertEqual(a[1].situation[0].msg, 'AnotherOne')
        self.assertEqual(c.exception.code, None)

    def test_two_alerts_greater(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 2 Trouble 200',
            'ALERT 1 AnotherOne 200',
        ]
        a,b = create_device(text_input)
        with self.assertRaises(SystemExit) as c:
            project1.running_program(text_input, a, b)
            self.assertEqual(a[0].situation[0].type, 'ALERT')
            self.assertEqual(a[0].situation[0].msg, 'Trouble')
            self.assertEqual(a[1].situation[0].type, 'ALERT')
            self.assertEqual(a[1].situation[0].msg, 'AnotherOne')
        self.assertEqual(c.exception.code, None)




if __name__ == '__main__':
    unittest.main()