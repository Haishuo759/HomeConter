import os
import shutil

# 当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 需要删除的文件列表
files_to_delete = [
    'README-部署指南.md',
    'README.md',
    'deploy.bat',
    'deploy.ps1',
    'requirements.txt',
    '启动.bat',
    '安装环境.bat',
    '快速开始.txt',
    '手动部署 - 分步指导.bat',
    '检查环境 - 简化版.bat',
    '检查环境.bat',
    '📖 手动检查环境指南.md',
    '📤 快速部署到互联网.md',
    '📦 一键部署说明.md',
    '📦 使用 PowerShell 脚本部署.md',
    '钉钉集成版',  # 文件夹
]

# 删除文件
deleted_count = 0
for filename in files_to_delete:
    filepath = os.path.join(current_dir, filename)
    try:
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f'已删除文件：{filename}')
                deleted_count += 1
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
                print(f'已删除文件夹：{filename}')
                deleted_count += 1
    except Exception as e:
        print(f'删除失败 {filename}: {e}')

print(f'\n清理完成！共删除 {deleted_count} 个文件/文件夹')
