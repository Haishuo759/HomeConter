@echo off
title 修复防火墙 - 允许局域网访问
color 0B

:: 防止乱码
chcp 65001 >nul 2>&1

:: 清屏
cls

echo.
echo ========================================
echo    防火墙配置工具
echo ========================================
echo.
echo 此脚本将添加防火墙规则，允许手机访问网页
echo.
echo 注意：需要管理员权限
echo.
echo 按任意键继续...
pause >nul
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [错误] 检测到未以管理员身份运行！
    echo.
    echo ========================================
    echo   操作方法:
    echo ========================================
    echo.
    echo 方法 1（推荐）:
    echo   1. 右键点击此文件
    echo   2. 选择"以管理员身份运行"
    echo.
    echo 方法 2:
    echo   1. 在开始菜单搜索"cmd"
    echo   2. 右键点击"命令提示符"
    echo   3. 选择"以管理员身份运行"
    echo   4. 输入以下命令后回车:
    echo      netsh advfirewall firewall add rule name^="Python HTTP Server 8080" dir=in action=allow protocol=TCP localport=8080
    echo.
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo [步骤 1/3] 正在检查现有规则...
echo.

:: 尝试删除旧规则（避免重复）
netsh advfirewall firewall delete rule name="Python HTTP Server 8080" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ 已清理旧的防火墙规则
) else (
    echo   ℹ 未发现旧规则，跳过清理
)

echo.
echo [步骤 2/3] 正在添加入站规则...
echo.

:: 添加入站规则
netsh advfirewall firewall add rule name="Python HTTP Server 8080" dir=in action=allow protocol=TCP localport=8080 program="%SystemRoot%\System32\svchost.exe" profile=any >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ 入站规则添加成功
    echo     允许 TCP 端口 8080 的入站连接
) else (
    echo   ✗ 添加入站规则失败
    echo     错误代码：%errorlevel%
    echo.
    echo   请手动添加:
    echo   1. 打开"控制面板" → "Windows Defender 防火墙"
    echo   2. 点击"高级设置"
    echo   3. 右键"入站规则" → "新建规则"
    echo   4. 选择"端口" → "TCP" → 特定本地端口"8080"
    echo   5. 选择"允许连接" → 完成
    echo.
    pause
    exit /b 1
)

echo.
echo [步骤 3/3] 正在添加出站规则...
echo.

:: 添加出站规则
netsh advfirewall firewall add rule name="Python HTTP Server 8080 Out" dir=out action=allow protocol=TCP remoteport=8080 program="%SystemRoot%\System32\svchost.exe" profile=any >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ 出站规则添加成功
    echo     允许 TCP 端口 8080 的出站连接
) else (
    echo   ⚠ 出站规则添加失败（通常不影响使用）
    echo     错误代码：%errorlevel%
)

echo.
echo ========================================
echo    ✅ 配置完成！
echo ========================================
echo.
echo 防火墙规则已成功添加：
echo   • 入站：允许外部设备访问本机 8080 端口
echo   • 出站：允许本机 8080 端口的出站连接
echo.
echo ========================================
echo    下一步操作:
echo ========================================
echo.
echo 1. 运行 start_server.py 启动服务器
echo.
echo 2. 查看屏幕上显示的 IP 地址
echo    （格式类似：http://192.168.1.100:8080）
echo.
echo 3. 在手机浏览器输入该 IP 地址
echo    确保手机和电脑连接同一个 WiFi
echo.
echo 4. 输入密码 888888 登录使用
echo.
echo ========================================
echo    故障排查:
echo ========================================
echo.
echo 如果手机仍然无法访问：
echo.
echo 【检查 1】确认同一网络
echo   • 手机和电脑必须连接同一个路由器
echo   • 不要使用 4G/5G 流量
echo.
echo 【检查 2】确认 IP 地址
echo   • 按 Win+R，输入 cmd，回车
echo   • 输入 ipconfig，找到 IPv4 地址
echo   • 应该是 192.168.x.x 或 10.x.x.x
echo.
echo 【检查 3】临时关闭防火墙测试
echo   • 打开"控制面板" → "Windows Defender 防火墙"
echo   • 点击"启用或关闭 Windows Defender 防火墙"
echo   • 暂时关闭专用和公用网络的防火墙
echo   • 再次尝试手机访问
echo   • 测试后记得重新开启防火墙
echo.
echo 【检查 4】使用其他端口
echo   • 如果 8080 被占用，修改 start_server.py
echo   • 将 PORT = 8080 改为 PORT = 8081
echo   • 然后在本脚本中也修改对应的端口号
echo.
echo ========================================
echo.
echo 按任意键退出...
pause >nul

exit /b 0
