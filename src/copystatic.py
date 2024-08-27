import shutil
import os


def copy(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    nodes = os.listdir(source)
    for node in nodes:
        if os.path.isfile(f"{source}/{node}"):
            shutil.copy(f"{source}/{node}", destination)
        else:
            copy(f"{source}/{node}", f"{destination}/{node}")


def main():
    copy("static/", "public/")
