from library import LibraryString
from unittest import main, TestCase

class MockPrinter(object):
    def print(self, msg):
        self.msg = msg

class TestLibraryString(TestCase):
    def setUp(self):
        self.lib = LibraryString(MockPrinter)
        self.lib._users.add('person1')

    def test_add_user(self):
        self.lib.add_user('person1')
        self.assertEqual(self.lib.printer.msg,
                         F'User not created, user with name person1 already exists.')
        self.lib.add_user('person2')
        self.assertEqual(self.lib.printer.msg,
                         F'User person2 created.')

    def test_add_book(self):
        self.lib.add_book('book1')
        self.assertEqual(self.lib.printer.msg,
                         F'Book book1 added. We have 1 coppies of the book.')
        self.lib.add_book('book1')
        self.assertEqual(self.lib.printer.msg,
                         F'Book book1 added. We have 2 coppies of the book.')

if __name__ == '__main__':
    main()
