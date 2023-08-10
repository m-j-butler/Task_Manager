import os
from datetime import datetime, date
import re

def set_up_tasks():
    '''Compiles task list from tasks.txt file.
    Creates tasks.txt if doesn't already exist.'''

    # create tasks.txt if it doesn't exist
    if not os.path.exists('tasks.txt'):
        with open('tasks.txt', 'w'):
            pass

    # compile list of tasks from source file
    with open('tasks.txt', 'r') as file:

        for index, line in enumerate(file):
            task = {}

            task_components = line.split(';')

            task['username'] = task_components[0]
            task['title'] = task_components[1]
            task['description'] = task_components[2]
            task['due_date'] = datetime.strptime(task_components[3], '%Y-%m-%d').date()
            task['assigned_date'] = datetime.strptime(task_components[4], '%Y-%m-%d').date()
            task['completed'] = False if task_components[5][:2] == 'No' else True           
            task['temp_ID'] = index

            task_list.append(task)



def set_up_users():
    '''Compiles lists of users / passwords from users.txt file.
    Creates users.txt if doesn't already exist.
        '''
    
    # create users.txt if it doesn't exist, with a default admin account
    if not os.path.exists('users.txt'):
        with open('users.txt', 'w') as default_file:
            default_file.write('admin;password\n')

    # create list of usernames and passwords from users.txt file
    with open('users.txt', 'r') as file:
        
        for line in file:
            username, password = line.split(';')
            # slicing password to remove newline character
            username_password[username] = password[:-1]



def login():
    '''requests username and password credentials and logs user in'''
    
    global curr_user

    while True:
        print('\nLOGIN')

        curr_user = input('Username: ')
        curr_pass = input('Password: ')
        if curr_user not in username_password.keys():
            print('Error. Incorrect user / password')
            continue
        elif username_password[curr_user] != curr_pass:
            print('Error. Incorrect user / password')
            continue
        else:
            print('Login successful')
            break
    
    main_menu()



def main_menu():
    '''Displays the main menu and requests user input to select option.
    Admin user has additional options available.'''

    while True:

        print('\nSelect one of the following options below:')
        print('r  - Registering a user')
        print('a  - Adding a task')
        print('va - View all tasks')
        print('vm - View my current tasks')
        print('vc - View my completed tasks')
        if curr_user == 'admin':
            print('gr - Generate reports')
            print('ds - Display statistics')
        print('e  - Exit')
        menu = input().lower()

        if menu == 'r':
            reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine()

        elif menu == 'vc':
            view_my_completed()
        
        elif menu == 'ds' and curr_user == 'admin': 
            display_statistics()

        elif menu == 'gr' and curr_user == 'admin':
            generate_reports()

        elif menu == 'e':
            print('-- exiting program --')
            exit()

        else:
            print('Invalid input. Please select either "r", "a", "va", "vm", "vc",', ['\b', '"gr", "ds"'][curr_user == "admin"], 'or "e"')



def reg_user():
    '''Takes user imput to create new user and password, and adds to users.txt file.'''
    
    # request input of new username
    while True:
        new_username = input('New Username: ')
        
        # check username is not blank
        if not new_username:
            print('Error. Username cannot be blank.')
            continue

        # check for invalid characters
        if re.match('^[\w\-_]+$', new_username) is None:
            print('Error. Invalid character(s) used.')
            print('Username can only contain letters, numbers, hyphens and underscores.')
            continue

        # check username is not already taken
        if new_username in username_password.keys():
            print('Error. Username already taken.')
            continue

        break

    # request input of a new password
    while True:
        while True:
            new_password = input('New Password: ')
            
            # check password is not blank
            if not new_password:
                print('Error. Password cannot be blank.')
                continue

            # check for invalid characters
            if re.match('^[\w\-_]+$', new_password) is None:
                print('Error. Invalid character(s) used.')
                print('Password can only contain letters, numbers, hyphens and underscores.')
                continue    

            break

        # request input of password confirmation and check they match
        confirm_password = input('Confirm Password: ')
        if new_password != confirm_password:
            print('Error. Passwords do not match.')
            continue
        
        break

    # add new user credentials to username_password dict
    username_password[new_username] = new_password

    # append new user credentials to users.txt file
    try:
        with open('users.txt', 'a') as f:
            f.write(f'{new_username};{new_password}\n')
    except:
        print('Error. Something went wrong. User not added.')



def add_task():
    '''Allows a user to add a new task to task.txt file
    Prompts the user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - The due date of the task.'''

    # task assignee
    while True:
        task_username = input('Name of person assigned to task: ')    
        if task_username not in username_password.keys():
            print('User does not exist.')
            while True:
                print('Select option:')
                print('t - try again')
                print('c - cancel')
                option = input().lower()
                if option == 't':
                    break
                
                if option == 'c':
                    return
                
                else:
                    print('Invalid input. Please select either "t" or "c"')   
        
        else:
            break
    
    # task title
    while True:
        task_title = input('Title of Task: ')
        if task_title:
            break
        
        else:
            print('Error. Task title cannot be blank.')

    # task description
    while True:
        task_description = input('Description of Task: ')
        if task_description:
            break
        
        else:
            print('Error. Task description cannot be blank.')

    # task due date
    while True:
        try:
            raw_date = input('Due date of task (YYYY-MM-DD): ')
            due_date = datetime.strptime(raw_date, '%Y-%m-%d').date()
            
            # check due date is not in the past
            if due_date < date.today():
                print('Error. Due date cannot be in the past.')
                continue
           
            break

        except ValueError:
            print('Invalid datetime format. Please use the format specified.')

    # display details of task
    print('\n')
    print(task_title)
    print(f'Assigned to:            {task_username}')
    print(f'Due Date:               {due_date}')
    print(task_description)
    
    # request user to confirm details of task  
    while True:
        confirm = input('\nConfirm details of new task. Enter "Y" to confirm or "N" to cancel: ').upper()
        if confirm == 'N':
            print('Task not saved.')
            return
        
        if confirm != 'Y':
            print('Invalid input. Please enter either "Y" or "N"')
            continue
        
        break

# add task details to task_list
    new_task = {'username': task_username,
                'title': task_title,
                'description': task_description,
                'due_date': due_date,
                'assigned_date': date.today(),
                'completed': False,
                'temp_ID': str(len(task_list))
                } 
    
    task_list.append(new_task)
    
    # append new task details to tasks.txt file
    try:
        with open('tasks.txt', 'a') as f:

            f.write(f'{task_username};')
            f.write(f'{task_title};')
            f.write(f'{task_description};')
            f.write(f'{due_date.strftime("%Y-%m-%d")};')
            f.write(f'{date.today().strftime("%Y-%m-%d")};')
            f.write(f'No\n')
            
        print('Task successfully added.')

    except:
        print('An error occured. Unable to save new task to file.')



def write_task_list_to_file(task_list):
    '''Writes updated task list to tasks.txt file'''

    try:
        with open('tasks.txt', 'w') as f:
            for task in task_list:
                f.write(f'{task["username"]};')
                f.write(f'{task["title"]};')
                f.write(f'{task["description"]};')
                f.write(f'{task["due_date"].strftime("%Y-%m-%d")};')
                f.write(f'{task["assigned_date"].strftime("%Y-%m-%d")};')
                f.write(f'{"Yes" if task["completed"] else "No"}\n')

        print('Task file successfully updated.')

    except:
        print('An unexpected error occured.')



def view_all():
    '''Reads the tasks from task.txt file and prints to the console.'''
    
    print()
    if len(task_list) == 0:
        print('No tasks logged.')

    for task in task_list:
        status = 'Completed' if task['completed'] else 'OVERDUE' if task['due_date'] < date.today() else 'Ongoing'

        print(f'Task:                   {task["title"]}')
        print(f'Assigned to:            {task["username"]}')
        print(f'Date Assigned:          {task["assigned_date"].strftime("%Y-%m-%d")}')
        print(f'Due Date:               {task["due_date"].strftime("%Y-%m-%d")}')
        print(f'Status:                 {status}')
        print(f'Task Description:       {task["description"]}\n')



def view_mine():
    '''Displays list of uncompleted tasks assigned to the user.'''

    outstanding_user_tasks = []
    # compile list of uncompleted tasks assigned to the user
    for task in task_list:
        if task['username'] == curr_user and task['completed'] == False:
            outstanding_user_tasks.append(task)

    if len(outstanding_user_tasks) == 0:
        print('\nYou have no outstanding tasks.')
        return

    print()
    for index, task in enumerate(outstanding_user_tasks, start=1):
        status = 'Completed' if task['completed'] else 'OVERDUE' if task['due_date'] < date.today() else 'Ongoing'
        
        print(f'Task {f"{index}:":<3}                {task["title"]}')
        print(f'Assigned to:            {task["username"]}')
        print(f'Date Assigned:          {task["assigned_date"].strftime("%Y-%m-%d")}')
        print(f'Due Date:               {task["due_date"].strftime("%Y-%m-%d")}')
        print(f'Status:                 {status}')
        print(f'Task Description:       {task["description"]}\n')


    # allow user to select task
    while True:
        selection = input('Select a task number or enter "-1" to return to the main menu: ')
        
        if selection == '-1':
            return
        
        if not selection.isdecimal():
            print('Error. Invalid selection.')
            continue

        if not int(selection) in range(1, len(outstanding_user_tasks) + 1):
            print('Error. Invalid selection.')
            continue

        break


    temp_ID_of_selected_task = int(outstanding_user_tasks[int(selection) - 1]['temp_ID'])
    
    print(f'\n\nTask {selection}: {task_list[temp_ID_of_selected_task]["title"]}')
    print('Select option:')
    print('m - mark the task as complete')
    print('a - edit who the task is assigned to')
    print('d - edit the due date of the task')
    print('x - cancel')


    while True:
        option = input()

        if option == 'x':
            return
        
        elif option == 'm':
            mark_task_as_complete(temp_ID_of_selected_task)
        
        elif option == 'a':
            edit_task_assignee(temp_ID_of_selected_task)

        elif option == 'd':
            edit_task_due_date(temp_ID_of_selected_task)
        
        else:
            print('\nError. Invalid selection. Choose either "m", "a", "d" or "x".')
            continue

        # commiting changes to file
        try:
            write_task_list_to_file(task_list)
        
        except:
            print('An unexpected error occured. Any changes made were not saved to file.\n')
        
        break
       


def view_my_completed():
    '''Displays lists of completed tasks assigned to user.'''

    print()
    for task in task_list:
        if task['username'] == curr_user and task['completed'] == True:
            
            print(f"Task                    {task['title']}")
            print(f"Assigned to:            {task['username']}")
            print(f"Date Assigned:          {task['assigned_date'].strftime('%Y-%m-%d')}")
            print(f"Due Date:               {task['due_date'].strftime('%Y-%m-%d')}")
            print( "Status:                 Completed")
            print("Task Description:")
            print(f"{task['description']}\n")



def mark_task_as_complete(temp_ID):
    '''Mark the task as complete'''

    print('\nConfirm marking the task as complete.')
    
    while True:
        confirm = input('Enter "Y" to confirm or "N" to cancel: ').upper()

        if confirm == 'Y':
            task_list[temp_ID]['completed'] = True
            print('\nTask marked as complete.')
            return
        
        if confirm == 'N':
            print('Task still marked as uncompleted.')
            return
        
        else:
            print('Invalid input. Please enter either "Y" or "N"')



def edit_task_assignee(temp_ID):
    '''Takes user input to change who the task is assigned to.'''

    print(f'\nTask currently assigned to {task_list[temp_ID]["username"]}')
    
    while True:
        new_assignee = input('Enter name of user to reassign task to: ')

        if new_assignee not in username_password.keys():
            print('\nError. User does not exist.\n')
            continue
        
        break
    

    print(f'\nConfirm changing the task assignee from {task_list[temp_ID]["username"]} to {new_assignee}.')

    while True:
        confirm = input('Enter "Y" to confirm or "N" to cancel: ').upper()
        
        if confirm == 'Y':
            task_list[temp_ID]['username'] = new_assignee
            print(f'Task now assigned to {new_assignee}')
            return

        if confirm == 'N':
            print('Changes not saved.')
            return

        else:
            print('Invalid input. Please enter either "Y" or "N"')



def edit_task_due_date(temp_ID):
    '''Takes user input to change the due date of the task.'''

    print(f'\nTask currently due on {task_list[temp_ID]["due_date"]}')

    while True:
        try:
            new_due_date = input('Enter the new due date (YYYY-MM-DD): ')
            new_due_date_time = datetime.strptime(new_due_date, '%Y-%m-%d').date()
            break

        except ValueError:
            print('\nInvalid datetime format. Please use the format specified.\n')


    print(f'\nConfirm changing the task due date from {task_list[temp_ID]["due_date"]} to {new_due_date}.')

    while True:
        confirm = input('Enter "Y" to confirm or "N" to cancel: ').upper()
        
        if confirm == 'Y':
            task_list[temp_ID]['due_date'] = new_due_date_time
            print(f'Task now due on {new_due_date_time}')
            return

        if confirm == 'N':
            print('Changes not saved.')
            return

        else:
            print('Invalid input. Please enter either "Y" or "N"')



def display_statistics():
    '''Display statistics about number of users and tasks.'''
    
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print('\n','-' * 37, sep='')
    print(f'Number of users: {num_users :>20}')
    print(f'Number of tasks: {num_tasks :>20}')
    print('-' * 37)   



def generate_reports():
    '''Creates two reports summarising task and user statistics.'''
    
    # creates task_overview.txt if doens't already exist, 
    # or overwrites with up-to date report if file already exists
    try:
        with open('task_overview.txt', 'w') as f:
            total_tasks = len(task_list)
            completed_tasks = sum(task['completed'] == True for task in task_list)
            percent_complete = f'{completed_tasks / total_tasks :.2%}' if total_tasks > 0 else '-'
            uncompleted_tasks = sum(task['completed'] == False for task in task_list)
            percent_incomplete = f'{uncompleted_tasks / total_tasks :.2%}' if total_tasks > 0 else '-'
            overdue_tasks = sum(task['completed'] == False and task['due_date'] < date.today() for task in task_list)
            percent_overdue = f'{overdue_tasks / total_tasks :.2%}' if total_tasks > 0 else '-'

            f.write(f'Task Overview Report          {date.today()}\n\n')
            f.write(f'Total tasks:           {total_tasks :>6}\n')
            f.write(f'Completed tasks:       {completed_tasks :>6} {percent_complete :>10}\n')
            f.write(f'Uncompleted tasks:     {uncompleted_tasks :>6} {percent_incomplete :>10}\n')
            f.write(f'Overdue tasks:         {overdue_tasks :>6} {percent_overdue :>10}\n')

        print('Task overview report successfully generated.')
    
    except:
        print('An unexpected error occured. Task overview report was not generated.')


    # creates user_overview.txt if doens't already exist, 
    # or overwrites with up-to date report if file already exists
    try:
        with open('user_overview.txt', 'w') as f:
            total_users = len(username_password)
            total_tasks = len(task_list)
            
            tasks_per_user = {user:0 for user in username_password}
            for task in task_list:
                tasks_per_user[task['username']] += 1

            total_users_str = f'Total users: {total_users}'
            total_tasks_str = f'Total tasks: {total_tasks}'
            f.write(f'User Overview Report          {date.today()}\n\n')
            f.write(f'{total_users_str :<20}{total_tasks_str :>20}\n\n\n')

            
            f.write(f'{"USER" :<23} {"TASKS" :>5} {"%" :>10}\n')
            for user, task in tasks_per_user.items():
                percent = f'{task / total_tasks :.2%}' if total_tasks > 0 else '-'
                f.write(f'{user :<23} {task :>5} {percent :>10}\n')
            total_percent = '100.00%' if total_tasks > 0 else '-'
            f.write('_' * 40 + '\n')
            f.write(f'{"TOTAL" :<23} {total_tasks :>5} {total_percent :>10}\n\n\n')

            
            for user in username_password:

                user_stats = {
                    'tasks': 0,
                    'completed': 0,
                    'incomplete': 0,
                    'overdue': 0
                    }

                for task in task_list:
                    if task['username'] == user:
                        user_stats['tasks'] += 1
                        if task['completed'] == True:
                            user_stats['completed'] += 1
                        else:
                            user_stats['incomplete'] += 1
                            if task['due_date'] < date.today():
                                user_stats['overdue'] += 1

                
                percent_completed = f'{user_stats["completed"] / user_stats["tasks"] :.2%}' if user_stats["tasks"] > 0 else '-'
                percent_incomplete = f'{user_stats["incomplete"] / user_stats["tasks"] :.2%}' if user_stats["tasks"] > 0 else '-'
                percent_overdue = f'{user_stats["overdue"] / user_stats["tasks"] :.2%}' if user_stats["tasks"] > 0 else '-'

                f.write(f'{user}\n')
                f.write(f'Assigned tasks:        {user_stats["tasks"]:>6}\n')
                f.write(f'Completed tasks:       {user_stats["completed"]:>6} {percent_completed:>10}\n')
                f.write(f'Outstanding tasks:     {user_stats["incomplete"]:>6} {percent_incomplete:>10}\n')
                f.write(f'Overdue tasks:         {user_stats["overdue"]:>6} {percent_overdue:>10}\n\n\n')
                

        print('User overview report successfully generated.')
    
    except:
        print('An unexpected error occured. User overview report was not generated.')





# run program
if __name__ == "__main__":
    task_list = []
    username_password = {}
    curr_user = None
    
    set_up_tasks()
    set_up_users()
    login()
