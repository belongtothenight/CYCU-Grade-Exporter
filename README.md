# CYCU-Grade-Exporter

[![Version](https://img.shields.io/github/v/release/belongtothenight/CYCU-Grade-Exporter)](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/latest) [![Code Check](https://img.shields.io/github/workflow/status/belongtothenight/CYCU-Grade-Exporter/CodeQL)](https://github.com/belongtothenight/CYCU-Grade-Exporter/actions) [![Download](https://img.shields.io/github/downloads/belongtothenight/CYCU-Grade-Exporter/total)](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases)

Students from CYCU can use this to get their grade, credit, and course info exported from I-touch student's grade page.

## !!ATTENTION!! This repo is archived, and will no longer be updated

1. Previous releases including v1.0.1~v1.1.0 are all deleted since they can't perform the full functionality and some contains major flaw.
2. The calculation of G.P.A has not been proven correct yet, so only take it as a proximate number.
3. The auto-generated G.P.A score only calculates the courses you've passed.
4. Windows defender will try to stop you from executing this program, but no malicious code is contained, and it is safe to use despite Windows might give warnings. The table below is the test result from [VirusTotal](https://www.virustotal.com/gui/home/upload) which shows few alerts, and the source code itself had passed [CodeQL scans](https://github.com/belongtothenight/CYCU-Grade-Exporter/actions). Thus it's safe to execute.

| Release Version | Virus Test Score |                                             Virus Test Picture                                              | Release Version | Virus Test Score |                                             Virus Test Picture                                              |
| :-------------: | :--------------: | :---------------------------------------------------------------------------------------------------------: | :-------------: | :--------------: | :---------------------------------------------------------------------------------------------------------: |
|     v1.0.1      |       5/70       | [Virus Test 1](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal1.png) |     v1.0.1      |       5/70       | [Virus Test 2](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal2.png) |
|     v1.0.2      |       5/69       | [Virus Test 3](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal3.png) |     v1.1.0      |       4/66       | [Virus Test 4](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal4.png) |
|     v1.1.1      |       3/70       | [Virus Test 5](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal5.png) |     v2.0.0      |       3/69       | [Virus Test 6](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal6.png) |

## Develop Environment

- Windows 11
- Chrome (same as installed Chrome version)
  - chromedriver 104.0.5112.**
  - chromedriver 105.0.5195.**
  - chromedriver 106.0.5249.**
- python
  - numpy
  - bs4
  - selenium
  - pyautogui
  - pyperclip
  - requests

## Install

1. Go to [relase page](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/) and download the [latest installer](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/latest).
2. After starting the installer, click 'More Info' and 'run anyway' on Windows Defender Notification Page to start installing.
3. For installation destination, it is recommended to install in folders that don't need administrator permission. Suppose you want to install it in those folders, you'll need to execute it with administrator permission every time you want to use it.

## Steps to Use

Step 2-5 can be skipped if you press 'Auto'. But you might run into bugs.

1. Select the file type and extract the directory.
2. Click the button 'I-touch' to open up an i-touch website and sign in.
3. Go to '??????/????????????/??????????????????/???????????????(????????????+??????????????????)', and focus on the newly opened tab.
4. Use hotkey 'ctrl+u' to open the source code of the tab, and use 'ctrl+c' to copy all codes.
5. Paste the code using 'ctrl+v' into the text box and select exporting format (CSV suggested).
6. Click 'Extract'.
Once the button 'Extract' is clicked and successfully exported the file, a windows file browser window should pop up showing the exported file and open the file with default software. If not, please check if all the code on the webpage is pasted.

![Tutorial Video](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/video/tutorial.gif)

## Resource

[??????????????????????????????????????????](https://tdpba.cycu.edu.tw/wp-content/uploads/%E4%B8%AD%E5%8E%9F%E5%A4%A7%E5%AD%B8%E5%AD%B8%E7%94%9F%E5%AD%B8%E6%A5%AD%E6%88%90%E7%B8%BE%E8%80%83%E6%A0%B8%E8%BE%A6%E6%B3%95.pdf)

## Code Structure

- [CYCU_Grade_Exporter.py](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/src/CYCU_Grade_Exporter.py) (exe convertion)
  - [source_code_graber.py](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/src/source_code_graber.py)
- [CYCU_Grade_Exporter_Updater.py](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/src/CYCU_Grade_Exporter_Updater.py) (failed attempt/not deployed)
- [get_cursor_info.py](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/src/get_cursor_info.py) (not deployed)

## Update Log & Detail

| Release Version | Virus Test Score |                                             Virus Test Picture                                              |                                                                                    Download Link                                                                                    | Detail                     | Date     |
| :-------------: | :--------------: | :---------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | -------------------------- | -------- |
|     v1.0.1      |       5/70       | [Virus Test 1](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal1.png) |                                                                                      abandoned                                                                                      | -                          | 20220909 |
|     v1.0.1      |       5/70       | [Virus Test 2](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal2.png) |                                                                                      abandoned                                                                                      | + GUI + Grade Extractor    | 20220909 |
|     v1.0.2      |       5/69       | [Virus Test 3](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal3.png) |                                                                                      abandoned                                                                                      | + Bug Fix                  | 20220909 |
|     v1.1.0      |       4/66       | [Virus Test 4](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal4.png) |                                                                                      abandoned                                                                                      | + Auto Grade Extractor     | 20220910 |
|     v1.1.1      |       3/70       | [Virus Test 5](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal5.png) | [![v1.1.1](https://img.shields.io/github/downloads/belongtothenight/CYCU-Grade-Exporter/v1.1.1/total)](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/tag/v1.1.1) | + Bug Fix                  | 20220915 |
|     v2.0.0      |       3/69       | [Virus Test 6](https://github.com/belongtothenight/CYCU-Grade-Exporter/blob/main/virustest/virustotal6.png) | [![v2.0.0](https://img.shields.io/github/downloads/belongtothenight/CYCU-Grade-Exporter/v2.0.0/total)](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/tag/v2.0.0) | + Auto Update Notification | 20220916 |
