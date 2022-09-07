from bs4 import BeautifulSoup
from os import system
import numpy as np
import csv
pathA = 'D:/Note_Database/School/Master/Consolation/Grab grade from text/https __itouch.cycu.edu.tw_active_system_quary_s_grade.jsp'
pathB = 'D:/Note_Database/School/Master/Consolation/Grab grade from text/'


class wp:
    def __init__(self, path):
        with open(path, 'rb') as f:
            self.doc = BeautifulSoup(f, 'html.parser')

    def str_purify(self, string):
        string = str(string.text).strip()
        string = string.replace('\n', '')
        string = string.replace('\r', '')
        string = string.replace(' ', '')
        return string

    def find_identity(self):
        doc_identity = str(self.doc.find_all('b')[1])
        doc_identity = doc_identity.split(' ')
        doc_identity = list(filter(None, doc_identity))
        doc_identity = doc_identity[2:-1]
        doc_identity = [x.strip() for x in doc_identity]
        return doc_identity

    def find_exemption(self):
        soup = []
        doc_exemption = []
        title = ''
        header_row = []
        content_row = []

        def filter_vowels(list):
            vowels = ['\n']
            return False if list in vowels else True

        for element in self.doc.find_all('table', ['700', '#000000', '#808080', '#FFFFFF', '9-font', '#000000', '1', 'center']):
            element = list(filter(None, element))
            soup.append(element)
        soup = soup[0]
        soup = list(filter(filter_vowels, soup))

        '''title'''
        title = self.str_purify(soup[0])
        # print(title)

        '''header_row'''
        # print(soup[1].prettify())
        for element in soup[1].find_all('b'):
            element = self.str_purify(element)
            header_row.append(element)
        # print(header_row)

        '''content_row'''
        for i in range(2, len(soup)-1):
            # print(soup[i].prettify() + '\n')
            for element in soup[i].find_all('td'):
                element = self.str_purify(element)
                content_row.append(element)

        '''combine'''
        doc_exemption.append(title)
        doc_exemption.append(header_row)
        doc_exemption.append(content_row)
        return doc_exemption

    def find_grade(self):
        doc_grade = []
        title = []
        header_row = ['編號', '開課系級', '課程類別', '課程名稱',
                      '必 / 選修', '成績', '學分數', '備註一', '備註二', '備註三']
        content_row = []
        soup = self.doc.find_all('table', [
            'center', '#000000', '#000000', '#FFFFFF', '#808080', '1', '9-font', '99%'])
        soup = soup[2:]
        soup_len = len(soup)
        content_row = np.zeros(shape=(soup_len, 10), dtype=str)
        for element1 in soup:
            element2 = element1.find_all('tr')
            '''title'''
            title.append(self.str_purify(element2[0]))
            '''content_row'''
            for i in range(2, len(element2)-1):
                buf = []
                for element3 in element2[i].find_all('font'):
                    element3 = self.str_purify(element3)
                    buf.append(element3)
                content = np.array(buf)
                content = np.expand_dims(content, axis=0)
                content_row = np.append(content_row, content, axis=0)
        content_row = np.ndarray.tolist(content_row)
        content_row = [x for x in content_row if x !=
                       ['', '', '', '', '', '', '', '', '', '']]
        '''return'''
        doc_grade.append(title)
        doc_grade.append(header_row)
        doc_grade.append(content_row)
        # print(len(header_row))
        # print(len(content_row))
        return doc_grade

    def print_all(self):
        print(self.doc.prettify())

    def print_element(self, list):
        i = 0
        try:
            for element in list:
                # print(str(i) + ' ' + str(element))
                print(str(i) + ' ' + str(element) + '\n')
                i += 1
        except:
            print(list)


class wpp(wp):
    def __init__(self, pathA, pathB, csv_mode):
        sg = wp(pathA)
        self.identity = sg.find_identity()
        self.exemption = sg.find_exemption()
        self.grade = sg.find_grade()
        self.credit = []
        self.semester = []
        self.gpa = []

        '''gather credit data'''
        semester_buf = self.grade[2][0][0]
        self.semester.append(semester_buf)
        credit_sum = 0
        course = []
        for x in self.grade[2]:
            if x[0] == semester_buf:
                if x[7] == '及格':
                    credit_sum += int(x[6])
                # print(str(x[6]) + ' / ' + str(credit_sum))
            else:
                semester_buf = x[0]
                self.semester.append(semester_buf)
                self.credit.append(credit_sum)
                credit_sum = 0
                if x[7] == '及格':
                    credit_sum += int(x[6])
                # print(str(x[6]) + ' / ' + str(credit_sum))
        self.credit.append(credit_sum)
        self.credit.append(sum(self.credit))

        '''deal with duplicate subject'''
        for x in range(len(self.grade[2])-1, 0, -1):
            if self.grade[2][x][3] in course and self.grade[2][x][7] == '及格':
                self.credit[-1] -= int(self.grade[2][x][6])
                # index = self.semester.index(self.grade[2][x][0])
                # self.credit[index] -= int(self.grade[2][x][6])
            course.append(self.grade[2][x][3])
        '''append grade info'''
        self.grade[1].append('等第')
        self.grade[1].append('RANK')
        self.grade[1].append('G.P.A')
        for x in self.grade[2]:
            try:
                score = int(x[5])
            except:
                score = -1
            if score >= 95:
                x.append('甲')
                x.append('A+')
                x.append(4)
            elif score >= 90:
                x.append('甲')
                x.append('A')
                x.append(4)
            elif score >= 80:
                x.append('甲')
                x.append('A-')
                x.append(4)
            elif score >= 77:
                x.append('乙')
                x.append('B+')
                x.append(3.67)
            elif score >= 73:
                x.append('乙')
                x.append('B')
                x.append(3.33)
            elif score >= 70:
                x.append('乙')
                x.append('B-')
                x.append(3)
            elif score >= 67:
                x.append('丙')
                x.append('C+')
                x.append(2.67)
            elif score >= 63:
                x.append('丙')
                x.append('C')
                x.append(2.33)
            elif score >= 60:
                x.append('丙')
                x.append('C-')
                x.append(2)
            elif score >= 57:
                x.append('丁')
                x.append('D+')
                x.append(1.67)
            elif score >= 53:
                x.append('丁')
                x.append('D')
                x.append(1.33)
            elif score >= 50:
                x.append('丁')
                x.append('D-')
                x.append(1)
            else:
                x.append('戊')
                x.append('F')
                x.append(0)
        '''gpa'''
        rng = np.empty(shape=(len(self.semester)))
        rng = np.ndarray.tolist(rng)
        self.gpa = np.empty(shape=(len(self.semester)))
        self.gpa = np.ndarray.tolist(self.gpa)
        cross_buf1 = 0
        cross_buf2 = 0
        credit_buf1 = 0
        credit_buf2 = 0
        i = 0
        for x in self.grade[2]:
            y = self.semester.index(x[0])
            rng[y] = i
            i += 1
        i = 0
        for x in self.grade[2]:
            # print(str(i) + ' ' + str(x))
            if i in rng:
                j = rng.index(i)
                self.gpa[j] = (cross_buf2 / credit_buf2)
                # print(str(cross_buf2) + ' / ' + str(credit_buf2))
                cross_buf2 = 0
                credit_buf2 = 0
                # print()
            if x[7] != '及格':
                i += 1
                continue
            cross_buf2 += int(x[6]) * int(x[-1])
            credit_buf2 += int(x[6])
            # print(str(x[6]) + ' * ' + str(x[-1]) + ' = ' +
            #       str(int(x[6])*int(x[-1])) + ' / ' + str(cross_buf2) + ' / ' + str(credit_buf2))
            cross_buf1 += cross_buf2
            credit_buf1 += credit_buf2
            i += 1
        self.gpa.append(cross_buf1 / credit_buf1)
        # print(rng)
        '''export'''
        if csv_mode == 0:
            print('Nothing is exported.')
        elif csv_mode == 1:
            pathB = pathB + self.identity[1] + '_' + self.identity[2] + '.csv'
            with open(pathB, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.identity)
                writer.writerow('\n')
                writer.writerow([self.exemption[0]])
                writer.writerow('\n')
                writer.writerow(self.exemption[1])
                i = 0
                for x in range(0, len(self.semester[1])):
                    writer.writerow(
                        self.exemption[2][i:i+len(self.exemption[1])])
                    i += len(self.exemption[1])
                writer.writerow('\n')
                writer.writerow(self.grade[0])
                writer.writerow('\n')
                writer.writerow(self.grade[1])
                for x in self.grade[2]:
                    writer.writerow(x)
                writer.writerow('\n')
                for x in self.semester:
                    writer.writerow([x])
                writer.writerow('\n')
                for x in self.credit:
                    writer.writerow([x])
                writer.writerow('\n')
                for x in self.gpa:
                    writer.writerow([x])
            print('Exported to ' + pathB)
        elif csv_mode == 2:
            print('Exported to ' + pathB)


if __name__ == '__main__':
    system('cls')
    s = wpp(pathA, pathB, 1)
