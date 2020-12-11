# TextFlex: Streamlined Textbook Searches for WPI Students

<h2 align="center"> What does it do?</h2>

<p>TextFlex is a web-application that utilizes python web scraping to collect a student’s schedule from their Bannerweb account  and input that information into the school store to obtain a list of textbooks associated with each class. The application goes a step further by then searching online for vendors who carry the book and returning to the user a list of their textbooks, and where they can buy them. The goal of this is to reduce the tedious nature of obtaining quarterly textbooks and to make the process of identifying and obtaining vendors streamlined at the press of a button.</p>

<h2 align="center">How is it built?</h2>

The application is written using the Django framework and utilizes basic HTML, CSS, Javascript, and some convinient bootstrap classes. The back end of the application uses the BeautifulSoup web scraping library as well as Google's google api for searching for book vendors.

<h2 align="center">What do I need to run it?</h2>

<p>Here is a list of all the software and python packages you will need in order to download and run the program:</p>
<ul>
  <li>Anaconda
  <li>PIP
  <li>Django
  <li>CrispyForms
  <li>BeautifulSoup
  <li>google
</ul>

<h2>Directions for Install</h2>

<ol>
<li> <h3>Install Anaconda</h3>
  <p>The official Anaconda Install Documentation: https://docs.anaconda.com/anaconda/install/</p>

<li> <h3>Install PIP (if not already installed)</h3>
  <p>The Official PIP Install Documentation: https://pip.pypa.io/en/stable/installing/</p>

<li> <h3>Install Django (Official Release)</h3>
  <p>The Official Django Intstall Documentation: https://docs.djangoproject.com/en/3.1/topics/install/</p>

<li> <h3>Install Crispy Forms</h3>
  <p></p>

</ol>

-Anaconda

-------------------------------
-pip

-------------------------------
-django

python -m pip install Django

-------------------------------
-crispyforms

pip install django-crispy-forms

-------------------------------
To start the server run the following command when in the TextFlex folder:

-python manage.py runserver

If for whatever reason, you run into issues getting the Django server up and running please contact me! I got this working on a VM so I can probably figure out what went wrong.

Other Notes: I initially had a recover password system in place, but it required personal email information which I had to remove when I made the repo public, as a result that no longer functions.

I also need to give credit to GitHub user Krconv for their work on a bannerweb scraping system. I was able to modify their system to pulls schedules instead of register for classes. Their framework was very organized and I used their methodology to scrape the barnes and noble store also!

Link:https://github.com/krconv/PyRegister 
