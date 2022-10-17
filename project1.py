from pathlib import Path
from IO_file import read_instructions_from_file
from conflicts import find_conflict
import sys

class situation:
    """Contain situation to store

    variables:
        self.type: str, can be 'CANCEL' or 'ALERT'
        self.msg: str, that contains the message of alert or cancel
    """
    def __init__(self, types, msg):
        self.type = types
        self.msg = msg

class DEVICE:
    """Module of the devices

    functions:
        add_situation: adding situation to device log
        show_id: returns device ID
        handle_cancel: receive the message of alert to be canceled and delete that from log
    """
    def __init__(self, ID):
        self._ID = ID
        self.situation = []
    def add_situation(self, sit):
        self.situation.append(sit)
    def show_id(self):
        return self._ID

    def handle_cancel(self, msg):
        flag = False
        for i in range(len(self.situation)):
            if self.situation[i].msg == msg:
                self.situation.pop(i)
                flag = True
        if not flag:
            si = situation('CANCEL', msg)
            self.add_situation(si)

class PROPAGATE:
    """An module that contains the propagation

    variables:
        self.type: contains if the information is cancellation or alert
        self.time: int that contains the time to receive the message
        self.from_ID: int that contains the ID of the sending device
        self.to_ID: int that contains the ID of receiving device
    """
    def __init__(self, time, types, from_ID, to_ID):
        self.type = types
        self.time = time
        self.from_ID = from_ID
        self.to_ID = to_ID

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def check_if_PROPAGATE(temp: list[PROPAGATE], time_counter: int, device:list[DEVICE]) -> (list[DEVICE], list[PROPAGATE]):
    """Function that handles the propagate instruction and check if it needs to process"""
    x = None
    if temp:
        # Handel the receiving of message
        for i in temp:
            if i.time == time_counter:
                device_from, device_to, situations = i.from_ID, i.to_ID, i.type
                for s in situations:
                    if s.type == 'ALERT':
                        for z in device:
                            if z.show_id() == int(device_to):
                                z.add_situation(s)
                                print("@{} #{}: RECEIVED ALERT FROM #{}: {}".format(time_counter,
                                                                                    device_to,
                                                                                    device_from,
                                                                                    s.msg))
                    if s.type == 'CANCEL':
                        for z in device:
                            if z.show_id() == int(device_to):
                                z.handle_cancel(s.msg)
                                print("@{} #{}: RECEIVED CANCELLATION FROM #{}: {}".format(
                                    time_counter, device_to, device_from, s.msg))
                temp.remove(i)
        if not temp:
            sys.exit()
    return device, temp

def create_DEVICE(inst: list[str]) -> tuple[list[DEVICE], int]:
    """Takes in instructions and finds all that creates a device.
    Create the DEVICE instance using the instructions.

    Returns:
        the list of devices and the log of instructions carried.
    """
    device = []
    inst_log = 0
    for i in range(len(inst)):
        if inst[i].split(' ')[0] == 'DEVICE':
            device.append(DEVICE(int(inst[i].split()[1])))
            inst_log += 1
    return device, inst_log

def only_one_instruction(to_do, device):
    if to_do[0].split(' ')[0] == 'ALERT':
        for z in device:
            if z.show_id() == int(to_do[0].split(' ')[1]):
                print('ALERT when single')
                con = situation('ALERT', to_do[0].split(' ')[-2])
                z.add_situation(con)
    elif to_do[0].split(' ')[0] == 'CANCEL':
        for z in device:
            if z.show_id() == int(to_do[0].split(' ')[1]):
                print('CANCEL when single ')
                z.handle_cancel(to_do[0].split(' ')[-2])
    return device

def running_program(inst: list[str]):
    time_counter = 0
    temp = []
    x = None
    other_instruction = find_conflict(inst)
    device, inst_log = create_DEVICE(inst)
    while True:
        #Process Propagation
        device, temp = check_if_PROPAGATE(temp, time_counter, device)
        try:
            time_to_do = time_counter
            if inst[inst_log].split(' ')[0] == 'PROPAGATE':
                #Send cancel/alert to the receiving device.
                print("sending message")
                org = inst[inst_log].split(' ')[1]
                dest = inst[inst_log].split(' ')[2]
                time_to_do = time_counter + int(inst[inst_log].split(' ')[-1])
                for z in device:
                    if z.show_id() == int(org):
                        x = z.situation
                l1 = PROPAGATE(time_to_do,x,int(org),int(dest))
                for d in x:
                    if d.type == 'CANCEL':
                        print("@{} #{}: SENT CANCELLATION TO #{}: {}".format(time_counter, org, dest, d.msg))
                    if d.type == 'ALERT':
                        print(
                            "@{} #{}: SENT ALERT TO #{}: {}".format(time_counter, org, dest, d.msg))
                temp.append(l1)
                inst_log +=1
        except IndexError:
            pass
        if str(time_counter) in other_instruction.keys():
            #In Which alert and cancel are processed.
            to_do = other_instruction[str(time_counter)]
            if len(to_do) == 1:
                inst_log += 1
                device = only_one_instruction(to_do, device)
            if len(to_do) > 1:
                inst_log += len(to_do)
                # Multiple actions at the same time.
                if to_do[0].split(' ')[0] == 'CANCEL' and to_do[1].split(' ')[0] == 'ALERT':
                    if int(to_do[0].split(' ')[1]) == int(to_do[1].split(' ')[1]):
                        # Two instructions sent to same DEVICE
                        if to_do[0].split(' ')[-2] == to_do[1].split(' ')[-2]:
                            # Same message
                            pass
                        else:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    print('CANCEL')
                                    z.handle_cancel(to_do[0].split(' ')[-2])
                                    con = situation('ALERT', to_do[1].split(' ')[2])
                                    z.add_situation(con)
                    else:
                        for z in device:
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                print('CANCEL')
                                z.handle_cancel(to_do[0].split(' ')[-2])
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                print('ALERT')
                                con = situation('ALERT', to_do[1].split(' ')[2])
                                z.add_situation(con)
                                z.handle_cancel(to_do[0].split(' ')[-2])
                elif to_do[0].split(' ')[0] == 'ALERT' and to_do[1].split(' ')[0] == 'CANCEL':
                    if int(to_do[1].split(' ')[1]) == int(to_do[1].split(' ')[1]):
                        # Two instructions sent to same DEVICE
                        if to_do[1].split(' ')[-2] == to_do[1].split(' ')[-2]:
                            # Same message
                            inst_log += 1
                        else:
                            for z in device:
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    print('CANCEL')
                                    z.handle_cancel(to_do[1].split(' ')[-2])
                                    con = situation('ALERT', to_do[0].split(' ')[2])
                                    z.add_situation(con)
                    else:
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                print('CANCEL')
                                z.handle_cancel(to_do[1].split(' ')[-2])
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                print('ALERT')
                                con = situation('ALERT', to_do[0].split(' ')[2])
                                z.add_situation(con)
                                z.handle_cancel(to_do[1].split(' ')[-2])

                if to_do[0].split(' ')[0] == 'ALERT' and to_do[1].split(' ')[0] == 'ALERT':
                    print('Multiple alerts detected.')
                    if int(to_do[0].split(' ')[1]) > int(to_do[1].split(' ')[1]):
                        print('Greater')
                        # Command For First Device Greater
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                con = situation('ALERT', to_do[1].split(' ')[2])
                                z.add_situation(con)
                        for z in device:
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                print("ALERT")
                                con = situation('ALERT', to_do[0].split(' ')[2])
                                z.add_situation(con)
                    elif int(to_do[0].split(' ')[1]) < int(to_do[1].split(' ')[1]):
                        print('smaller')
                        # Command For First Device Smaller
                        for z in device:
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                print("ALERT")
                                con = situation('ALERT', to_do[0].split(' ')[2])
                                z.add_situation(con)
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                print("ALERT")
                                con = situation('ALERT', to_do[1].split(' ')[2])
                                z.add_situation(con)
                    elif int(to_do[0].split(' ')[1]) == int(to_do[1].split(' ')[1]):
                        # Same id
                        if to_do[0].split(' ')[2] < to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    print("ALERT")
                                    con = situation('ALERT', to_do[0].split(' ')[2])
                                    z.add_situation(con)
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    print("ALERT")
                                    con = situation('ALERT', to_do[1].split(' ')[2])
                                    z.add_situation(con)
                        else:
                            for z in device:
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    print("ALERT")
                                    con = situation('ALERT', to_do[1].split(' ')[2])
                                    z.add_situation(con)
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    print("ALERT")
                                    con = situation('ALERT', to_do[0].split(' ')[2])
                                    z.add_situation(con)
                    inst_log += 1
                elif to_do[0].split(' ')[0] == 'CANCEL' and to_do[1].split(' ')[0] == 'CANCEL':
                    if to_do[1].split(' ')[2] == to_do[0].split(' ')[2]:
                        if to_do[0].split(' ')[2] < to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    print('CANCEL')
                                    z.handle_cancel(to_do[0].split(' ')[-2])
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    z.handle_cancel(to_do[1].split(' ')[-2])
                        if to_do[0].split(' ')[2] > to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    print('CANCEL')
                                    z.handle_cancel(to_do[1].split(' ')[-2])
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    z.handle_cancel(to_do[0].split(' ')[-2])
                    else:
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                print('CANCEL')
                                z.handle_cancel(to_do[1].split(' ')[-2])
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                z.handle_cancel(to_do[0].split(' ')[-2])
        time_counter += 1



def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    inst = read_instructions_from_file(input_file_path)
    running_program(inst)


if __name__ == '__main__':
    main()
