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
                current[j]=0
    return max_teams


def xl_longest_ever_t(all_teams, sheet):
    sheet.write(0, 0, 'Data Retrieved 3/13/2015 from footballdb.com')
    a, b = 1, 0
    for i, j in enumerate(['Team', 'College', 'Start', 'Years -->'])
        sheet.write(1, i, j)
    for i in all_teams:
        print i, longest_ever_t(all_teams[i])



def most_years_t(team_dict):
    pass

if __name__ == "__main__":
    with open("all_teams3.json", 'r') as outfile:
        all_teams = json.load(outfile)
    book = xlsx.Workbook('NFL Colleges.xlsx')
    c_team = book.add_worksheet('Longest Current')
    xl_longest_current_t(all_teams, c_team)

    l_ever_team = book.add_worksheet("Longest Tenure ever")
    xl_longest_ever_t(all_teams, l_ever_team)

    book.close()
