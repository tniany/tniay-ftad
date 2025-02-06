# TNIAY-FTAD

一个基于Flask的文件传输和文本共享应用程序，支持本地网络内的快速文件传输和即时消息交流。

## 功能特点

- 📝 文本消息传输
  - 支持实时消息发送和接收
  - 消息历史记录保存
  - 支持消息删除和清空
  
- 📁 文件传输
  - 支持多种文件类型上传和下载
  - 文件安全性检查
  - 上传进度显示
  
- 🖼️ 媒体预览
  - 图片在线预览
  - 文件类型识别
  - 文件图标显示
  
- 📋 剪贴板集成
  - 支持文件路径快速复制
  - 便捷的文本复制功能
  
- 🛠️ 其他特性
  - 自定义端口设置
  - GUI配置界面
  - 管理员权限支持
  - 跨平台兼容

## 快速开始

### 使用可执行文件--推荐

1. 从Release页面下载最新版本的可执行文件
2. 运行程序，通过GUI界面设置端口
3. 在浏览器中访问显示的地址
4. 愉快使用 

### 使用源代码

1. 克隆仓库
```bash
git clone https://github.com/tniany/tniay-ftad.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python run.py [端口号]
```

## 系统要求

- Windows 7/8/10/11
- Python 3.7+（如果使用源代码运行）
- 现代浏览器（Chrome、Firefox、Edge等）

## 技术栈

- 后端：Flask + Flask-SocketIO
- 前端：HTML5 + CSS3 + JavaScript
- GUI：Python GUI库
- 构建工具：PyInstaller

## 版本历史

### v1.1.0 (2024-01)
- 新增：自定义端口功能
  - exe运行时通过GUI对话框设置端口
  - 脚本运行时通过命令行设置端口
- 优化：移除AI思考功能
- 优化：移除文件类型限制
- 优化：添加文件安全检查
- 优化：代码结构优化

### v1.0.0 (2024-01)
- 初始版本发布
- 实现基本功能集

## 许可证

本项目采用 GNU General Public License v3.0 开源协议。这意味着你可以：

- 使用
- 分享
- 修改

但必须：

1. 开源：如果你修改了代码，你必须开源
2. 协议：使用相同的协议（GPLv3）
3. 声明：保留原作者的版权和许可说明

## 项目地址

https://github.com/tniany/tniay-ftad

## 作者

tniay (mo-tniay)

## 贡献

欢迎提交Issue和Pull Request来帮助改进项目。

## 致谢

感谢所有为这个项目做出贡献的开发者。 


## Stargazers over time
[![Stargazers over time](https://starchart.cc/tniany/tniay-ftad.svg?variant=adaptive)](https://starchart.cc/tniany/tniay-ftad)

