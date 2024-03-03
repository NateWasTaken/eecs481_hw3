import unittest

class TestStringProcessor(unittest.TestCase):

    def test_replace_non_letters_non_numbers_with_whitespace(self):
        result = StringProcessor.replace_non_letters_non_numbers_with_whitespace("Hello123!")
        self.assertEqual(result, "Hello123 ")

    def test_strip(self):
        result = StringProcessor.strip("   Hello World   ")
        self.assertEqual(result, "Hello World")

    def test_to_lower_case(self):
        result = StringProcessor.to_lower_case("Hello World")
        self.assertEqual(result, "hello world")

    def test_to_upper_case(self):
        result = StringProcessor.to_upper_case("hello world")
        self.assertEqual(result, "HELLO WORLD")

class TestFunctions(unittest.TestCase):

    def test_validate_string(self):
        self.assertTrue(validate_string("Hello"))
        self.assertFalse(validate_string(""))
        self.assertFalse(validate_string(None))

    def test_check_for_none_decorator(self):
        @check_for_none
        def add(a, b):
            return a + b

        result = add(3, 4)
        self.assertEqual(result, 7)

        result_none = add(3, None)
        self.assertEqual(result_none, 0)

    def test_check_empty_string_decorator(self):
        @check_empty_string
        def concatenate_strings(s1, s2):
            return s1 + s2

        result = concatenate_strings("Hello", " World")
        self.assertEqual(result, "Hello World")

        result_empty_string = concatenate_strings("Hello", "")
        self.assertEqual(result_empty_string, 0)

    def test_full_process(self):
        result = full_process(" Hello123! ", force_ascii=False)
        self.assertEqual(result, "hello123")

    def test_ratio(self):
        result = ratio("Hello", "Holle")
        self.assertEqual(result, 80)

    def test_partial_ratio(self):
        result = partial_ratio("Hello", "Holle")
        self.assertEqual(result, 80)

    # Add more test cases for other functions as needed

if __name__ == '__main__':
    unittest.main()
