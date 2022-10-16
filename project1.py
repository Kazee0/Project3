from pathlib import Path


class situation:
    def __init__(self, types, msg):
        self.type = types
        self.msg = msg

class DEVICE:
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
    def __init__(self, time, types, from_ID, to_ID):
        self.type = types
        self.time = time
        self.from_ID = from_ID
        self.to_ID = to_ID

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()


if __name__ == '__main__':
    main()
