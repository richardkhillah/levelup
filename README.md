# LevelUP

Level up is a Python Flask application currently in a very early stage of development. It can support user registration and authentication, and forgotten password support. For e-mail support, there are a couple of additional required actions as noted below.

In it's full glory, LevelUP will be the Ultimate Township player resource for managing your Township town and running tight regattas!

While the application is currently in development (and will be for quite some time) you are able to run local copies of the application. You will need python3 installed on your local machine.

The following commands are given for unix/linux environments.

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
echo FLASK_APP=levelup.py > .env
flask run
```

The above will run a server in the same command line window you run them in. To kill the server, simply type `ctrl + c` (control + c) in the server window.

Open a browser window, and goto `http://localhost:5000/`.

For e-mail support, the current version of this application requires requires the use of a gmail account with the 'allow less secure applications' security setting changed to true and the use of two exported variables, namely `MAIL_USERNAME` and `MAIL_PASSWORD`.
To make your life easy, simply run:
```
echo MAIL_USERNAME='<Your-gmail-usernam>' >>.env
echo MAIL_PASSWORD='<Your-gmail-password>' >>.env
```
