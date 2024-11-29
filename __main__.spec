# homeassistant.spec

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
import os
from PyInstaller import __main__  # 引入 PyInstaller 主模块
from PyInstaller.utils.hooks import copy_metadata  # 用于复制元数据文件

# 设置 Home Assistant 主入口文件路径
homeassistant_path = '/jxn/下载/core/homeassistant'  # 请替换为 Home Assistant 实际路径
matter_server_path = os.path.join(homeassistant_path, 'matter_server_main.py')  # 你需要的 Matter Server 文件路径

# 添加需要隐藏导入的模块
hiddenimports = [
    'homeassistant',
    'homeassistant.core',
    'homeassistant.components',
    'homeassistant.bootstrap',
    'homeassistant.setup',
    'homeassistant.components.recorder',
    'homeassistant.components.http',
    'homeassistant.components.persistent_notification',
    'homeassistant.helpers',
    'homeassistant.components.websocket_api',
    'pyotp',  # 如果你使用了 TOTP 集成
    'pyqrcode',  # 如果你使用了二维码生成
    'sqlalchemy',  # 如果使用数据库
    'turbojpeg',  # 如果你使用了图像处理相关的 TurboJPEG
    'asyncio',  # Home Assistant 使用 asyncio
    'async_timeout',  # timeout 模块
    'aiohttp',  # HTTP 请求相关
    'yarl',  # 如果使用了 URL 处理
]

# 收集 Home Assistant 和外部模块的所有子模块
hiddenimports.extend(collect_submodules('homeassistant'))
hiddenimports.extend(collect_submodules('aiohttp'))
hiddenimports.extend(collect_submodules('sqlalchemy'))
hiddenimports.extend(collect_submodules('pyotp'))

# 收集数据文件（如配置、图标、模板等）
datas = collect_data_files('homeassistant')  # 获取 Home Assistant 相关的静态资源文件
datas.extend(collect_data_files('aiohttp'))  # 添加 aiohttp 的静态资源文件

# 添加 Home Assistant 配置文件（如果有特定的配置文件，确保它们被打包）
#datas.append(('/path/to/config', 'config'))  # 替换为你的配置路径

# 打包与数据库相关的文件（如果你有数据库配置）
#datas.append(('/path/to/db', 'db'))  # 替换为数据库的实际路径

# PyInstaller 分析部分，解析源代码和文件
a = Analysis(
    ['homeassistant/__main__.py'],  # 指定 Home Assistant 主文件路径
    pathex=[homeassistant_path],  # Home Assistant 根目录
    binaries=[],
    datas=datas,  # 数据文件
    hiddenimports=hiddenimports,  # 隐藏导入的模块
    hookspath=[],  # 如果你有自定义的 hook 文件
    runtime_hooks=[],  # 如果有运行时需要的钩子
    excludes=['tkinter'],  # 排除不需要的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)

# 将所有 Python 文件打包为压缩文件（.pyz）
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 定义最终生成的可执行文件（EXE）
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='homeassistant',  # 最终生成的可执行文件名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # 如果不需要控制台输出，设置为 False
)

# 将所有内容合并为一个完整的目录（COLLECT）
coll = COLLECT(
    exe,
    a.datas,
    a.binaries,
    a.zipfiles,
    a.uihooks,
    name='homeassistant',
)

# 添加 Matter Server 启动文件
matter_exe = EXE(
    [matter_server_path],
    a.scripts,
    [],
    exclude_binaries=True,
    name='matter_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # 如果不需要控制台输出，设置为 False
)

# 合并 Matter Server 到最终的输出目录
coll = COLLECT(
    matter_exe,
    a.datas,
    a.binaries,
    a.zipfiles,
    name='matter_server',
)


