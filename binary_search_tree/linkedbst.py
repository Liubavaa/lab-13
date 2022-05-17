"""
File: linkedbst.py
Author: Ken Lambert
"""

import copy
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from random import sample, shuffle
from time import time


class LinkedBST(AbstractCollection):
    """A link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if top.left is None and top.right is None:
                return 0
            elif top.left is None:
                return height1(top.right) + 1
            elif top.right is None:
                return height1(top.left) + 1
            return max(height1(top.left), height1(top.right)) + 1

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        return self.height() < (2 * log(self._size + 1, 2) - 1)

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        elements = list(self.inorder())
        return elements[elements.index(low):elements.index(high)+1]

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """

        def rebalance1(nodes):
            if nodes:
                mid = len(nodes)//2
                self.add(nodes[mid])
                rebalance1(nodes[:mid])
                rebalance1(nodes[mid+1:])

        lst = list(self.inorder())
        self.clear()
        rebalance1(lst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for i in self.inorder():
            if i > item:
                return i
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item: any
        :return:
        :rtype: BSTNode.data or None
        """
        stack = LinkedStack(self.inorder())
        while not stack.isEmpty():
            elem = stack.pop()
            if elem < item:
                return elem
        return None

    @staticmethod
    def make_simp_tree(words):
        """Make tree based on vocabulary"""
        tree_bst = LinkedBST()
        for word in words:
            tree_bst.add(word)
        return tree_bst

    @staticmethod
    def make_random_tree(words):
        """Make random tree"""
        new_words = copy.deepcopy(words)
        shuffle(new_words)
        return LinkedBST(new_words)

    @staticmethod
    def search_with_vocab(vocab: list, words):
        """Search words in vocabulary"""
        for word in words:
            vocab.index(word)

    @staticmethod
    def search_with_tree(tree, words):
        """Search words in tree"""
        for word in words:
            tree.find(word)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path: path to file with words
        :type path: str
        :return: nothing
        :rtype: None
        """
        with open(path, 'r', encoding='UTF-8') as words_f:
            words = [word.strip() for word in words_f.readlines()]
            random_words = sample(words, 10000)

            start = time()
            self.search_with_vocab(words, random_words)
            end = time()
            vocab_result = end-start

            simple_tree = self.make_simp_tree(words)
            start = time()
            self.search_with_tree(simple_tree, random_words)
            end = time()
            simp_tree_result = end - start

            random_tree = self.make_random_tree(words)
            start = time()
            self.search_with_tree(random_tree, random_words)
            end = time()
            random_tree_result = end - start

            random_tree.rebalance()
            balanced_tree = random_tree
            start = time()
            self.search_with_tree(balanced_tree, random_words)
            end = time()
            balanced_tree_result = end - start

            print("Search 10000 words with:   | time")
            print('--------------------------------------')
            print("Vocabulary:                |", round(vocab_result, 5))
            print("Simple tree:               |", round(simp_tree_result, 5))
            print("Random made tree:          |", round(random_tree_result, 5))
            print("Balanced tree:             |", round(balanced_tree_result, 5))
