from bs4 import BeautifulSoup
from requester import Requester
from product import Product
from MenuBuilder import build_menu

from typing import List

# this will be json which includes products name /lookup, url, filters,
products = {}
# requires javascript to load the filters. Selenium Solution in seperate file perhaps
# (just to load filters and detrmine names)

# sorted asc
# ~pa means "price ascending"
# default is "popularity descending"
filters = {
    'Nvidia_GeForce_RTX_4070 SUPER': '?sfh=oi~ongff417x14%3Asv104433%2Bs~pa'
}


#class Menu:
#    def __init__(self, name='Root', parent=None):
#        self.name = name
#        self.parent = parent
#        self.children = {}
#
#    def add(self, path: List):
#        if not path:
#            return
#
#        if path[0] not in self.children:
#            self.children[path[0]] = Menu(path[0], self)
#        return self.children[path[0]].add(path[1:])
#
#    def navigate(self):
#        kids = [child for child in self.children.values()]
#        if not kids:
#            return self.path()
#
#        for i, child in enumerate(kids):
#            print(f"{i}:\t{child.name}")
#        selection = int(input('which menu you want?\n'))
#        return kids[selection].navigate()
#
#    def path(self, path=''):
#        if self.parent:
#            return self.parent.path(f"{self.name}/{path}")
#        return f"/{path}"
#
#    def __str__(self, level = 0):
#        indent = "  " * level  # Indentation for each level
#        result = f"{indent}- {self.name}\n"
#        for child in self.children.values():
#            result += child.__str__(level + 1)
#        return result

#def build_menu(soup):
#    links = soup.find_all('a')
#    menu = Menu()
#
#    for link in links:
#        tab = str(link.get('href'))
#        if '/produktsuche/' in tab:
#            path = tab.split('/')
#            menu.add(path[1:])
#
#    return menu


def main():
    requests_client = Requester()

    menu = build_menu()
    path = menu.navigate()

    r = requests_client.get_products_list(path)

    soup = BeautifulSoup(r.content, 'html5lib')

    print()

    results = soup.find_all('div', {'class': 'Plugin_Product'})
    for result in results:
        product = Product(result)

        print(product.link)
        print(product.name)
        print(product.price, 'CHF')


if __name__ == '__main__':
    main()
