from bs4 import BeautifulSoup as bs
import urllib2
import re
import json

# get list of current teams (list)


def get_teams():
    url = 'http://www.footballdb.com/teams/index.html'
    a = urllib2.urlopen(url).read()
    soup = bs(a)
    e = soup.find(id='leftcol')
    q = e.find(class_='stattable')
    w = q.find_all(class_=re.compile("row"))
    team_urls = {}
    for i in w:
        team_urls[i.find('a').text] = (
            'http://www.footballdb.com' + i.find('a').get('href'))
    return team_urls

# take that list of current teams and go through each season (dict)
# for i in team_urls


def get_years(url, start=None):
    url += '/roster'
    a = urllib2.urlopen(url).read()
    soup = bs(a)
    r = soup.find_all(class_='fifth fleft')
    t = []
    for i in r:
        m=i.find('a')
        if int(i.text)>=start:
            t.append('http://www.footballdb.com' + m.get('href'))
    return t


def get_schools(url):
    print url
    try:
        year = int(url[-4:])
    except ValueError:
        print "current year"
        print url
        return current(url), 2015
    a = urllib2.urlopen(url).read()
    soup = bs(a)
    e = soup.find(id='leftcol')
    w = e.find_all(class_=re.compile('row'))
    t = set()
    for i in w:
        t.add(i.find_all('td')[-1].text.strip())
    return list(t), year


def current(url):
    a = urllib2.urlopen(url).read()
    soup = bs(a)
    e = soup.find(id='leftcol')
    r = e.find(class_='stattable')
    w = r.find_all(class_=re.compile('row'))
    t = set()
    for i in w:
        t.add(i.find_all('td')[-1].text.strip())
    return list(t)


# within each season get each college that is listed (list)


# create something that visualizes this is some manner

if __name__ == '__main__':
    f = get_teams()
    with open("all_teams2.json", 'r') as outfile:
        full_list = json.load(outfile)
    for i, j in f.iteritems():
        t = get_years(j, start=2014)
        for k in t:
            n, m = get_schools(k)
            full_list[i][str(m)] = n
    with open('all_teams3.json', 'w') as outfile:
        json.dump(full_list, outfile, sort_keys=True, indent=4)
    # f=get_years('http://www.footballdb.com/teams/nfl/buffalo-bills/roster')
    # f=get_schools('http://www.footballdb.com/teams/afl/buffalo-bills/roster')
