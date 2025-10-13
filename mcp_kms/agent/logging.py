import pprint
import pathlib

def save_log(text: dict):
    file_path = pathlib.Path(__file__).parent.parent.parent
    file_name = "result.txt"
    file_path = file_path / file_name
    with open(file=str(file_path), mode="w") as f:
        printer = pprint.PrettyPrinter(stream=f, indent=4)
        printer.pprint(text)