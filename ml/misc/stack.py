"""
ml/misc/stack
"""


class Stack:
    """
    Stack modulo using list
    """

    def __init__(self, init_list=[]):
        """
        Initiator of Stack
        """
        if not isinstance(init_list, list):
            self.stack = []
        else:
            self.stack = init_list
        pass

    def is_empty(self):
        """
        check if self.head is empty
        @return: Boolean
        """
        return self.stack == []

    def peek(self):
        """
        give the last pushed item
        @return: last pushed item
        """
        if not self.stack:
            return None
        return self.stack[-1]

    def pop(self):
        """
        pop the last pushed item from self.head
        @return: popped item
        """
        if len(self.stack) > 0:
            return self.stack.pop()
        return None

    def push(self, input_item):
        """
        push the input_item to self.head
        @return:
        """
        self.stack.append(input_item)


class QueueStack:
    """
    Stack class with Queue
    """

    def __init__(self):
        from ml.misc.queue import Queue

        self.q1 = Queue([])
        self.q2 = Queue([])
        self.temp = Queue([])
    pass

    def from_list(self, input_list=[]):
        """
        form the q.stack with input list
        @return:
        """
        if not isinstance(input_list, list):
            input_list = []
        for item in input_list:
            self.push(item)

    def peek(self):
        return self.q1.peek()

    def pop(self):
        return self.q1.dequeue()

    def push(self, item):
        self.q2.enqueue(item)
        while not self.q1.is_empty():
            self.q2.enqueue(self.q1.dequeue())
        self.q1, self.q2 = self.q2, self.q1
