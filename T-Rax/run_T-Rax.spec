# -*- mode: python -*-
a = Analysis(['run_T-Rax.py'],
             pathex=['D:\\Programming\\VS Projects\\T-Rax\\T-Rax'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='run_T-Rax.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='run_T-Rax')
