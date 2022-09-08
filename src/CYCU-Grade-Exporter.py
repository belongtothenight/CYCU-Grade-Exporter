from tkinter.filedialog import askdirectory
from bs4 import BeautifulSoup
from os import system, startfile, remove, getcwd
from os.path import join, exists
from csv import writer
from webbrowser import open as open_url
import numpy as np
import tkinter as tk
from tkinter import ttk

sizex = 960
sizey = 540
size = str(sizex) + 'x' + str(sizey)
color = '#002EA4'
description_text = [
    'ATTENSION: ',
    'This program is only for the students of Chung Yuan Christian University to extract grades from I-touch. \n\
If you use this program to extract grades from other websites or grades of other students, you will be responsible for the consequence.',
    'How To Use: ',
    '1. Click the button \'I-touch\' to open up an i-touch website and sign in. \n\
2. Go to \'學業/學習足跡/歷年學習成績/新視窗開啟\', and focus on the newly opened tab. \n\
3. Use hotkey \'ctrl+u\' to open source code of the tab, and use \'ctrl+c\' to copy all codes. \n\
4. Paste the codes using \'ctrl+v\' into the text box and select exporting format. \n\
5. Select the file type and extract directory. \n\
6. Click \'Extract\'.',
]
i_touch_link = 'https://itouch.cycu.edu.tw/home/#/ann'


class WP:
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as f:
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
        doc_identity = list(filter(None, doc_identity))
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


class WPP(WP):
    def __init__(self, pathA, pathB, output_mode):
        self.pathA = pathA
        self.pathB = pathB
        self.output_mode = output_mode
        sg = WP(self.pathA)
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
        self.grade[0].append('Total')
        self.semester.append('Total')
        self.identity = list(filter(None, self.identity))
        export_data_a = []
        export_data_b = []
        i = 0
        buf = []
        for x in range(0, len(self.semester[1])):
            buf.append(
                self.exemption[2][i:i+len(self.exemption[1])])
            i += len(self.exemption[1])
        export_data_a.append(self.identity)
        export_data_a.append([self.exemption[0]])
        export_data_a.append(self.exemption[1])
        for x in buf:
            export_data_a.append(x)
        export_data_a.append(self.grade[1])
        for x in self.grade[2]:
            export_data_a.append(x)
        export_data_a.append(self.grade[0])
        export_data_a.append(self.semester)
        export_data_a.append(self.credit)
        export_data_a.append(self.gpa)
        # print(export_data_a)
        if self.output_mode == 1:
            # export csv
            print('exporting csv...')
            path_csv = self.pathB + \
                self.identity[1] + '_' + self.identity[-2] + '.csv'
            with open(path_csv, 'w+', encoding='utf-8-sig', newline='') as f:
                w = writer(f)
                for element in export_data_a:
                    w.writerow(element)
            print('Exported to ' + self.pathB)
            startfile(self.pathB)
            startfile(path_csv)
        elif self.output_mode == 2:
            # export txt
            print('exporting txt...')
            path_txt = self.pathB + \
                self.identity[1] + '_' + self.identity[-2] + '.txt'
            with open(path_txt, 'w', encoding='utf-8') as f:
                for element in export_data_a:
                    f.write(str(element) + '\n')
            print('Exported to ' + self.pathB)
            startfile(self.pathB)
            startfile(path_txt)
        else:
            print('Nothing is exported.')


class Window(tk.Tk, WPP):
    def __init__(self, size, sizex, sizey, color):
        self.size = size
        self.color = color
        tk.Tk.__init__(self)
        self.title('CYCU Grade Exporter')
        self.geometry(self.size)
        self.configure(bg=self.color)
        self.resizable(False, False)
        self.dst = tk.StringVar()
        self.source_code = tk.StringVar()
        self.canvas = tk.Canvas(
            self, width=sizex, height=sizey, bg=self.color, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_text(
            sizex/2, 40, text='CYCU Grade Exporter', font=('Arial', 30), fill='white')
        self.description = tk.Label(self, text=description_text[0], font=(
            'Arial', 17), bg=self.color, fg='white', anchor='center', justify='left')
        self.description.place(x=sizex/2-390, y=60)
        self.description = tk.Label(self, text=description_text[1], font=(
            'Consolas', 12), bg=self.color, fg='white', anchor='center', justify='left', wraplength=sizex*0.9)
        self.description.place(x=sizex/2-420, y=90)
        self.description = tk.Label(self, text=description_text[2], font=(
            'Arial', 17), bg=self.color, fg='white', anchor='center', justify='left')
        self.description.place(x=sizex/2-390, y=190)
        self.description = tk.Label(self, text=description_text[3], font=(
            'Consolas', 12), bg=self.color, fg='white', anchor='center', justify='left', wraplength=sizex*0.9)
        self.description.place(x=sizex/2-420, y=230)
        self.canvas.create_text(
            sizex/2-380, 380, text='Export Folder', font=('Consolas', 14), fill='white', justify='left')
        self.dst_path = tk.Entry(self, width=60, font=(
            'Consolas', 14), textvariable=self.dst)
        self.dst_path.place(x=sizex/2-300, y=380, anchor='w')
        self.browse = tk.Button(self, text='Browse', font=(
            'Consolas', 14), command=self.find_dst)
        self.browse.place(x=sizex/2+400, y=380, anchor='e')
        self.canvas.create_text(
            sizex/2-380, 420, text='Source Code', font=('Consolas', 14), fill='white', justify='right')
        self.code = tk.Entry(self, width=50, font=(
            'Consolas', 14), textvariable=self.source_code)
        self.code.place(x=sizex/2-300, y=420, anchor='w')
        self.filetype = ttk.Combobox(self, width=5, font=('Consolas', 14))
        self.filetype['values'] = ('.csv', '.txt')
        self.filetype.place(x=sizex/2+300, y=420, anchor='e')
        self.i_touch = tk.Button(self, text='I-touch', font=(
            'Consolas', 12), command=self.openwp)
        self.i_touch.place(x=sizex/2+400, y=420, anchor='e')
        self.extract = tk.Button(self, text='Extract', font=(
            'Consolas', 17), command=self.extract_data)
        self.extract.place(x=sizex/2, y=490, anchor='center')
        self.focus_force()
        self.mainloop()

    def find_dst(self):
        self.dst.set(tk.filedialog.askdirectory(initialdir=getcwd()))
        print(self.dst.get())

    def openwp(self):
        open_url(i_touch_link)

    def extract_data(self):
        try:
            self.source_code = self.code.get()
            self.dst = self.dst_path.get()
            if not exists(self.dst):
                return
            if str(self.source_code) == '':
                return
            filename = 'source_code_buffer'
            with open(join(self.dst, filename + '.txt'), 'w', encoding='utf-8') as f:
                f.write(self.source_code)
            print('Source code is saved to ' +
                  join(self.dst, filename + '.txt'))
            mode = self.filetype.get()
            # print(mode)
            if mode == '.csv':
                WPP(join(self.dst, filename + '.txt'),
                    join(self.dst, ''), 1)
            elif mode == '.txt':
                WPP(join(self.dst, filename + '.txt'),
                    join(self.dst, ''), 2)
            else:
                print('Please select a file type.')
            remove(join(self.dst, filename + '.txt'))
        except:
            pass


if __name__ == '__main__':
    system('cls')
    main_window = Window(size, sizex, sizey, color)
