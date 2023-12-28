# DVA269-Lab-Group-1 Python Health App

Uploaded here is the main python file of the lab

functions:
1. You can login using username and password
2. you can register a new account using username, password and email
3. When logged in you can delete your account or change the password
4. A button to contact customer support exist which will open the mail app on a user's computer where the contact info of the company will already be written
5. Forgot password will prompt the user to enter an e-mail adress and if the e-mail is registered it will send to the users mail the username and a code needed to be able to change the password which did popup after the e-mail was found.

The libraries used:
*tkinter was used for the user inteface

*hashlib was used to encrypt the password stored with sha256 bit encryption

*os was used for the storing of customer data by creating or modifying a credentials text file

*json was used for storing the file in a easy to work with format

*wbbrowser was used to open the standard mail app in a os and automaticaly put in the company email as sending adress

*smtplib was used to be able to send an email from the company to the user to showing the username and a code to input for the changing of password if forgotten

*random was used to generate the random code that would be used to be able to change password

"problems" with the code:
credentials would in a real enviroment be saved on a company server not localy.
