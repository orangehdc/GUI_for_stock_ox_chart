from distutils.core import setup
import py2exe,sys
import matplotlib

sys.path.append(r'D:\Program Files\
Microsoft Visual Studio 10.0\VC\redist\x86\Microsoft.VC100.CRT')
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
setup(
    windows = [
    {
        "script": "main_window.py",
        #"icon_resources": [(1, "5.ICO")]
    }
    ],
options = {
"py2exe":
{
"includes": ["sip"],
"compressed":1,
"optimize":2,
"excludes":["Tkinter",],
"dll_excludes":["MSVCP90.dll"]}
},
data_files=matplotlib.get_py2exe_datafiles(),
)