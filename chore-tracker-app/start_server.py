#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
局域网 HTTP 服务器 - 增强版
自动检测网络环境，提供详细的连接指导
"""

import http.server
import socketserver
import os
import socket
import sys
import subprocess
import re

def get_local_ip():
    """获取本机局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def check_firewall(port):
    """检查防火墙是否阻止端口"""
    try:
        # 尝试从本地另一个 IP 访问
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)
        result = test_socket.connect_ex(('127.0.0.1', port))
        test_socket.close()
        return result == 0
    except Exception:
        return True

def get_network_adapters():
    """获取网络适配器信息"""
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=5)
        return result.stdout
    except Exception:
        return ""

def main():
    PORT = 8080
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(DIRECTORY)
    
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    local_ip = get_local_ip()
    
    print("=" * 70)
    print("🎉 家务管理系统服务器已启动！")
    print("=" * 70)
    print()
    print("📱 访问地址:")
    print(f"   • 本机访问：http://localhost:{PORT}")
    print(f"   • 手机/其他设备：http://{local_ip}:{PORT}")
    print()
    
    if local_ip == "127.0.0.1":
        print("⚠️  警告：未检测到局域网 IP")
        print("   可能原因：电脑未连接 WiFi 或网线")
        print("   解决方法：请确保电脑已连接到路由器网络")
        print()
    
    print("💡 手机访问步骤:")
    print("   1. 确保手机和电脑连接同一个 WiFi（重要！）")
    print("   2. 在手机浏览器输入：http://" + local_ip + ":" + str(PORT))
    print("   3. 如果无法访问，请看下面的解决方案")
    print()
    
    print("🔧 常见问题解决:")
    print()
    print("【问题 1】手机输入 IP 后无法打开页面")
    print("   原因：Windows 防火墙阻止了连接")
    print("   解决：按以下步骤操作")
    print("   方法 A - 临时关闭防火墙测试:")
    print("     1. 搜索并打开'Windows Defender 防火墙'")
    print("     2. 点击'启用或关闭 Windows Defender 防火墙'")
    print("     3. 暂时关闭专用和公用网络的防火墙")
    print("     4. 再次尝试手机访问")
    print("     5. 测试成功后建议重新开启防火墙")
    print()
    print("   方法 B - 添加防火墙例外（推荐）:")
    print("     以管理员身份运行 PowerShell，执行:")
    print("     netsh advfirewall firewall add rule name=\"Python Server\" dir=in action=allow protocol=TCP localport=" + str(PORT))
    print()
    print("【问题 2】找不到电脑的 IP 地址")
    print("   在命令行执行：ipconfig")
    print("   找到'IPv4 地址'，通常是 192.168.x.x 或 10.x.x.x")
    print()
    print("【问题 3】手机和电脑不是同一网络")
    print("   检查：手机是否连了 WiFi，而电脑用了有线网络？")
    print("   解决：确保两者连接同一个路由器的网络")
    print()
    
    print("=" * 70)
    print("⚠️  按 Ctrl+C 停止服务器")
    print("=" * 70)
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("✅ 服务器正在监听端口 " + str(PORT))
            print("   等待连接中...")
            print()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n服务器已停止")
                sys.exit(0)
                
    except OSError as e:
        if e.errno == 10048:
            print(f"❌ 端口 {PORT} 已被占用！")
            print("解决方法:")
            print("1. 关闭其他正在运行的 Python 服务器")
            print("2. 或者修改 PORT 值为其他端口（如 8081、8888）")
        elif e.errno == 10013:
            print(f"❌ 端口 {PORT} 被防火墙阻止！")
            print("解决方法:")
            print("1. 以管理员身份运行此脚本")
            print("2. 或者按照上面的方法添加防火墙例外")
        else:
            print(f"❌ 启动失败：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
