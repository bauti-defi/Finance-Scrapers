import pathlib

directory = pathlib.Path(__file__).parent.absolute()

# modes: append = a | overwrite = w
def save(file, data, mode):
    with open(f"{directory}/data/{file}", mode) as dump:
        dump.write(data)