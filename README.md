# Author
<ul>
  <li>Name: Qinyu Liu</li>
  <li>ID: N9325247</li>
  <li>Project: IFN702</li>
</ul>

# Prerequisites
It’s a good idea to keep all your virtual environments in one place, for example in .virtualenvs/ in your home directory.

Create a new virtual environment by running:
MacOS & Linux:
$ python3 -m venv ~/.virtualenvs/djangodev
Windows:
> py -m venv %HOMEPATH%\.virtualenvs\djangodev

The path is where the new environment will be saved on your computer.

The final step in setting up your virtual environment is to activate it:
$ source ~/.virtualenvs/djangodev/bin/activate

Make sure you have installed MongoDB.

# Installation
Clone the repository to your local machine, and then: <br>
pip install -r requirements.txt

# Configuration
Rename settings.sample.py to settings.py <br>
Set your own SECRET_KEY in that file <br>
Then Set DATABASES name to your database's name

# Run
First launch MongoDB: <br>
mongod

Then run the server hosted on http://localhost:8000: <br>
python manage.py runserver

# The Screenshots
![Homepage](https://raw.githubusercontent.com/MrOrangeLiu/IFN702/master/screenshots/homepage.png)

![My Files](https://raw.githubusercontent.com/MrOrangeLiu/IFN702/master/screenshots/myfiles.png)

![Search](https://raw.githubusercontent.com/MrOrangeLiu/IFN702/master/screenshots/search.png)

# Test
python manage.py test login <br>
python manage.py test dashboard <br>
###Or you can test all: <br>
python manage.py test <br>
###The test results: <br>
![Search](https://raw.githubusercontent.com/MrOrangeLiu/IFN702/master/screenshots/test.png)
