"""
ml/misc/big_number
"""


class BigNumber:
    """
    class BigNumber calculating with big ints using strings
    """

    def _normalize_num_string(self, input_string):
        """
        modify the input string to string of positive int
        @return: string of number, '' if not a string of int
        """
        input_string = str(input_string).strip().lstrip('+')
        for char in input_string:
            if not '0' <= char <= '9':
                input_string = ''
                break
        if not input_string:
            input_string = '0'
        return input_string

    def _num_string_to_num_list(self, input_string):
        """
        input string to num list
        eg. '123' ---> [1, 2, 3]
        @param input_string: string has to be modified
        @return: num list, from first digit to last digit
        """
        my_list = []
        for i in range(len(input_string)):
            my_list.append(int(input_string[i]))
        return my_list

    def __init__(self, init_string=''):
        """
        initiator of BigNumber,
        if string is not made of digits, head will be '0'
        @param init_string: input string of int
        """
        self.list = self._num_string_to_num_list(self._normalize_num_string(init_string))

    def add(self, input_string):
        """
        add the input_string of numbers to head, 0 if not a string of pure int
        @param input_string: string of numbers to be added to head
        @return:
        """
        my_list = self.list
        input_list = self._num_string_to_num_list(self._normalize_num_string(input_string))
        my_list.reverse()  # reverse self.list
        input_list.reverse()  # reverse input_list
        carry, new_list = 0, []
        larger_list = input_list if len(input_list) > len(my_list) else my_list
        smaller_list = my_list if len(input_list) > len(my_list) else input_list  # checking which is the larger
        for i in range(len(larger_list)):
            try:
                current_sum = larger_list[i] + smaller_list[i] + carry  # summing up each digits with carry
            except IndexError:
                current_sum = larger_list[i] + carry
            if current_sum >= 10:
                current_sum -= 10
                carry = 1
            else:
                carry = 0  # compute carry and modify current sum to 1-figure-digit
            new_list.append(current_sum)  # append sum to new list
        if carry != 0:
            new_list.append(carry)  # append the possible one more digit
        new_list.reverse()
        self.list = new_list
        pass

    def to_string(self):
        """
        convert self.list to string
        @return: string
        """
        result = ''
        for item in self.list:
            result += str(item)
        return result

    def get_scale(self):
        """
        get the scale of self.list, like how big in human language
        in the form of name, description
        @return: name, description
        """
        deca_scale = {"name": 'deca', "description": 'Ten'}
        hecto_scale = {"name": 'hecto', "description": 'Hundred'}
        kilo_scale = {"name": 'kilo', "description": 'Thousand'}
        mega_scale = {"name": 'mega', "description": 'Million'}
        giga_scale = {"name": 'giga', "description": 'Billion'}
        tera_scale = {"name": 'tera', "description": 'Trillion'}
        peta_scale = {"name": 'peta', "description": 'Quadrillion'}
        exa_scale = {"name": 'exa', "description": 'Quintillion'}
        zeta_scale = {"name": 'zeta', "description": 'Sextillion'}
        yotta_scale = {"name": 'yotta', "description": 'Septillion'}
        scale_book = [deca_scale, deca_scale, hecto_scale, kilo_scale, kilo_scale, kilo_scale,
                      mega_scale, mega_scale, mega_scale, giga_scale, giga_scale, giga_scale,
                      tera_scale, tera_scale, tera_scale, peta_scale, peta_scale, peta_scale,
                      exa_scale, exa_scale, exa_scale, zeta_scale, zeta_scale, zeta_scale,
                      yotta_scale, yotta_scale, yotta_scale]
        if len(self.list) <= len(scale_book):
            name = scale_book[len(self.list) - 1]["name"]
            description = scale_book[len(self.list) - 1]["description"]
            return name, description
        else:
            return 'unknown', 'too big'
