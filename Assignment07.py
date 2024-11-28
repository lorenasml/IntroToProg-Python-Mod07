# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# Change Log: (Who, When, What)
#   Lorena,11/24/2024,Created Script
#   Lorena, 11/25/2024,Added docstrings
#   <Your Name Here>,<Date>, <Activity>
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = """
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
"""
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
# student_first_name: str = ""
# student_last_name: str = ""
# course_name: str = ""
# csv_data: str = ""
# file = None
menu_choice: str = ""
# student_data: dict = {}
students: list = []

# Data --------------------------------------- #
class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
    """
    def __init__(self, first_name:str = '', last_name:str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property  # (Use this decorator for the getter or accessor)
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers or be empty.")

    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # is character or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers or be empty.")

    def __str__(self):
        return f'{self.first_name},{self.last_name}'

class Student(Person):
    """
    A class representing student data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        course_name (str): The course name that the student enrolls in.
    """
    def __init__(self, first_name:str = '', last_name:str = '',course_name:str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        if value.isprintable():
            self.__course_name = value
        else:
            raise Exception("The course name should not be empty.")

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing functions that work with Json files
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads student data from a JSON file and converts it into a list of Student objects.

        Args:
            file_name (str): The path to the JSON file containing the student data.
            student_data (list): A list to which the created `Student` objects will be appended.

        Returns:
            list: The updated `student_data` list containing `Student` objects created from the file data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: For any other unexpected errors that occur during file reading or data processing.
        """

        try:
            with open(file_name, "r") as file:
                list_of_dictionary_data = json.load(file)
            for student in list_of_dictionary_data:  # Convert the list of dictionary rows into Student objects
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name= student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)

        except FileNotFoundError as e:
            IO.output_error_messages(f"The file {file_name} does not exist. Please check the file path.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Writes a list of Student objects to a JSON file.

        Args:
            file_name (str): The path to the JSON file where the student data will be written.
            student_data (list): A list of Student objects to be written to the file.

        Returns:
            None: Writes to the file, no return value.

        Raises:
            IOError: If there is an issue with writing to the file.
            Exception: For any other unexpected errors that occur during file reading or data processing.
        """

        try:
            list_of_dictionary_data: list = []
            for student in student_data:  # Convert List of Student objects to list of dictionary rows.
                student_json: dict = {"FirstName": student.first_name, "LastName": student.last_name, "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)

            with open(file_name, "w") as file:
                json.dump(list_of_dictionary_data, file, indent=4)
        except IOError as e:
            IO.output_error_messages(f"Error: Could not write to file '{file_name}'. Please check file permissions and path.", e)
        except Exception as e:  # catch all
            IO.output_error_messages("There was a non-specific error!", e)

        print("Student successfully enrolled!")

# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation functions that manage user input and output
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Displays a custom error message to the user and optionally includes technical details for debugging.

        Args:
            message (str): A custom error message that will be displayed to the user.
            error (Exception, optional): An optional exception object that contains technical error details.
                                        If provided, additional error information will be printed for debugging.

        Returns:
            None: This function does not return any value, but it prints the error messages to the console.
        """

        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')


    @staticmethod
    def output_menu(menu: str):
        """
        Displays a menu of choices to the user.

        Args:
            menu (str): A string representing the menu to be displayed. This could be a list of options
                         or a formatted string to show to the user.

        Returns:
            None: This function does not return any value, but it prints the menu to the console.
        """

        print()  # Adding extra space to make it look nicer.
        print(MENU)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        Prompts the user to input a menu choice and returns the user's selection.

        This function displays a prompt asking the user to enter a menu choice (typically a number),
        then returns the user's input as a string.

        Returns:
            str: The user's input choice, which is returned as a string.
        """

        choice = input("Enter your menu choice number: ")
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """
        Prompts the user to input student data (first name, last name, and course name) and stores
        the information in a list of `Student` objects.

        Args:
            student_data (list): A list that stores the `Student` objects. The new student will be appended to this list.

        Returns:
            list: The updated `student_data` list with the newly added `Student` object.

        Raises:
            ValueError: If the input data is not the expected type (though this is handled by the except block).
            Exception: A generic exception if an unexpected error occurs during the process.
        """

        try:
            student = Student() # Instantiate a new Student object
            student.first_name = input("What is the student's first name? ")
            student.last_name = input("What is the student's last name? ")
            student.course_name = input("Which course are you enrolled in? ")
            student_data.append(student)  # Add the student object to the list

            print()
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:  # catch-all
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data


    @staticmethod
    def output_student_courses(student_data: list):
        """
        Displays the list of students along with their enrolled course information.

        Args:
            student_data (list): A list of `Student` objects containing student data to be displayed.

        Returns:
            None: This function does not return any value, but it prints the student data to the console.

        """

        print("-" * 50)
        for student in student_data:
            print(f'{student.first_name},{student.last_name},{student.course_name}')
            print("-" * 50)

#  End of function definitions

# Beginning of the main body of this script
FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Repeat the follow tasks
while True:
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break  # out of the while loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")