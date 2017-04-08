import requests, json

semester = '92016' # September (Fall) 2016
campus = 'NB' # New Brunswick
level = 'U' # Undergraduate

def main():

    courses_to_scrape = {"01:198:170": {"name": None, "sections_wanted": []},
                         "01:198:211": {"name": None, "sections_wanted": [5, 6, 7]}}

    list_of_subjects = get_all_subjects(courses_to_scrape)
    start_check(list_of_subjects, courses_to_scrape)

    return


def get_all_subjects(d): # d = courses_to_scrape

    tmp_list = set()

    for course in d:
        subject_code = str(course).split(':')[1]
        tmp_list.add(subject_code)

    return list(tmp_list)

def start_check(s, c):

    for subject in s:
        url = 'https://sis.rutgers.edu/soc/courses.json?subject={}&semester={}&campus={}&level={}'\
            .format(subject, semester, campus, level)

        r = requests.get(url)
        r_dict = json.loads(r.text)

        for x in r_dict:
            course = '{}:{}:{}'.format(x['offeringUnitCode'], x['subject'], x['courseNumber'])
            if course in c:
                c[course]['name'] = x['title']
                print ("{} ({})".format(course, c[course]['name']))
                for section in x['sections']:

                    section_status = 'OPEN' if section['openStatus'] else 'CLOSED'

                    if int(section['number']) in c[course]['sections_wanted']:
                        print ("\t\t{} | {}".format(section['number'], section_status))
                    elif not c[course]['sections_wanted']:
                        print ("\t\t{} | {}".format(section['number'], section_status))

    return

if __name__ == '__main__':
    main()
