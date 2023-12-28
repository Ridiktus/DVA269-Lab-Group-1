import json
import hashlib
import os
import tkinter as tk
import tkinter.messagebox as mb
import webbrowser
import smtplib
import random


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def save_credentials(credentials):
    with open('credentials.txt', 'w') as f:
        f.write(json.dumps(credentials))

def load_credentials():
    if not os.path.exists('credentials.txt'):
        return None, None
    try:
        with open('credentials.txt') as f:
            read = json.loads(f.read())
    except:
        print('\nthere are no saved users')
        read = {}

    return read


def register(username_entry,password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    register_window = tk.Toplevel(root)
    register_window.title('Registration')
    center_window(register_window)

    username_label = tk.Label(register_window, text='Select username')
    username_label.pack()
    register_username = tk.Entry(register_window)
    register_username.pack()

    email_label = tk.Label(register_window, text='E-mail Adress')
    email_label.pack()
    register_email = tk.Entry(register_window)
    register_email.pack()

    password_label = tk.Label(register_window, text='select Password')
    password_label.pack()
    register_password= tk.Entry(register_window, show='*')
    register_password.pack()

    register_window.bind('<Return>', lambda event: submit_registration(register_username.get(), register_password.get(),register_email.get(), register_window))
    submit_button = tk.Button(register_window, text='Submit', command=lambda: submit_registration(register_username.get(), register_password.get(), register_email.get(),register_window))
    submit_button.pack()

def submit_registration(username, password, email, register_window):
    credentials = load_credentials()
    
    if username in credentials:
        mb.showerror('Error', 'Account already exists')

    elif not username or not password or not email:
        mb.showerror('Error', 'not all required information was entered')

    else:
        password = encrypt_string(password)
        credentials[username] = {'password': password, 'email': email}
        save_credentials(credentials)
        register_window.destroy()
        mb.showinfo('Success', 'Account was created')


def delete_account(username, success_window):
    credentials = load_credentials()
    if username in credentials:
        del credentials[username]
        save_credentials(credentials)
        mb.showinfo('Success', 'Account was deleted')
        success_window.destroy()
    else:
        mb.showerror('Error', 'Account not found')


def login(username, password):
    credentials = load_credentials()
    username = username.get()
    password = password.get()
    password = encrypt_string(password)

    if not username or not password:
        mb.showerror('Error', 'Username and password cannot be empty')
        return
    
    if username in credentials:
        if credentials[f'{username}']['password'] == password:
            success_window = tk.Toplevel(root)
            center_window(success_window)
            success_window.title('Account')
            root.withdraw()
            success_label = tk.Label(success_window, text='Login was successful')
            success_label.pack()
            change_password_button = tk.Button(success_window, text='Change Password', command = lambda: [change_password(username)])
            change_password_button.pack()
            delete_account_button = tk.Button(success_window, text='Delete Account', command=lambda: [delete_account(username, success_window), root.deiconify()])
            delete_account_button.pack()
            return_button = tk.Button(success_window, text='Logout', command=lambda: [success_window.destroy(), root.deiconify()])
            return_button.pack()
            success_window.bind('<Escape>', lambda event: [success_window.destroy(), root.deiconify()])
            success_window.protocol('WM_DELETE_WINDOW', lambda: [root.deiconify(), success_window.destroy()])

        else:
            mb.showerror('Error', 'Incorrect password')
    else:
        mb.showerror('Error', 'Username not found')


def change_password(username):
    change_password_window = tk.Toplevel(root)
    change_password_window.title('Change Password')
    center_window(change_password_window)

    username_label = tk.Label(change_password_window, text='Username')
    username_label.pack()
    username_entry = tk.Label(change_password_window, text=username)
    username_entry.pack()

    current_password_label = tk.Label(change_password_window, text='Current Password')
    current_password_label.pack()
    current_password_entry = tk.Entry(change_password_window, show='*')
    current_password_entry.pack()

    new_password_label = tk.Label(change_password_window, text='New Password')
    new_password_label.pack()
    new_password_entry = tk.Entry(change_password_window, show='*')
    new_password_entry.pack()
    
    submit_button = tk.Button(change_password_window, text='Submit', command=lambda: submit_password_change(username, current_password_entry.get(), new_password_entry.get(), change_password_window))
    submit_button.pack()
    change_password_window.bind('<Return>', lambda event: submit_password_change(username, current_password_entry.get(), new_password_entry.get(), change_password_window))

def submit_password_change(username_entry, current_password_entry, new_password_entry, change_password_window):
    credentials = load_credentials()
    current_password_entry = encrypt_string(current_password_entry)
    if username_entry in credentials:
        if credentials[f'{username_entry}']['password'] == current_password_entry:
            change_password_window.destroy()
            success_window = tk.Toplevel(root)
            center_window(success_window)
            new_pass = encrypt_string(new_password_entry)
            credentials[f'{username_entry}']['password'] = new_pass
            save_credentials(credentials)
            success_label = tk.Label(success_window, text='Password has been changed')
            success_label.pack()
            return_button = tk.Button(success_window, text='Return', command=lambda: [success_window.destroy()])
            return_button.pack()
            success_window.bind('<Escape>', lambda event: success_window.destroy())
            success_window.bind('<Return>', lambda event: success_window.destroy())
        else:
            mb.showerror('Error', 'Incorrect password')
    else: 
        mb.showerror('Error', 'Incorrect password')

def contact_support():
    webbrowser.open('mailto:healthappsweden@outlook.com', new=1)

def forgot_password():
    forgot_password_window = tk.Toplevel(root)
    forgot_password_window.title('Forgot Password')
    center_window(forgot_password_window)

    email_label = tk.Label(forgot_password_window, text='Email')
    email_label.pack()
    email_entry = tk.Entry(forgot_password_window)
    email_entry.pack()

    submit_button = tk.Button(forgot_password_window, text='Submit', command=lambda: [reset_password(email_entry.get(), forgot_password_window)])
    submit_button.pack()

    forgot_password_window.bind('<Return>', lambda event: reset_password(email_entry.get(), forgot_password_window))

def reset_password(email, prev_window):
    credentials = load_credentials()
    for username, user_info in credentials.items():
        if user_info['email'] == email:
            code = random.randint(100000, 999999)
            prev_window.destroy()
            send_email(email, code, username)
            code_entry_window = tk.Toplevel(root)
            center_window(code_entry_window)
            code_entry_window.title('Enter Code')

            code_label = tk.Label(code_entry_window, text='Code')
            code_label.pack()
            code_entry = tk.Entry(code_entry_window)
            code_entry.pack()

            new_password_label = tk.Label(code_entry_window, text='New Password')
            new_password_label.pack()
            new_password_entry = tk.Entry(code_entry_window, show='*')
            new_password_entry.pack()

            submit_button = tk.Button(code_entry_window, text='Submit', command=lambda: change_password_with_code(username, code, code_entry.get(), new_password_entry.get(), code_entry_window))
            submit_button.pack()

            code_entry_window.bind('<Return>', lambda event: change_password_with_code(username, code, code_entry.get(),new_password_entry.get(), code_entry_window))
            break
    else:
        mb.showerror('Error', 'No account associated with this email')

def change_password_with_code(username, correct_code, entered_code, new_password, prev_window):
    if int(entered_code) == correct_code:
        credentials = load_credentials()
        credentials[username]['password'] = encrypt_string(new_password)
        save_credentials(credentials)
        prev_window.destroy()
        mb.showinfo('Success', 'Password has been changed')
    else:
        mb.showerror('Error', 'Incorrect code')

def send_email(email, code, username):

    subject = 'Password Reset!'
    body = f'Hi {username}! to reset your password use the folowing code: {code}.'

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login('healthappsweden@outlook.com', 'Losenord1!')
    complete_message = f'Subject: {subject}\n\n{body}'
    server.sendmail('healthappsweden@outlook.com', email, complete_message)
    server.quit()
    
def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position
    x = (screen_width / 2) - (window.winfo_reqwidth() / 2)
    y = (screen_height / 2) - (window.winfo_reqheight() / 2)

    # Set window position
    window.geometry('+%d+%d' % (x, y))

def create_main_window():
    global root
    root = tk.Tk()
    root.update_idletasks()
    center_window(root)
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
    root.title('Login: Health App')

    username_label = tk.Label(root, text='Username')
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text='Password')
    password_label.pack()
    password_entry = tk.Entry(root, show='*')
    password_entry.pack()

    root.bind('<Return>', lambda event: login(username_entry, password_entry))
    login_button = tk.Button(root, text='Login', command=lambda: login(username_entry, password_entry))
    login_button.pack()

    register_button = tk.Button(root, text='Register', command=lambda: register(username_entry, password_entry))
    register_button.pack()

    contact_support_button = tk.Button(bottom_frame, text='Customer Support', command=contact_support)
    contact_support_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    spacer_frame = tk.Frame(bottom_frame)
    spacer_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=90)    

    forgot_password_button = tk.Button(bottom_frame, text='Forgot Password', command=forgot_password)
    forgot_password_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    root.mainloop()

if __name__ == '__main__':
    create_main_window()
    