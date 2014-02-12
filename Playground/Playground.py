print('Hello World')


class FileName(object):
    def __init__(self, filename):
        self.filename=filename
        self._get_file_name_info()

    def _get_file_name_info(self):
        file_str = ''.join(self.filename.split('.')[0:-1])
        self._file_type = self.filename.split('.')[-1]

        self._file_number_str=self._get_ending_number(file_str)
        self._file_number = int(self._file_number_str)
        self._file_base_str = file_str[:-len(self._file_number_str)]

    def _get_ending_number(self, str):
        res = ''
        print str
        for char in reversed(str):
            if char.isdigit():
                print char
                res+=char
            else:
                return res[::-1]

    def get_next_file_names(self):
        new_file_name = self._file_base_str + str(self._file_number + 1) + \
                        '.' + self._file_type
        format_str = '0' + str(len(self._file_number_str)) + 'd'
        number_str = ("{0:" + format_str + '}').format(self._file_number + 1)
        new_file_name_with_leading_zeros = self._file_base_str + \
                    number_str + '.' + self._file_type
        return new_file_name, new_file_name_with_leading_zeros

    def get_previous_file_names(self):
        new_file_name = self._file_base_str + str(self._file_number - 1) + \
                        '.' + self._file_type
        format_str = '0' + str(len(self._file_number_str)) + 'd'
        number_str = ("{0:" + format_str + '}').format(self._file_number - 1)
        new_file_name_with_leading_zeros = self._file_base_str + \
                    number_str + '.' + self._file_type
        return new_file_name, new_file_name_with_leading_zeros


test1=FileName('Fe7C3_150_1000.spe')
print test1.get_next_file_names()
print test1.get_previous_file_names()