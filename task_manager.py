"""
Task Manager: A command-line tool for managing team tasks using plain text files.
Users can add, view, and edit tasks stored in tasks.txt. Admins can
register users, view completed tasks, and generate reports in task_overview.txt
and user_overview.txt. Features include formatted task displays, overdue task
tracking, task editing with validation, and recursive input for task selection.
"""

# ====================
# Import the datetime module for date operations
from datetime import datetime
# Import os module for file existence check
import os

# Helper Functions
# ====================
# Define functions for file operations, task management, and reporting
def load_users():
    """
    Reads user credentials from user.txt and stores them in a dictionary for
    login validation. Each line in user.txt contains a username and password
    separated by a comma. If the file is missing, creates a new file with a
    default admin user (username: admin, password: adm1n).

    Returns:
        dict: A dictionary with usernames as keys and passwords as values.
    """
    # Initialize an empty dictionary for users
    users = {}
    # Attempt to read user.txt
    try:
        with open("user.txt", "r", encoding="utf-8-sig") as file:
            for line in file:
                # Split line into username and password
                parts = line.strip().split(", ")
                # Check if line has exactly two parts
                if len(parts) != 2:
                    # Warn about invalid line format
                    print(f"Warning: Skipping invalid line: '{line.strip()}'")
                    # Skip to next line
                    continue
                # Unpack username and password
                username, password = parts
                users[username] = password
    # Handle missing user.txt file
    except FileNotFoundError:
        print("Error: user.txt not found. Creating new file with admin.")
        # Create new user.txt file
        with open("user.txt", "w", encoding="utf-8-sig") as file:
            # Write default admin user
            file.write("admin, adm1n\n")
        # Add admin to dictionary
        users["admin"] = "adm1n"
    # Return the users dictionary
    return users


def save_user(username, password):
    """
    Adds a new user to user.txt by appending their username and password.
    Ensures the file ends with a newline to prevent formatting issues when
    adding new entries.

    Args:
        username (str): The username to add to the file.
        password (str): The password associated with the username.
    """
    # Attempt to ensure file ends with newline
    try:
        with open("user.txt", "r+", encoding="utf-8-sig") as file:
            content = file.read()
            # Check if content exists and lacks newline
            if content and not content.endswith("\n"):
                # Append newline
                file.write("\n")
    except FileNotFoundError:
        # File will be created in append mode
        pass
    # Append new user to file
    with open("user.txt", "a", encoding="utf-8-sig") as file:
        file.write(f"{username}, {password}\n")


def reg_user():
    """
    Registers a new user by collecting a unique username and password.
    Checks for duplicate usernames and ensures passwords match before saving
    to user.txt. Users can cancel by entering a blank username.
    """
    # Load existing users
    users = load_users()
    # Loop until valid input or cancellation
    while True:
        new_username = input("Enter new username (blank to cancel): ").strip()
        # Check if user cancelled
        if not new_username:
            # Notify cancellation
            print("Registration cancelled.")
            # Exit function
            return
        # Check for duplicate username
        if new_username in users:
            # Notify duplicate username
            print(f"Username '{new_username}' already exists. Try another.")
            # Continue loop
            continue
        # Prompt for new password
        new_password = input("Enter new password: ").strip()
        # Prompt to confirm password
        confirm_password = input("Confirm password: ").strip()
        # Check if passwords match
        if new_password != confirm_password:
            # Notify password mismatch
            print("Passwords do not match. Try again.")
            # Continue loop
            continue
        # Save new user to file
        save_user(new_username, new_password)
        # Notify successful registration
        print(f"User '{new_username}' registered successfully.")
        # Exit loop
        break


def save_new_task(username, title, description, assigned_date, due_date, completed):
    """
    Appends a new task to tasks.txt with details like username, title, and due
    date. Ensures the file ends with a newline to maintain proper formatting
    for subsequent entries.

    Args:
        username (str): The username to assign the task to.
        title (str): The title of the task.
        description (str): A brief description of the task.
        assigned_date (str): The date the task was assigned (YYYY-MM-DD).
        due_date (str): The due date for the task (YYYY-MM-DD).
        completed (str): Completion status ("Yes" or "No").
    """
    # Attempt to ensure file ends with newline
    try:
        with open("tasks.txt", "r+", encoding="utf-8-sig") as file:
            content = file.read()
            # Check if content exists and lacks newline
            if content and not content.endswith("\n"):
                # Append newline
                file.write("\n")
    except FileNotFoundError:
        # File will be created in append mode
        pass
    # Append new task to file
    with open("tasks.txt", "a", encoding="utf-8-sig") as file:
        # Write task details
        file.write(f"{username}, {title}, {description}, " + \
                    f"{assigned_date}, {due_date}, {completed}\n")


def load_tasks():
    """
    Reads all tasks from tasks.txt and converts them into a list of
    dictionaries. Each task includes username, title, description, assigned
    date, due date, and completion status. Creates an empty file if tasks.txt
    is missing.

    Returns:
        list: A list of dictionaries, each containing task details.
    """
    # Initialize empty list for tasks
    tasks = []

    try:
        with open("tasks.txt", "r", encoding="utf-8-sig") as file:
            for line in file:
                # Split line into task fields
                parts = line.strip().split(", ")
                # Check if line has exactly six fields
                if len(parts) != 6:
                    # Warn about invalid line format
                    print(f"Warning: Skipping invalid line: '{line.strip()}'")
                    # Skip to next line
                    continue
                # Add task dictionary to list
                tasks.append({
                    "username": parts[0],
                    "title": parts[1],
                    "description": parts[2],
                    "assigned_date": parts[3],
                    "due_date": parts[4],
                    "completed": parts[5],
                })
    # Handle missing tasks.txt file
    except FileNotFoundError:
        # Notify user about missing file
        print("Error: tasks.txt not found. Creating empty file.")
        # Create empty tasks.txt file
        with open("tasks.txt", "w", encoding="utf-8-sig") as file:
            # No content needed for empty file
            pass
    # Return the tasks list
    return tasks


def display_task(task):
    """
    Displays a task in a formatted text box with borders for clear
    presentation. Aligns fields like title and username for readability and
    returns the box width for use in demarcation lines.

    Args:
        task (dict): A dictionary containing task details.

    Returns:
        int: The width of the formatted box.
    """
    # Define task fields with aligned formatting
    lines = [
        f"{'Task':<18}{task['title']}",
        f"{'Assigned to':<18}{task['username']}",
        f"{'Description':<18}{task['description']}",
        f"{'Assigned on':<18}{task['assigned_date']}",
        f"{'Due by':<18}{task['due_date']}",
        f"{'Completed':<18}{task['completed']}",
    ]
    # Find length of longest line
    max_length = max(len(line) for line in lines)
    # Calculate box width with padding and borders
    box_width = max_length + 4
    # Print top border
    print(f"+{'-' * (box_width - 2)}+")
    # Print each formatted line
    for line in lines:
        # Print line with borders
        print(f"| {line:<{max_length}} |")
    # Print bottom border
    print(f"+{'-' * (box_width - 2)}+")
    # Add blank line after box
    print()
    # Return box width
    return box_width


def save_tasks(tasks):
    """
    Overwrites tasks.txt with the provided list of tasks, saving all details
    including username, title, description, dates, and completion status.

    Args:
        tasks (list): A list of task dictionaries to save.
    """
    # Open tasks.txt for writing
    with open("tasks.txt", "w", encoding="utf-8-sig") as file:
        # Process each task
        for task in tasks:
            # Write task details
            file.write(f"{task['username']}, {task['title']}, " + \
                        f"{task['description']}, {task['assigned_date']}, " + \
                        f"{task['due_date']}, {task['completed']}\n")


def is_overdue(due_date):
    """
    Checks if a task is overdue by comparing its due date to the current date.
    Handles invalid date formats by assuming the task is not overdue.

    Args:
        due_date (str): The task's due date in YYYY-MM-DD format.

    Returns:
        bool: True if the task is overdue, False otherwise.
    """
    # Attempt to parse due date
    try:
        # Convert due date to datetime object
        due = datetime.strptime(due_date, "%Y-%m-%d")
        # Get current date and time
        today = datetime.now()
        # Check if due date is past
        return due < today
    # Handle invalid date format
    except ValueError:
        # Assume task is not overdue
        return False


def calculate_task_stats(tasks):
    """
    Calculates statistics for all tasks, including total tasks, completed
    tasks, uncompleted tasks, overdue uncompleted tasks, and percentage
    metrics for incomplete and overdue tasks.

    Args:
        tasks (list): A list of task dictionaries.

    Returns:
        dict: A dictionary with task statistics (counts and percentages).
    """
    # Count total tasks
    total_tasks = len(tasks)
    # Count completed tasks
    completed = sum(1 for task in tasks if task["completed"] == "Yes")
    # Calculate uncompleted tasks
    uncompleted = total_tasks - completed
    # Count overdue uncompleted tasks
    overdue_uncompleted = sum(1 for task in tasks if task["completed"] == "No" and \
                              is_overdue(task["due_date"]))
    # Calculate percentage of incomplete tasks
    incomplete_percent = (uncompleted / total_tasks * 100) if total_tasks else 0
    # Calculate percentage of overdue tasks
    overdue_percent = (overdue_uncompleted / total_tasks * 100) if total_tasks else 0
    # Return statistics dictionary
    return {
        "total": total_tasks,
        "completed": completed,
        "uncompleted": uncompleted,
        "overdue_uncompleted": overdue_uncompleted,
        "incomplete_percent": round(incomplete_percent, 2),
        "overdue_percent": round(overdue_percent, 2)
    }


def calculate_user_stats(tasks, users):
    """
    Calculates user-specific statistics, including tasks assigned, completed
    tasks, overdue tasks, and percentages for total tasks, completion,
    incompletion, and overdue tasks per user.

    Args:
        tasks (list): A list of task dictionaries.
        users (dict): A dictionary of usernames and passwords.

    Returns:
        dict: A dictionary with total users, total tasks, and per-user stats.
    """
    # Count total tasks
    total_tasks = len(tasks)
    # Count total users
    total_users = len(users)
    # Initialize user statistics dictionary
    user_stats = {username: {"tasks": 0, "completed": 0, "overdue": 0}
                  for username in users}
    # Process each task
    for task in tasks:
        # Get task's username
        username = task["username"]
        # Check if user exists in stats
        if username in user_stats:
            # Increment task count
            user_stats[username]["tasks"] += 1
            # Check if task is completed
            if task["completed"] == "Yes":
                # Increment completed count
                user_stats[username]["completed"] += 1
            # Check if task is overdue
            elif is_overdue(task["due_date"]):
                # Increment overdue count
                user_stats[username]["overdue"] += 1
    # Calculate percentages for each user
    for username in user_stats:
        # Get number of tasks assigned
        tasks_assigned = user_stats[username]["tasks"]
        # Calculate percentage of total tasks
        user_stats[username]["percent_total"] = \
            (tasks_assigned / total_tasks * 100) if total_tasks else 0
        # Calculate percentage of completed tasks
        user_stats[username]["percent_completed"] = \
            (user_stats[username]["completed"] / tasks_assigned * 100) \
            if tasks_assigned else 0
        # Calculate percentage of incomplete tasks
        user_stats[username]["percent_incomplete"] = \
            ((tasks_assigned - user_stats[username]["completed"]) / \
             tasks_assigned * 100) if tasks_assigned else 0
        # Calculate percentage of overdue tasks
        user_stats[username]["percent_overdue"] = \
            (user_stats[username]["overdue"] / tasks_assigned * 100) \
            if tasks_assigned else 0
        # Round all percentages
        for key in ["percent_total", "percent_completed", "percent_incomplete",
                    "percent_overdue"]:
            # Round to two decimal places
            user_stats[username][key] = round(user_stats[username][key], 2)
    # Return statistics dictionary
    return {"total_users": total_users, "total_tasks": total_tasks,
            "user_stats": user_stats}


def generate_reports():
    """
    Generates two report files: task_overview.txt with overall task statistics
    and user_overview.txt with per-user statistics. Includes counts and
    percentages for tasks and user metrics.
    """
    # Load all tasks
    tasks = load_tasks()
    # Load all users
    users = load_users()
    # Calculate task statistics
    task_stats = calculate_task_stats(tasks)
    # Calculate user statistics
    user_stats = calculate_user_stats(tasks, users)
    # Attempt to write task overview
    try:
        # Open task_overview.txt for writing
        with open("task_overview.txt", "w", encoding="utf-8-sig") as file:
            # Write report title
            file.write("Task Overview\n")
            # Write total tasks
            file.write(f"Total tasks: {task_stats['total']}\n")
            # Write completed tasks
            file.write(f"Completed tasks: {task_stats['completed']}\n")
            # Write uncompleted tasks
            file.write(f"Uncompleted tasks: {task_stats['uncompleted']}\n")
            # Write overdue uncompleted tasks
            file.write(f"Overdue uncompleted tasks: " + \
                        f"{task_stats['overdue_uncompleted']}\n")
            # Write incomplete percentage
            file.write(f"Incomplete percentage: " + \
                        f"{task_stats['incomplete_percent']}%\n")
            # Write overdue percentage
            file.write(f"Overdue percentage: " + \
                        f"{task_stats['overdue_percent']}%\n")
    # Handle write error
    except IOError:
        # Notify write failure
        print("Error: Could not write to task_overview.txt")
        # Exit function
        return
    # Attempt to write user overview
    try:
        # Open user_overview.txt for writing
        with open("user_overview.txt", "w", encoding="utf-8-sig") as file:
            # Write report title
            file.write("User Overview\n")
            # Write total users
            file.write(f"Total users: {user_stats['total_users']}\n")
            # Write total tasks
            file.write(f"Total tasks: {user_stats['total_tasks']}\n")
            # Process each user's statistics
            for username, stats in user_stats["user_stats"].items():
                # Write user header
                file.write(f"\nUser: {username}\n")
                # Write tasks assigned
                file.write(f"Tasks assigned: {stats['tasks']}\n")
                # Write percentage of total tasks
                file.write(f"Percentage of total tasks: " + \
                            f"{stats['percent_total']}%\n")
                # Write percentage completed
                file.write(f"Percentage completed: " + \
                            f"{stats['percent_completed']}%\n")
                # Write percentage incomplete
                file.write(f"Percentage incomplete: " + \
                            f"{stats['percent_incomplete']}%\n")
                # Write percentage overdue
                file.write(f"Percentage overdue: " + \
                            f"{stats['percent_overdue']}%\n")
    # Handle write error
    except IOError:
        # Notify write failure
        print("Error: Could not write to user_overview.txt")
        # Exit function
        return
    # Notify successful report generation
    print("Reports generated: task_overview.txt, user_overview.txt")


def display_statistics():
    """
    Displays the contents of task_overview.txt and user_overview.txt in a
    formatted manner. Generates reports if the files are missing to ensure
    statistics are available.
    """
    # Check if both report files exist
    if not (os.path.exists("task_overview.txt") and
            os.path.exists("user_overview.txt")):
        # Notify missing reports
        print("Reports not found. Generating reports first.")
        # Generate missing reports
        generate_reports()
    # Attempt to display task overview
    try:
        # Print task overview header
        print("\n=== Task Overview ===")
        # Open task_overview.txt for reading
        with open("task_overview.txt", "r", encoding="utf-8-sig") as file:
            # Print file contents
            print(file.read())
    # Handle missing file
    except FileNotFoundError:
        # Notify missing file
        print("Error: task_overview.txt not found.")
        # Exit function
        return
    # Handle read error
    except IOError:
        # Notify read failure
        print("Error: Could not read task_overview.txt")
        # Exit function
        return
    # Attempt to display user overview
    try:
        # Print user overview header
        print("\n=== User Overview ===")
        # Open user_overview.txt for reading
        with open("user_overview.txt", "r", encoding="utf-8-sig") as file:
            # Print file contents
            print(file.read())

    except FileNotFoundError:
        # Notify missing file
        print("Error: user_overview.txt not found.")
        # Exit function
        return

    except IOError:
        # Notify read failure
        print("Error: Could not read user_overview.txt")
        # Exit function
        return


def get_valid_task_number(user_tasks):
    """
    Recursively prompts the user for a valid task number (1 to the number of
    tasks or -1 to exit). Validates input and handles errors to ensure a
    correct selection.

    Args:
        user_tasks (list): A list of tasks assigned to the user.

    Returns:
        int: A valid task number (1 to len(user_tasks)) or -1 to return.
    """
    # Attempt to get user input
    try:
        # Prompt for task number
        choice = input("Enter task number (-1 to main menu): ").strip()
        # Convert input to integer
        choice = int(choice)
        # Check if user wants to return
        if choice == -1:
            # Return exit code
            return -1
        # Check if choice is within valid range
        if 1 <= choice <= len(user_tasks):
            # Return valid task number
            return choice
        # Notify invalid task number
        print("Invalid task number. Try again.")
        # Recursively prompt again
        return get_valid_task_number(user_tasks)
    # Handle non-integer input
    except ValueError:
        # Notify invalid input
        print("Please enter a valid number.")
        # Recursively prompt again
        return get_valid_task_number(user_tasks)


def manage_my_tasks(current_user):
    """
    Displays the user's tasks in a numbered list and allows them to mark tasks
    as complete or edit task details (username or due date). Uses recursive
    input validation for task selection and restricts editing of completed
    tasks.

    Args:
        current_user (str): The username of the logged-in user.
    """
    tasks = load_tasks()
    # Filter tasks for current user
    user_tasks = [task for task in tasks if task["username"] == current_user]
    # Check if user has tasks
    if not user_tasks:
        print(f"No tasks assigned to you, {current_user}.")
        # Exit function
        return
    # Print tasks header
    print(f"\nMy Tasks ({current_user})")
    # Display each task with index
    for idx, task in enumerate(user_tasks, 1):
        # Print task number
        print(f"\nTask {idx}:")
        # Display task in formatted box
        display_task(task)
    # Get valid task number
    choice = get_valid_task_number(user_tasks)
    # Check if user wants to return to main menu
    if choice == -1:
        # Exit function
        return
    # Get selected task
    selected_task = user_tasks[choice - 1]
    # Find task index in full task list
    task_index = tasks.index(selected_task)
    # Print action menu
    print("\nSelect an action:")
    # Option to mark complete
    print("c - mark as complete")
    # Option to edit task
    print("e - edit task")
    # Get action choice
    action = input(": ").lower()
    # Handle mark complete action
    if action == "c":
        # Update task status
        tasks[task_index]["completed"] = "Yes"
        # Save updated tasks
        save_tasks(tasks)
        # Notify completion
        print(f"Task '{selected_task['title']}' marked complete.")
    # Handle edit task action
    elif action == "e":
        # Check if task is completed
        if selected_task["completed"] == "Yes":
            # Notify cannot edit completed task
            print("Cannot edit completed task.")
            # Exit function
            return
        # Print edit menu
        print("\nSelect edit option:")
        # Option to edit username
        print("1 - edit username")
        # Option to edit due date
        print("2 - edit due date")
        # Option to edit both
        print("3 - edit both")
        # Get edit choice
        edit_choice = input(": ")
        # Handle username edit
        if edit_choice in ["1", "3"]:
            # Prompt for new username
            new_username = input("Enter new username: ").strip()
            # Validate username exists
            if new_username not in load_users():
                # Notify invalid username
                print(f"User '{new_username}' does not exist.")
                # Exit function
                return
            # Update task username
            tasks[task_index]["username"] = new_username
        # Handle due date edit
        if edit_choice in ["2", "3"]:
            # Prompt for new due date
            new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
            # Attempt to validate date
            try:
                # Parse date to check format
                datetime.strptime(new_due_date, "%Y-%m-%d")
            # Handle invalid date
            except ValueError:
                # Notify invalid format
                print("Invalid date format. Use YYYY-MM-DD.")
                # Exit function
                return
            # Update task due date
            tasks[task_index]["due_date"] = new_due_date
        # Check if edit was valid
        if edit_choice in ["1", "2", "3"]:
            # Save updated tasks
            save_tasks(tasks)
            # Notify task updated
            print(f"Task '{selected_task['title']}' updated.")
        # Handle invalid edit choice
        else:
            print("Invalid edit option.")
    else:
        print("Invalid action. Choose 'c' or 'e'.")


def delete_task():
    """
    Allows the admin to delete a task by selecting its number from a
    numbered list of all tasks. Updates tasks.txt after deletion and
    supports cancellation.
    """

    tasks = load_tasks()

    if not tasks:
        # Notify no tasks to delete
        print("No tasks to delete.")
        # Exit function
        return

    print("\nSelect a task to delete:")
    # Display each task with index
    for idx, task in enumerate(tasks, 1):
        # Print task number
        print(f"\nTask {idx}:")
        display_task(task)
    # Attempt to get user choice
    try:
        choice = int(input("Enter task number to delete (0 to cancel): "))
        # Check if user cancelled
        if choice == 0:
            print("Deletion cancelled.")
            return
        # Check if choice is valid
        if 1 <= choice <= len(tasks):
            # Remove selected task
            deleted_task = tasks.pop(choice - 1)
            # Save updated tasks
            save_tasks(tasks)
            # Notify successful deletion
            print(f"Task '{deleted_task['title']}' deleted successfully.")
        # Handle invalid task number
        else:
            print("Invalid task number. Try again.")
    # Handle non-integer input
    except ValueError:
        print("Please enter a valid number.")

# Login Section
# ====================
# Define function for user authentication
def login():
    """
    Authenticates a user by checking their username and password against
    user.txt. Prompts repeatedly until valid credentials are provided,
    displaying error messages for invalid inputs.

    Returns:
        str: The username of the authenticated user.
    """
    # Load user credentials
    users = load_users()

    print("Welcome to the Task Manager. Please log in.")
    # Loop until valid login
    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        # Check if username exists
        if username not in users:
            print(f"Username '{username}' does not exist. Try again.")
        # Check if password matches
        elif users[username] != password:
            print("Incorrect password. Try again.")
        # Handle successful login
        else:
            print(f"Login successful. Welcome, {username}.")
            # Return username
            return username


# Menu Program
# ====================
# Define main program for menu-driven interface
def main():
    """
    Displays a menu for task management and processes user selections.
    Supports task creation, viewing, editing, deletion, and reporting
    (admin-only). Checks user privileges to restrict admin-only features.
    """
    # Authenticate user
    current_user = login()
    # Check if user is admin
    is_admin = current_user == "admin"
    # Run menu loop
    while True:
        print("\nPlease select one of the following options:")
        # Show admin-only option if applicable
        if is_admin:
            # Option to register user
            print("r - register user")
        # Option to add task
        print("a - add task")
        # Option to view all tasks
        print("va - view all tasks")
        # Option to view user's tasks
        print("vm - view my tasks")
        # Show admin-only options if applicable
        if is_admin:
            # Option to view completed tasks
            print("vc - view completed tasks")
            # Option to delete a task
            print("del - delete a task")
            # Option to display statistics
            print("ds - display statistics")
            # Option to generate reports
            print("gr - generate reports")
        # Option to exit
        print("e - exit")
        # Get user choice
        menu = input(": ").lower()
        # Handle admin-only user registration
        if menu == "r" and is_admin:
            # Register new user
            reg_user()
        # Handle add task
        elif menu == "a":
            # Prompt for username to assign task
            username = input("Enter username to assign task: ").strip()
            # Validate username exists
            if username not in load_users():
                print(f"User '{username}' does not exist. Try again.")
                # Continue loop
                continue
            # Prompt for task title
            title = input("Enter task title: ").strip()
            # Prompt for task description
            description = input("Enter task description: ").strip()
            # Prompt for due date
            due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            # Attempt to validate date
            try:
                # Parse due date to check format
                datetime.strptime(due_date, "%Y-%m-%d")
            # Handle invalid date
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD. Try again.")
                # Continue loop
                continue
            # Get current date for assigned date
            assigned_date = datetime.now().strftime("%Y-%m-%d")
            # Save new task
            save_new_task(username, title, description, assigned_date,
                          due_date, "No")
            # Notify task added
            print(f"Task '{title}' added for {username}.")
        # Handle view all tasks
        elif menu == "va":
            # Load all tasks
            tasks = load_tasks()
            # Check if tasks exist
            if not tasks:
                # Notify no tasks
                print("No tasks to display.")
            # Display tasks
            else:
                # Print tasks header
                print("\nAll Tasks")
                # Find maximum box width
                max_length = max(display_task(task) for task in tasks)
                # Print demarcation line
                print("-" * max_length)
        # Handle view my tasks
        elif menu == "vm":
            # Manage user's tasks
            manage_my_tasks(current_user)
        # Handle admin-only view completed tasks
        elif menu == "vc" and is_admin:
            # Load all tasks
            tasks = load_tasks()
            # Filter completed tasks
            completed_tasks = [task for task in tasks if task["completed"] == "Yes"]
            # Check if completed tasks exist
            if not completed_tasks:
                # Notify no completed tasks
                print("No completed tasks to display.")
            # Display completed tasks
            else:
                # Print completed tasks header
                print("\nCompleted Tasks")
                # Find maximum box width
                max_length = max(display_task(task) for task in completed_tasks)
                # Print demarcation line
                print("-" * max_length)
        # Handle admin-only delete task
        elif menu == "del" and is_admin:
            # Delete a task
            delete_task()
        # Handle admin-only display statistics
        elif menu == "ds" and is_admin:
            # Generate reports
            generate_reports()
            # Display statistics
            display_statistics()
        # Handle admin-only generate reports
        elif menu == "gr" and is_admin:
            # Generate reports
            generate_reports()
        # Handle exit
        elif menu == "e":
            print(f"\nGoodbye, {current_user}. See you next time.")
            # Exit loop
            break
        else:
            print("Invalid option. Please select a valid option.")


if __name__ == "__main__":
    main()