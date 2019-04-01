"""
ml/misc/queue
"""


class Queue:
    """
    Queue modulo using list
    """

    def __init__(self, init_list=[]):
        """
        initiator of Queue modulo
        """
        if not isinstance(init_list, list):
            self.queue = []
        else:
            self.queue = init_list

    def dequeue(self):
        """
        pop the first-in item in self.head
        @return: first-in item
        """
        if len(self.queue) > 0:
            return self.queue.pop()
        return None

    def enqueue(self, input_item):
        """
        add the last-in item in self.head
        @return:
        """
        self.queue.insert(0, input_item)

    def is_empty(self):
        """
        check if self.head is empty
        @return: boolean
        """
        return self.queue == []

    def peek(self):
        if not self.queue:
            return None
        return self.queue[-1]


class StackQueue:
    """
    Queue class with Stack
    """

    def __init__(self):
        from ml.misc.stack import Stack

        self.s1 = Stack([])
        self.s2 = Stack([])

    def _move(self, src, dst):
        if src.is_empty():
            return
        item = src.pop()
        self._move(src, dst)
        dst.push(item)

    def dequeue(self):
        return self.s1.pop()

    def enqueue(self, item):
        self.s2.push(item)
        self._move(self.s1, self.s2)
        self.s1, self.s2 = self.s2, self.s1
        return item

    def from_list(self, input_list=[]):
        """
        form the q.stack with input list
        @return:
        """
        if not isinstance(input_list, list):
            input_list = []
        for item in input_list:
            self.enqueue(item)

    def peek(self):
        return self.s1.peek()
