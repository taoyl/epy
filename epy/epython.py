# encoding: utf-8
# Copyright (c) 2008-2009 H.Miyamoto
# Copyright (c) 2007 Makoto Kuwata (TinyEruby)
#
# License: MIT (http://www.opensource.org/licenses/mit-license.php)

r"""A fast and compact implementation of ePython - "embedded Python".

The original implementation created by Makoto Kuwata (www.kuwata-lab.com>).
ePython and epy.py is a python implementation of his logic and eRuby.

cf.) 30 Lines Implementation of eRuby
<http://www.kuwata-lab.com/support/2007/10/09/30-lines-implementation-of-eruby/>

Update history:
R-0.7.3: from original auther H.Miyamoto
R-0.8: update by Yuliang Tao
       a) Fix issues in python3.x
       b) Add multi-line code feature
       c) Add more initial paramters for flexible usage
"""

__version_info__ = (0, 7, 3)
__version__ = '0.7.3'
__author__ = 'H.Miyamoto'

import re
import os

class ePython(object):
    #taoyl@2021-12-01: add delimiter and indentspace as parameter
    def __init__(self, src=None, encoding='utf-8', filename=None, cache=True, cachepath=None,
                 delim='%', indentspace=2):
        self.encoding = encoding
        self.filename = filename

        if src:
            self.src = src
        else:
            self.src = self._read(filename)

        if filename:
            self.cache = cache
            if cachepath:
                self.cachepath = cachepath
            else:
                # taoyl@2021-12-01: use hidden file in unix as the cache file name
                # self.cachepath = '.'.join([filename, 'cache'])
                self.cachepath = os.path.join(os.path.dirname(filename), f'.{os.path.basename(filename)}.cache')
        else:
            self.cache = None
            self.cachepath = ''

        self.delm = f'{delim}'
        self.indentunit = ' ' * indentspace 
        self.pysrc = None
        self.escfunc = None

    def prepend_src(self, src):
        """Prepend source code to self.src
           Added by Yuliang Tao
        """

        self.src = src + self.src

    def convert(self):
        if not self.pysrc:
            if self.cached():
                self.pysrc = self._read(self.cachepath)
            else:
                self.__convert()
        if self.cache:
            self._write(self.cachepath, self.pysrc)

        return self.pysrc

    def cached(self):
        return self.cache and \
        os.path.exists(self.filename) and os.path.exists(self.cachepath) and \
        os.path.getmtime(self.filename) < os.path.getmtime(self.cachepath)

    def _read(self, filename):
        fh = open(filename)
        s = fh.read()
        fh.close()

        #return s.decode(self.encoding)
        return s

    def _write(self, filename, content):
        fh = open(filename, 'w')
        # fh.write(content.encode(self.encoding))
        fh.write(content)
        fh.close()

        return

    def __convert(self):
        def _is_avoid_syntax(code):
            return code.endswith(':') and \
                    (code.startswith('else') or \
                     code.startswith('elif') or \
                     code.startswith('except') or \
                     code.startswith('finally'))

        def _convert(mo):
            ret = list()
            text, ch, rawmode, code, newline = mo.groups()
            # print(f"{text=}, {code=}, {self._indent=}")
            if text:
                if code.strip() == '':
                    text = text.rstrip('\s').rstrip('\t')
                text = self._esc_quote(text)
                arg = (self._indent * self.indentunit, text.replace('\n', r'\n'))
                # ret.append(u"%s_buf.append(u'%s')\n" % arg)
                ret.append(f"{arg[0]}_buf.append('{arg[1]}')\n")
            if ch == '=':
                c = code.strip()
                arg = (self._indent * self.indentunit, c)
                if rawmode:
                    # ret.append(u"%s_buf.append(%s)\n" % arg)
                    ret.append(f"{arg[0]}_buf.append({arg[1]})\n")
                else:
                    # ret.append(u"%s_buf.append(_esc(%s))\n" % arg)
                    ret.append(f"{arg[0]}_buf.append(_esc({arg[1]}))\n")
                # taoyl@2021-12-01: fix the bug when newline follows <>
                if newline:
                    ret.append(f"{arg[0]}_buf.append('\\n')\n")
            elif ch == '#':
                arg = (self._indent * self.indentunit, code.strip())
                ret.append(u"%s# %s\n" % arg)
            else:
                c = code.strip()
                if c == '':
                    self._indent -= 1
                elif _is_avoid_syntax(c):
                    ret.append(''.join([(self._indent - 1) * ' ', c, '\n']))
                else:
                    ret.append(''.join([self._indent * self.indentunit, c, '\n']))
                if c.endswith(':') and not _is_avoid_syntax(c):
                    self._indent += 1
                #taoyl@2021-12-01: support multi-line code, indent may occurs in middle of code
                elif re.search(r':\n', c) and not _is_avoid_syntax(c):
                    self._indent += len(re.findall(r':\n', c))
            return ''.join(ret)

        self._indent = 0
        r = re.compile(u'(.*?)<%s([=#])?(r)?(.*?)%s>(\n)?' % \
                       (self.delm, self.delm), re.MULTILINE | re.DOTALL)
        endmark = u'<%s %s>' % (self.delm, self.delm)

        # pysrcbase = u"_buf = []\n%s\n__result = ''.join(_buf)"
        # taoyl@2021-12-01: str join doesn't support non-str list items like integer
        pysrcbase = u"_buf = []\n%s\n__result = ''.join([str(x) for x in _buf])"
        self.pysrc = r.sub(_convert, ''.join([self.src, endmark]))
        self.pysrc = pysrcbase % self.pysrc

        return self.pysrc

    def _esc_quote(self, text):
        return text.replace('\\', '\\\\').replace("'", "\\'")

    def render(self, environ={}):
        if not self.pysrc:
            self.convert()
        if self.escfunc:
            environ['_esc'] = self.escfunc
        else:
            environ['_esc'] = lambda x: x
        #taoyl@2021-12-01: Fix exec calling in python3.x
        # exec self.pysrc in environ
        exec(self.pysrc, globals(), environ)

        return environ['__result']

import cgi

class ePythonHTML(ePython):
    def __init__(self, src=None, encoding='utf-8', filename=None, cache=True):
        super(ePythonHTML, self).__init__(src, encoding, filename, cache)
        self.escfunc = lambda x: cgi.escape(x, quote=True)
