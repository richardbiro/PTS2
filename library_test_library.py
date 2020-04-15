from library import *
from unittest import main, TestCase

class MockReservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(self._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_

    def overlapping(self, other):
        return (self._book == other._book
                and self._to >= other._from)

    def includes(self, date):
        return (self._from <= date <= self._to)

    def identify(self, date, book, for_):
        return (book == self._book
                and for_ == self._for
                and self.includes(date))   

    def change_for(self, for_):
        self._for = for_



class TestLibrary(TestCase):
    def setUp(self):
        MockReservation._ids = count(0)
        self.lib = Library()
        self.lib._users.add('person1')
        self.lib._users.add('person2')
        self.lib._users.add('person3')
        self.lib._books['book1'] = 1
        self.lib._books['book2'] = 2
        self.lib._books['book3'] = 3
        self.lib.reserve_book('person1','book1',0,2,MockReservation)
        self.lib.reserve_book('person2','book2',0,3,MockReservation)
        self.lib.reserve_book('person3','book2',1,3,MockReservation)
        self.lib.reserve_book('person1','book3',4,5,MockReservation)
        self.lib.reserve_book('person3','book3',4,7,MockReservation)
        

    def test_add_user_same(self):
        self.assertFalse(self.lib.add_user('person1'))
        self.assertFalse(self.lib.add_user('person2'))
        self.assertFalse(self.lib.add_user('person3'))

    def test_add_user_different(self):
        self.assertTrue(self.lib.add_user('person4'))

        

    def test_add_book_same(self):
        self.lib.add_book('book1')
        self.assertEqual(self.lib._books['book1'], 2)
        self.lib.add_book('book2')
        self.assertEqual(self.lib._books['book2'], 3)
        self.lib.add_book('book3')
        self.assertEqual(self.lib._books['book3'], 4)

    def test_add_book_different(self):
        self.lib.add_book('book4')
        self.assertEqual(self.lib._books['book4'], 1)

        

    def test_reserve_book_wrong_user(self):
        self.assertFalse(self.lib.reserve_book('person4','book1',0,2,MockReservation))
        self.assertFalse(self.lib.reserve_book('person5','book2',3,3,MockReservation))

    def test_reserve_book_wrong_date_format(self):
        self.assertFalse(self.lib.reserve_book('person1','book1',2,1,MockReservation))
        self.assertFalse(self.lib.reserve_book('person2','book2',3,1,MockReservation))

    def test_reserve_book_wrong_book(self):
        self.assertFalse(self.lib.reserve_book('person1','book4',0,2,MockReservation))
        self.assertFalse(self.lib.reserve_book('person2','book5',0,2,MockReservation))

    def test_reserve_book_not_enough_books(self):
        self.assertFalse(self.lib.reserve_book('person2','book1',1,2,MockReservation))
        self.assertFalse(self.lib.reserve_book('person1','book2',3,3,MockReservation))

    def test_reserve_book_correct(self):
        self.assertTrue(self.lib.reserve_book('person1','book1',3,8,MockReservation))
        self.assertTrue(self.lib.reserve_book('person2','book3',3,6,MockReservation))
        self.assertTrue(self.lib.reserve_book('person1','book3',6,7,MockReservation))
        self.assertTrue(self.lib.reserve_book('person3','book2',0,0,MockReservation))



    def test_check_reservation_doesnt_exist_wrong_user(self):
        self.assertFalse(self.lib.check_reservation('person1','book2',1))
        self.assertFalse(self.lib.check_reservation('person2','book3',5))

    def test_check_reservation_doesnt_exist_wrong_book(self):
        self.assertFalse(self.lib.check_reservation('person1','book3',1))
        self.assertFalse(self.lib.check_reservation('person3','book2',4))

    def test_check_reservation_doesnt_exist_wrong_date(self):
        self.assertFalse(self.lib.check_reservation('person1','book1',3))
        self.assertFalse(self.lib.check_reservation('person3','book2',0))

    def test_check_reservation_exists(self):
        self.assertTrue(self.lib.check_reservation('person1','book1',0))
        self.assertTrue(self.lib.check_reservation('person2','book2',2))
        self.assertTrue(self.lib.check_reservation('person3','book3',7))



    def test_change_reservation_wrong_new_user(self):
        self.assertFalse(self.lib.change_reservation('person1','book1',1,'person4'))
        self.assertFalse(self.lib.change_reservation('person2','book2',1,'person5'))

    def test_change_reservation_wrong_user_in_reservation(self):
        self.assertFalse(self.lib.change_reservation('person1','book2',1,'person2'))
        self.assertFalse(self.lib.change_reservation('person2','book3',5,'person3'))

    def test_change_reservation_wrong_book_in_reservation(self):
        self.assertFalse(self.lib.change_reservation('person1','book3',1,'person2'))
        self.assertFalse(self.lib.change_reservation('person3','book2',4,'person2'))

    def test_change_reservation_wrong_date_in_reservation(self):
        self.assertFalse(self.lib.change_reservation('person1','book1',3,'person3'))
        self.assertFalse(self.lib.change_reservation('person3','book2',0,'person1'))

    def test_change_reservation_correct(self):
        self.assertTrue(self.lib.change_reservation('person1','book1',0,'person2'))
        self.assertTrue(self.lib.change_reservation('person2','book2',2,'person1'))
        self.assertTrue(self.lib.change_reservation('person3','book3',7,'person1'))


if __name__ == '__main__':
    main()
