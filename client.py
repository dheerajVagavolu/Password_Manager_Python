from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import subprocess
import pyfiglet
import argparse
import socket
import os

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'list',
        'message': 'Select the action to be done:',
        'name': 'options',
        'choices': [
            {
                'name': 'Log In',
                'checked': True
            },
            {
                'name': 'Register'
            },
            {
                'name': 'Update my password'
            },
            {
                'name': 'Delete my account'
            },
            {
                'name': 'exit'
            }
        ],
        'validate': lambda answer: 'You must choose at least one option.' \
            if len(answer) == 0 else True
    }
]

login_questions = [
    {
        'type': 'input',
        'name': 'Email',
        'message': 'Enter your e-mail address: ',
    },
    {
        'type': 'password',
        'name': 'Password',
        'message': 'Enter your password: '
    }
]

create_remove_questions = [
    {
        'type': 'input',
        'name': 'Email',
        'message': 'Enter your e-mail address: ',
    },
    {
        'type': 'password',
        'name': 'Password',
        'message': 'Enter your password: '
    },
    {
        'type': 'password',
        'name': 'Re-Password',
        'message': 'Re-enter your password to confirm: '
    }
]

update_questions = [
    {
        'type': 'input',
        'name': 'Email',
        'message': 'Enter your e-mail address: ',
    },
    {
        'type': 'password',
        'name': 'Old Password',
        'message': 'Enter your current password: '
    },
    {
        'type': 'password',
        'name': 'New Password',
        'message': 'Enter your new password: '
    }
]

password_queries = [
    {
        'type': 'list',
        'message': 'Select the query:',
        'name': 'options',
        'choices': [
            {
                'name': 'Add a new account',
                'checked': True
            },
            {
                'name': 'Display all accounts'
            },
            {
                'name': 'Logout'
            }
        ],
        'validate': lambda answer: 'You must choose at least one option.' \
            if len(answer) == 0 else True
    }
]

add_account = [
    {
        'type': 'input',
        'name': 'Account',
        'message': 'Enter the Account name: ',
    },
    {
        'type': 'password',
        'name': 'Password',
        'message': 'Enter the password: '
    },
    {
        'type': 'input',
        'name': 'Domain',
        'message': 'Enter the domain/website name: '
    }
]


parser = argparse.ArgumentParser(description = "This is client for mt socket")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Connecting to server: {args.host} on port: {args.port}")

ascii_banner = pyfiglet.figlet_format("Password Manager")
print(ascii_banner)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    try:
        conn.connect((args.host, args.port))
    except Exception as e:
        raise SystemExit(f"Failed to connect to host: {args.host} on port: {args.port}")

    while True:
        answers = prompt(questions, style = style)

        if(answers['options'] == 'Log In'):
            answers = prompt(login_questions, style = style)
            conn.sendall(str.encode('Log' + ' ' + answers['Email'] + ' ' + answers['Password']))

            data = conn.recv(1024).decode()
            if data.split(' ')[0] == "Error:":
                print('\n' + f"{data}" + '\n')
            else:
                auth_key = data.split(' ')[0]

                while True:
                    answers1 = prompt(password_queries, style = style)

                    if(answers1['options'] == 'Add a new account'):
                        answers1 = prompt(add_account, style = style)
                        conn.sendall(str.encode('Add' + ' ' + answers1['Account'] + ' ' + 
                            answers1['Password'] + ' ' + answers1['Domain'] + ' ' + auth_key))

                        data = conn.recv(1024).decode()
                        print('\n' + data + '\n')

                    elif(answers1['options'] == 'Display all accounts'):
                        conn.sendall(str.encode('Display' + ' ' + auth_key))

                        data = conn.recv(1024).decode()
                        if(data.split(' ')[0] != 'Error:'):
                            account_list = [
                                {
                                    'type': 'list',
                                    'message': 'Select the account to view the password:',
                                    'name': 'accounts',
                                    'choices': data.split(' '),
                                }
                            ]

                            answers1 = prompt(account_list, style = style)
                            conn.sendall(str.encode(answers1['accounts']))
                            
                            data = conn.recv(1024).decode()
                            print('\n' + 'Password for \'' + answers1['accounts'] + '\': ' + data + '\n')
                        else:
                            print('\n' + data + '\n')

                    elif(answers1['options'] == 'Logout'):
                        break

        elif(answers['options'] == 'Register'):
            answers = prompt(create_remove_questions, style = style)

            while True:
                if(answers['Password'] == answers['Re-Password']):
                    break
                else:
                    print("\nPasswords didn't match! Retry..\n")
                    answers = prompt(create_remove_questions, style = style)

            conn.sendall(str.encode('Register' + ' ' + answers['Email'] + ' ' + answers['Password']))
            
            data = conn.recv(1024)
            print('\n' + f"{data.decode()}" + '\n')

        elif(answers['options'] == 'Update my password'):
            answers = prompt(update_questions, style = style)
            conn.sendall(str.encode('Update' + ' ' + answers['Email'] + ' ' 
                + answers['Old Password'] + ' ' + answers['New Password']))

            data = conn.recv(1024)
            print('\n' + f"{data.decode()}" + '\n')

        elif(answers['options'] == 'Delete my account'):
            answers = prompt(create_remove_questions, style = style)

            while True:
                if(answers['Password'] == answers['Re-Password']):
                    break
                else:
                    print("\nPasswords didn't match! Retry..\n")
                    answers = prompt(create_remove_questions, style=style)
            
            conn.sendall(str.encode('Delete' + ' ' + answers['Email'] + ' ' + answers['Password']))

            data = conn.recv(1024)
            print('\n' + f"{data.decode()}" + '\n')

        elif(answers['options'] == 'exit'):
            exit(0)