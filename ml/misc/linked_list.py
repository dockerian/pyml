"""
ml/misc/linked_list.py
"""
import copy


# Build a LinkedList class and implement reverse function
class LinkedList:

    def __init__(self, init_list=[]):
        self.head = None
        self.length = 0
        self.from_list(init_list)
        pass

    def _get_circular_link(self):
        """
        @return: met, last_item to met, whether is circular
        """
        if self.head is None:
            return None, None, None
        head, slower = self.head, self.head.get('next')
        last, faster = head, None if slower is None else slower.get('next')

        while slower is not None and faster is not None and slower != faster:
            last = slower
            slower = slower.get('next')
            faster = faster.get('next')
            faster = faster.get('next') if faster is not None else None

        if faster is None or slower is None:
            return None, None, False

        return faster, last, True

    def from_list(self, init_list):
        if not isinstance(init_list, list):
            init_list = []
        current = None
        for v in init_list:
            item = copy.deepcopy(v)
            next_item = {
                'data': item,
                'next': None,
            }
            if current is None:
                self.head = next_item
            else:
                current['next'] = next_item
            current = next_item
        self.length = len(init_list)
        # self.print()

    def add(self, input_item, position=0):
        """
        add input_item to certain position, if the input position is larger than the length of original head, will
        place the input item to the end, and put to the begin if position <= 0
        @param input_item: item to be added
        @param position: position to be added
        @return:
        """
        new_item = {
            'data': input_item,
            'next': None,
        }
        if self.head is None:
            self.head = new_item
            return new_item
        if not isinstance(position, int):
            return None
        head = self.head
        if position <= 0:
            new_item['next'] = head
            self.head = new_item
            return new_item
        counter, current = 0, head
        while counter < position-1 and not current.get('next') is None:
            current = current.get('next')
            counter += 1
        old_next = current.get('next')
        current['next'] = new_item
        new_item['next'] = old_next
        self.length += 1
        return new_item
        # self.print()

    def append(self, input_item):
        """
        append input_item to self.head
        @param input_item: item that needs to be appended
        @return:
        """
        new_item = {
            'data': input_item,
            'next': None,
        }
        if self.head is None:
            self.head = new_item
            return new_item
        current = self.head
        while current.get('next') is not None:
            current = current.get('next')

        current['next'] = new_item
        self.length += 1
        return new_item

    def check_circular_link(self):
        """
        Example of circular link:
             1        2        3        4
        (A)----->(B)----->(C)----->(D)----->(E)
                           \\_______________/
                                    5
        """
        met, last, has_cyclic = self._get_circular_link()
        return has_cyclic

    def delete(self, position=0):
        """
        delete item in self.head in certain input position,
        and return the deleted item
        @param position: position that we item deleted
        @return: deleted item, or None if nothing deleted
        """
        if not isinstance(position, int):
            raise TypeError
        if self.head is None:
            return None
        head = self.head
        if position > self.length - 1:
            position = self.length - 1
        if position <= 0:
            deleted = {
                'data': head['data'],
                'next': None,
            }
            head = head['next']
            self.head = head
            self.length -= 1
            return deleted
        current = head
        counter = 0
        while current.get('next') is not None and counter < position - 1:
            current = current.get('next')
            counter += 1
        deleted = {
            'data': current.get('next').get('data'),
            'next': None,
        }
        current['next'] = current.get('next').get('next')
        self.head = head
        self.length -= 1
        return deleted

    def find_middle_item(self):
        """
        find the middle item of self.head,
        if the length of self.head is even number, then return the ((length/2)-1)'th of self.head
        @return: the middle item of self.head
        """
        if self.head is None:
            return None
        current, temp = self.head, self.head
        counter = 0
        while current is not None:
            counter += 1
            current = current['next']
        mid_index = (counter+1)//2  # same when for example, counter = 5 and 6
        while counter > mid_index:
            temp = temp['next']
            counter -= 1
        return temp

    def fix_circular_link(self):
        """
        fix the circular link in self.head
        @return:
        """
        circular_item = self.get_circular_link_item()
        if circular_item is None:
            return
        circular_item['next'] = None

    def get_circular_link_item(self):
        """
        get the item that has circular link,
        @return: the item that has circular link reference;
                 or None if self.head has no circular link.
        """
        next_item, last, has_cyclic = self._get_circular_link()

        if has_cyclic:
            current = self.head
            if current == next_item:
                return last
            while current != next_item:
                if current.get('next') == next_item.get('next'):
                    return next_item
                current = current.get('next')
                next_item = next_item.get('next')
        return next_item

    def print(self):
        print('linked list [length= {}]: {}'.format(self.length, self.head))

    def reverse(self):
        if self.head is None:
            return None
        current, previous = self.head, None
        while current is not None:
            next_item = current['next']
            current['next'] = previous
            current, previous = next_item, current
        self.head = previous
        # print('built:', self.head)

    def to_list(self):
        if self.head is None:
            return None
        result = []
        current = self.head
        while current is not None:
            item = current.get('data')
            current = current.get('next')
            result.append(item)
        return result
