# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main_GUI.py'],
             pathex=['C:\\Users\\Hadar\\PycharmProjects\\Clustring_Tool_Analisys\\CTA'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

a.datas += [('.\\images\\green_v.png','C:\\Users\Hadar\\PycharmProjects\\Clustring_Tool_Analisys\\CTA\\Images\\green_v.png', 'Data')]
a.datas += [('.\\images\\red_x.png','C:\\Users\Hadar\\PycharmProjects\\Clustring_Tool_Analisys\\CTA\\Images\\red_x.png', 'Data')]


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='CTA',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
