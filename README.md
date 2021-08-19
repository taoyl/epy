# epy
A fork of embedded python from H.Miyamoto: http://wids.net/lab/epy.en.html

# Introduction
epy.py is a Python implementation of ePython(embedded Python) like Perl's ePerl and Ruby's eRuby. I referenced to 30 Lines Implementation of eRuby, written by creator of Erubis)(fastest eRuby implementation) and pyTenjin(fastest python template system).

# Feature
Only one file and only 200 lines! (targetting compact cgi scripts, not framework)
Fast. (included Erubis and pyTenjin's technology. ex. cache)
99% Python syntax surface compatible. (Templates are converted to a pure python code)

# Syntax
```<% (python code) %>```
do python code

```<%= (python code) %>```
do python code and print return value

```<%# (python code) %>```
code comment. It's exists in python code but not print.

```<%=r (python code) %>```
raw mode.

```<% %>```
1% of incompatible. This is like endfor, endif, and end at other template systems, and outdent one level to python code. I brought this idea form Python Server Pages.
