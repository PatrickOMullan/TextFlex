from bs4 import BeautifulSoup
import json, urllib
from datetime import datetime, datetime
from time import sleep
from getpass import getpass
import requests
import re
from io import StringIO
from googlesearch import search
import sys

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def store_json(courselist, username):
    
    courses =[]

    for i in range(len(courselist)):
        if courselist[i].isbn != None:
            a_course = {'err': 0, 'dept': courselist[i].dept, 'number': courselist[i].number, 'section': courselist[i].section, 'term': courselist[i].term, 'year': courselist[i].year, 'title': courselist[i].title, 'isbn': courselist[i].isbn, 'image': courselist[i].image, 'links': courselist[i].links}
            courses.append(a_course)
        else:
            null_course = {'err': 0, 'dept': courselist[i].dept, 'number': courselist[i].number, 'section': courselist[i].section, 'term': courselist[i].term, 'year': courselist[i].year, 'title': 'No Textbook', 'isbn': 'No ISBN', 'image': None, 'links': []}
            courses.append(null_course)
            

    with open(f'findbooks/web_scraper/json/books_{username}.json', 'w+') as f:
        json.dump(courses, f)
    
        f.close()

class course_info:
    def __init__(self, dept, number, section, term, year):
        self.dept = dept
        self.number = number
        self.section = section
        self.term = term
        self.year = year
        self.links = []

    def book_info(self, title, isbn, image):
        self.title = title
        self.isbn = isbn
        self.image = image
        
    def append_links(self, results):
        for result in results:
            self.links.append(result)

    def to_str(self):
        return f'DEPARTMENT: {self.dept}\nCOURSE#: {self.number}\nSECTION: {self.section}\nBOOK:{self.title}\nISBN:{self.isbn}\nIMAGE:{self.image}\nLINKS:{self.links}\n\n'

class pullSchedule(object):

    page_urls = {
        'home': '/twbkwbis.P_WWWLogin',
        'login': '/twbkwbis.P_ValLogin',
        'select_term': '/bwskflib.P_SelDefTerm',
        'save_term': 'bwcklibs.P_StoreTerm',
        'semester_info': '/bwskfshd.P_CrseSchdDetl'
    }

    def __init__(self, url, username, password=None):
        if(password == None):
            password = getpass(f"Enter the password for {username}: ")

        self.base_url = url
        self.session = requests.Session()

        self.middle_url = None

        for attempt in ['/pls/owa_prod', '/pls/prod']:
            response = self.session.send(self.prepped_request(self.page_urls['home'], "GET", middle_url=attempt))

            if(response.status_code == 200):
                self.middle_url = attempt
                break
        
        if (self.middle_url == None):
            raise Exception("Couldn't determine URL! ")
            
        
        response = self.session.send(self.prepped_request(self.page_urls['login'], "POST", data={'sid':username, 'PIN':password}))
    
        if (response.cookies.get('SESSID') == None):
            raise Exception('INCORRECT LOGIN INFO')

        page = self.session.get(self.base_url + self.middle_url + self.page_urls['select_term'], headers={'referer':self.base_url})
        self.soup = BeautifulSoup(page.text, 'html5lib')

        self.offset = datetime.strptime(response.headers['Date'], '%a, %d %b %Y %H:%M:%S %Z') - datetime.utcnow()

        self.cache = None

    def prepped_request(self, page_url, method, data={}, middle_url=None):
        
        if (middle_url == None):
            middle_url = self.middle_url
        
        sleep(0.5)

        prepped = requests.Request(method, self.base_url + middle_url + page_url, headers={'referer':self.base_url}, data=data)
        print("Prepped Request:" + self.base_url + middle_url + page_url)
        return self.session.prepare_request(prepped)
    

    def get_classes(self, term, year):
        self.term = term
        self.year = year
        semester = ''

        if(term == 'A' or term == 'B'):
            semester = 'Fall'
        elif(term == 'C' or term =='D'):
            semester = 'Spring'
        elif(term == 'E1' or term == 'E2'):
            semester = 'Summer'
        else:
            raise Exception(f"Invalid Term {term}")

        options = self.soup.find_all('option')
        
        form_option = None

        for elmt in options:
            if f'{semester} {year}' in elmt.text:
                form_option = elmt
        
        if form_option == None:
            form = 'TERM NOT YET LISTED'
            return form

        term_id = form_option.get('value')

        if(not self.cache):
            prepped = self.prepped_request(self.page_urls['semester_info'], "POST", {'term_in': term_id})
            response = self.session.send(prepped)
            form = BeautifulSoup(response.text, 'html5lib')
            self.cache = form
        else:
            form = self.cache
        
        return form

    def extract_class_info(self, form):
        if form == 'TERM NOT YET LISTED':
            return form

        blacklist = ['Scheduled Meeting Times']
        courses = []

        for course in form.find_all('caption', class_='captiontext'):
            if course.text not in blacklist:
                content = course.text
                start = content.find(' - ')
                courses.append(content[start+1:])

        student_schedule = []

        depts = []
        nums = []
        sects = []

        for course in courses:

            dept = re.compile(r'\s\D\D\s')
            number = re.compile(r'\d\d\d\d')

            deptmatches = dept.finditer(course)
            
            origin_dept_len = len(depts)

            for match in deptmatches:
                depts.append(course[match.start()+1:match.end()-1])
            
            post_dept_len = len(depts)

            if origin_dept_len == post_dept_len:
                dept = re.compile(r'\s\D\D\D\s')
                deptmatches = dept.finditer(course)

                origin_dept_len = len(depts)

                for match in deptmatches:
                    depts.append(course[match.start()+1:match.end()-1])

                post_dept_len = len(depts)

                if origin_dept_len == post_dept_len:
                    dept = re.compile(r'\s\D\D\D\D\s')
                    deptmatches = dept.finditer(course)

                    origin_dept_len = len(depts)

                    for match in deptmatches:
                        depts.append(course[match.start()+1:match.end()-1])
                    
                    post_dept_len = len(depts)

                    if origin_dept_len == post_dept_len:
                        raise Exception("FAILURE")

            numbermatches = number.finditer(course)

            sec_terms = ['A', 'B', 'C', 'D', 'E']
            
            sect_str = ''

            for match in numbermatches:
                nums.append(course[match.start():match.end()])
                sect_str = course[match.end():]

            x = None

            for term in sec_terms:
                x = re.search(term, sect_str[sect_str.find('- ')+1:])
                if x:
                    break
            
            sects.append(sect_str[x.start()+2:])

        for i in range(len(courses)):
            if sects[i][0] == 'A' or sects[i][0] == 'B' or sects[i][0] == 'C' or sects[i][0] == 'D' or sects[i][0] == 'E':
                if sects[i][0] == self.term:
                    student_schedule.append(course_info(depts[i], nums[i], sects[i], self.term, self.year))
            else:
                print("Invalid section format, likely an independent study, contact professor!")

        return student_schedule

class pullBooks(object):

    page_urls = {
        'find_books': '/shop/wpi/page/find-textbooks',
        'results': '/shop/BNCBTBListView?catalogId=10001&langId=-1&storeId=32554',
        'referer': '/shop/TextbookForwardControllerCmd'
    }



    def __init__(self, url, courselist):
        self.base_url = url
        self.courselist = courselist

        self.session = requests.Session()

        self.response = self.session.send(self.prepped_request(self.page_urls['find_books'], "GET"))

        self.cache = None

    def get_books(self):

        blacklist = ['PE']

        for course in self.courselist:
            if course.dept in blacklist:
                self.courselist.remove(course)

        search_results = []

        for i in range(len(self.courselist)):
            self.response = self.session.send(self.prepped_request(self.page_urls['find_books'], "GET"))
            self.cache = None
            term = ''
            if self.courselist[i].term == 'A' or self.courselist[i].term == 'B':
                term = 'Fall'
            elif self.courselist[i].term == 'C' or self.courselist[i].term == 'D':
                term = 'Spring'
            elif self.courselist[i].term == 'EI' or self.courselist[i].term == 'EII':
                term = 'Summer'

            term_string = f'{term} {self.courselist[i].year}({self.courselist[i].term}-term)'
        
            #ISOLATE TERM CODE

            inputpage = BeautifulSoup(self.response.text, 'html5lib')

            terms = inputpage.find_all('li', class_='bncbOptionItem termOption')

            term_code = None

            for term_item in terms:
                if term_string in term_item.text:
                    term_code = int(term_item.get('data-optionvalue'))
            
            if term_code == None:
                search_results = 'TERM NOT YET LISTED'
                break

            opener = AppURLopener()
            #DEPT URL

            dept_url = f'https://wpi.bncollege.com/shop/TextBookProcessDropdownsCmd?catalogId=10001&langId=-1&storeId=32554&campusId=30747386&termId={term_code}&deptId=&courseId=&sectionId=&dropdown=term&isOER=false'

            json_url = opener.open(dept_url)

            data = json.loads(json_url.read())

            dept_code = None

            for elmt in data:
                if self.courselist[i].dept in elmt['categoryName']:
                    dept_code = elmt['categoryId']

            if dept_code == None:
                raise Exception("Error obtaining dept code")

            #COURSE URL

            course_url = f'https://wpi.bncollege.com/shop/TextBookProcessDropdownsCmd?catalogId=10001&langId=-1&storeId=32554&campusId=30747386&termId={term_code}&deptId={dept_code}&courseId=&sectionId=&dropdown=dept&isOER=false'

            json_url = opener.open(course_url)

            data = json.loads(json_url.read())

            course_code = None

            for elmt in data:
                if self.courselist[i].number in elmt['categoryName']:
                    course_code = elmt['categoryId']

            if course_code == None:
                raise Exception("Error obtaining course code")

            #SECTION URL

            section_url = f'https://wpi.bncollege.com/shop/TextBookProcessDropdownsCmd?catalogId=10001&langId=-1&storeId=32554&campusId=30747386&termId={term_code}&deptId={dept_code}&courseId={course_code}&sectionId=&dropdown=course&isOER=false'

            json_url = opener.open(section_url)

            data = json.loads(json_url.read())

            section_code = None

            for elmt in data:
                if self.courselist[i].section in elmt['categoryName']:
                    section_code = elmt['categoryId']

            if section_code == None:
                raise Exception('Error obtaining section code')

            #SEARCH TERM CODE MATCHING SECTION AND SAVE IN VARIABLE


            search_info = {'isOER': False, 'storeId': 32554, 'catalogId': 10001, 'langId': -1, 'clearAll': '',
                           'viewName': 'TBWizardView', 'secCatList': '', 'removeSectionId': '', 'mcEnabled': 'N',
                           'showCampus': False, 'selectTerm': 'Select Term', 'selectDepartment': 'Select Department',
                           'selectSection': 'Select Section', 'selectCourse': 'Select Course', 'campus1': 30747386,
                           'firstTermName_30747386': 'Spring 2021(C-term)', 'firstTermID_30747386': 100604605,
                           'section_1': section_code, 'section_2': '', 'section_3': '', 'section_4': '', 'numberOfCourseAlready': 4}
            self.response = self.session.send(self.prepped_request(self.page_urls['results'], "POST", data=search_info))

            search_results.append(BeautifulSoup(self.response.text, 'html5lib'))

        return search_results

    def prepped_request(self, page_url, method, data={}):
        
        sleep(0.5)

        prepped = requests.Request(method, self.base_url + page_url, headers={'referer':self.base_url + self.page_urls['referer'], 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}, data=data)
        print("Prepped Request:" + self.base_url + page_url)
        return self.session.prepare_request(prepped)


    def update_classes(self, pages):

        if(pages == 'TERM NOT YET LISTED'):
            return(pages)


        for i in range(len(pages)):
            title = None
            ISBN = None
            Image = None

            try:
                title = pages[i].find('a', class_='clr121').get('title')
            except:
                title = None

            try:
                ISBN = pages[i].find('li', class_='book_c2_180616').text
            except:
                ISBN = None

            try:    
                Image = pages[i].find('img', class_='noImageDisReq').get('src')
            except:
                Image = None

            self.courselist[i].book_info(title, ISBN, Image)
    
    def find_online_vendors(self):
        sellers = ['amazon.com', 'barnesandnoble.com', 'cambridge.org']

        for course in self.courselist:
            search_results = None
            filtered_results = []
            if(course.title != None and course.isbn != None):
                search_results = search(f'{course.title} {str(course.isbn)}', tld="co.in", num=10, stop=10, pause=2)

                for result in search_results:
                    for seller in sellers:
                        if seller in result:
                            filtered_results.append(result)

            course.append_links(filtered_results)
            #NEED TO WEBSCRAPE THE LINKS FOR PRICES

def run_scrape(year, term, username, password):
    banner = pullSchedule('https://bannerweb.wpi.edu', username, password)
    classes = banner.extract_class_info(banner.get_classes(term, year))

    if classes == 'TERM NOT YET LISTED':
        err_courses = {'err': 1}

        with open(f'findbooks/web_scraper/json/books_{username}.json', 'w+') as f:
            json.dump(err_courses, f)
    
            f.close()
    else:
        bn_finder = pullBooks('https://wpi.bncollege.com', classes)
        err = bn_finder.update_classes(bn_finder.get_books())

        if err == 'TERM NOT YET LISTED':
            err_courses = {'err': 1}

            with open(f'findbooks/web_scraper/json/books_{username}.json', 'w+') as f:
                json.dump(err_courses, f)
        
                f.close()
        else:
            bn_finder.find_online_vendors()

            print("\n\nCOURSE-LIST\n\n")

            for course in classes:
                print(course.to_str())

            store_json(classes, username)
