import json
import hashlib
import os
import tkinter as tk
import tkinter.messagebox as mb
import webbrowser
import smtplib
import random


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = self.encrypt_string(password)
        self.email = email

    def encrypt_string(self, hash_string):
        sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def change_password(self, new_password):
        self.password = self.encrypt_string(new_password)

    def __str__(self):
        return f'Username: {self.username}, Email: {self.email}'


class Nutritionist(User):
    def __init__(self, username, password, email):
        super().__init__(username, password, email)

    def provide_nutritional_advice(self):
        pass


class Customer(User):
    def __init__(self, username, password, email):
        super().__init__(username, password, email)

    def __str__(self):
        return super().__str__()


class CustomerSupportRepresentative(User):
    def __init__(self, username, password, email, department):
        super().__init__(username, password, email)
        self.department = department

    def handle_customer_inquiries(self):
        pass

    def __str__(self):
        return super().__str__() + f', Department: {self.department}'


class HealthApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.update_idletasks()
        self.center_window(self.root)
        self.root.title('Login: Health App')

        self.username_label = tk.Label(self.root, text='Username')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text='Password')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        self.root.bind('<Return>', lambda event: self.login())
        self.login_button = tk.Button(self.root, text='Login', command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.root, text='Register', command=self.register)
        self.register_button.pack()

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        self.contact_support_button = tk.Button(self.bottom_frame, text='Customer Support', command=self.contact_support)
        self.contact_support_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.spacer_frame = tk.Frame(self.bottom_frame)
        self.spacer_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=90)

        self.forgot_password_button = tk.Button(self.bottom_frame, text='Forgot Password', command=self.forgot_password)
        self.forgot_password_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate position
        x = (screen_width / 2) - (window.winfo_reqwidth() / 2)
        y = (screen_height / 2) - (window.winfo_reqheight() / 2)

        # Set window position
        window.geometry('+%d+%d' % (x, y))

    def encrypt_string(self, hash_string):
        sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def save_credentials(self, credentials):
        with open('credentials.txt', 'w') as f:
            f.write(json.dumps(credentials))

    def load_credentials(self):
        if not os.path.exists('credentials.txt'):
            return None, None
        try:
            with open('credentials.txt') as f:
                read = json.loads(f.read())
        except:
            print('\nthere are no saved users')
            read = {}

        return read

    def register(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        register_window = tk.Toplevel(self.root)
        register_window.title('Registration')
        self.center_window(register_window)

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
        register_password = tk.Entry(register_window, show='*')
        register_password.pack()

        register_window.bind('<Return>', lambda event: self.submit_registration(register_username.get(), register_password.get(), register_email.get(), register_window))
        submit_button = tk.Button(register_window, text='Submit', command=lambda: self.submit_registration(register_username.get(), register_password.get(), register_email.get(), register_window))
        submit_button.pack()

    def submit_registration(self, username, password, email, register_window):
        credentials = self.load_credentials()

        if username in credentials:
            mb.showerror('Error', 'Account already exists')

        elif not username or not password or not email:
            mb.showerror('Error', 'not all required information was entered')

        else:
            password = self.encrypt_string(password)
            credentials[username] = {'password': password, 'email': email}
            self.save_credentials(credentials)
            register_window.destroy()
            mb.showinfo('Success', 'Account was created')

    def login(self):
        credentials = self.load_credentials()
        username = self.username_entry.get()
        password = self.password_entry.get()
        password = self.encrypt_string(password)

        if not username or not password:
            mb.showerror('Error', 'Username and password cannot be empty')
            return

        if username in credentials:
            if credentials[f'{username}']['password'] == password:
                user_type = credentials[username].get('type', 'Customer')
                user_instance = self.create_user_instance(user_type, username, password, credentials[username]['email'])
                success_window = tk.Toplevel(self.root)
                self.center_window(success_window)
                success_window.title('Account')
                self.root.withdraw()
                success_label = tk.Label(success_window, text=f'Login was successful\nUser Type: {user_type}')
                success_label.pack()

                if isinstance(user_instance, Customer):
                    change_password_button = tk.Button(success_window, text='Change Password', command=lambda: [self.change_password(username)])
                    change_password_button.pack()
                    delete_account_button = tk.Button(success_window, text='Delete Account', command=lambda: [self.delete_account(username, success_window), self.root.deiconify()])
                    delete_account_button.pack()
                    
                elif isinstance(user_instance, Nutritionist):
                    provide_advice_button = tk.Button(success_window, text='Provide Nutritional Advice', command=user_instance.provide_nutritional_advice)
                    provide_advice_button.pack()

                elif isinstance(user_instance, CustomerSupportRepresentative):
                    handle_inquiries_button = tk.Button(success_window, text='Handle Customer Inquiries', command=user_instance.handle_customer_inquiries)
                    handle_inquiries_button.pack()

                return_button = tk.Button(success_window, text='Logout', command=lambda: [success_window.destroy(), self.root.deiconify()])
                return_button.pack()
                success_window.bind('<Escape>', lambda event: [success_window.destroy(), self.root.deiconify()])
                success_window.protocol('WM_DELETE_WINDOW', lambda: [self.root.deiconify(), success_window.destroy()])

            else:
                mb.showerror('Error', 'Incorrect password')
        else:
            mb.showerror('Error', 'Username not found')

    def create_user_instance(self, user_type, *args):
        if user_type == 'Nutritionist':
            return Nutritionist(*args)
        elif user_type == 'Customer':
            return Customer(*args)
        elif user_type == 'CustomerSupportRepresentative':
            return CustomerSupportRepresentative(*args)
        else:
            return User(*args)
        
    def change_password(self, username):
        change_password_window = tk.Toplevel(self.root)
        change_password_window.title('Change Password')
        self.center_window(change_password_window)

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

        submit_button = tk.Button(change_password_window, text='Submit', command=lambda: self.submit_password_change(username, current_password_entry.get(), new_password_entry.get(), change_password_window))
        submit_button.pack()
        change_password_window.bind('<Return>', lambda event: self.submit_password_change(username, current_password_entry.get(), new_password_entry.get(), change_password_window))

    def submit_password_change(self, username_entry, current_password_entry, new_password_entry, change_password_window):
        credentials = self.load_credentials()
        current_password_entry = self.encrypt_string(current_password_entry)
        if username_entry in credentials:
            if credentials[f'{username_entry}']['password'] == current_password_entry:
                change_password_window.destroy()
                success_window = tk.Toplevel(self.root)
                self.center_window(success_window)
                new_pass = self.encrypt_string(new_password_entry)
                credentials[f'{username_entry}']['password'] = new_pass
                self.save_credentials(credentials)
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

    def delete_account(self, username, success_window):
        credentials = self.load_credentials()
        if username in credentials:
            del credentials[username]
            self.save_credentials(credentials)
            mb.showinfo('Success', 'Account was deleted')
            success_window.destroy()
        else:
            mb.showerror('Error', 'Account not found')

    def contact_support(self):
        try:
            with open('company_email_config.json') as f:
                mail = json.loads(f.read())
            webbrowser.open(f'mailto:{mail["email"]}', new=1)
        except Exception:
            mb.showerror('Error', '"company_email_config.json" Does not excist')

    def forgot_password(self):
        forgot_password_window = tk.Toplevel(self.root)
        forgot_password_window.title('Forgot Password')
        self.center_window(forgot_password_window)

        email_label = tk.Label(forgot_password_window, text='Email')
        email_label.pack()
        email_entry = tk.Entry(forgot_password_window)
        email_entry.pack()

        submit_button = tk.Button(forgot_password_window, text='Submit', command=lambda: [self.reset_password(email_entry.get(), forgot_password_window)])
        submit_button.pack()

        forgot_password_window.bind('<Return>', lambda event: self.reset_password(email_entry.get(), forgot_password_window))

    def reset_password(self, email, prev_window):
        credentials = self.load_credentials()
        for username, user_info in credentials.items():
            if user_info['email'] == email:
                code = random.randint(100000, 999999)
                prev_window.destroy()
                self.send_email(email, code, username)
                code_entry_window = tk.Toplevel(self.root)
                self.center_window(code_entry_window)
                code_entry_window.title('Enter Code')

                code_label = tk.Label(code_entry_window, text='Code')
                code_label.pack()
                code_entry = tk.Entry(code_entry_window)
                code_entry.pack()

                new_password_label = tk.Label(code_entry_window, text='New Password')
                new_password_label.pack()
                new_password_entry = tk.Entry(code_entry_window, show='*')
                new_password_entry.pack()

                submit_button = tk.Button(code_entry_window, text='Submit', command=lambda: self.change_password_with_code(username, code, code_entry.get(), new_password_entry.get(), code_entry_window))
                submit_button.pack()

                code_entry_window.bind('<Return>', lambda event: self.change_password_with_code(username, code, code_entry.get(),new_password_entry.get(), code_entry_window))
                break
        else:
            mb.showerror('Error', 'No account associated with this email')

    def change_password_with_code(self, username, correct_code, entered_code, new_password, prev_window):
        if int(entered_code) == correct_code:
            credentials = self.load_credentials()
            credentials[username]['password'] = self.encrypt_string(new_password)
            self.save_credentials(credentials)
            prev_window.destroy()
            mb.showinfo('Success', 'Password has been changed')
        else:
            mb.showerror('Error', 'Incorrect code')

    def send_email_from_company(self):
        try:
            with open('company_email_config.json') as f:
                mail_info = json.loads(f.read())
            return mail_info
        except Exception:
            mb.showerror('Error', '"company_email_config.json" Does not excist')

    def send_email(self, email, code, username):
        subject = 'Password Reset!'
        body = f'Hi {username}! to reset your password use the folowing code: {code}.'
        company_info = self.send_email_from_company()

        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(f'{company_info["email"]}', f'{company_info["password"]}')
        complete_message = f'Subject: {subject}\n\n{body}'
        server.sendmail('healthappsweden@outlook.com', email, complete_message)
        server.quit()

    def create_main_window(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = HealthApp()
    app.create_main_window()
