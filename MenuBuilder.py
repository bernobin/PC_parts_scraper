from typing import List
import json


class Menu:
    def __init__(self, name='Root', parent=None):
        self.name = name
        self.parent = parent
        self.children = {}

    def add(self, path: List):
        if not path:
            return

        if path[0] not in self.children:
            self.children[path[0]] = Menu(path[0], self)
        return self.children[path[0]].add(path[1:])

    def navigate(self):
        kids = [child for child in self.children.values()]
        if not kids:
            return self.path()

        for i, child in enumerate(kids):
            print(f"{i}:\t{child.name}")

        selection = None
        while selection not in range(len(kids)):
            selection = int(input('which menu you want?\n'))

        return kids[selection].navigate()

    def path(self, path=''):
        if self.parent:
            return self.parent.path(f"{self.name}/{path}")
        return f"/{path}"

    def __str__(self, level=0):
        indent = "  " * level  # Indentation for each level
        result = f"{indent}- {self.name}\n"
        for child in self.children.values():
            result += child.__str__(level + 1)
        return result


def build_menu():
    with open('menu.json', 'r') as f:
        links = json.load(f)

    menu = Menu()

    for link in links:
        path = link.split('/')
        menu.add(path[3:])

    return menu
