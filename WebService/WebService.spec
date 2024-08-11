# my_app.spec

# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import copy_metadata
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

a = Analysis(
    ['source/main.py'],  # Thay 'source/main.py' bằng file chính của bạn
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/*.joblib', 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='my_app',  # Tên của file exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    cipher=block_cipher,
    hookspath=[],
    hooksconfig={},
)