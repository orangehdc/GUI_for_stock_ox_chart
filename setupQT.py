# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:57:11 2014
http://www.pythoner.com/111.html
@author: Administrator
"""
from distutils.core import setup
import py2exe
import sys


sys.path.append(r'D:\Program Files\
Microsoft Visual Studio 10.0\VC\redist\x86\Microsoft.VC100.CRT')
#this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
        "includes": ["sip"],
        "dll_excludes": ["MSVCP90.dll","MSVCP100.dll"],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,
        
        }
data_files = [
            ('phonon_backend', [
                'C:\Python27\Lib\site-packages\PyQt4\plugins\phonon_backend\phonon_ds94.dll'
                ])
]
setup(
      name = 'demo',
      version = '1.0',
      windows = ['main_window.py',], 
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )
