# DVA269-Lab-Group-1 Python Diet App

Uploaded here is the main python file of the lab

We have a user as a main class, and different people like customer, nutritionist and customer support representative as child classes to the user. Nutritionist and support does not do anything in this version.

# **_Functions_**
1. Customer can login using username and password.
2. Customer can register a new account using username, password and email.
3. When Customer is logged in they can delete their account or change their password.
4. A button to contact customer support exist which will open the mail app on a Customer's computer where the contact info of the company will already be written.
5. Forgot password will prompt the Customer to enter an e-mail adress and if the e-mail is registered it will send to the Customer's mail the username and a code needed to be able to change the password which did popup after the e-mail was found.
6. Generate mealplan will ask a user for the type of diet they are looking for, e.g. low-carb, high-protein, etc. And it will also ask for common allergens like gluten and dairy allergy.

# **_NOTE_**
To contact customer support or receive code for password recovery the "Company_email_config" must be configured with an Microsoft outlook email and password of choice with smtp enabled(Seems to usually be enabled by default). 

# **_The libraries used_**

*tkinter was used for the user inteface

*hashlib was used to encrypt the password stored with sha256 bit encryption

*os was used for the storing of customer data by creating or modifying a credentials text file

*json was used for storing the file in a easy to work with format

*wbbrowser was used to open the standard mail app in a os and automaticaly put in the company email as sending adress

*smtplib was used to be able to send an email from the company to the user to showing the username and a code to input for the changing of password if forgotten

*random was used to generate the random code that would be used to be able to change password

# **_"Problems" with the code_**
credentials would in a real-world environment be saved on a company server and not locally, same goes for the company e-mail credentials.

# **_Guide for installation_**

Python needs to be installed on the user's computer. The tested version is python 3.12.1

Make sure you have the following files downloaded into the same folder before proceeding with the installation:

1. **Health_app_group_1 part2.py**
2. **FoodList.csv**
3. **company_email_config.json**

### Setting up `company_email_config.json`

Before running the application, you need to configure the email settings in the `company_email_config.json` file. Open the file using a text editor and replace the placeholder values with your actual email credentials so you can receive a password reset and send mail to support:

```json
{
    "email": "COMPANY_EMAIL_HERE",
    "password": "COMPANY_EMAIL_PASSWORD_HERE"
}

After setting up you can just run the Health_app_group_1 part2.py
