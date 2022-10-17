from pathlib import Path
from IO_file import read_instructions_from_file
from InstructionsProcess import *
import sys
from ElemetsInstance import *


def _read_input_file_path() -> Path:
    # This function cannot be tested as no way to put input in shell from test
    """Reads the input file path from the standard input"""
    return Path(input())


def check_if_propagate(temp: list[Propagate], time_counter: int, device: list[Device]) -> (
        list[Device], list[Propagate]):
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


def only_one_instruction(to_do: list[str], device: list[Device]) -> list[Device]:
    """
    This executes the situation where there is only one instruction at a given time.
    """
    if to_do[0].split(' ')[0] == 'ALERT':
        for z in device:
            if z.show_id() == int(to_do[0].split(' ')[1]):
                print('ALERT when single')
                con = Situation('ALERT', to_do[0].split(' ')[-2])
                z.add_situation(con)
    elif to_do[0].split(' ')[0] == 'CANCEL':
        for z in device:
            if z.show_id() == int(to_do[0].split(' ')[1]):
                print('CANCEL when single ')
                z.handle_cancel(to_do[0].split(' ')[-2])
    return device


def two_at_same_time(to_do: list[str], device: list[Device], reverse: bool) -> list[Device]:
    """Handles two instructions that are scheduled at the same time."""
    if reverse:
        num_1 = 0
        num_2 = 1
    else:
        num_1 = 1
        num_2 = 0
    if int(to_do[0].split(' ')[1]) == int(to_do[1].split(' ')[1]):
        # Two instructions sent to same DEVICE
        if to_do[0].split(' ')[-2] == to_do[1].split(' ')[-2]:
            # Same message and to same device
            pass
        else:
            # Different message
            for z in device:
                if z.show_id() == int(to_do[num_1].split(' ')[1]):
                    z.handle_cancel(to_do[num_1].split(' ')[-2])
                    con = Situation('ALERT', to_do[num_2].split(' ')[2])
                    z.add_situation(con)
    else:
        for z in device:
            if z.show_id() == int(to_do[num_1].split(' ')[1]):
                print('CANCEL')
                z.handle_cancel(to_do[num_1].split(' ')[-2])
            if z.show_id() == int(to_do[num_2].split(' ')[1]):
                print('ALERT')
                con = Situation('ALERT', to_do[num_2].split(' ')[2])
                z.add_situation(con)
    return device


def check_number_propagate(inst: list[str]) -> int:
    """
    Look for number of propagate instances need to do
    """
    num = 0
    for i in inst:
        if i.split(' ')[0] == 'PROPAGATE':
            num += 1
    return num


def running_program(inst: list[str], device: list[Device], log_ins: int):
    """Main function to run the entire program"""
    time_counter = 0
    temp = []
    temp_1 = []
    propagate_runned = 0
    x = None
    store = []
    other_instruction = find_conflict(inst)
    for i in other_instruction.keys():
        store.append(int(i))
    max_time = max(store)
    needed = check_number_propagate(inst)
    while True:
        # Process Propagation
        device, temp_1 = check_if_propagate(temp, time_counter, device)
        if time_counter > max_time and not temp_1 and propagate_runned >= needed:
            sys.exit()
        try:
            time_to_do = time_counter
            if inst[log_ins].split(' ')[0] == 'PROPAGATE':
                propagate_runned += 1
                # Send cancel/alert to the receiving device.
                print("sending message")
                org = inst[log_ins].split(' ')[1]
                dest = inst[log_ins].split(' ')[2]
                time_to_do = time_counter + int(inst[log_ins].split(' ')[-1])
                for z in device:
                    if z.show_id() == int(org):
                        x = z.situation
                l1 = Propagate(time_to_do, x, int(org), int(dest))
                temp_1.append(l1)
                for d in x:
                    if d.type == 'CANCEL':
                        print("@{} #{}: SENT CANCELLATION TO #{}: {}".format(time_counter, org, dest, d.msg))
                    if d.type == 'ALERT':
                        print(
                            "@{} #{}: SENT ALERT TO #{}: {}".format(time_counter, org, dest, d.msg))
                log_ins += 1
        except IndexError:
            pass
        if str(time_counter) in other_instruction.keys():
            # In Which alert and cancel are processed.
            to_do = other_instruction[str(time_counter)]
            if len(to_do) == 1:
                log_ins += 1
                device = only_one_instruction(to_do, device)
            if len(to_do) > 1:
                log_ins += len(to_do)
                # Multiple actions at the same time.
                if to_do[0].split(' ')[0] == 'CANCEL' and to_do[1].split(' ')[0] == 'ALERT':
                    device = two_at_same_time(to_do, device, True)
                elif to_do[0].split(' ')[0] == 'ALERT' and to_do[1].split(' ')[0] == 'CANCEL':
                    device = two_at_same_time(to_do, device, False)

                if to_do[0].split(' ')[0] == 'ALERT' and to_do[1].split(' ')[0] == 'ALERT':
                    if int(to_do[0].split(' ')[1]) > int(to_do[1].split(' ')[1]):
                        print('Greater')
                        # Command For First Device Greater
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                con = Situation('ALERT', to_do[1].split(' ')[2])
                                z.add_situation(con)
                        for z in device:
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                con = Situation('ALERT', to_do[0].split(' ')[2])
                                z.add_situation(con)
                    elif int(to_do[0].split(' ')[1]) < int(to_do[1].split(' ')[1]):
                        print('smaller')
                        # Command For First Device Smaller
                        for z in device:
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                con = Situation('ALERT', to_do[0].split(' ')[2])
                                z.add_situation(con)
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                con = Situation('ALERT', to_do[1].split(' ')[2])
                                z.add_situation(con)
                    elif int(to_do[0].split(' ')[1]) == int(to_do[1].split(' ')[1]):
                        # Same id
                        if to_do[0].split(' ')[2] < to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    con = Situation('ALERT', to_do[0].split(' ')[2])
                                    z.add_situation(con)
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    con = Situation('ALERT', to_do[1].split(' ')[2])
                                    z.add_situation(con)
                        else:
                            for z in device:
                                if z.show_id() == int(to_do[1].split(' ')[1]):
                                    con = Situation('ALERT', to_do[1].split(' ')[2])
                                    z.add_situation(con)
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    con = Situation('ALERT', to_do[0].split(' ')[2])
                                    z.add_situation(con)
                    log_ins += 1
                elif to_do[0].split(' ')[0] == 'CANCEL' and to_do[1].split(' ')[0] == 'CANCEL':
                    if int(to_do[1].split(' ')[1]) == int(to_do[0].split(' ')[1]):
                        # Two cancel have same ID
                        if to_do[0].split(' ')[2] < to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    z.handle_cancel(to_do[0].split(' ')[-2])
                                    z.handle_cancel(to_do[1].split(' ')[-2])
                        elif to_do[0].split(' ')[2] > to_do[1].split(' ')[2]:
                            for z in device:
                                if z.show_id() == int(to_do[0].split(' ')[1]):
                                    z.handle_cancel(to_do[1].split(' ')[-2])
                                    z.handle_cancel(to_do[0].split(' ')[-2])
                    else:
                        for z in device:
                            if z.show_id() == int(to_do[1].split(' ')[1]):
                                z.handle_cancel(to_do[1].split(' ')[-2])
                            if z.show_id() == int(to_do[0].split(' ')[1]):
                                z.handle_cancel(to_do[0].split(' ')[-2])
        time_counter += 1


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    inst = read_instructions_from_file(input_file_path)
    device_1, inst_log = create_device(inst)
    running_program(inst, device_1, inst_log)


if __name__ == '__main__':
    main()
