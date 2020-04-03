from data.post_params import __EVENTARGUMENT, __EVENTARGUMENT, __EVENTTARGET, __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION, __LASTFOCUS
from data.codes import course_drop_down
from lib.validate import validate

from urllib.parse import urlencode
import pycurl

from bs4 import BeautifulSoup
import re

import csv

class CallBack:
  def __init__(self):
    self.contents = ''

  def body_callback(self, buf):
    self.contents = self.contents + buf.decode('utf-8')

cb=CallBack()

PARAMS = {
    "__EVENTARGUMENT": __EVENTARGUMENT,
    "__EVENTTARGET": __EVENTTARGET,
    "__VIEWSTATE": __VIEWSTATE,
    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
    "__EVENTVALIDATION": __EVENTVALIDATION,
    "__LASTFOCUS": __LASTFOCUS,
    "ctl00$HeaderContent$CourseYearDropdown": 1,
    "ctl00$HeaderContent$CourseDropdown": "LM338"
}

url = "http://www.timetable.ul.ie/UA/CourseTimetable.aspx"

def post_call(course, year):
  PARAMS["ctl00$HeaderContent$CourseDropdown"] = course
  PARAMS["ctl00$HeaderContent$CourseYearDropdown"] = year  

  crl = pycurl.Curl()
  crl.setopt(crl.URL, url)
  data = PARAMS #{'field': 'value'}
  pf = urlencode(data)

  crl.setopt(crl.POSTFIELDS, pf)
  crl.setopt(pycurl.WRITEFUNCTION, cb.body_callback)

  data = crl.perform()

  crl.close()
  return cb.contents

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def parse_html(html_data, course, year):
  soup = BeautifulSoup(html_data, features="html.parser")

  tables = soup.find_all('table')
  extracts = []
  for i, table in enumerate(tables):
    for i, rows in enumerate(table.find_all('tr')):
      #print('--------------------col----------------start')
      for di, col in enumerate(rows.find_all('td')):
        #print(col)
        fonts = col.find_all('font')
        for font in fonts:
          if font.contents[0] != "\xa0":
            line = ""
            flag = True
            for text in font.contents:
              if isinstance(text, str):
                #print(f"******{text}*********")
                if text == ' ':
                  line = line + '|' + days[di] + '|' + course + '|' + year
                  extracts.append(line)
                  line = ""
                  flag = False
                  continue
                line = line + '|' + text.strip()
            line = line + '|' + days[di] + '|' + course + '|' + year




            #print(line)
            if flag:
              extracts.append(line)
      #print('--------------------col----------------end')

  return extracts


filename = "./one.1.csv"
f = csv.writer(open(filename, "w"))
f.writerow(["start_time", "end_time", "module", "class_type", "staff", "room_number", "duration", "start_weeek", "week", "day", "course", "year"])

def get_all_weeks(duration):
  #print(duration)
  if len(duration) == 1:
    return [int(duration)]

  ranges = duration.split(',')
  arr = []
  for rng in ranges:
    #print(f"rng-->{rng}<---")
    if len(rng) == 1 or len(rng) == 2:
      arr = [int(rng)]
      continue
    data = rng.split('-')
    data = [int(s) for s in data]
    arr = arr + list(range(data[0], data[1]+1))
  return arr

def write_to_csv(extracts):

  for line in extracts:
    data = line.split('|')
    data = validate(data)

    #print("***2", data)
    time = data[1].split('-')
    st = time[0].strip().split(':')[0]
    et = time[1].strip().split(':')[0]
 
    module_d = data[2].split('-')
    module = module_d[0].strip()
    class_type = module_d[1].strip()
 
    staff = data[3].strip()
    room_no = data[4].strip()
 
    duration = data[5].strip()
    weeks = get_all_weeks(duration)
    #print("weeks----->", weeks)

    start_week = duration.split('-')[0]
 
    day = data[6]
    #others = data[]
    course = data[7]
    year = data[8]
 
    for week in weeks: 
      f.writerow([ st, et, module, class_type, staff, room_no, duration, start_week, week, day, course, year ])

  return True


years = [1, 2, 3, 4]
for year in years:
  for i, course in enumerate(course_drop_down):
    print("--->course--->", course, year)
    #try:
    if i == 10:
      break
    html_data = post_call(course, year)
    extracts  = parse_html(html_data, course, str(year))
    csv       = write_to_csv(extracts)
    #except:
    #  pass


