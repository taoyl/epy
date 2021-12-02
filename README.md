# epy
epy is a command-line tool enabling flexiable embedded python code for template systems. It is similar to Perl's ePerl and Ruby's eRuby.


epy is based on epython module which is a fork of embedded python from H.Miyamoto. epython module is developed based on Python 2.x, I ported it to Python 3.x and added some enhanced featurs like multi-line code, flexiable user-control parameter, etc, as well as fixing some minor issues.


For more details on original version of epython module, please visit http://wids.net/lab/epy.en.html


# Features
epy includes all featurs of epython module, visit link above for more details.

Here is the feature list from the view of a command-line tool.

Command-line arguments:
```  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file
  -o OUTPUT, --output OUTPUT
                        Output file
  -y YAML [YAML ...], --yaml YAML [YAML ...]
                        Read yaml file as python variables
  -p PARAM [PARAM ...], --param PARAM [PARAM ...]
                        Read param (NAME=VALUE) py file as python variables
  -d DEFINE [DEFINE ...], --define DEFINE [DEFINE ...]
                        Define python variable, format is NAME=VALUE
  -D SETENV [SETENV ...], --setenv SETENV [SETENV ...]
                        Define environment variable, format is NAME=VALUE
  -x, --debug           Enable debug
  -c, --cache           Enable cache for preprocessed file
  --delimiter DELIMITER
                        Specify the code delimiter, default is %
  --indent INDENT       Python code indent spaces, default is 2
```

# Syntax
```<% (python code) %>```

do python code, support multi-line code

For multi-line code, users should follow the python syntax including indent.

For plain text, epy doesn't care the indent. However, users should use a sparate line ```<% %>``` as an enclosing indicator to python code.


```<%= (python code) %>```

do python code and print return value


```<%# (python code) %>```

code comment. It's exists in python code but not print.

```<%=r (python code) %>```

raw mode.

```<% %>```

This is like endfor, endif, and end at other template systems, and outdent one level to python code. I brought this idea form Python Server Pages.


# Usage

Refer to demo example.
