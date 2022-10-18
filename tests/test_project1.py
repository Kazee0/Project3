import unittest
from pathlib import Path
import project1
from IO_file import read_instructions_from_file
from InstructionsProcess import *
from ElemetsInstance import *
import io
from contextlib import redirect_stdout

class MyTestCase(unittest.TestCase):
    def test_file(self):
        """Test the opening and reading of the given files."""
        path = Path('test.txt')
        self.assertEqual(read_instructions_from_file(path), ['PROPAGATE 1 2 750','PROPAGATE 2 3 1250'])
        path = Path('nothing.txt')
        self.assertEqual(str(read_instructions_from_file(path)),"[Errno 2] No such file or directory: 'nothing.txt'")

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
        device_1 = Device(1)
        self.assertEqual(device_1.show_id(), 1)
        self.assertEqual(device_1.situation, [])
        sit = Situation('ALERT', 'Trouble')
        device_1.add_situation(sit)
        self.assertEqual(device_1.situation[0].type, 'ALERT')
        self.assertEqual(device_1.situation[0].msg, 'Trouble')
        sit = Situation('ALERT', 'Trouble')
        try:
            device_1.add_situation(sit)
        except Exception as e:
            self.assertEqual(str(e), 'Duplicate Alerts with same message')
        device_1.handle_cancel('Trouble')
        self.assertEqual(device_1.situation, [])
        sit = Situation('ALERT', 'Trouble')
        device_1.add_situation(sit)
        sit = Situation('CANCEL', 'Trouble')
        device_1.add_situation(sit)
        self.assertEqual(device_1.situation, [])
        sit = Situation('CANCEL', 'Trouble')
        device_1.add_situation(sit)
        sit = Situation('ALERT', 'Trouble')
        device_1.add_situation(sit)
        self.assertEqual(device_1.situation, [])

    def test_PRO(self):
        """Test the propagate instance created."""
        pro = Propagate(0, 'ALERT', 1, 2)
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
    def test_File(self):
        b = read_instructions_from_file('ABC')
        self.assertEqual(str(b), "[Errno 2] No such file or directory: 'ABC'")



    def test_creation_devices(self):
        """Testing the device created successfully"""
        text_input=[
            'DEVICE 1',
            'DEVICE 22'
        ]
        out = project1.create_device(text_input)
        self.assertEqual(2, out[-1])
        self.assertEqual(1, out[0][0]._id)
        self.assertEqual(22, out[0][1]._id)

    def test_propagate(self):
        """Testing for receiving propagate"""
        device_1 = project1.Device(1)
        can = project1.Situation('CANCEL', 'HELP')
        device_1.add_situation(can)
        device_input = [project1.Device(2), device_1]
        time_input = 10
        temp_input = [project1.Propagate(10, [can], 1, 2)]
        try:
            out,b = project1.check_if_propagate(temp_input, time_input, device_input)
            self.assertEqual(out[0].situation[0].msg, 'HELP')
            self.assertEqual(out[0].situation[0].type, 'CANCEL')
        except SystemExit:
            pass

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
        a, b = create_device(text_input)
        with self.assertRaises(SystemExit) as c:
            project1.running_program(text_input, a, b)
        self.assertEqual(c.exception.code, None)

    def test_two_alerts(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'ALERT 2 AnotherOne 200',
        ]
        a,b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].type, 'ALERT')
            self.assertEqual(a[0].situation[0].msg, 'Trouble')
            self.assertEqual(a[1].situation[0].type, 'ALERT')
            self.assertEqual(a[1].situation[0].msg, 'AnotherOne')

    def test_two_alerts_greater(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 2 Trouble 200',
            'ALERT 1 AnotherOne 200',
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].type, 'ALERT')
            self.assertEqual(a[0].situation[0].msg, 'AnotherOne')
            self.assertEqual(a[1].situation[0].type, 'ALERT')
            self.assertEqual(a[1].situation[0].msg, 'Trouble')

    def test_two_same(self):
        text_input = ['DEVICE 8']
        inst_input = ['ALERT 8 ABC 10', 'CANCEL 8 NC 10']
        a, b = create_device(text_input)
        de_li = project1.two_at_same_time(inst_input, a, True)
        self.assertEqual(de_li[0].situation[0].type, 'CANCEL')
        self.assertEqual(de_li[0].situation[1].type, 'ALERT')
        text_input = ['DEVICE 8']
        inst_input = ['ALERT 8 NC 10', 'CANCEL 8 NC 10']
        a, b = create_device(text_input)
        de_li = project1.two_at_same_time(inst_input, a, True)
        self.assertEqual(de_li[0].situation, [])

    def test_two_at_same_time_differnt_cotnent(self):
        text_input = ['DEVICE 8', 'DEVICE 10']
        a, b = create_device(text_input)
        inst_input = ['ALERT 8 ABC 10', 'CANCEL 10 NC 10']
        de_li = project1.two_at_same_time(inst_input, a, False)
        a, b = create_device(text_input)
        self.assertEqual(de_li[0].situation[0].msg, 'ABC')
        self.assertEqual(de_li[1].situation[0].msg, 'NC')
        self.assertEqual(de_li[0].situation[0].type, 'ALERT')
        self.assertEqual(de_li[1].situation[0].type, 'CANCEL')
        inst_input = ['CANCEL 10 NC 10', 'ALERT 8 ABC 10']
        de_li = project1.two_at_same_time(inst_input, a, True)
        self.assertEqual(de_li[0].situation[0].msg, 'ABC')

    def test_running(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'ALERT 2 AnotherOne 500',
            'CANCEL 2 AnotherOne 600'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit as e:
            self.assertEqual(a[1].situation,[])

    def test_running_same_device_same_msg(self):
        text_input = [
            'DEVICE 2',
            'ALERT 2 AnotherOne 500',
            'CANCEL 2 AnotherOne 500'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation, [])

    def test_running_diff_device_same_time(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'ALERT 2 AnotherOne 200'
        ]
        # Two alerts first smaller
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'Trouble')
            self.assertEqual(a[1].situation[0].msg, 'AnotherOne')
    def test_same_time_first_greater(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 2 Trouble 200',
            'ALERT 1 AnotherOne 200'
        ]
        # Two Alerts first greater
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'AnotherOne')
            self.assertEqual(a[1].situation[0].msg, 'Trouble')
    def test_same_device_alerts(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'ALERT 1 AnotherOne 200',
            'CANCEL 2 AnotherOne 400',
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[1].situation[0].type, 'CANCEL')
    def test_two_cancel_dif_device(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'CANCEL 1 Trouble 200',
            'CANCEL 2 AnotherOne 200',
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'Trouble')
            self.assertEqual(a[1].situation[0].msg, 'AnotherOne')
    def test_same_device_first_greater(self):
        text_input = [
            'DEVICE 1',
            'CANCEL 1 BAJFIOQEO 200',
            'CANCEL 1 A 200',
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'A')

    def test_running_propagate(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'PROPAGATE 1 2 500'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[1].situation[0].msg, 'Trouble')
        
    def test_propagate_alert(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Trouble 200',
            'PROPAGATE 1 2 500'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[1].situation[0].msg, 'Trouble')

    def test_propagate_cancel(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'CANCEL 1 Trouble 200',
            'PROPAGATE 1 2 500'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[1].situation[0].msg, 'Trouble')

    def test_two_cancel_dif(self):
        text_input = [
            'DEVICE 1',
            'CANCEL 1 A 200',
            'CANCEL 1 AoooA 200'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'A')
            self.assertEqual(a[0].situation[1].msg, 'AoooA')

    def test_cancel_alert(self):
        text_input = [
            'DEVICE 1',
            'CANCEL 1 First 200',
            'ALERT 1 Second 200'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'First')
            self.assertEqual(a[0].situation[1].msg, 'Second')
    def test_two_alerts_same_time(self):
        text_input = [
            'DEVICE 1',
            'ALERT 1 First 200',
            'ALERT 1 Second 200'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[0].situation[0].msg, 'First')
            self.assertEqual(a[0].situation[1].msg, 'Second')

    def test_string_out(self):
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 Random 100',
            'PROPAGATE 1 2 Random 10',
            'CANCEL 1 Random 20'
        ]
        a, b = create_device(text_input)
        try:
            project1.running_program(text_input, a, b)
        except SystemExit:
            self.assertEqual(a[1].situation[0].msg, 'Random')
            self.assertEqual(a[0].situation, [])

    def test_standard_output(self):
        f = io.StringIO()
        text_input = [
            'DEVICE 1',
            'DEVICE 2',
            'ALERT 1 AnAlert 10',
            'PROPAGATE 1 2 AnAlert 10'
        ]
        a, b = create_device(text_input)
        with redirect_stdout(f):
            try:
                project1.running_program(text_input, a, b)
            except SystemExit:
                pass
        output = f.getvalue()
        self.assertEqual(output, '@11 #1: SENT ALERT TO #2: AnAlert\n@21 #2: RECEIVED ALERT FROM #1: AnAlert\n')

if __name__ == '__main__':
    unittest.main()