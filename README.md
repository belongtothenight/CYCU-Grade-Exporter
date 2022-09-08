# CYCU-Grade-Exporter

This script take webpage source code and spite out csv file containing CYCU student's grade related data.

## ATTENTION

The calculation of G.P.A has not being proven correct yet, so only take it only as a proximate number.
Also, the auto generated G.P.A score only calculate the courses you've passed.

## Develop Environment

- Windows 11
- python
  - numpy
  - bs4

## Install

Go to [relase page](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/tag/V1.0.2) and download installer.</br>
For installation destination, it is recommended to install in folders that doesn't need admistrator permisson. If you want to install in those folders, you'll need to execute it with admistrator permisson everytime you want to use it.

No malicious code is contained, it is safe to use despite Windows might give warning. The table below is the test result from [VirusTotal](https://www.virustotal.com/gui/home/upload).
| Virus Detection | Score | Picture                                                                                            |
| --------------- | ----- | -------------------------------------------------------------------------------------------------- |
| v1.0.1          | 5/67  | [Test 1](https://github.com/belongtothenightCYCU-Grade-Exporter/blob/main/picture/virustotal1.png) |
| v1.0.1          | 5/67  | [Test 2](https://github.com/belongtothenightCYCU-Grade-Exporter/blob/main/picture/virustotal2.png) |
| v1.0.2          | 5/67  | [Test 3](https://github.com/belongtothenightCYCU-Grade-Exporter/blob/main/picture/virustotal3.png) |

## Steps to Use

1. Use webbrowser like Google or Firefox to open up i-touch website and sign-in.
2. Go to '學業/學習足跡/歷年學習成績/新視窗開啟(右上角灰+白的圓形按鈕)', and focus on the new opened tab.
3. Use hotkey 'ctrl+u' to open source code of the tab, and use 'ctrl+c' to copy all codes.
4. Paste the code using 'ctrl+v' into the text box and select exportint format (csv suggested).
5. Select file type and extract directory.
6. Click 'Extract'.
Once the button 'Extract' is clicked and successfully exported the file, a windows file browser window should pop up showing the exported file and open the file with default software. If not, please check if all the code in the webpage is pasted.

## Resource

[中原大學學生學業成績考核辦法](https://tdpba.cycu.edu.tw/wp-content/uploads/%E4%B8%AD%E5%8E%9F%E5%A4%A7%E5%AD%B8%E5%AD%B8%E7%94%9F%E5%AD%B8%E6%A5%AD%E6%88%90%E7%B8%BE%E8%80%83%E6%A0%B8%E8%BE%A6%E6%B3%95.pdf)
