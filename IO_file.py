from pathlib import Path

def read_instructions_from_file(path: Path) -> list[str]:
    """Takes input file path and returns a list of lines within the file.
    Takes in file for the given path.

    Returns:
        a list of instructions found in the file
    """
    try:
        instruction = []
        with open(path) as my_file:
            print('File Open')
            for line in my_file:
                if line.split(' ')[0] == 'CANCEL' or line.split(' ')[0] == 'PROPAGATE' or line.split(' ')[0] == 'ALERT' or line.split(' ')[0] == 'DEVICE':
                    instruction.append(line.strip('\n'))
            return instruction
    except FileNotFoundError:
        pass