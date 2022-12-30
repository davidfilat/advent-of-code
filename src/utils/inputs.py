import os


def read_inputs(filename: str) -> str:
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "../../inputs", filename)
    with open(filepath, "r") as f:
        text = f.read()
    return text.strip()
