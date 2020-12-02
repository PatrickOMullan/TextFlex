from bs4 import BeautifulSoup
from lxml import html
import requests
import re
import pandas as pd
from googlesearch import search

class course_info:
    def __init__(self, dept, number, section):
        self.dept = dept
        self.number = number
        self.section = section

    def book_info(self, title, isbn):
        self.title = title
        self.isbn = isbn

#SECTION THAT OPENNS

with open('Student Detail Schedule.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')


blacklist = ['Scheduled Meeting Times']
courses = []

for course in soup.find_all('caption', class_='captiontext'):
    if course.text not in blacklist:
        content = course.text
        start = content.find('- ')
        courses.append(content[start+1:])

student_schedule = []

depts = []
nums = []
sects = []

for course in courses:
    dept = re.compile(r'\s\D\D\s')
    number = re.compile(r'\d\d\d\d')
    sect = re.compile(r'...\Z')

    deptmatches = dept.finditer(course)
    numbermatches = number.finditer(course)
    sectmatches = sect.finditer(course)

    for match in deptmatches:
        depts.append(course[match.start()+1:match.end()-1])

    for match in numbermatches:
        nums.append(course[match.start():match.end()])

    for match in sectmatches:
        sects.append(course[match.start():match.end()])

for i in range(len(courses)):
    student_schedule.append(course_info(depts[i], nums[i], sects[i]))

html_file.close()

#SECTION TO NOW GET TEXTBOOK INFO

with open('results.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
    
    title = soup.find('a', class_='clr121', text=True).text
    
    title_pattern = re.compile(r'\w.*\w')

    title_info = title_pattern.finditer(title)

    for elmt in title_info:
        title = title[elmt.start(): elmt.end()]

    isbn = soup.find('li', class_='book_c2_180616').text

    isbn_pattern = re.compile(r'\d\d\d\d\d\d\d\d\d\d\d\d\d')

    isbn_info = isbn_pattern.finditer(isbn)

    for elmt in isbn_info:
        isbn = isbn[elmt.start(): elmt.end()]

    for elmt in student_schedule:
        elmt.book_info(title, isbn)
    
html_file.close()

#GOOGLE SEARCH
sellers = ['amazon.com', 'barnesandnoble.com']
search_results = []

for elmt in student_schedule:
    search_results.append(search(elmt.title, tld="co.in", num=10, stop=10, pause=2))

filtered_results = []

for elmt in search_results:
    for subelmt in elmt:
        for seller in sellers:
            if seller in subelmt:
                filtered_results.append(subelmt)
    break
print (filtered_results)
