from tkinter.filedialog import askdirectory
from bs4 import BeautifulSoup
from os import system, startfile, remove, getcwd
from os.path import join, exists
from csv import writer
from webbrowser import open as open_url
import numpy as np
import tkinter as tk
from tkinter import ttk
from requests import get
import ctypes
from source_code_graber import auto_get_source_code

system('cls')
'''software information'''
# get latest release version
sf_version = 'v2.0.0'
github_repo_release_url = 'https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/'
github_repo_latest_release_url = 'https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/latest/'
i_touch_link = 'https://itouch.cycu.edu.tw/home/#/ann'
response = get(github_repo_latest_release_url)
html = response.text
html = BeautifulSoup(html, 'html.parser').find_all('meta')
text = []
for x in html:
    text.append(x.get('content'))
i = 0
# for x in text:
#     print(str(i) + ' ' + str(x))
#     i += 1
latest_sf_version = text[20].split('/')[-1]  # get from release page
# print(latest_sf_version)
# print(text[24])
if ('Update necessity: True' or 'Update necessity: true') in text[24]:
    update_necessity = True
elif ('Update necessity: False' or 'Update necessity: false') in text[24]:
    update_necessity = False
else:
    update_necessity = False

'''window variable'''
user32 = ctypes.windll.user32
max_width = int(user32.GetSystemMetrics(0))
max_height = int(user32.GetSystemMetrics(1))
sizex = max_width // 2
sizey = max_height // 2
size_updater = str(sizex//3) + 'x' + str(sizey//3) + \
    '+' + str(sizex-sizex//3//2) + '+' + str(sizey-sizey//3//2)
size = str(sizex) + 'x' + str(sizey) + '+' + \
    str(sizex-sizex//2) + '+' + str(sizey-sizey//2)
color = '#002EA4'
updater_text = ['\t\t\t\t\t\n', 'New version available. Please update.\n',
                'Update necessity: {0}\n'.format(update_necessity)]
description_text = [
    'ATTENSION: ',
    'This program is only for the students of Chung Yuan Christian University to extract grades from I-touch. \n\
If you use this program to extract grades from other websites or grades of other students, you will be responsible for the consequence.',
    'How To Use: ',
    'Step 2-5 can be skipped if you press \'Auto\'. But you might run into bugs.\n\
1. Select extract directory and file type. \n\
2. Click the button \'I-touch\' to open up an i-touch website and sign in. \n\
3. Go to \'學業/學習足跡/歷年學習成績/新視窗開啟\', and focus on the newly opened tab. \n\
4. Use hotkey \'ctrl+u\' to open source code of the tab, and use \'ctrl+c\' to copy all codes. \n\
5. Paste the codes using \'ctrl+v\' into the text box and select exporting format. \n\
6. Click \'Extract\'.',
]


def version_check():
    def release_fun():
        open_url(github_repo_release_url)
        exit()

    def latest_release_fun():
        open_url(github_repo_latest_release_url)
        exit()
    version_path = join(getcwd(), 'version.txt')
    # print(version_path)
    if exists(version_path):
        with open(version_path, 'r') as f:
            version = f.read()
        print(version)
        if version != latest_sf_version:
            print('version not match')
            updater = tk.Tk()
            updater.title('CYCU Grade Exporter Updater')
            updater.configure()
            updater.geometry(size_updater)
            updater.resizable(False, False)
            update_message = tk.Label(
                updater, text="\n".join(
                    updater_text), justify='center', wraplength=sizex*0.4)
            update_message.pack(side='top', fill='x')
            '''if update_necessity == True:
                updater_path = join(getcwd(), 'updater.exe')
                if exists(updater_path):
                    startfile(updater_path)
                    progress = tk.Label(
                        updater, text='updating...', justify='center')
                    progress.pack()
                    updater.after(1500, lambda: updater.destroy())
                    updater.focus_force()
                    updater.mainloop()
                    exit()
                else:
                    progress = tk.Label(
                        updater, text='Updater not found, please reinstall.', justify='center')
                    progress.pack()
                    release = tk.Button(
                        updater, text='Release', command=release_fun)
                    latest_release = tk.Button(
                        updater, text='Latest Release', command=latest_release_fun)
                    latest_release.pack(side='left', expand=True)
                    release.pack(side='left', expand=True)
                    updater.focus_force()
                    updater.mainloop()

            else:
                release = tk.Button(
                    updater, text='Release', command=release_fun)
                latest_release = tk.Button(
                    updater, text='Latest Release', command=latest_release_fun)
                latest_release.pack(side='left', expand=True)
                release.pack(side='left', expand=True)
                updater.focus_force()
                updater.mainloop()'''
            version_text = 'Current version: {0}\nLatest version: {1}'.format(
                sf_version, latest_sf_version)
            version = tk.Label(updater, text=version_text, justify='center')
            version.pack()
            release = tk.Button(
                updater, text='Release', command=release_fun)
            latest_release = tk.Button(
                updater, text='Latest Release', command=latest_release_fun)
            release.pack(side='left', expand=True)
            latest_release.pack(side='left', expand=True)
            updater.focus_force()
            updater.mainloop()

    else:
        with open(version_path, 'w') as f:
            f.write(sf_version)


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
        soup = soup[0:1]
        soup = soup[0]
        soup = list(filter(filter_vowels, soup))

        '''title'''
        title = self.str_purify(soup[0])
        # print(title)

        '''header_row'''
        for element in soup[1].find_all('b'):
            element = self.str_purify(element)
            header_row.append(element)

        '''content_row'''
        for i in range(2, len(soup)):
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
        return doc_grade

    def print_all(self):
        print(self.doc.prettify())

    def print_element(self, list):
        i = 0
        try:
            for element in list:
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
            else:
                semester_buf = x[0]
                self.semester.append(semester_buf)
                self.credit.append(credit_sum)
                credit_sum = 0
                if x[7] == '及格':
                    credit_sum += int(x[6])
        self.credit.append(credit_sum)
        self.credit.append(sum(self.credit))

        '''deal with duplicate subject'''
        for x in range(len(self.grade[2])-1, 0, -1):
            if self.grade[2][x][3] in course and self.grade[2][x][7] == '及格':
                self.credit[-1] -= int(self.grade[2][x][6])
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
            if i in rng:
                j = rng.index(i)
                self.gpa[j] = (cross_buf2 / credit_buf2)
                cross_buf2 = 0
                credit_buf2 = 0
            if x[7] != '及格':
                i += 1
                continue
            cross_buf2 += int(x[6]) * int(x[-1])
            credit_buf2 += int(x[6])
            cross_buf1 += cross_buf2
            credit_buf1 += credit_buf2
            i += 1
        self.gpa.append(cross_buf1 / credit_buf1)
        '''export'''
        self.grade[0].append('Total')
        self.semester.append('Total')
        self.identity = list(filter(None, self.identity))
        export_data_a = []
        i = 0
        buf = []
        export_data_a.append(self.identity)
        export_data_a.append([''])
        for x in range(0, len(self.exemption[1])):
            buf.append(
                self.exemption[2][i:i+len(self.exemption[1])])
            i += len(self.exemption[1])
        export_data_a.append([self.exemption[0]])
        export_data_a.append(self.exemption[1])
        for x in buf:
            export_data_a.append(x)
        export_data_a.append([''])
        export_data_a.append(self.grade[1])
        for x in self.grade[2]:
            export_data_a.append(x)
        export_data_a.append([''])
        export_data_a.append(self.grade[0])
        export_data_a.append(self.semester)
        export_data_a.append(self.credit)
        export_data_a.append(self.gpa)
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
        self.filetype_selected = tk.StringVar(value='select')
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
        self.description.place(x=sizex/2-390, y=180)
        self.description = tk.Label(self, text=description_text[3], font=(
            'Consolas', 12), bg=self.color, fg='white', anchor='center', justify='left', wraplength=sizex*0.9)
        self.description.place(x=sizex/2-420, y=210)
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
        self.code = tk.Entry(self, width=45, font=(
            'Consolas', 14), textvariable=self.source_code)
        self.code.place(x=sizex/2-300, y=420, anchor='w')
        self.filetype = ttk.Combobox(self, width=6, font=(
            'Consolas', 12), textvariable=self.filetype_selected)
        self.filetype['values'] = ('.csv', '.txt')
        self.filetype.place(x=sizex/2+240, y=420, anchor='e')
        self.i_touch = tk.Button(self, text='Auto', font=(
            'Consolas', 12), command=self.get_source_code)
        self.i_touch.place(x=sizex/2+300, y=420, anchor='e')
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

    def get_source_code(self):
        def confirm():
            username.set(entry_1.get())
            password.set(entry_2.get())
            graber.destroy()
            self.source_code.set(auto_get_source_code(
                username.get(), password.get()))
            if self.source_code.get() == '':
                return
        graber = tk.Tk()
        graber.title('CYCU Grade Exporter')
        graber.configure()
        graber.resizable(False, False)
        username = tk.StringVar(value='')
        password = tk.StringVar(value='')
        label1 = tk.Label(graber, text='Username', font=(
            'Consolas', 12))
        label1.grid(column=0, row=0)
        entry_1 = tk.Entry(graber, width=20, font=(
            'Consolas', 12), textvariable=username)
        entry_1.grid(column=1, row=0)
        label2 = tk.Label(graber, text='Password', font=(
            'Consolas', 12))
        label2.grid(column=0, row=1)
        entry_2 = tk.Entry(graber, width=20, font=(
            'Consolas', 12), textvariable=password, show='*')
        entry_2.grid(column=1, row=1)
        button1 = tk.Button(graber, text='Confirm', font=(
            'Consolas', 12), command=confirm)
        button1.grid(column=1, row=2)
        graber.focus_force()
        graber.mainloop()
        # self.source_code.set(auto_get_source_code(
        #     username.get(), password.get()))

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
    version_check()
    main_window = Window(size, sizex, sizey, color)
