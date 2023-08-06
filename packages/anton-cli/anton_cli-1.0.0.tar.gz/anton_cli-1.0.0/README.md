# Collection Framework
 
**anton_cli** is a commands-line program that takes a string and returns the number of unique characters in the string.

### Install

```python
pip install anton-cli
```

### How to Use
```python
from anton_cli import split_letters, read_from_file

print(split_letters('hello')) # 3
```
also you can get a unique numbers of string from the file

```python
print(read_from_file('words.txt')) # SOME RESULT
```


### Launch

You can use this program from the terminal

if you want to pass a string use --string [YOUR STRING]
```python
python -m anton_cli.cli --string [YOUR STRING]
```
or if you want to pass a file use --file [YOUR FILE PATH]
```python
python -m anton_cli.cli --file [YOUR PATH TO FILE]
```

<br>

See the source at  [Link](https://git.foxminded.com.ua/foxstudent102894/task-5-create-the-python-package)
<br>
© 2022 Anton Skazko