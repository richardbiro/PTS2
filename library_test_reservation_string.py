from library import ReservationString
from unittest import main, TestCase

class MockPrinter(object):
    def print(self, msg):
        self.msg = msg


class TestReservationString(TestCase):
    def setUp(self):
        self.res = ReservationString(0, 2, 'book1', 'person1', MockPrinter)
        
    def test_include_string(self):
        self.res.includes(1)
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} includes 1')
        self.res.includes(3)
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} does not include 3')

    def test_identify_string(self):
        self.res.identify(1, 'book2', 'person1')
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} reserves {self.res._book} not book2.')
        self.res.identify(1, 'book1', 'person2')
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} is for {self.res._for} not person2.')
        self.res.identify(3, 'book1', 'person1')
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} is from {self.res._from} to {self.res._to} which does not include 3.')
        self.res.identify(1, 'book1', 'person1')
        self.assertEqual(self.res.printer.msg,
                         F'Reservation {self.res._id} is valid person1 of book1 on 1.')



if __name__ == '__main__':
    main()
