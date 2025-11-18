#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
互动打字练习游戏 - 图形界面版本
使用pygame实现，具有更好的视觉效果和动画
支持中文显示
"""

import pygame
import time
import random
import sys
import os
from typing import List, Tuple

# 初始化pygame
pygame.init()

# 获取支持中文的字体
def get_chinese_font(size):
    """
    获取支持中文的字体
    按优先级尝试不同的中文字体
    """
    # 常见中文字体列表（按系统分类）
    chinese_fonts = []
    
    if sys.platform == 'win32':  # Windows
        chinese_fonts = [
            'microsoftyahei',  # 微软雅黑
            'simsun',          # 宋体
            'simhei',          # 黑体
            'msgothic',        # MS Gothic (日文但支持中文)
            'C:\\Windows\\Fonts\\msyh.ttc',  # 微软雅黑完整路径
            'C:\\Windows\\Fonts\\simhei.ttf', # 黑体完整路径
        ]
    elif sys.platform == 'darwin':  # macOS
        chinese_fonts = [
            'PingFang SC',
            'Heiti SC',
            'STHeiti',
            'Arial Unicode MS',
        ]
    else:  # Linux
        chinese_fonts = [
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei',
            'Droid Sans Fallback',
            'Noto Sans CJK SC',
            'DejaVu Sans',
        ]
    
    # 尝试加载字体
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # 测试是否支持中文
            test_surface = font.render('测试', True, (255, 255, 255))
            if test_surface.get_width() > 0:
                return font
        except:
            continue
    
    # 如果都失败，返回默认字体（可能不支持中文）
    try:
        return pygame.font.Font(None, size)
    except:
        return pygame.font.SysFont('arial', size)

# 颜色定义
COLORS = {
    'background': (20, 20, 30),
    'text': (240, 240, 240),
    'correct': (46, 204, 113),
    'error': (231, 76, 60),
    'highlight': (241, 196, 15),
    'accent': (52, 152, 219),
    'purple': (155, 89, 182),
    'gray': (149, 165, 166),
}

# 窗口设置
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# 字体大小
FONT_SIZES = {
    'title': 48,
    'subtitle': 24,
    'text': 28,
    'small': 20,
}

# 练习文本
TEXTS = {
    "简单": [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a great programming language.",
        "Practice makes perfect in typing.",
        "Hello world from the typing game!",
        "Keep calm and type on.",
        "Coding is fun and creative.",
        "Learn something new every day.",
    ],
    "中等": [
        "The art of programming is the art of organizing complexity.",
        "Any fool can write code that a computer can understand.",
        "Experience is the name everyone gives to their mistakes.",
        "Simplicity is the soul of efficiency in coding.",
        "First, solve the problem. Then, write the code.",
        "Good code is its own best documentation.",
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
        "class Animal: def __init__(self, name): self.name = name",
        "import sys; sys.stdout.write('Hello, World!\\n')",
    ]
}


class Button:
    """按钮类"""
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False
    
    def draw(self, screen, font):
        """绘制按钮"""
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLORS['text'], self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                return True
        return False


class Particle:
    """粒子效果类"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.life = 30
        self.max_life = 30
    
    def update(self):
        """更新粒子"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # 重力
        self.life -= 1
    
    def draw(self, screen):
        """绘制粒子"""
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = int(5 * (self.life / self.max_life))
            color = (*self.color, alpha)
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (size, size), size)
            screen.blit(s, (int(self.x - size), int(self.y - size)))
    
    def is_alive(self):
        """检查粒子是否存活"""
        return self.life > 0


class TypingGameGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("⌨️ 超级打字练习游戏")
        self.clock = pygame.time.Clock()
        
        # 加载支持中文的字体
        print("正在加载字体...")
        self.fonts = {
            'title': get_chinese_font(FONT_SIZES['title']),
            'subtitle': get_chinese_font(FONT_SIZES['subtitle']),
            'text': get_chinese_font(FONT_SIZES['text']),
            'small': get_chinese_font(FONT_SIZES['small']),
        }
        print("✓ 字体加载完成")
        
        self.difficulty = "中等"
        self.current_text = ""
        self.user_input = ""
        self.start_time = 0
        self.end_time = 0
        self.is_running = False
        self.state = "menu"  # menu, playing, results
        
        self.particles = []
        self.score = 0
        self.combo = 0
        
        # 结果界面按钮
        self.restart_btn = None
        self.menu_btn = None
        
        self.create_menu_buttons()
    
    def create_menu_buttons(self):
        """创建菜单按钮"""
        self.menu_buttons = []
        button_width = 300
        button_height = 60
        start_y = 250
        spacing = 80
        
        difficulties = ["简单", "中等", "困难", "编程挑战"]
        colors = [COLORS['correct'], COLORS['accent'], COLORS['purple'], COLORS['error']]
        
        for i, (diff, color) in enumerate(zip(difficulties, colors)):
            x = (WINDOW_WIDTH - button_width) // 2
            y = start_y + i * spacing
            button = Button(x, y, button_width, button_height, diff, color, COLORS['text'])
            self.menu_buttons.append((button, diff))
    
    def show_menu(self):
        """显示菜单"""
        self.screen.fill(COLORS['background'])
        
        # 标题
        title = self.fonts['title'].render("⌨️ 超级打字练习", True, COLORS['highlight'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 副标题
        subtitle = self.fonts['subtitle'].render("选择你的挑战难度", True, COLORS['text'])
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 绘制按钮
        for button, _ in self.menu_buttons:
            button.draw(self.screen, self.fonts['subtitle'])
        
        # 提示信息
        hint = self.fonts['small'].render("ESC 退出游戏", True, COLORS['gray'])
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(hint, hint_rect)
    
    def prepare_game(self):
        """准备游戏"""
        self.current_text = random.choice(TEXTS[self.difficulty])
        self.user_input = ""
        self.start_time = 0
        self.end_time = 0
        self.is_running = False
        self.particles = []
        self.score = 0
        self.combo = 0
    
    def draw_game_screen(self):
        """绘制游戏界面"""
        self.screen.fill(COLORS['background'])
        
        # 标题
        title = self.fonts['subtitle'].render(f"难度: {self.difficulty}", True, COLORS['highlight'])
        self.screen.blit(title, (20, 20))
        
        # 提示
        hint = self.fonts['small'].render("ESC 返回菜单", True, COLORS['gray'])
        self.screen.blit(hint, (WINDOW_WIDTH - 200, 20))
        
        # 目标文本区域
        target_y = 120
        target_label = self.fonts['subtitle'].render("目标文本:", True, COLORS['accent'])
        self.screen.blit(target_label, (50, target_y - 40))
        
        # 绘制目标文本框
        text_box_rect = pygame.Rect(50, target_y, WINDOW_WIDTH - 100, 100)
        pygame.draw.rect(self.screen, (40, 40, 50), text_box_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['accent'], text_box_rect, 2, border_radius=10)
        
        # 显示目标文本
        self.draw_wrapped_text(self.current_text, 70, target_y + 20, WINDOW_WIDTH - 140, 
                              self.fonts['text'], COLORS['text'])
        
        # 用户输入区域
        input_y = 280
        input_label = self.fonts['subtitle'].render("你的输入:", True, COLORS['highlight'])
        self.screen.blit(input_label, (50, input_y - 40))
        
        # 绘制输入框
        input_box_rect = pygame.Rect(50, input_y, WINDOW_WIDTH - 100, 100)
        pygame.draw.rect(self.screen, (40, 40, 50), input_box_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLORS['highlight'], input_box_rect, 2, border_radius=10)
        
        # 显示用户输入（带颜色）
        x = 70
        y = input_y + 20
        for i, char in enumerate(self.user_input):
            if i < len(self.current_text):
                color = COLORS['correct'] if char == self.current_text[i] else COLORS['error']
            else:
                color = COLORS['error']
            
            char_surf = self.fonts['text'].render(char, True, color)
            self.screen.blit(char_surf, (x, y))
            x += char_surf.get_width()
            
            # 换行处理
            if x > WINDOW_WIDTH - 130:
                x = 70
                y += 35
        
        # 光标
        if int(time.time() * 2) % 2 == 0:
            cursor_surf = self.fonts['text'].render("_", True, COLORS['highlight'])
            self.screen.blit(cursor_surf, (x, y))
        
        # 统计信息
        self.draw_stats()
        
        # 绘制粒子效果
        for particle in self.particles:
            particle.draw(self.screen)
    
    def draw_wrapped_text(self, text, x, y, max_width, font, color):
        """绘制自动换行的文本"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            self.screen.blit(line_surf, (x, y + i * 35))
    
    def draw_stats(self):
        """绘制统计信息"""
        stats_y = 440
        
        # 背景
        stats_rect = pygame.Rect(50, stats_y, WINDOW_WIDTH - 100, 200)
        pygame.draw.rect(self.screen, (30, 30, 40), stats_rect, border_radius=10)
        
        # 进度
        progress = len(self.user_input) / len(self.current_text) if self.current_text else 0
        progress_text = f"进度: {progress * 100:.1f}%"
        
        # 准确率
        accuracy = self.calculate_accuracy()
        accuracy_text = f"准确率: {accuracy:.1f}%"
        
        # WPM
        wpm = self.calculate_wpm()
        wpm_text = f"速度: {wpm:.1f} WPM"
        
        # Combo
        combo_text = f"连击: {self.combo}x"
        
        # 显示统计
        stats = [progress_text, accuracy_text, wpm_text, combo_text]
        colors = [COLORS['accent'], COLORS['correct'], COLORS['highlight'], COLORS['purple']]
        
        for i, (stat, color) in enumerate(zip(stats, colors)):
            stat_surf = self.fonts['subtitle'].render(stat, True, color)
            self.screen.blit(stat_surf, (70, stats_y + 20 + i * 40))
        
        # 进度条
        bar_y = stats_y + 170
        bar_width = WINDOW_WIDTH - 140
        bar_height = 20
        
        # 背景条
        pygame.draw.rect(self.screen, (60, 60, 70), (70, bar_y, bar_width, bar_height), border_radius=10)
        
        # 进度条
        filled_width = int(bar_width * progress)
        if filled_width > 0:
            # 渐变效果
            for x in range(filled_width):
                ratio = x / bar_width
                color = (
                    int(COLORS['correct'][0] * (1 - ratio) + COLORS['accent'][0] * ratio),
                    int(COLORS['correct'][1] * (1 - ratio) + COLORS['accent'][1] * ratio),
                    int(COLORS['correct'][2] * (1 - ratio) + COLORS['accent'][2] * ratio),
                )
                pygame.draw.rect(self.screen, color, (70 + x, bar_y, 1, bar_height))
            
            pygame.draw.rect(self.screen, COLORS['highlight'], 
                           (70, bar_y, filled_width, bar_height), 2, border_radius=10)
    
    def calculate_accuracy(self):
        """计算准确率"""
        if len(self.user_input) == 0:
            return 100.0
        
        correct = sum(1 for i, char in enumerate(self.user_input) 
                     if i < len(self.current_text) and char == self.current_text[i])
        return (correct / len(self.user_input)) * 100
    
    def calculate_wpm(self):
        """计算WPM"""
        if not self.is_running or self.start_time == 0:
            return 0.0
        
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0.0
        
        minutes = elapsed_time / 60
        words = len(self.user_input) / 5
        return words / minutes if minutes > 0 else 0.0
    
    def add_particle_burst(self, x, y, color, count=10):
        """添加粒子爆发效果"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def show_results(self):
        """显示结果"""
        self.screen.fill(COLORS['background'])
        
        # 计算统计
        elapsed_time = self.end_time - self.start_time
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
        
        # 评级
        if wpm >= 80 and accuracy >= 95:
            rating = "🏆 打字大师！"
            rating_color = COLORS['highlight']
        elif wpm >= 60 and accuracy >= 90:
            rating = "⭐ 优秀！"
            rating_color = COLORS['correct']
        elif wpm >= 40 and accuracy >= 85:
            rating = "👍 良好！"
            rating_color = COLORS['accent']
        else:
            rating = "💪 继续加油！"
            rating_color = COLORS['purple']
        
        # 标题
        title = self.fonts['title'].render("游戏结束", True, COLORS['highlight'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # 评级
        rating_surf = self.fonts['title'].render(rating, True, rating_color)
        rating_rect = rating_surf.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(rating_surf, rating_rect)
        
        # 统计信息
        stats = [
            f"用时: {elapsed_time:.2f} 秒",
            f"速度: {wpm:.1f} WPM",
            f"准确率: {accuracy:.1f}%",
            f"总字符: {len(self.user_input)}",
            f"最高连击: {self.combo}",
        ]
        
        y = 260
        for stat in stats:
            stat_surf = self.fonts['subtitle'].render(stat, True, COLORS['text'])
            stat_rect = stat_surf.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(stat_surf, stat_rect)
            y += 50
        
        # 按钮
        button_y = 520
        button_width = 200
        button_height = 50
        spacing = 20
        
        # 创建或更新重新开始按钮
        if self.restart_btn is None:
            self.restart_btn = Button(WINDOW_WIDTH // 2 - button_width - spacing // 2, button_y,
                               button_width, button_height, "重新开始", COLORS['correct'], COLORS['text'])
        self.restart_btn.draw(self.screen, self.fonts['subtitle'])
        
        # 创建或更新返回菜单按钮
        if self.menu_btn is None:
            self.menu_btn = Button(WINDOW_WIDTH // 2 + spacing // 2, button_y,
                            button_width, button_height, "返回菜单", COLORS['accent'], COLORS['text'])
        self.menu_btn.draw(self.screen, self.fonts['subtitle'])
        
        # 绘制粒子效果（完成时的烟花）
        for particle in self.particles:
            particle.draw(self.screen)
    
    def handle_game_input(self, event):
        """处理游戏输入"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
                return
            
            elif event.key == pygame.K_BACKSPACE:
                if len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]
                    self.combo = 0
            
            elif event.unicode and len(event.unicode) == 1 and 32 <= ord(event.unicode) <= 126:
                # 第一次输入开始计时
                if not self.is_running:
                    self.start_time = time.time()
                    self.is_running = True
                
                char = event.unicode
                self.user_input += char
                
                # 检查正确性并添加粒子效果
                if len(self.user_input) <= len(self.current_text):
                    if char == self.current_text[len(self.user_input) - 1]:
                        self.combo += 1
                        self.add_particle_burst(500, 300, COLORS['correct'], 5)
                    else:
                        self.combo = 0
                        self.add_particle_burst(500, 300, COLORS['error'], 8)
                
                # 检查是否完成
                if len(self.user_input) >= len(self.current_text):
                    self.end_time = time.time()
                    self.state = "results"
                    # 完成时的烟花效果
                    for _ in range(50):
                        x = random.randint(100, WINDOW_WIDTH - 100)
                        y = random.randint(100, WINDOW_HEIGHT - 100)
                        color = random.choice([COLORS['correct'], COLORS['highlight'], 
                                             COLORS['accent'], COLORS['purple']])
                        self.add_particle_burst(x, y, color, 3)
    
    def run(self):
        """运行游戏"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            # 更新粒子
            self.particles = [p for p in self.particles if p.is_alive()]
            for particle in self.particles:
                particle.update()
            
            # 渲染（需要先渲染才能创建按钮）
            if self.state == "menu":
                self.show_menu()
            elif self.state == "playing":
                self.draw_game_screen()
            elif self.state == "results":
                self.show_results()
            
            # 显示更新
            pygame.display.flip()
            
            # 事件处理（在渲染之后，这样按钮已经创建）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.state == "menu":
                        running = False
                
                if self.state == "menu":
                    for button, difficulty in self.menu_buttons:
                        if button.handle_event(event):
                            self.difficulty = difficulty
                            self.prepare_game()
                            self.state = "playing"
                
                elif self.state == "playing":
                    self.handle_game_input(event)
                
                elif self.state == "results":
                    if self.restart_btn and self.restart_btn.handle_event(event):
                        self.prepare_game()
                        self.state = "playing"
                        # 重置按钮以便下次重新创建
                        self.restart_btn = None
                        self.menu_btn = None
                    if self.menu_btn and self.menu_btn.handle_event(event):
                        self.state = "menu"
                        # 重置按钮以便下次重新创建
                        self.restart_btn = None
                        self.menu_btn = None
        
        pygame.quit()


def main():
    """主函数"""
    game = TypingGameGUI()
    game.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"游戏出错: {e}")
        import traceback
        traceback.print_exc()

