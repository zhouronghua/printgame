#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
互动打字练习游戏 - 终端版
特点：实时反馈、计分系统、多难度级别、有趣的文本内容
支持Windows/Linux/macOS
"""

import time
import random
import sys
import os
from typing import List, Tuple

# Windows兼容性处理
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    # Windows上需要安装windows-curses
    print("检测到Windows系统，正在尝试安装curses支持...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses", "-q"])
        import curses
        CURSES_AVAILABLE = True
        print("✓ 安装成功！")
    except:
        print("\n" + "="*50)
        print("❌ 无法自动安装curses库")
        print("\n请手动运行以下命令安装：")
        print("    pip install windows-curses")
        print("\n或者使用图形界面版本：")
        print("    python typing_game_gui.py")
        print("="*50)
        sys.exit(1)

# 不同难度的练习文本
TEXTS = {
    "简单": [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a great programming language.",
        "Practice makes perfect in typing.",
        "Hello world from the typing game!",
        "Keep calm and type on.",
    ],
    "中等": [
        "The art of programming is the art of organizing complexity.",
        "Any fool can write code that a computer can understand.",
        "Experience is the name everyone gives to their mistakes.",
        "Simplicity is the soul of efficiency in coding.",
        "First, solve the problem. Then, write the code.",
    ],
    "困难": [
        "Programs must be written for people to read, and only incidentally for machines to execute.",
        "The function of good software is to make the complex appear to be simple.",
        "Debugging is twice as hard as writing the code in the first place.",
        "Code is like humor. When you have to explain it, it's bad.",
        "Measuring programming progress by lines of code is like measuring aircraft building progress by weight.",
    ],
    "编程挑战": [
        "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
        "lambda x, y: x if x > y else y",
        "for i in range(10): print(f'Number {i}: {i**2}')",
        "[x**2 for x in range(10) if x % 2 == 0]",
        "import sys; sys.stdout.write('Hello, World!\\n')",
    ]
}


class TypingGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.difficulty = "中等"
        self.current_text = ""
        self.user_input = ""
        self.start_time = 0
        self.end_time = 0
        self.errors = 0
        self.total_chars = 0
        self.is_running = False
        
        # 初始化颜色
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # 正确
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # 错误
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # 高亮
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)     # 标题
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # 统计
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)    # 普通文本
        
        # 隐藏光标
        curses.curs_set(0)
        
    def show_menu(self) -> str:
        """显示主菜单"""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        title = "⌨️  超级打字练习游戏  ⌨️"
        subtitle = "提升你的打字速度和准确率！"
        
        # 显示标题
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(2, (w - len(title)) // 2, title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(3, (w - len(subtitle)) // 2, subtitle)
        self.stdscr.attroff(curses.color_pair(3))
        
        # 菜单选项
        menu_items = [
            "",
            "选择难度级别：",
            "",
            "1. 简单 - 短句子，适合初学者",
            "2. 中等 - 技术名言，适合练习者",
            "3. 困难 - 长句子，挑战高手",
            "4. 编程挑战 - Python代码片段",
            "",
            "5. 查看历史最佳成绩",
            "Q. 退出游戏",
            "",
            "请选择 (1-5 或 Q):"
        ]
        
        start_y = 6
        for i, item in enumerate(menu_items):
            y = start_y + i
            if item.startswith(("1.", "2.", "3.", "4.", "5.")):
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(y, (w - len(item)) // 2, item)
                self.stdscr.attroff(curses.color_pair(3))
            else:
                self.stdscr.addstr(y, (w - len(item)) // 2, item)
        
        self.stdscr.refresh()
        
        # 获取用户选择
        while True:
            key = self.stdscr.getch()
            if key == ord('1'):
                return "简单"
            elif key == ord('2'):
                return "中等"
            elif key == ord('3'):
                return "困难"
            elif key == ord('4'):
                return "编程挑战"
            elif key == ord('5'):
                self.show_stats()
                return self.show_menu()
            elif key in [ord('q'), ord('Q')]:
                return "quit"
    
    def show_stats(self):
        """显示统计信息"""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        stats_title = "🏆 历史最佳成绩 🏆"
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(2, (w - len(stats_title)) // 2, stats_title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        stats_lines = [
            "",
            "功能开发中... 敬请期待！",
            "",
            "将会包含：",
            "- 最高WPM记录",
            "- 最佳准确率",
            "- 总练习时间",
            "- 进步曲线",
            "",
            "按任意键返回菜单..."
        ]
        
        start_y = 5
        for i, line in enumerate(stats_lines):
            self.stdscr.addstr(start_y + i, (w - len(line)) // 2, line)
        
        self.stdscr.refresh()
        self.stdscr.getch()
    
    def prepare_game(self):
        """准备游戏"""
        self.current_text = random.choice(TEXTS[self.difficulty])
        self.user_input = ""
        self.start_time = 0
        self.end_time = 0
        self.errors = 0
        self.total_chars = 0
        self.is_running = False
    
    def draw_game_screen(self):
        """绘制游戏界面"""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # 显示标题和难度
        title = f"打字练习 - {self.difficulty}难度"
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(1, (w - len(title)) // 2, title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        # 显示提示
        hint = "开始输入即开始计时 | ESC键重新开始"
        self.stdscr.attron(curses.color_pair(6))
        self.stdscr.addstr(2, (w - len(hint)) // 2, hint)
        self.stdscr.attroff(curses.color_pair(6))
        
        # 显示目标文本
        target_y = 5
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(target_y - 1, 3, "目标文本:")
        self.stdscr.attroff(curses.color_pair(3))
        
        # 分行显示长文本
        max_width = w - 6
        lines = self.wrap_text(self.current_text, max_width)
        for i, line in enumerate(lines):
            self.stdscr.addstr(target_y + i, 3, line)
        
        # 显示用户输入（带颜色标记）
        input_y = target_y + len(lines) + 2
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(input_y - 1, 3, "你的输入:")
        self.stdscr.attroff(curses.color_pair(3))
        
        # 逐字符比较并着色
        for i, char in enumerate(self.user_input):
            if i < len(self.current_text):
                if char == self.current_text[i]:
                    self.stdscr.attron(curses.color_pair(1))  # 绿色=正确
                else:
                    self.stdscr.attron(curses.color_pair(2))  # 红色=错误
                
                x = 3 + (i % max_width)
                y = input_y + (i // max_width)
                if y < h - 8:  # 确保不超出屏幕
                    self.stdscr.addstr(y, x, char)
                
                self.stdscr.attroff(curses.color_pair(1))
                self.stdscr.attroff(curses.color_pair(2))
        
        # 显示光标位置（下划线）
        if len(self.user_input) < len(self.current_text):
            cursor_pos = len(self.user_input)
            x = 3 + (cursor_pos % max_width)
            y = input_y + (cursor_pos // max_width)
            if y < h - 8:
                self.stdscr.attron(curses.A_UNDERLINE | curses.color_pair(3))
                self.stdscr.addstr(y, x, "_")
                self.stdscr.attroff(curses.A_UNDERLINE | curses.color_pair(3))
        
        # 显示实时统计
        stats_y = h - 6
        self.stdscr.attron(curses.color_pair(5))
        self.stdscr.addstr(stats_y, 3, "=" * (w - 6))
        
        progress = len(self.user_input) / len(self.current_text) * 100
        accuracy = self.calculate_accuracy()
        wpm = self.calculate_wpm()
        
        stats_line1 = f"进度: {progress:.1f}% | 准确率: {accuracy:.1f}% | 速度: {wpm:.1f} WPM"
        self.stdscr.addstr(stats_y + 1, 3, stats_line1)
        
        # 进度条
        bar_width = w - 10
        filled = int(bar_width * progress / 100)
        progress_bar = "█" * filled + "░" * (bar_width - filled)
        self.stdscr.addstr(stats_y + 2, 5, progress_bar)
        
        self.stdscr.attroff(curses.color_pair(5))
        
        self.stdscr.refresh()
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
        """将文本按宽度分行"""
        lines = []
        current_line = ""
        for word in text.split():
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.rstrip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.rstrip())
        return lines if lines else [text[:max_width]]
    
    def calculate_accuracy(self) -> float:
        """计算准确率"""
        if len(self.user_input) == 0:
            return 100.0
        
        correct = sum(1 for i, char in enumerate(self.user_input) 
                     if i < len(self.current_text) and char == self.current_text[i])
        return (correct / len(self.user_input)) * 100
    
    def calculate_wpm(self) -> float:
        """计算每分钟单词数（WPM）"""
        if not self.is_running or self.start_time == 0:
            return 0.0
        
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0.0
        
        # WPM = (字符数 / 5) / 分钟数
        minutes = elapsed_time / 60
        words = len(self.user_input) / 5
        return words / minutes if minutes > 0 else 0.0
    
    def show_results(self):
        """显示最终结果"""
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # 计算最终统计
        elapsed_time = self.end_time - self.start_time
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        
        # 评级
        if wpm >= 80 and accuracy >= 95:
            rating = "🏆 打字大师！"
            rating_color = 4
        elif wpm >= 60 and accuracy >= 90:
            rating = "⭐ 优秀！"
            rating_color = 1
        elif wpm >= 40 and accuracy >= 85:
            rating = "👍 良好！"
            rating_color = 3
        else:
            rating = "💪 继续加油！"
            rating_color = 2
        
        # 显示结果
        title = "游戏结束 - 统计结果"
        self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        self.stdscr.addstr(3, (w - len(title)) // 2, title)
        self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        results = [
            "",
            f"用时: {elapsed_time:.2f} 秒",
            f"速度: {wpm:.1f} WPM",
            f"准确率: {accuracy:.1f}%",
            f"总字符数: {len(self.user_input)}",
            f"错误数: {self.total_chars - sum(1 for i, c in enumerate(self.user_input) if i < len(self.current_text) and c == self.current_text[i])}",
            "",
        ]
        
        start_y = 6
        self.stdscr.attron(curses.color_pair(5))
        for i, line in enumerate(results):
            self.stdscr.addstr(start_y + i, (w - len(line)) // 2, line)
        self.stdscr.attroff(curses.color_pair(5))
        
        # 显示评级
        self.stdscr.attron(curses.color_pair(rating_color) | curses.A_BOLD)
        self.stdscr.addstr(start_y + len(results), (w - len(rating)) // 2, rating)
        self.stdscr.attroff(curses.color_pair(rating_color) | curses.A_BOLD)
        
        # 选项
        options = [
            "",
            "",
            "按 R 重新开始",
            "按 M 返回菜单",
            "按 Q 退出游戏",
        ]
        
        for i, line in enumerate(options):
            self.stdscr.addstr(start_y + len(results) + 2 + i, (w - len(line)) // 2, line)
        
        self.stdscr.refresh()
        
        # 等待用户选择
        while True:
            key = self.stdscr.getch()
            if key in [ord('r'), ord('R')]:
                return "restart"
            elif key in [ord('m'), ord('M')]:
                return "menu"
            elif key in [ord('q'), ord('Q')]:
                return "quit"
    
    def play(self):
        """游戏主循环"""
        self.prepare_game()
        self.draw_game_screen()
        
        while True:
            key = self.stdscr.getch()
            
            # ESC键重新开始
            if key == 27:
                return "restart"
            
            # 退格键
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
                    self.draw_game_screen()
            
            # 普通字符输入
            elif 32 <= key <= 126:
                # 第一次输入时开始计时
                if not self.is_running:
                    self.start_time = time.time()
                    self.is_running = True
                
                char = chr(key)
                self.user_input += char
                self.total_chars += 1
                
                # 检查是否完成
                if len(self.user_input) >= len(self.current_text):
                    self.end_time = time.time()
                    return self.show_results()
                
                self.draw_game_screen()
    
    def run(self):
        """运行游戏"""
        while True:
            # 显示菜单
            choice = self.show_menu()
            
            if choice == "quit":
                break
            
            self.difficulty = choice
            
            # 游戏循环
            while True:
                result = self.play()
                
                if result == "restart":
                    self.prepare_game()
                    continue
                elif result == "menu":
                    break
                elif result == "quit":
                    return


def main(stdscr):
    """主函数"""
    game = TypingGame(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n感谢游玩！再见！")

