# -*- mode: python -*-
a = Analysis(['main.py'],
         pathex=['C:\\Users\\XPS\\Desktop\\Pro Portfolio\\Calculator'],
         datas=[('C:\\Users\\XPS\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\customtkinter', 'customtkinter/')],
         hiddenimports=[],
         hookspath=None,
         runtime_hooks=None)

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

a.datas += [('files/images/logo.ico', 'C:\\Users\\XPS\\Desktop\\Pro Portfolio\\Calculator\\files\\images\\logo.ico', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      name='Amos Calculator.exe',
      debug=False,
      strip=None,
      upx=True,
      console=False,
      icon='C:\\Users\\XPS\\Desktop\\Pro Portfolio\\Calculator\\files\\images\\logo.ico')
