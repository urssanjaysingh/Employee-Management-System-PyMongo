# Built-in modules included by default in Python environments
import sys  # Module for interacting with the system
import os  # Module for interacting with the operating system
import time  # Module for time-related operations
from dataclasses import dataclass  # Used for creating data classes
from typing import Optional  # Used for type hinting
from bson import ObjectId  # Used for representing MongoDB ObjectIds

# Third-party modules requiring installation
import keyboard  # Windows-specific module for getting keypresses
from colorama import Fore, Style  # Library for colored output
from pymongo import MongoClient  # MongoDB driver for Python
import pymongo.errors  # Import pymongo.errors module
from tabulate import tabulate  # Library for creating formatted tables from data
from dotenv import (
    load_dotenv,
)  # Library for loading environment variables from a .env file

load_dotenv()  # Load environment variables from .env file if present


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system("cls")


def pause_screen():
    """
    Pauses the screen and waits for a keypress from the user.
    """
    print()
    os.system("pause")


def print_error_message(message):
    """
    Print an error message in red color.
    """
    print("\n" + Fore.RED + message + Style.RESET_ALL)


def print_information_message(message):
    """
    Print an information message in blue color.
    """
    print("\n" + Fore.BLUE + message + Style.RESET_ALL, end="", flush=True)


def print_success_message(message):
    """
    Print a success message in green color.
    """
    print("\n" + Fore.GREEN + message + Style.RESET_ALL)


def get_valid_input(prompt, validator_function, allow_blank=False):
    """Get user input and validate it using a custom validator function."""
    while True:
        user_input = input(prompt).strip()

        # Check if the input is empty and allow_blank is True
        if user_input == "" and allow_blank:
            return ""

        # Validate the input using the provided validator function
        if validator_function(user_input):
            return user_input


class Validator:
    """
    A class containing static methods for input validation.

    Static methods can be called without creating an instance of the class.

    Methods:
    - validate_name(name): Validate a name.
    - validate_designation(designation): Validate a designation.
    - validate_salary(salary): Validate a salary.
    - validate_age(age): Validate an age.
    - validate_phone(phone): Validate a phone number.
    - validate_address(address): Validate an address.
    """

    @staticmethod
    def validate_name(name):
        """
        Validate a name.

        Parameters:
        - name (str): The name to validate.

        Returns:
        - bool: True if the name contains only alphabetic characters, False otherwise.
        """

        # Check if the name, after removing spaces, contains only alphabetic characters
        if name.replace(" ", "").isalpha():
            return True
        print_error_message("Name must contain only alphabetic characters.")
        return False

    @staticmethod
    def validate_designation(designation):
        """
        Validate a designation.

        Parameters:
        - designation (str): The designation to validate.

        Returns:
        - bool: True if the designation contains only alphabetic characters, False otherwise.
        """

        # Check if the designation, after removing spaces, contains only alphabetic characters
        if designation.replace(" ", "").isalpha():
            return True
        print_error_message("Designation must contain only alphabetic characters.")
        return False

    @staticmethod
    def validate_salary(salary):
        """
        Validate a salary.

        Parameters:
        - salary (str): The salary to validate.

        Returns:
        - bool: True if the salary is at least 500 and in a valid format, False otherwise.
        """

        # Check if salary is a digit and greater than or equal to 500
        if salary.isdigit() and int(salary) >= 500:
            return True
        print_error_message(
            "Salary must be at least 500 and in a valid numeric format."
        )
        return False

    @staticmethod
    def validate_age(age):
        """
        Validate an age.

        Parameters:
        - age (str): The age to validate.

        Returns:
        - bool: True if the age is from 18 to 99 and in a valid format, False otherwise.
        """

        # Check if age is a digit and within the range of 18 to 99
        if age.isdigit() and 18 <= int(age) <= 99:
            return True
        print_error_message(
            "Age must be a positive number between 18 and 99 in a valid numeric format."
        )
        return False

    @staticmethod
    def validate_phone(phone):
        """
        Validate a phone number.

        Parameters:
        - phone (str): The phone number to validate.

        Returns:
        - bool: True if the phone number is a 10-digit number, False otherwise.
        """

        # Check if phone is a digit and has a length of 10
        if phone.isdigit() and len(phone) == 10:
            return True
        print_error_message(
            "Phone number must be a 10-digit number in a valid numeric format."
        )
        return False

    @staticmethod
    def validate_address(address):
        """
        Validate an address.

        Parameters:
        - address (str): The address to validate.

        Returns:
        - bool: True if the address is not empty after stripping whitespace, False otherwise.
        """

        # Check if the address is not empty after stripping whitespace
        if address.strip():
            return True
        print_error_message("Address cannot be empty.")
        return False


# The @dataclass decorator automatically generates special methods
# such as __init__, __repr__, __eq__, etc., based on the class attributes.
@dataclass
class Employee:
    """
    Represents an employee with various attributes.

    Attributes:
        name (str): The name of the employee.
        designation (str): The designation of the employee.
        salary (float): The salary of the employee.
        age (int): The age of the employee.
        phone (int): The phone number of the employee.
        address (str): The address of the employee.
        _id (Optional[ObjectId]): The optional ID of the employee.
    """

    name: str
    designation: str
    salary: float
    age: int
    phone: int
    address: str
    # The Optional[] type hint indicates that this attribute can be either an ObjectId or None.
    _id: Optional[ObjectId] = None  # Employee ID, default to None if not provided

    def get_id(self):
        """
        Getter method to access the employee ID.
        """
        return self._id

    def to_dict(self):
        """
        Convert the Employee object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Employee object,
                including name, designation, salary, age, phone number,
                address.
        """
        data = {
            "name": self.name,
            "designation": self.designation,
            "salary": self.salary,
            "age": self.age,
            "phone": self.phone,
            "address": self.address,
        }
        return data  # Return the dictionary representation of the employee


class Database:
    """
    Represents a connection to a MongoDB database.

    This class is responsible for establishing a connection to a MongoDB database
    using the provided URI. It provides access to the 'employees' database and its
    collections, such as 'users' and 'staff', for storing employee and user records.
    """

    # Initialize the Database class with a MongoDB URI: Uniform Resource Identifier.
    def __init__(self, uri):
        # Connect to MongoDB using the provided URI
        self.client = MongoClient(
            uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000
        )
        # Access the 'employees' database
        self.db = self.client.employees
        # Access the 'users' collection within the 'employees' database
        self.users = self.db.users
        # Access the 'staff' collection within the 'employees' database
        self.staff = self.db.staff

    def find_user_by_email(self, email):
        """
        Check if a user with the provided email exists in the database.

        Args:
            email (str): The email of the user to search for.

        Returns:
            dict or None: The user document if found, otherwise None.
        """
        try:
            return self.users.find_one({"email": email})
        except pymongo.errors.AutoReconnect:
            print_error_message(
                "Lost connection to MongoDB while finding user by email."
            )
            return False

    def get_employee_list(self):
        """
        Retrieve a list of all employees from the database.

        Returns:
            list: A list of Employee objects representing the employees in the database.
        """
        try:
            # Retrieve all documents from the collection
            employee_documents = self.staff.find()

            # Initialize an empty list to store Employee objects
            employee_list = []

            if employee_documents:
                # Iterate over each document in the employee_documents
                for emp in employee_documents:
                    # Create an Employee object using the data from the document
                    # Unpacks the dictionary 'emp',
                    # into individual key-value pairs for the Employee constructor
                    employee = Employee(**emp)

                    # Append the created Employee object to the list
                    employee_list.append(employee)

            # Return the list of Employee objects
            return employee_list
        except pymongo.errors.AutoReconnect:
            print_error_message(
                "Lost connection to MongoDB while retrieving employees list."
            )

        # Explicitly return None if no employees are found
        return None

    def insert_employee(self, employee):
        """
        Insert a new employee into the database.

        Args:
            employee (Employee): The Employee object to be inserted.

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        try:
            # Convert employee object to a dictionary before insertion
            employee_data = employee.to_dict()

            # Insert the employee data into the collection
            result = self.staff.insert_one(employee_data)

            # Check if insertion was successful
            return bool(result.inserted_id)
        except pymongo.errors.AutoReconnect:
            print_error_message(
                "Lost connection to MongoDB while inserting employee details."
            )
            return False  # Failed addition due to exception

    def get_employee_by_id(self, emp_id):
        """
        Retrieve an employee from the database based on their ID.

        Args:
            emp_id (str): The ID of the employee to retrieve.

        Returns:
            Employee or None: The Employee object if found, None if not found.
        """
        try:
            # Find the employee document by its ID in the collection
            emp = self.staff.find_one({"_id": emp_id})

            # If an employee document is found,
            if emp:
                # Create an Employee object from the document
                # Unpacks the dictionary 'emp',
                # into individual key-value pairs for the Employee constructor
                employee = Employee(**emp)

                # Return the created Employee object
                return employee
            # If no employee document is found, return None
            return None
        except pymongo.errors.AutoReconnect:
            print_error_message(
                "Lost connection to MongoDB while getting employee details."
            )
            return False

    def update_employee_by_id(self, emp_id, employee):
        """
        Update an employee's information in the database based on their ID.

        Args:
            emp_id (str): The ID of the employee to update.
            employee (Employee): The updated Employee object containing the new information.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            # Convert employee object to a dictionary
            employee_data = employee.to_dict()

            # Update the employee document in the collection with the provided ID
            update_result = self.staff.update_one(
                {"_id": emp_id},
                {
                    # Use $set operator to update specific fields
                    "$set": employee_data
                },
            )

            # Check if any document was modified during the update operation
            if update_result.modified_count > 0:
                return True
            return None  # No documents were modified
        except pymongo.errors.AutoReconnect:
            return False

    def remove_employee_by_id(self, emp_id):
        """
        Remove an employee from the database based on their ID.

        Args:
            emp_id (str): The ID of the employee to remove.

        Returns:
            bool: True if the removal was successful, False otherwise.
        """
        try:
            # Delete the employee document from the collection with the provided ID
            delete_result = self.staff.delete_one({"_id": emp_id})

            # Check if any document was deleted during the operation
            if delete_result.deleted_count > 0:
                return True
            return False
        except pymongo.errors.AutoReconnect:
            print_error_message("Lost connection to MongoDB while deleting employee.")
            return False

    def search_employee(self, term):
        """
        Search for employees in the database based on a search term.

        Args:
            term (str): The search term to match against employee names, designations, or addresses.

        Returns:
            list: A list of Employee objects matching the search term.
        """
        try:
            # Search for employee documents in the collection based on the provided term
            search_results = self.staff.find(
                {
                    # Using $or operator to search for documents,
                    # that match any of the specified conditions
                    "$or": [
                        {
                            "name": {  # Field to search: "name"
                                # Regular expression pattern to match against the "name" field
                                "$regex": term,
                                # Options for the regular expression:
                                # "i" for case-insensitive matching
                                "$options": "i",
                            }
                        },
                        {
                            "designation": {"$regex": term, "$options": "i"}
                        },  # Search by designation (case-insensitive)
                        {
                            "address": {"$regex": term, "$options": "i"}
                        },  # Search by address (case-insensitive)
                    ]
                }
            )

            # Create Employee objects from the search results and return them as a list
            # Define an empty list to store the Employee objects
            result_list = []

            # Iterate over each dictionary in search_results
            for emp in search_results:
                # Create an Employee object using the dictionary emp and add it to the result_list
                employee_object = Employee(**emp)
                result_list.append(employee_object)

            # Return the result_list
            return result_list
        except pymongo.errors.AutoReconnect:
            print_error_message("Lost connection to MongoDB while searching employee.")
            return []


class EmployeeManagementSystem:
    """
    Initialize the EmployeeManagementSystem with a database connection.

    Args:
        db: The database connection object.

    Attributes:
        db: The database connection object.
        database (Database): An instance of Database initialized
            with the provided database connection.
        id_mapping (dict): A dictionary to store mappings of employee IDs to objects.
            This is used to keep track of Employee objects created during runtime.
    """

    def __init__(self, uri):
        # Initialize an instance of Database with the provided database connection
        self.database = Database(uri)

        # Initialize an empty dictionary to store mappings of employee IDs to objects
        # This will be used to keep track of Employee objects created during runtime
        self.id_mapping = {}

    def update_id_mapping(self, employees):
        """
        Update the ID mapping based on the provided list of employees.

        Args:
        - employees (list): A list of Employee objects retrieved from the database.
        """
        self.id_mapping.clear()  # Clear the existing ID mapping
        for i, emp in enumerate(employees, start=1):
            self.id_mapping[i] = emp.get_id()

    def display_employee_details(self, emp_id, employee):
        """
        Display details of a specific employee.

        Args:
            emp_id (int): The ID of the employee.
            employee (Employee): The Employee object containing the employee's details.

        Prints the details of the specified employee, including ID, name, designation,
        salary, age, phone number, and address.
        """
        data = []
        employee_dict = {
            "ID": emp_id,
            "Name": employee.name,
            "Designation": employee.designation,
            "Salary": employee.salary,
            "Age": employee.age,
            "Phone": employee.phone,
            "Address": employee.address,
        }
        data.append(employee_dict)
        for data_dict in data:
            print(tabulate(data_dict.items(), tablefmt="fancy_grid"))

    def login(self):
        """
        Allow users to log in to the system.

        This method prompts the user to enter their email and password.
        It then checks if a user with the provided email exists in the database.

        Returns:
            None
        """
        while True:
            clear_screen()
            # Prompt the user to enter their email and password
            email = input("Enter your email: ").strip()
            password = input("\nEnter your password: ").strip()

            # Check if a user with the provided email exists in the database
            user = self.database.find_user_by_email(email)
            # If user exists and provided password matches the stored password, log in
            if user and user["password"] == password:
                # Notify the user about successful login
                print_success_message("Login successful!")
                pause_screen()

                # Redirect the user to the main menu
                self.main_menu()
                # Exit the login loop
                break

            if user and user["password"] != password:
                # Notify the user about invalid password
                print_error_message("Invalid password! Please try again.")
            elif user is None:
                # Notify the user that the email is not registered
                print_error_message("No user found with the provided email.")

            print_information_message(
                "Press 'Enter' to try again or 'esc' to return to the login menu..."
            )
            retry = True
            while retry:
                # Add a short delay to prevent instant confirmation due to fast key presses
                time.sleep(0.2)
                invalid_credentials_key_pressed = keyboard.read_event(
                    suppress=True
                ).name
                if invalid_credentials_key_pressed == "esc":
                    print_information_message("\nReturning to the login menu...")
                    time.sleep(0.2)
                    retry = False
                    break

                if invalid_credentials_key_pressed == "enter":
                    print_information_message("\nRetrying...")
                    time.sleep(0.2)
                    retry = True
                    break
            if retry:
                continue
            self.login_menu()  # Call login_menu if the user chooses to exit
            break  # Exit the login loop

    def login_menu(self):
        """
        Display the login menu and handle user login or program exit.

        This method presents the user with options to login or exit the program.
        It calls the login method if the user chooses to login,
            and exits the program if the user chooses to exit.

        Returns:
            None
        """
        while True:
            try:
                clear_screen()
                print(
                    """
                    ================================
                       EMPLOYEE MANAGEMENT SYSTEM    
                    ================================
                    
                          *** LOGIN MENU ***      
                     ______________________________
                    |                              |
                    |_______ 1) Login _____________|
                    |                              |
                    |_______ 2) Exit ______________|
                    |                              |
                    |______________________________|
                    """
                )
                # Get user choice
                choice = int(input("\n\t\t    Select any option: "))
                if choice == 1:
                    # Call the login function
                    self.login()
                    break

                if choice == 2:
                    # Exit the program
                    clear_screen()
                    sys.exit(0)
                else:
                    # Display an error message for invalid choices
                    print_error_message("\t\t    Invalid choice! Please try again.")
                    pause_screen()
            except ValueError:
                # Handle non-numeric input
                print_error_message("\t\t    Please enter a valid numeric choice.")
                pause_screen()

    def main_menu(self):
        """
        Display the main menu and handle user choices.

        This method displays the main menu of the Employee Management System
            and prompts the user to select an option.
        It allows the user to view employees list, edit employees list, search records, or logout.

        Returns:
            None
        """
        # Retrieve all employees from the database
        all_employees = self.database.get_employee_list()

        # Check if there are employees in the database
        if all_employees:
            # Iterate over each employee and their index, starting from 1
            for i, emp in enumerate(all_employees, start=1):
                # Store the employee ID in the id_mapping dictionary using the index i
                # Access _id using the get_id() method
                self.id_mapping[i] = emp.get_id()

        while True:
            clear_screen()
            print(
                """
                    ==================================
                        EMPLOYEE MANAGEMENT SYSTEM    
                    ==================================
                    
                           *** MAIN MENU ***       
                     ________________________________
                    |                                |
                    |____ 1) View Employees List ____|
                    |                                |
                    |____ 2) Edit Employees List ____|
                    |                                |
                    |____ 3) Search Record __________|
                    |                                |
                    |____ 4) Logout_________________ |
                    |                                |
                    |________________________________|
                """
            )

            try:
                # Get user choice
                choice = int(input("\n\t\t    Enter your choice: "))

                # Process user choice
                if choice == 1:
                    # View employees list
                    clear_screen()
                    self.display_employees_list()
                    pause_screen()
                elif choice == 2:
                    # Edit employees list
                    self.edit_menu()
                elif choice == 3:
                    # Search record
                    self.search_record()
                elif choice == 4:
                    # Logout
                    self.login_menu()
                    break
                else:
                    # Invalid choice
                    print_error_message("\t\t    Invalid choice! Please try again.")
                    pause_screen()
            except ValueError:
                # Handle non-numeric input
                print_error_message("\n\t\t    Please enter a valid numeric choice.")
                pause_screen()
                continue

    def edit_menu(self):
        """
        Display the edit menu for managing employees and handle user choices.

        This method presents the user with options to add, modify, or delete employees,
            or return to the main menu.
        It allows the user to perform various editing operations on the employees list.

        Returns:
            None
        """
        while True:
            try:
                clear_screen()
                print(
                    """
                    ============================
                     EMPLOYEE MANAGEMENT SYSTEM  
                    ============================
                    
                    *** EDIT EMPLOYEE LIST ***
                     __________________________
                    |                          |
                    |______ 1) Add ____________|
                    |                          |
                    |______ 2) Modify _________|
                    |                          |
                    |______ 3) Delete _________|
                    |                          |
                    |______ 4) Main Menu ______|
                    |                          |
                    |__________________________|
                    """
                )
                # Prompt for user input
                choice = int(input("\n\t\t    Select any option: "))

                # Process user choice
                if choice == 1:
                    # Add employee
                    self.add_employee()
                elif choice == 2:
                    # Modify employee
                    self.modify_employee()
                elif choice == 3:
                    # Delete employee
                    self.delete_employee()
                elif choice == 4:
                    # Go back to main menu
                    self.main_menu()
                    break
                else:
                    # Handle invalid choice
                    print_error_message("\t\t    Invalid choice! Please try again.")
                    pause_screen()
            except ValueError:
                # Handle non-numeric input
                print_error_message("\t\t    Please enter a valid numeric choice.")
                pause_screen()

    def display_employees_list(self):
        """
        Display a formatted list of employees retrieved from the database.

        Retrieves all employees from the database and formats their data for display.
        If no employees are found, prints an error message.
        """
        # Clear the screen before displaying the employee list
        clear_screen()

        # Retrieve all employees from the database
        all_employees = self.database.get_employee_list()

        # Check if there was an error while retrieving employees
        if all_employees is None:
            return

        # Check if there are any employees
        if all_employees:
            # Define the header for the employee list table
            header = [
                "ID",
                "Name",
                "Designation",
                "Salary",
                "Age",
                "Phone",
                "Address",
            ]

            # Initialize an empty list to hold the formatted employee data
            data = []

            # Iterate over each employee and format their data for display
            index = 1
            for employee in all_employees:
                # Within each iteration, employee variable holds one employee object
                # from all_employees list
                i = index  # Assign the current index to i
                index += 1

                # Convert phone number to string for formatting
                phone_number = str(employee.phone)

                # Append employee data to the list for tabulation
                data.append(
                    [
                        i,  # Employee ID
                        employee.name,
                        employee.designation,
                        employee.salary,
                        employee.age,
                        phone_number,
                        employee.address,
                    ]
                )

            # Print the formatted employee list using tabulate
            print(tabulate(data, headers=header, tablefmt="fancy_grid"))
        else:
            # Print a message if no employees are found
            print_error_message("No employees found.")

    def add_employee(self):
        """
        Allow user to input employee details and add them to the database.

        This method prompts the user to input various details for a new employee,
        such as name, designation, salary, age, phone number, and address. It validates
        each input using the Validator class. After successful validation, an Employee
        object is created and added to the database. The user can choose to add more
        employees or return to the edit menu.

        Returns:
            None
        """
        while True:
            clear_screen()
            print("\n*** Add Employee Details ***\n")

            name = get_valid_input(
                "\nName (alphabetic characters only): ", Validator.validate_name
            )
            designation = get_valid_input(
                "\nDesignation (alphabetic characters only): ",
                Validator.validate_designation,
            )
            salary = float(
                get_valid_input(
                    "\nSalary (must be a number, minimum 500): ",
                    Validator.validate_salary,
                )
            )
            age = int(
                get_valid_input(
                    "\nAge (must be a number from 18 to 99): ",
                    Validator.validate_age,
                )
            )
            phone = int(
                get_valid_input(
                    "\nPhone Number (10-digit number): ", Validator.validate_phone
                )
            )
            address = get_valid_input("\nAddress: ", Validator.validate_address)

            # Create an Employee object with the provided details
            employee = Employee(name, designation, salary, age, phone, address)

            print_information_message(
                "Press 'Enter' to add employee details or 'esc' to cancel..."
            )
            while True:
                # Add a short delay to prevent instant confirmation due to fast key presses
                time.sleep(0.2)

                # Read the key pressed by the user while suppressing the input
                add_employee_key_pressed = keyboard.read_event(suppress=True).name

                if add_employee_key_pressed == "esc":
                    # If the user presses 'esc', cancel the operation
                    print_information_message("\nCanceling...")
                    time.sleep(0.2)
                    print_error_message("\nOperation Canceled.")
                    break

                if add_employee_key_pressed == "enter":
                    print_information_message("\nAdding...")
                    time.sleep(0.2)
                    # If the user presses 'enter', attempt to add the employee to the database
                    if self.database.insert_employee(employee):
                        # Retrieve all employees from the database
                        all_employees = self.database.get_employee_list()

                        # Update the ID mapping after adding the employee
                        if all_employees:
                            self.update_id_mapping(all_employees)
                        # Notify the user about the successful addition of employee details
                        print_success_message("\nEmployee details added successfully!")
                        break
                    break

            # After successfully adding an employee, ask if the user wants to add more
            while True:
                ans = input("\nDo you want to add more employees? (Y/N): ")

                if ans.lower() == "n":
                    # If the user inputs 'n' (or 'N'), exit the loop and go back to the edit menu
                    self.edit_menu()
                    return

                if ans.lower() == "y":
                    # If user inputs 'y' (or 'Y'), break the loop & continue adding more employees
                    break
                # If user inputs anything else, display an error message and continue the loop
                print_error_message(
                    "Invalid input. Please enter 'Y' for Yes or 'N' for No."
                )

    def confirm_modify_employee(self, employee_id, emp_id, employee):
        """
        Edit employee details.

        Args:
            employee_id (int): The ID of the employee being modified.
            emp_id (int): The ID of the employee in the database.
            employee (Employee): The Employee object containing the employee's current details.

        Prompts the user to confirm modifications for the specified employee. If confirmed,
        allows the user to enter new details for the employee, validates the input, and updates
        the employee record in the database. If the operation is successful, prints a success
        message; otherwise, prints an error message.

        Returns:
            None
        """
        print_information_message(
            "Press 'Enter' to proceed with modifications or 'esc' to cancel..."
        )
        while True:
            modify_employee_key_pressed = keyboard.read_event(suppress=True).name

            if modify_employee_key_pressed == "esc":
                print_information_message("\nCanceling...")
                time.sleep(0.2)
                print_error_message("\nOperation Canceled.")
                pause_screen()
                self.modify_employee()
                return

            if modify_employee_key_pressed == "enter":
                print()
                print(f"\n*** Enter New Details for Employee ID: {employee_id} ***")
                time.sleep(0.2)

                new_name = (
                    get_valid_input(
                        f"\nName (alphabetic characters and spaces only, "
                        f"leave blank to keep '{employee.name}'): ",
                        Validator.validate_name,
                        allow_blank=True,
                    )
                    or employee.name
                )

                new_designation = (
                    get_valid_input(
                        f"\nDesignation (alphabetic characters and spaces only, "
                        f"leave blank to keep '{employee.designation}'): ",
                        Validator.validate_designation,
                        allow_blank=True,
                    )
                    or employee.designation
                )

                new_salary = (
                    get_valid_input(
                        f"\nSalary (must be a number, minimum 500, "
                        f"leave blank to keep '{employee.salary}'): ",
                        Validator.validate_salary,
                        allow_blank=True,
                    )
                    or employee.salary
                )

                new_age = (
                    get_valid_input(
                        f"\nAge (must be a number from 18 to 99, "
                        f"leave blank to keep '{employee.age}'): ",
                        Validator.validate_age,
                        allow_blank=True,
                    )
                    or employee.age
                )

                new_phone = (
                    get_valid_input(
                        f"\nPhone Number (must be a 10-digit number, "
                        f"leave blank to keep '{employee.phone}'): ",
                        Validator.validate_phone,
                        allow_blank=True,
                    )
                    or employee.phone
                )

                new_address = (
                    get_valid_input(
                        f"\nAddress (Leave blank to keep '{employee.address}'): ",
                        Validator.validate_address,
                        allow_blank=True,
                    )
                    or employee.address
                )

                updated_employee = Employee(
                    new_name,
                    new_designation,
                    float(new_salary),
                    int(new_age),
                    int(new_phone),
                    new_address,
                )

                print_information_message("Updating...")
                time.sleep(0.2)

                if self.database.update_employee_by_id(emp_id, updated_employee):
                    print_success_message("\nEmployee updated successfully!")
                    break

                if (
                    self.database.update_employee_by_id(emp_id, updated_employee)
                    is None
                ):
                    print_error_message("\nNo changes found.")
                    break
                print_error_message(
                    "\nLost connection to MongoDB while updating employee."
                )
                break

    def modify_employee(self):
        """
        Allow user to modify details of an existing employee.

        This method prompts the user to input the ID of the employee to modify,
        then displays the current details of the employee. The user can choose
        to proceed with modifications or cancel the operation. If modifications
        are confirmed, the user can input new details for the employee, which are
        then validated and updated in the database. The user can choose to modify
        another employee or return to the edit menu.

        Returns:
            None
        """
        while True:
            clear_screen()
            # Check if there are any employees
            if not self.database.get_employee_list():
                print_error_message("No employees found to modify.")
                pause_screen()
                break
            # Display the current list of employees
            self.display_employees_list()

            try:
                # Prompt the user to input the ID of the employee to modify
                employee_id = int(input("\nEnter Employee ID: "))

                # Get the corresponding employee ID from the ID mapping
                emp_id = self.id_mapping.get(employee_id)

                if emp_id:
                    # Clear the screen after pressing 'Enter' to proceed
                    clear_screen()
                    # Retrieve the employee details from the database
                    employee = self.database.get_employee_by_id(emp_id)

                    # Check if employee exists
                    if not employee:
                        print_error_message(
                            "Lost connection to MongoDB while getting employee details."
                        )
                        break

                    # Display the current details of the employee
                    if employee:
                        self.display_employee_details(employee_id, employee)

                        self.confirm_modify_employee(employee_id, emp_id, employee)
                else:
                    print_error_message(f"Employee not found with ID: {employee_id}")

                while True:
                    ans = input("\nDo you want to modify another employee? (Y/N): ")

                    if ans.lower() == "n":
                        self.edit_menu()
                        return

                    if ans.lower() == "y":
                        break
                    print_error_message(
                        "Invalid input. Please enter 'Y' for Yes or 'N' for No."
                    )

            except ValueError:
                print_error_message("Please enter a valid numeric ID.")
                pause_screen()

    def confirm_delete_employee(self, emp_id):
        """
        Delete an employee.

        Args:
            emp_id (int): The ID of the employee to be deleted.

        Prompts the user for confirmation before proceeding
        with the deletion of the specified employee.
        If confirmed, deletes the employee record from the database
        and prints a success message.
        If the operation fails or is canceled,
        appropriate error or cancelation messages are printed.

        Returns:
            None
        """
        # Prompt the user for confirmation before proceeding with deletion
        print_information_message(
            "Press 'Enter' to confirm deletion or 'esc' to cancel..."
        )
        while True:
            # Add a short delay to prevent instant confirmation due to fast key presses
            time.sleep(0.2)
            # Read the key pressed by the user while suppressing the input
            delete_employee_key_pressed = keyboard.read_event(suppress=True).name
            if delete_employee_key_pressed == "esc":
                print_information_message("\nCanceling...")
                time.sleep(0.2)
                print_error_message("\nOperation canceled.")
                pause_screen()
                self.delete_employee()
                return

            if delete_employee_key_pressed == "enter":
                print_information_message("\nDeleting...")
                time.sleep(0.2)
                # Remove the employee from the database
                if self.database.remove_employee_by_id(emp_id):
                    print_success_message(
                        "\nEmployee deleted successfully!"
                    )  # Print success message if deletion was successful
                break  # Exit the confirmation loop after processing the key press

    def delete_employee(self):
        """
        Allows the user to delete an employee from the database.
        The user is prompted to enter the ID of the employee to delete.
        Once confirmed, the employee is removed from the database.
        """
        while True:
            clear_screen()
            # Check if there are any employees
            if not self.database.get_employee_list():
                print_error_message("No employees found to delete.")
                pause_screen()
                break
            # Display the current list of employees
            self.display_employees_list()

            try:
                # Prompt the user to enter the ID of the employee to delete
                employee_id = int(input("\nEnter Employee ID: "))
                # Get the corresponding employee ID from the ID mapping
                emp_id = self.id_mapping.get(employee_id)

                if emp_id:
                    # Clear the screen after pressing 'Enter' to proceed
                    clear_screen()
                    # Retrieve the employee details from the database
                    employee = self.database.get_employee_by_id(emp_id)

                    # Check if employee exists
                    if not employee:
                        print_error_message(
                            "Lost connection to MongoDB while getting employee details."
                        )
                        break

                    # Display the current details of the employee
                    if employee:
                        self.display_employee_details(employee_id, employee)

                        self.confirm_delete_employee(emp_id)
                else:
                    print_error_message(f"Employee with ID {employee_id} not found.")

                # Prompt the user to indicate whether they want to delete another employee
                while True:
                    ans = input("\nDo you want to delete another employee? (Y/N): ")
                    if ans.lower() == "n":
                        # Exit the loop if the user chooses not to delete another employee
                        self.edit_menu()
                        return

                    if ans.lower() == "y":
                        # If the user inputs 'y' (or 'Y') or presses enter (input is empty),
                        # continue deleting another employee
                        break
                    # If the user inputs anything else, display an error message
                    print_error_message(
                        "Invalid input. Please enter 'Y' for Yes or 'N' for No."
                    )

            except ValueError:
                print_error_message("Please enter a valid numeric ID.")
                pause_screen()

    def search_record(self):
        """
        Allows the user to search for employee records based on name, designation, or address.
        The user is prompted to enter a search term, and matching records are displayed.
        If no matching records are found, an error message is displayed.
        The user can press 'enter' to continue searching or 'esc' to return to the edit menu.
        """
        while True:
            clear_screen()
            # Prompt the user to enter the search term
            search_term = input("Enter search term (name/designation/address): ")

            # Search for employees based on the provided search term
            if len(search_term) > 0:
                search_results = self.database.search_employee(search_term)
                if search_results:
                    clear_screen()
                    data = []

                    # Iterate through the search results and create a dictionary for each employee
                    for i, employee in enumerate(search_results, start=1):
                        employee_dict = {
                            "ID": i,
                            "Name": employee.name,
                            "Designation": employee.designation,
                            "Salary": employee.salary,
                            "Age": employee.age,
                            "Phone": employee.phone,
                            "Address": employee.address,
                        }
                        data.append(employee_dict)
                    print()
                    # Print each dictionary in 'data' using tabulate for a nicely formatted output
                    for data_dict in data:
                        print(tabulate(data_dict.items(), tablefmt="fancy_grid"))
                        print()  # Add an empty line between dictionaries
                else:
                    print_error_message(
                        f"No records found for {search_term}."
                    )  # Print error message if no matching records found

                # Wait for user input, allowing them to press 'enter' to continue searching
                # or 'esc' to return to the main menu
                print_information_message(
                    "Press 'enter' to continue searching or 'esc' to return to the main menu..."
                )
                while True:
                    search_record_key_pressed = keyboard.read_event(suppress=True).name
                    if search_record_key_pressed == "esc":
                        print_information_message("\nReturning to the edit menu...")
                        time.sleep(0.2)
                        self.main_menu()
                        return  # Return to the edit menu if 'esc' is pressed

                    if search_record_key_pressed == "enter":
                        print("")
                        break  # Continue searching if 'enter' is pressed
            else:
                print_information_message("Search term cannot be empty.")
                print("\n")
                pause_screen()

    def run(self):
        """
        Executes the Employee Management System.
        Clears the screen before displaying the login menu to prompt the user for authentication.
        """
        clear_screen()  # Clear the screen before displaying the login menu

        # Display the login menu to prompt the user for authentication
        self.login_menu()


# The special variable __name__ is set to "__main__" only when the script is executed directly
# If the script is imported as a module in another script,
# __name__ will be set to the module's name instead of "__main__"
# It is commonly used to include code that should only run
# when the script is executed directly, not when it's imported
if __name__ == "__main__":
    clear_screen()
    print_information_message("Starting Employee Management System...")

    while True:
        try:
            # Retrieve MongoDB URI from the environment variables
            mongodb_uri = os.environ.get("MONGODB_URI")

            # Create a Database instance using the provided URI
            database = Database(mongodb_uri)

            # Create a instance of the EmployeeManagementSystem class with the initialized database
            system = EmployeeManagementSystem(mongodb_uri)

            # Start the Employee Management System by invoking the 'run' method
            system.run()
            break  # Exit the loop if the system runs successfully
        except pymongo.errors.ConfigurationError:
            clear_screen()
            print_error_message("\nConnection to MongoDB server timed out.")
            # Inform the user about the option to retry or exit
            print_information_message("Press 'Enter' to retry or 'esc' to exit...")
            while True:
                # Read the key pressed by the user while suppressing the input
                key_pressed = keyboard.read_event(suppress=True).name
                if key_pressed == "esc":
                    # If the user presses 'esc', terminate the program
                    print_information_message("\nExiting...")
                    time.sleep(0.2)
                    clear_screen()
                    sys.exit(0)
                elif key_pressed == "enter":
                    # If the user presses 'enter', retry connecting to MongoDB
                    print_information_message("\nRetrying...")
                    time.sleep(0.2)
                    break
