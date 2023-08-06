# datedays
## What can it do?

* [1. Get common date data](#datadays)
* [2. Operating excel report](#Excel)
* [3. Perform common encryption signature](#hash)
* [4. Obtain the encrypted signature of the file](#file)

datedays is available on PyPI:

```console
$ pip install datedays
```

### Still updating

## 1. Get common date data

Method | description | return result | parameter < a id = "datadays" ></a>
:---: | :---:| :---:| :---:
Getnow() | get today's date | for example: 2022-08-16 17:56:17|
Gettomorrow() | tomorrow | 2022-08-17 | select the next day (just pass in the number you want)
Getyesterday() | yesterday | 2022-08-15 | select the last day (just pass in the desired number)
Getdays() | default date set within three months |... (test printing is recommended) | number = number of months you want
Getnowtimestamp() | get the current timestamp | 1660644568238 | default milliseconds (optional seconds, milliseconds, microseconds)
Gettodaydays() | get the set of remaining days of this month by default |... (it is recommended to test and print) | you can specify a day of a month to get the remaining days of the month
Getnextdays() | get the total number of days of the next month by default |... (test printing is recommended) | you can specify the month and the number of months
Getstr2timestamp() | date string to timestamp |... (test printing is recommended) | parameter 1: date, parameter 2: date format

## 2. Operate excel report

Method | description | return result | parameter < a id = "excel" ></a>
:---: | :---:| :---:| :---:
excel_ write_ Openpyxl() | write excel report |... (recommended test) | filename: file name, data: data to be saved, format: [first line], [second line], [Third Line]...]
excel_ read_ Openpyxl() | read excel report |... (recommended test) | filename: filename, sheet_ Index: subscript of sheet
excel_ read_ Xlrd() | read excel report (support XLS) |... (recommended test) | filename: filename, sheet_ Index: subscript of sheet

## 3. Perform common encryption signature

Method | description | return result | parameter < a id = "hash" ></a>
:---: | :---:| :---:| :---:
Md2() | MD2 encryption |... (recommended test) | body: encrypted content, encode: encoding format
Md5() | MD5 encryption |... (default 32-bit result) | body: encrypted content, encode: encoding format, length_: Return length, optional 16
Sha1() | SHA1 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA2_ 224() |SHA2_ 224 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA2_ 256() |SHA2_ 256 ENCRYPTION |... (recommended test) | body: encrypted content, encode: encoding format
SHA2_ 384() |SHA2_ 384 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA2_ 512() |SHA2_ 512 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA3_ 224() |SHA3_ 224 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA3_ 256() |SHA3_ 256 ENCRYPTION |... (recommended test) | body: encrypted content, encode: encoding format
SHA3_ 384() |SHA3_ 384 encryption |... (recommended test) | body: encrypted content, encode: encoding format
SHA3_ 512() |SHA3_ 512 encryption |... (recommended test) | body: encrypted content, encode: encoding format

## 4. Obtain the encrypted signature of the file

Method | description | return result | parameter < a id = "file" ></a>
:---: | :---:| :---:| :---:
encrypt_ Smallfile() | encrypt small files |... (recommended test) | filename: filename, mode: default MD5 (optional encryption above)
encrypt_ Bigfile() | encrypt large files |... (recommended test) | filename: filename, mode: default MD5 (optional encryption above)

**For Example**:

all dates within 2 days to 10 days 
```
import datedays

if __name__ == '__main__':
    print(datedays.getdays()[2:10]) 
```
output:
```
['2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14', '2022-08-15', '2022-08-16', '2022-08-17', '2022-08-18']
```
