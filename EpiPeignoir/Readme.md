# EpiPeignoir
Epitech Ranking by GPA

## How to use it
Firstly, fill the config file config.ini with your creditentials.  
You must provide to the script this config file (-c) and a login list (-l).  
You can do it like this:
```
./EpiPeignoir.py -c config.ini -l login_list.txt
```

## Features
* Rank a list of logins by GPA:
  * Input: stdin or txtfile
  * Output: txt, csv (TBD) or just display on stdout
* Get and display GPA/credits by login.

## Requirements
* requests (pip install requests)  
    Requests is an Apache2 Licensed HTTP library, written in Python, for human beings.
* pandas (pip install pandas)  
    pandas is a library providing data structures and data analysis tools for Python.
  
All those requirements can be easily installed by doing ``pip install -r requirements.txt``

## Changelog
### Version 0.2 (19/12/2015)
* Stdin input added.
* Csv output added.
* Txt output added.
* Silent and NoResult options added.
### Version 0.1 (14/12/2015)
* Initial release.
