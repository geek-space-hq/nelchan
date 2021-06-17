from pathlib import Path

nelchan_path = Path("./nelchan")
usecase_path = nelchan_path / "usecase"
template_path = Path("./scripts/templates")


def new_inputport(command_name, file_name):
    f = open(usecase_path / "inputport" / f"{file_name}_usecase.py", "a+")

    with open(template_path / "/usecase.py.template", "r") as tmpl:
        template = tmpl.read()

    f.write(template.format(name=command_name))
    f.close()


def new_outputport(command_name, file_name):
    f = open(usecase_path / "outputport" / f"{file_name}_outputport.py", "a+")

    with open(template_path / "/outputport.py.template", "r") as tmpl:
        template = tmpl.read()

    f.write(template.format(name=command_name))
    f.close()


def new_interactor(command_name, file_name):
    f = open(usecase_path / "interactor" / f"{file_name}_interactor.py", "a+")

    with open(template_path / "/interactor.py.template", "r") as tmpl:
        template = tmpl.read()

    f.write(template.format(name=command_name))
    f.close()


def new_presenter(command_name, file_name):
    f = open(usecase_path / "presenter" / f"{file_name}_presenter.py", "a+")

    with open(template_path / "/presenter.py.template", "r") as tmpl:
        template = tmpl.read()

    f.write(template.format(name=command_name))
    f.close()


if __name__ == "__main__":
    import sys

    command_name = sys.argv[1]
    file_name = sys.argv[2]

    new_inputport(command_name, file_name)
    new_interactor(command_name, file_name)
    new_outputport(command_name, file_name)
    new_presenter(command_name, file_name)
