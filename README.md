# CYCU-Grade-Exporter

This script take webpage source code and spite out csv file containing CYCU student's grade related data.

## ATTENTION

The calculation of G.P.A has not being proven correct yet, so only take it only as a proximate number.

## Develop Environment

- Windows 11
- python
  - numpy
  - bs4

## Install

Go to [relase page](https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/tag/V1.0.0) and download EXE file.</br>
Once it's downloaded, double click to execute it rightaway.

## Steps to Use

1. Use webbrowser like Google or Firefox to open up i-touch website and sign-in.
2. Go to '學業/學習足跡/歷年學習成績/新視窗開啟', and focus on the new opened tab.
3. Use hotkey 'ctrl+u' to open source code of the tab, and use 'ctrl+c' to copy all codes.
4. Paste the code using 'ctrl+v' into the text box and select exportint format.
5. Select file type and extract directory.
6. Click 'Extract'.
Once the button 'Extract' is clicked and successfully exported the file, a windows file browser window should pop up showing the exported file. If not, please check if all the code in the webpage is pasted.

## Resource

[中原大學學生學業成績考核辦法](https://tdpba.cycu.edu.tw/wp-content/uploads/%E4%B8%AD%E5%8E%9F%E5%A4%A7%E5%AD%B8%E5%AD%B8%E7%94%9F%E5%AD%B8%E6%A5%AD%E6%88%90%E7%B8%BE%E8%80%83%E6%A0%B8%E8%BE%A6%E6%B3%95.pdf)
