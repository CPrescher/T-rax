# -*- mode: python -*-
a = Analysis(['T-Rax.py'],
             pathex=['D:\\Programming\\VS Projects\\T-Rax\\T-Rax'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='T-Rax.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
		  icon = 'D:\Programming\VS Projects\T-Rax\T-Rax\icons\T-rax.ico')
		  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='T-Rax')
