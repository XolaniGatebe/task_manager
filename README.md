# Task Manager

## About
Task Manager is a Python-based application designed to help users organize and track tasks efficiently. It supports creating, updating, deleting, and viewing tasks, making it ideal for personal productivity or small team project management. This project demonstrates core Python programming, file handling, and user interface design (CLI or GUI). This README provides setup instructions, usage details, and guidance for contributing to the project. For questions, feel free to open an issue on the GitHub repository.

## Setup
Follow these steps to set up Task Manager locally:

1. **Fork the repository**:
   - Click the 'Fork' button at the top right corner of the [repository's GitHub page](https://github.com/XolaniGatebe/task_manager).
   - This creates a copy in your GitHub account.

2. **Clone your forked repository**:
     ```bash
     git clone https://github.com/XolaniGatebe/task_manager.git
     ```
   - Navigate to the directory:
     ```bash
     cd task_manager
     ```

3. **Install Python libraries**:
   - Ensure Python 3.8+ is installed (`python --version` or `python3 --version`).
   - Install dependencies (e.g., `tkinter` for GUI, included with Python):
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the application**:
   - Execute the main script:
     ```bash
     python3 task_manager.py
     ```
   - The app should launch (CLI prompts or GUI window, depending on implementation).

5. **Navigate to the app**:
   - For CLI: Follow on-screen prompts to manage tasks.
   - For GUI: Interact with the graphical interface (e.g., click “Add Task”).
   - No server is required for local use; tasks are saved to a local file (e.g., `tasks.txt`).

## Making Changes and Pushing to Your Fork
After modifying `task_manager`, push changes to your forked GitHub repository:

```bash
git add -u
git commit -m "Your commit message (e.g., Added task priority feature)"
git push origin main
