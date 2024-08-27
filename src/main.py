import shutil
import os
from copystatic import copy
from helpers import generate_page_recursive


def main():
    print("Deleting")
    if os.path.exists("/public"):
        shutil.rmtree("/public")
    copy("static/", "public/")
    generate_page_recursive(
        "content/", "template.html", "public/")


main()
