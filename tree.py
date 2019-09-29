# CS3210 - Principles of Programming Languages - Fall 2019
# A tree data-structure
# Author: Thyago Mota
# Contributors:
#   Casey Jones
#   Conor McCandless

from operator import itemgetter
from tree_format import format_tree
from termcolor import colored


class Tree:

    def __init__(self):
        self.data = None
        self.children = []

    @property
    def node(self):
        return (colored(self.data, 'blue')
                if self.children
                else colored(self.data, 'magenta'),
                [child.node
                 for child
                 in self.children])

    def add(self, child):
        self.children.append(child)

    def print(self):
        print(format_tree(self.node,
            format_node = itemgetter(0),
            get_children = itemgetter(1)))


if __name__ == "__main__":

    subtree = Tree()
    subtree.data = "F"
    subtree.add("E")
    subtree.add("+")
    subtree.add("T")

    tree = Tree()
    tree.data = "T"
    tree.add(subtree)
    tree.add("+")
    tree.add("T")

    tree.print()
