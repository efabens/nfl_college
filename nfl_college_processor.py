import json
import xlsxwriter as xlsx
from collections import defaultdict


def longest_current_t(team_dict):
    e = sorted(team_dict.keys(), reverse=True)
    longest = set()
    prev = e[0]
    for i in e:
        # print i
        temp = set(team_dict[i])
        if len(longest) == 0:
            longest = temp
            # print sorted(list(temp))
        else:
            temp.intersection_update(longest)
            # print sorted(list(temp))
        if len(temp) == 0:
            return longest, prev
        else:
            longest = temp
        prev = i
    return longest, prev


def xl_longest_current_t(all_teams, c_team):
    c_team.write(0, 0, 'Data Retrieved 3/13/2015 from footballdb.com')
    a, b = 1, 0
    for i, j in enumerate(['Team', 'First Year', 'College -->']):
        c_team.write(1, i, j)
    a, b = a + 1, 0
    for i in all_teams.keys():
        j, k = longest_current_t(all_teams[i])

        c_team.write(a, b, i)
        b += 1
        c_team.write(a, b, int(k))
        b += 1
        for m, n in enumerate(j):
            c_team.write(a, b + m, n)
        a, b = a + 1, 0


def longest_ever_t(team_dict):
    e = sorted(team_dict.keys(), reverse=True)
    max_years = 0
    max_teams = []
    current = defaultdict(int)
    for i in e:
        temp = set(team_dict[i])
        for j in set(current.keys()).union(temp):
            if j in temp:
                current[j] += 1
                if current[j] > max_years:
                    max_teams = [[j, current[j], i]]
                    max_years = current[j]
                elif current[j] == max_years:
                    max_teams.append([j, current[j], i])
            else:
                current[j] = 0
    return max_teams


def xl_longest_ever_t(all_teams, sheet, func=longest_ever_t):
    sheet.write(0, 0, 'Data Retrieved 3/13/2015 from footballdb.com')
    a, b = 1, 0
    for i, j in enumerate(['Team', 'Years', 'College', 'Start -->']):
        sheet.write(a, i, j)
    a+=1
    for i in all_teams:
        m = func(all_teams[i])
        sheet.write(a, b, i)
        b += 1
        for j in m:
            if b == 1:
                sheet.write(a, b, j[1])
                b+=1
            sheet.write(a, b, j[0])
            b+=1
            sheet.write(a, b, int(j[2]))
            b += 1
        b = 0
        a += 1


def most_years_t(team_dict):
    e = sorted(team_dict.keys(), reverse=True)
    max_years = 0
    max_teams = []
    current = defaultdict(int)
    for i in e:
        temp = set(team_dict[i])
        for j in temp:
            current[j] += 1
            if current[j] > max_years:
                max_teams = [[j, current[j], i]]
                max_years = current[j]
            elif current[j] == max_years:
                max_teams.append([j, current[j], i])
    return max_teams

def college_years(all_teams, sheet, uni=True):
    p=defaultdict(lambda: defaultdict(int))
    for i, j in all_teams.iteritems():
        for k, l in j.iteritems():
            for m in l:
                p[m][k]+=1
    return p




if __name__ == "__main__":
    with open("all_teams3.json", 'r') as outfile:
        all_teams = json.load(outfile)
    book = xlsx.Workbook('NFL Colleges.xlsx')
    c_team = book.add_worksheet('Longest Current')
    xl_longest_current_t(all_teams, c_team)

    l_ever_team = book.add_worksheet("Longest Tenure ever")
    xl_longest_ever_t(all_teams, l_ever_team)

    most_years_sheet = book.add_worksheet("Most Seasons on Team")
    xl_longest_ever_t(all_teams, most_years_sheet, func=most_years_t)

    r = college_years(all_teams, [])

    book.close()
