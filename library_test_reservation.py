from library import Reservation
from unittest import main, TestCase


class TestReservation(TestCase):
    def setUp(self):
        self.res1 = Reservation(0, 3, 'book1', 'person1')
        self.res2 = Reservation(0, 5, 'book2', 'person2')
        self.res3 = Reservation(2, 4, 'book2', 'person3')
        self.res4 = Reservation(2, 9, 'book2', 'person2')
        self.res5 = Reservation(3, 9, 'book1', 'person3')
        self.res6 = Reservation(4, 7, 'book3', 'person4')
        self.res7 = Reservation(5, 8, 'book2', 'person3')
        self.res8 = Reservation(7, 10, 'book3', 'person4')
        self.res9 = Reservation(8, 8, 'book1', 'person2')
        
        

    def test_overlap_full_same_book(self):
        self.assertTrue(self.res2.overlapping(self.res3))
        self.assertTrue(self.res4.overlapping(self.res7))

    def test_overlap_partial_same_book(self):
        self.assertTrue(self.res1.overlapping(self.res5))
        self.assertTrue(self.res6.overlapping(self.res8))
    
    def test_overlap_none_same_book(self):
        self.assertFalse(self.res1.overlapping(self.res9))
        self.assertFalse(self.res3.overlapping(self.res7))

    def test_overlap_full_different_book(self):
        self.assertFalse(self.res1.overlapping(self.res2))
        self.assertFalse(self.res8.overlapping(self.res9))

    def test_overlap_partial_different_book(self):
        self.assertFalse(self.res3.overlapping(self.res6))
        self.assertFalse(self.res7.overlapping(self.res8))

    def test_overlap_none_different_book(self):
        self.assertFalse(self.res1.overlapping(self.res6))
        self.assertFalse(self.res2.overlapping(self.res8))
        


    def test_include_only_date(self):
        self.assertTrue(self.res9.includes(8))
        
    def test_include_sooner_date(self):
        self.assertFalse(self.res3.includes(0))
        self.assertFalse(self.res8.includes(6))
    
    def test_include_correct_date(self):
        self.assertTrue(self.res2.includes(5))
        self.assertTrue(self.res6.includes(4))
        self.assertTrue(self.res3.includes(3))

    def test_include_later_date(self):
        self.assertFalse(self.res4.includes(10))
        self.assertFalse(self.res5.includes(11))



    def test_identify_wrong_book(self):
        self.assertFalse(self.res1.identify(2, 'book2', 'person1'))
        self.assertFalse(self.res5.identify(6, 'book3', 'person3'))

    def test_identify_wrong_person(self):
        self.assertFalse(self.res2.identify(3, 'book2', 'person4'))
        self.assertFalse(self.res8.identify(8, 'book3', 'person1'))

    def test_identify_wrong_date(self):
        self.assertFalse(self.res3.identify(1, 'book2', 'person3'))
        self.assertFalse(self.res7.identify(9, 'book2', 'person3'))

    def test_identify_correct(self):
        self.assertTrue(self.res4.identify(2, 'book2', 'person2'))
        self.assertTrue(self.res6.identify(7, 'book3', 'person4'))
        


    def test_identify_changed_person(self):
        self.res1.change_for('person4')
        self.assertEqual(self.res1._for,'person4')

    def test_identify_multiple_times_changed_person(self):
        self.res3.change_for('person4')
        self.res3.change_for('person3')
        self.res3.change_for('person2')
        self.res3.change_for('person1')
        self.res3.change_for('person4')
        self.assertEqual(self.res3._for,'person4')



if __name__ == '__main__':
    main()
