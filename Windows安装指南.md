# Windows 用户安装指南

欢迎Windows用户！本指南将帮助你在Windows系统上顺利运行打字练习游戏。

## 🎯 推荐方案（图形版）

**推荐使用图形界面版本**，体验更好且已完美支持中文显示！

### 第一步：安装Python

1. 前往 [Python官网](https://www.python.org/downloads/) 下载最新版本
2. 运行安装程序，**务必勾选 "Add Python to PATH"**
3. 完成安装后，打开命令提示符（CMD）或PowerShell测试：
   ```cmd
   python --version
   ```

### 第二步：安装pygame

打开命令提示符（CMD）或PowerShell，运行：

```cmd
pip install pygame
```

### 第三步：运行游戏

```cmd
cd C:\path\to\caps
python typing_game_gui.py
```

**完成！** 现在就可以享受打字练习了！✨

---

## 💻 备选方案（终端版）

如果你想使用终端版本：

### 安装额外依赖

终端版在Windows上需要 `windows-curses` 库：

```cmd
pip install windows-curses
```

### 运行终端版

```cmd
python typing_game.py
```

**注意：** 程序会自动尝试安装 windows-curses，如果自动安装失败，请手动运行上述安装命令。

---

## 🔧 一键安装所有依赖

如果你想同时安装两个版本的依赖：

```cmd
pip install -r requirements_typing.txt
```

这会自动安装：
- pygame（图形版需要）
- windows-curses（终端版需要）

---

## ❓ 常见问题（Windows专属）

### Q1: 提示 'python' 不是内部或外部命令

**原因：** Python未添加到系统PATH

**解决方案：**
1. 重新安装Python，确保勾选 "Add Python to PATH"
2. 或手动添加Python到系统PATH
3. 或使用 `py` 命令代替 `python`：
   ```cmd
   py typing_game_gui.py
   ```

### Q2: pip安装速度很慢

**解决方案：** 使用国内镜像源

```cmd
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 终端版无法运行，提示 "No module named '_curses'"

**原因：** Windows缺少curses库

**解决方案：**
```cmd
pip install windows-curses
```

### Q4: 图形版中文显示为方块

**已修复！** 最新版本会自动检测并加载以下中文字体：
- 微软雅黑 (Microsoft YaHei)
- 宋体 (SimSun)
- 黑体 (SimHei)

如果仍有问题，请确保系统中至少安装了其中一种字体。

### Q5: 使用哪个终端更好？

推荐使用：
- **Windows Terminal**（推荐，支持完整颜色）
- PowerShell
- CMD（命令提示符）

不推荐使用旧版的CMD，建议升级到Windows Terminal。

### Q6: 权限问题，无法安装包

**解决方案：** 以管理员身份运行命令提示符

1. 搜索 "cmd" 或 "PowerShell"
2. 右键点击，选择 "以管理员身份运行"
3. 再次运行安装命令

---

## 🎮 推荐配置

### 最佳体验配置

1. **使用图形版**（typing_game_gui.py）
2. **安装Windows Terminal**
   - 从Microsoft Store免费下载
   - 更好的颜色和字体支持
3. **全屏运行**
   - 按 `Alt + Enter` 切换全屏
   - 更好的沉浸式体验

---

## 📝 快速命令备忘单

```cmd
# 检查Python版本
python --version

# 安装图形版依赖
pip install pygame

# 安装终端版依赖
pip install windows-curses

# 安装所有依赖
pip install -r requirements_typing.txt

# 运行图形版（推荐）
python typing_game_gui.py

# 运行终端版
python typing_game.py

# 使用国内镜像加速安装
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 🎉 开始游戏

安装完成后，推荐运行图形版：

```cmd
python typing_game_gui.py
```

享受打字练习的乐趣吧！💪⌨️

---

## 💡 提示

- 图形版体验更好，推荐使用
- 已完美支持中文显示
- 已完美支持Windows系统
- 如有问题，请查看详细文档：README_typing_game.md

祝你打字愉快！🎊

