from itertools import count

class Printer(object):
    def print(self, msg):
        print(msg)


class Reservation(object):
    _ids = count(0)
    
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0

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

        
        

class ReservationString(Reservation):
    _ids = count(0)
    
    def __init__(self, from_, to, book, for_, printer = Printer):
        super().__init__(from_, to, book, for_)
        self.printer = printer()
        self.printer.print(F'Created a reservation with id {self._id} of {self._book} from {self._from} to {self._to} for {self._for}.')

    def overlapping(self, other):
        ret = super().overlapping(other)
        if not ret:
            str = 'do'
        else:
            str = 'do not'
        self.printer.print(F'Reservations {self._id} and {other._id} {str} overlap')
        return ret
            
    def includes(self, date):
        ret = super().includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        self.printer.print(F'Reservation {self._id} {str} {date}')
        return ret        
        
    def identify(self, date, book, for_):
        ret = super().identify(date, book, for_)
        if book != self._book: 
            self.printer.print(F'Reservation {self._id} reserves {self._book} not {book}.')
        elif for_!=self._for:
            self.printer.print(F'Reservation {self._id} is for {self._for} not {for_}.')
        elif not self.includes(date):
            self.printer.print(F'Reservation {self._id} is from {self._from} to {self._to} which ' +
                               F'does not include {date}.')
        else:
            self.printer.print(F'Reservation {self._id} is valid {for_} of {book} on {date}.')
        return ret   
        
    def change_for(self, for_):
        print(F'Reservation {self._id} moved from {self._for} to {for_}')
        super().change_for(for_)
        



class Library(object):
    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from
                
    def add_user(self, name):
        unique = not (name in self._users)
        if unique:
            self._users.add(name) 
        return unique

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    def reserve_book(self, user, book, date_from, date_to, ReservationFactory = Reservation):
        book_count = self._books.get(book, 0)
        
        if (user not in self._users or
            date_from > date_to or
            book_count == 0):
            return False

        desired_reservation = ReservationFactory(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return False
                
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        return True

    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])    

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        change = (any(relevant_reservations)
                  and new_user in self._users)
        if change:
            relevant_reservations[0].change_for(new_user)
        return change



class LibraryString(Library):
    def __init__(self, printer = Printer):
        super().__init__()
        self.printer = printer()
        self.printer.print(F'Library created.')
                
    def add_user(self, name):
        ret = super().add_user(name)
        if not ret:
            self.printer.print(F'User not created, user with name {name} already exists.')
        else:
            self.printer.print(F'User {name} created.')
        return ret

    def add_book(self, name):
        super().add_book(name)
        self.printer.print(F'Book {name} added. We have {self._books[name]} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to, ReservationFactory = Reservation):
        ret = super().reserve_book(user, book, date_from, date_to, ReservationFactory)

        desired_reservation = ReservationFactory(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                     if desired_reservation.overlapping(res)] + [desired_reservation]
        
        if not ret:
            if user not in self._users:
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'User does not exist.')
            elif date_from > date_to:
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'Incorrect dates.')
            elif self._books.get(book, 0):
                self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                                   F'We do not have that book.')
            
            
            #we check that if we add this reservation then for every reservation record that starts 
            #between date_from and date_to no more than book_count books are reserved.
            for from_ in [res._from for res in relevant_reservations]:
                if desired_reservation.includes(from_):
                    if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                        self.printer.print(F'We cannot reserve book {book} for {user} from {date_from} ' +
                                           F'to {date_to}. We do not have enough books.')
                        break
                    
        else:
            self._reservations+=[desired_reservation]
            self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
            self.printer.print(F'Reservation {desired_reservation._id} included.')
            
        return ret

    def check_reservation(self, user, book, date):
        ret = super().check_reservation(user, book, date)
        str = 'exists'
        if not ret:
            str = 'does not exist'
        self.printer.print(F'Reservation for {user} of {book} on {date} {str}.')
        return ret        

    def change_reservation(self, user, book, date, new_user):
        ret = super().change_reservation(user, book, date, new_user)
        if ret:
            self.printer.print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')
        elif new_user not in self._users:
            self.printer.print(F'Cannot change the reservation as {new_user} does not exist.')
        else:
            self.printer.print(F'Reservation for {user} of {book} on {date} does not exist.')
        return ret
