a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
    ('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pyvi', 'pyvi'),
('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\tabulate', 'tabulate'),
('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\tqdm', 'tqdm'),
('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pycrfsuite', 'pycrfsuite'),
    ('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn_crfsuite', 'sklearn_crfsuite'),
('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\numpy', 'numpy'),
    ('D:\\KLTN_2024\\WebService\\config.ini', '.'),
    ('D:\\KLTN_2024\\WebService\\stopwords_project.txt', '.'),
('D:\\KLTN_2024\\WebService\\tfidf.model', '.'),
('D:\\KLTN_2024\\WebService\\svm.model', '.')
],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='WebService',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          onefile=True)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='WebService')