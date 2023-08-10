# Task Manager
### A simple task manager program that allows users to add tasks, mark them as complete, and edit attributes. Admin user can also generate .txt reports summarising user and task statistics.

<br>

#### FUNCTIONALITY OVERVIEW

- creates .txt file of users / passwords
- creates .txt file listing tasks and their attributes
- allows users to:
	- register new users
	- add tasks to task list
	- view list of all tasks
	- view list of tasks assigned to that user
	- edit details of tasks assigned to that user
	- view list of completed tasks assigned to that user
- additionally admin user can:
	- generate summary reports of user and task statistics
	- display statistics on screen
<br>

#### DATA STORAGE

.txt file of users / passwords:

- creates file in the current working directory if not already existing
- default files name = "user.txt"
- user and password stored as CSV (separator = ";")
- passwords are unhashed

.txt file listing tasks and their attributes:
- creates file in the current working directory if not already existing
- default files name = "tasks.txt"
- task attributes stored as CSV (separator = ";")
- task attributes:
  1. user task assigned to
  1. task name
  1. task description
  1. due date
  1. creation date
  1. task completion (Yes/No)
<br>

#### FUNCTIONALITY

#### Register a new user  `reg_user()`
- allows user to enter username and password
- checks against existing users in users.txt to ensure no duplication of usernames
- adds user and passoword to users.txt
<br>

#### Adding a new task  `add_task()`
- allows a user to add a new task to task.txt file
- prompts the user for the following: 
  1. username of the person whom the task is assigned to
  1. title of a task
  1. description of the task
  1. due date of the task
- displays the user input data and asks user to confirm details
- if user confirms then task is added to tasks.txt
<br>

#### View all tasks  `view_all()`
- reads the tasks from task.txt file and prints to the console
- displays all tasks assigned to all users
- calculates the completion status of each task (completed / overdue / ongoing)
<br>

#### View tasks assigned to the user  `view_mine()`
- displays list of uncompleted tasks assigned to the user
- only displays tasks not marked as completed
- calculates the completion status of each task (overdue / ongoing)
- allows the user to select a task to edit its attributes, to:
  - mark task as completed             `mark_task_as_complete()`
  - edit who the task is assigned to   `edit_task_assignee()`
  - edit the due date of the task      `edit_task_due_date()`
- if any edits are made the task, tasks.txt is updated to reflect updates
<br>

#### View tasks assigned to the user that have already been completed  `view_my_completed()`
- reads the tasks from task.txt file and prints to the console
- displays only tasks assigned to the user that have been marked as completed
<br>

#### Generate user and task statistics reports  `generate_reports()`
- option only available to admin user
- creates two reports; user_overview.txt and task_overview.txt
- reports are created in the current working directory
- if previous reports already exist they are overwritten with the new reports
- user_overview.txt contains:
  - the number of users and tasks
  - summary of how many tasks assigned to each user
  - details for each user showing:
    - how many tasks area assigned to them
    - how many tasks have been completed
    - how many tasks have are outstanding
    - how many tasks have are overdue
- task_overview.txt contains:
  - total number of tasks
  - how many tasks have been completed
  - how many tasks have are outstanding
  - how many tasks have are overdue
<br>

#### Display task and user statistics  `display_statistics()`
- option only available to admin user
- displays number of users and number of tasks in the console
