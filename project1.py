from pathlib import Path


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

def check_if_PROPAGATE(temp, time_counter, device):
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
            exit()
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


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()


if __name__ == '__main__':
    main()
