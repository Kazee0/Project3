from ElemetsInstance import Device


def find_conflict(inst: list[str]) -> dict[str]:
    """This is a function that takes in the instruction and find instructions that take place at the same time.

    Returns:
        a dictionary with keys being the time for instruction and contents being the list of instructions schedule at that time.
    """
    trained = {}
    for i in inst:
        if i.split()[0] == 'CANCEL' or i.split()[0] == 'ALERT':
            if i.split()[-1] not in trained.keys():
                li = []
                trained[i.split(' ')[-1]] = []
                trained[i.split(' ')[-1]].append(i)
            else:
                trained[i.split(' ')[-1]].append(i)
    return trained


def create_device(inst: list[str]) -> tuple[list[Device], int]:
    """Takes in instructions and finds all that creates a device.
    Create the DEVICE instance using the instructions.

    Returns:
        the list of devices and the log of instructions carried.
    """
    device = []
    inst_log = 0
    for i in range(len(inst)):
        if inst[i].split(' ')[0] == 'DEVICE':
            device.append(Device(int(inst[i].split()[1])))
            inst_log += 1
    return device, inst_log
