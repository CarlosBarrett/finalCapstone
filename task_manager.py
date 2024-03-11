# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d-%m-%Y"


# Function to read tasks from file
def read_tasks_from_file():
    '''
    Reads tasks and content within the file tasks.txt
    if the file exists.
    '''
    task_list = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                task_data = line.strip().split(";")
                task = {
                    "username": task_data[0],
                    "title": task_data[1],
                    "description": task_data[2],
                    "due_date": datetime.strptime(task_data[3], DATETIME_STRING_FORMAT),
                    "assigned_date": datetime.strptime(task_data[4], DATETIME_STRING_FORMAT),
                    "completed": task_data[5] == "Yes"
                }
                task_list.append(task)
    return task_list


# Function to write tasks to file
def write_tasks_to_file(task_list):
    '''
    Function to write tasks to .txt file and creates
    one if it doesn't already exist.
    '''
    with open("tasks.txt", "a+") as file:
        for task in task_list:
            completed = "Yes" if task["completed"] else "No"
            file.write(f"{task['username']};{task['title']};{task['description']};"
                       f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{completed}\n")


# Function to register a new user
def register_user(username_password):
    '''
    Function to register a new user and will
    give an error if the user name already exists
    or the password doesn't match on confirmation.
    '''
    while True:
        new_username = input("New Username: ")
        if new_username not in username_password:
            new_password = input("New Password: ")
            confirm_password = input("Confirm Password: ")
            if new_password == confirm_password:
                print("New user added")
                username_password[new_username] = new_password
                with open("user.txt", "a") as file:
                    file.write(f"{new_username};{new_password}\n")
                break
            else:
                print("ERROR: Passwords do not match")
        else:
            print("ERROR: Username already in use")


# Function to add a new task
def add_task(task_list):
    '''
    Function to add new tasks and the content within
    including title, description, due date and the user
    it is assigned to.
    '''
    task_username = input("Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (DD-MM-YYYY): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            if due_date_time.date() >= date.today():
                break
            else:
                print("ERROR: Due date must be in the future")
        except ValueError:
            print("ERROR: Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    write_tasks_to_file(task_list)
    print("Task successfully added.")


# Function to view all tasks
def view_all(task_list):
    '''
    Function to view all tasks with due date,
    date the task was assigned, title, description
    and if the task has been completed or not.
    '''
    for task in task_list:
        print("-" *80)
        print("Title:", task["title"])
        print("Assigned to:", task["username"])
        print("Date Assigned:", task["assigned_date"].strftime(DATETIME_STRING_FORMAT))
        print("Due Date:", task["due_date"].strftime(DATETIME_STRING_FORMAT))
        print("Description:", task["description"])
        print("Completed:", "Yes" if task["completed"] else "No")
        print("-" *80)


# Function to view tasks assigned to the current user
def view_my_tasks(task_list, curr_user):
    '''
    Function to see all of the current users tasks
    '''
    for task in task_list:
        if task["username"] == curr_user:
            print("\n-" *80)
            print("Title:", task["title"])
            print("Date Assigned:", task["assigned_date"].strftime(DATETIME_STRING_FORMAT))
            print("Due Date:", task["due_date"].strftime(DATETIME_STRING_FORMAT))
            print("Description:", task["description"])
            print("Completed:", "Yes" if task["completed"] else "No")
            print("-"*80)


# Function to edit a task
def edit_task(task_list, curr_user):
    '''
    Function to edit tasks and mark as complete or edit the due date
    '''
    task_title = input("Enter the title of the task you want to edit: ")
    found = False
    for task in task_list:
        if task["title"] == task_title and task["username"] == curr_user:
            found = True
            print("Task found. You can edit it.")
            while True:
                print("1. Mark as completed")
                print("2. Edit description")
                print("3. Edit due date")
                print("4. Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    task["completed"] = True
                    print("Task marked as completed.")
                    break
                elif choice == "2":
                    new_description = input("Enter the new description: ")
                    task["description"] = new_description
                    print("Description updated.")
                elif choice == "3":
                    while True:
                        new_due_date = input("Enter the new due date (DD-MM-YYYY): ")
                        try:
                            due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            if due_date_time.date() >= date.today():
                                task["due_date"] = due_date_time
                                print("Due date updated.")
                                break
                            else:
                                print("ERROR: Due date must be in the future")
                        except ValueError:
                            print("ERROR: Invalid datetime format. Please use the format specified")
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
            write_tasks_to_file(task_list)
            break
    if not found:
        print("Task not found or you don't have permission to edit it.")


# Function to generate a task report
def generate_task_report(task_list):
    '''
    Function to generate a task report and write it to a file
    named task_report.txt
    '''
    today = datetime.today()

    tasks_total = len(task_list)
    tasks_completed = sum(task['completed'] for task in task_list)
    tasks_uncompleted = tasks_total - tasks_completed
    tasks_overdue = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < today.date())

    percentage_incomplete = (tasks_uncompleted / tasks_total) * 100 if tasks_total > 0 else 0
    percentage_overdue = (tasks_overdue / tasks_total) * 100 if tasks_total > 0 else 0

    with open("task_report.txt", "w") as task_report:
        task_report.write("Task Report\n\n")
        task_report.write(f"Total number of tasks: {tasks_total}\n")
        task_report.write(f"Total number of completed tasks: {tasks_completed}\n")
        task_report.write(f"Total number of uncompleted tasks: {tasks_uncompleted}\n")
        task_report.write(f"Total number of tasks incomplete and overdue: {tasks_overdue}\n")
        task_report.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
        task_report.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n\n")

        for index, task in enumerate(task_list, start=1):
            task_report.write(f"Task {index}:\n")
            task_report.write(f"Title: {task['title']}\n")
            task_report.write(f"Assigned to: {task['username']}\n")
            task_report.write(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            task_report.write(f"Description: {task['description']}\n")
            status = 'Completed' if task['completed'] else 'Not Completed'
            task_report.write(f"Status: {status}\n")
            task_report.write("\n")


# Main function
def main():
    '''
    This function runs the programs main features
    - Check for file existance
    - Create file if it doesn't exist
    - Read file if found
    - Read tasks
    - User login
    - Main menu
    '''
    # Create user.txt if it doesn't exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as file:
            file.write("admin;password\n")

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    # Read usernames and passwords from user.txt
    with open("user.txt", "r") as file:
        lines = file.readlines()
        username_password = {line.split(";")[0]: line.split(";")[1].strip() for line in lines}

    # Read tasks from tasks.txt
    task_list = read_tasks_from_file()

    # Login
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if username in username_password and username_password[username] == password:
            print("Login successful!")
            break
        else:
            print("Invalid username or password. Please try again.")

    # Main menu
    while True:
        print("\n")
        print("MAIN MENU")
        print("1. Register a new user")
        print("2. Add a task")
        print("3. View all tasks")
        print("4. View my tasks")
        print("5. Edit a task")
        print("6. Generate report (ADMIN)")
        print("7. Statistics (ADMIN)")
        print("8. Exit")
        print("\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            register_user(username_password)
        elif choice == "2":
            add_task(task_list)
        elif choice == "3":
            view_all(task_list)
        elif choice == "4":
            view_my_tasks(task_list, username)
        elif choice == "5":
            edit_task(task_list, username)
        elif choice == "6":
            if username == 'admin':
                generate_task_report(task_list)
                print("Task report generated.")
            else:
                print("Only admin users can generate reports.")
        elif choice == "7":
            if username == "admin":
                num_users = len(username_password.keys())
                num_tasks = len(task_list)
                print("-" *80)
                print(f"Number of users: {num_users}")
                print(f"Number of tasks: {num_tasks}")
                print("-" *80)
            else:
                print("Only admin users can display statistics.")
        elif choice == "8":
            print("Thank you, Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Called main menu function
if __name__ == "__main__":
    main()