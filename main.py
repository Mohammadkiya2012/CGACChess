import flet as ft
import chess
import random
import copy
import json
import os
import sys
import threading
import time
import hashlib
import uuid
import webbrowser
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# =============================================
# Helper function for resource paths
# =============================================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =============================================
# Files
# =============================================
SETTINGS_FILE = "settings.json"
STATS_FILE = "stats.json"
REFERRAL_FILE = "referrals.json"
SUGGESTIONS_FILE = "suggestions.json"
VIP_CODES_FILE = "vip_codes.json"
HISTORY_FILE = "history.json"

# =============================================
# Constants
# =============================================
DAILY_REWARD = 100
REFERRAL_REWARD = 150000
REFERRAL_COUNT = 5
AD_REMOVAL_PRICE = 25000
FULL_VERSION_PRICE = 45000
BOARD_SIZE = 440
CELL_SIZE = BOARD_SIZE // 8
ANIMATION_STEPS = 20
ANIMATION_DELAY = 8

# =============================================
# Default settings
# =============================================
DEFAULT_SETTINGS = {
    'ai_level': 'easy',
    'sound': True,
    'timer_minutes': 3,
    'theme': 'dark',
    'ads_removed': False,
    'vip': False,
    'user_id': ''
}

# =============================================
# Themes
# =============================================
THEMES = {
    'dark': {
        'bg': '#0d0d1a',
        'bg_light': '#16162e',
        'bg_card': '#1a1a2e',
        'fg': '#e6b800',
        'fg_secondary': '#c9c9e0',
        'text': '#eeeeee',
        'text_muted': '#8888aa',
        'button_bg': '#2a2a5a',
        'button_hover': '#3d3d7a',
        'button_active': '#4a4a8a',
        'button_green': '#2e7d32',
        'button_green_hover': '#3d9a40',
        'button_red': '#7a2e2e',
        'button_red_hover': '#9a3d3d',
        'button_gold': '#b8860b',
        'button_gold_hover': '#d4a017',
        'board_light': '#f0d9b5',
        'board_dark': '#b58863',
        'board_border': '#c4a373',
        'history_bg': '#12121f',
        'history_fg': '#c9c9e0',
        'highlight': '#00ff88',
        'highlight_move': '#ffdd44',
        'legal_move': '#66cc66',
        'shadow': '#000000',
        'check_glow': '#ff2222',
        'success': '#4CAF50',
        'warning': '#FFC107',
        'error': '#f44336',
        'progress_green': '#4CAF50',
        'progress_yellow': '#FFC107',
        'progress_red': '#f44336',
        'ad_bg': '#1a1a2e',
        'ad_fg': '#e6b800'
    },
    'light': {
        'bg': '#f5f0e8',
        'bg_light': '#e8e0d5',
        'bg_card': '#dfd6c8',
        'fg': '#2c3e50',
        'fg_secondary': '#5a6a7a',
        'text': '#2c3e50',
        'text_muted': '#7a8a9a',
        'button_bg': '#3498db',
        'button_hover': '#2980b9',
        'button_active': '#1a6a9a',
        'button_green': '#27ae60',
        'button_green_hover': '#219a52',
        'button_red': '#e74c3c',
        'button_red_hover': '#c0392b',
        'button_gold': '#f39c12',
        'button_gold_hover': '#d68910',
        'board_light': '#f0d9b5',
        'board_dark': '#b58863',
        'board_border': '#8b7355',
        'history_bg': '#dfd6c8',
        'history_fg': '#2c3e50',
        'highlight': '#2ecc71',
        'highlight_move': '#ffdd44',
        'legal_move': '#82e0aa',
        'shadow': '#bdc3c7',
        'check_glow': '#ff2222',
        'success': '#27ae60',
        'warning': '#f39c12',
        'error': '#e74c3c',
        'progress_green': '#27ae60',
        'progress_yellow': '#f39c12',
        'progress_red': '#e74c3c',
        'ad_bg': '#e8e0d5',
        'ad_fg': '#2c3e50'
    },
    'classic': {
        'bg': '#2b2b2b',
        'bg_light': '#3d3d3d',
        'bg_card': '#4a4a4a',
        'fg': '#d4a373',
        'fg_secondary': '#b8a090',
        'text': '#e8e8e8',
        'text_muted': '#a0a0a0',
        'button_bg': '#5a5a5a',
        'button_hover': '#6a6a6a',
        'button_active': '#7a7a7a',
        'button_green': '#3d7a3d',
        'button_green_hover': '#4d8a4d',
        'button_red': '#7a3d3d',
        'button_red_hover': '#8a4d4d',
        'button_gold': '#c49a6c',
        'button_gold_hover': '#d4aa7c',
        'board_light': '#f0d9b5',
        'board_dark': '#b58863',
        'board_border': '#a08060',
        'history_bg': '#3d3d3d',
        'history_fg': '#d4a373',
        'highlight': '#e6b800',
        'highlight_move': '#ffdd44',
        'legal_move': '#7cb342',
        'shadow': '#000000',
        'check_glow': '#ff2222',
        'success': '#4CAF50',
        'warning': '#FFC107',
        'error': '#f44336',
        'progress_green': '#4CAF50',
        'progress_yellow': '#FFC107',
        'progress_red': '#f44336',
        'ad_bg': '#4a4a4a',
        'ad_fg': '#d4a373'
    }
}

# =============================================
# Load/Save functions
# =============================================
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        for key in DEFAULT_SETTINGS:
            if key not in settings:
                settings[key] = DEFAULT_SETTINGS[key]
        if not settings.get('user_id'):
            settings['user_id'] = str(uuid.uuid4())[:8]
            save_settings(settings)
        return settings
    except:
        settings = DEFAULT_SETTINGS.copy()
        settings['user_id'] = str(uuid.uuid4())[:8]
        save_settings(settings)
        return settings

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except:
        pass

def load_stats():
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0}

def save_stats(stats):
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except:
        pass

# =============================================
# VIP Code Manager
# =============================================
class VIPCodeManager:
    @staticmethod
    def load_codes():
        try:
            with open(VIP_CODES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def save_codes(codes):
        with open(VIP_CODES_FILE, 'w') as f:
            json.dump(codes, f, indent=2)

    @staticmethod
    def generate_code():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

    @staticmethod
    def create_new_code():
        codes = VIPCodeManager.load_codes()
        new_code = VIPCodeManager.generate_code()
        codes[new_code] = {'used': False, 'created_at': datetime.now().isoformat()}
        VIPCodeManager.save_codes(codes)
        return new_code

    @staticmethod
    def use_code(code):
        codes = VIPCodeManager.load_codes()
        if code in codes and not codes[code]['used']:
            codes[code]['used'] = True
            codes[code]['used_at'] = datetime.now().isoformat()
            VIPCodeManager.save_codes(codes)
            return True
        return False

# =============================================
# Ranking system
# =============================================
def get_ranking_level(stats):
    games = stats.get('games', 0)
    wins = stats.get('wins', 0)
    if games == 0:
        return "No games yet"
    win_rate = (wins / games) * 100
    if games < 10:
        return "Beginner (Novice)"
    elif games < 50 and win_rate >= 40:
        return "Intermediate (Amateur)"
    elif games < 100 and win_rate >= 50:
        return "Advanced (Skilled)"
    elif games < 200 and win_rate >= 60:
        return "Professional (Master)"
    elif games >= 200 and win_rate >= 70:
        return "Grandmaster (Legend)"
    else:
        return "Dedicated Player"

def is_grandmaster(stats):
    return get_ranking_level(stats) == "Grandmaster (Legend)"

# =============================================
# Referral System
# =============================================
class ReferralSystem:
    @staticmethod
    def generate_code(user_id):
        return hashlib.md5(user_id.encode()).hexdigest()[:6].upper()
    
    @staticmethod
    def load_data(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def save_data(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def register_referral(user_id):
        code = ReferralSystem.generate_code(user_id)
        data = ReferralSystem.load_data(REFERRAL_FILE)
        if code not in data:
            data[code] = {'user_id': user_id, 'uses': 0, 'earned': 0}
            ReferralSystem.save_data(REFERRAL_FILE, data)
        return code
    
    @staticmethod
    def use_referral(code):
        data = ReferralSystem.load_data(REFERRAL_FILE)
        if code in data:
            data[code]['uses'] += 1
            if data[code]['uses'] % REFERRAL_COUNT == 0:
                data[code]['earned'] += REFERRAL_REWARD
                ReferralSystem.save_data(REFERRAL_FILE, data)
                return True, f"🎉 تبریک! {REFERRAL_REWARD:,} تومان پاداش شما واریز شد!"
            ReferralSystem.save_data(REFERRAL_FILE, data)
            remaining = REFERRAL_COUNT - (data[code]['uses'] % REFERRAL_COUNT)
            return True, f"✅ ثبت شد! {remaining} نفر دیگر تا پاداش بعدی!"
        return False, "❌ کد معرف نامعتبر!"
    
    @staticmethod
    def get_daily_code():
        today = datetime.now().strftime("%Y%m%d")
        return f"CHESS-{hashlib.md5(today.encode()).hexdigest()[:4].upper()}"
    
    @staticmethod
    def check_daily_code(user_code):
        daily = ReferralSystem.get_daily_code()
        if user_code == daily:
            return True, f"🎉 کد درست! {DAILY_REWARD} تومان پاداش!"
        return False, "❌ کد اشتباه! کد روزانه را دوباره امتحان کنید."
    
    @staticmethod
    def submit_suggestion(name, suggestion):
        data = ReferralSystem.load_data(SUGGESTIONS_FILE)
        if not isinstance(data, list):
            data = []
        data.append({
            'name': name,
            'suggestion': suggestion,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        ReferralSystem.save_data(SUGGESTIONS_FILE, data)
        subject = "Chess Game Suggestion"
        body = f"Name: {name}\nSuggestion: {suggestion}"
        gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to=mkiya.maleki@gmail.com&su={subject}&body={body}"
        webbrowser.open(gmail_link)
        return True

# =============================================
# Chess AI (Minimax without external engine)
# =============================================
class ChessAI:
    def __init__(self, level='easy'):
        self.set_level(level)
    
    def set_level(self, level):
        self.level = level
        if level == 'easy':
            self.depth = 2
            self.mistake_chance = 0.4
        elif level == 'medium':
            self.depth = 3
            self.mistake_chance = 0.15
        elif level == 'hard':
            self.depth = 4
            self.mistake_chance = 0.0
        else:
            self.depth = 2
            self.mistake_chance = 0.4
    
    def get_best_move(self, board, is_white):
        # Use minimax (no external engine)
        move = self._minimax_move(board, is_white)
        if move is None:
            return None
        if self.mistake_chance > 0 and random.random() < self.mistake_chance:
            moves = list(board.legal_moves)
            if moves:
                return random.choice(moves[-5:]) if len(moves) > 5 else random.choice(moves)
        return move
    
    def _minimax_move(self, board, is_white):
        _, move = self._minimax(board, self.depth, -float('inf'), float('inf'), is_white)
        return move
    
    def _minimax(self, board, depth, alpha, beta, is_max):
        if depth == 0 or board.is_game_over():
            return self._evaluate(board), None
        moves = list(board.legal_moves)
        if not moves:
            return -10000 if is_max else 10000, None
        best_move = None
        if is_max:
            max_eval = -float('inf')
            random.shuffle(moves)
            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.push(move)
                eval_score, _ = self._minimax(board_copy, depth-1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            random.shuffle(moves)
            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.push(move)
                eval_score, _ = self._minimax(board_copy, depth-1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def _evaluate(self, board):
        if board.is_checkmate():
            return -10000 if board.turn == chess.WHITE else 10000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        score = 0
        values = {chess.PAWN:100, chess.KNIGHT:320, chess.BISHOP:330, chess.ROOK:500, chess.QUEEN:900, chess.KING:20000}
        for pt in values:
            score += len(board.pieces(pt, chess.WHITE)) * values[pt]
            score -= len(board.pieces(pt, chess.BLACK)) * values[pt]
        return score

# =============================================
# Main Flet Application
# =============================================
class ChessApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "♚ CHESS ♔"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.window_min_width = 850
        self.page.window_min_height = 700
        self.page.padding = 0
        
        self.settings = load_settings()
        self.stats = load_stats()
        self.theme = THEMES[self.settings.get('theme', 'dark')]
        self.game_state = None   # to store game state when navigating
        
        # Initialize AI
        self.ai = ChessAI(self.settings.get('ai_level', 'easy'))
        
        # Set up routing
        self.page.on_route_change = self.route_change
        self.page.go('/')
    
    def route_change(self, e):
        route = self.page.route
        self.page.views.clear()
        if route == '/':
            self.page.views.append(self.main_menu_view())
        elif route == '/game':
            self.page.views.append(self.game_view())
        elif route == '/settings':
            self.page.views.append(self.settings_view())
        elif route == '/stats':
            self.page.views.append(self.stats_view())
        elif route == '/leaderboard':
            self.page.views.append(self.leaderboard_view())
        elif route == '/weekly':
            self.page.views.append(self.weekly_challenge_view())
        else:
            self.page.views.append(self.main_menu_view())
        self.page.update()
    
    # ---------- Helper to create a themed container ----------
    def themed_container(self, content=None, padding=10, bg=None):
        if bg is None:
            bg = self.theme['bg']
        return ft.Container(content=content, padding=padding, bgcolor=bg, expand=True)
    
    # ---------- Main Menu ----------
    def main_menu_view(self):
        self.apply_theme_to_page()
        title = ft.Text("♚ CHESS ♔", size=48, weight=ft.FontWeight.BOLD, color=self.theme['fg'])
        subtitle = ft.Text("Strategy • Intelligence • Victory", size=18, italic=True, color=self.theme['text_muted'])
        
        btn_style = {
            'width': 220,
            'height': 50,
            'style': ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=self.theme['button_bg'],
                overlay_color=self.theme['button_hover'],
            )
        }
        
        buttons = ft.Column([
            ft.ElevatedButton("🎮 New Game", on_click=lambda _: self.page.go('/game'), **btn_style),
            ft.ElevatedButton("📊 Statistics", on_click=lambda _: self.page.go('/stats'), **btn_style),
            ft.ElevatedButton("🏅 Leaderboard", on_click=lambda _: self.page.go('/leaderboard'), **btn_style),
            ft.ElevatedButton("⚙️ Settings", on_click=lambda _: self.page.go('/settings'), **btn_style),
            ft.ElevatedButton("❤️ Support", on_click=self.support_us, **btn_style),
            ft.ElevatedButton("🚪 Exit", on_click=lambda _: self.page.window_close(), **btn_style),
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        content = ft.Column([
            title,
            subtitle,
            ft.Divider(height=20, color='transparent'),
            buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        
        return ft.View(
            route='/',
            controls=[self.themed_container(content, padding=50)],
            bgcolor=self.theme['bg'],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def support_us(self, e):
        webbrowser.open("https://zarinpal.com/your-link")
        dialog = ft.AlertDialog(
            title=ft.Text("Support"),
            content=ft.Text("❤️ Thank you for your support!\n\nYou can donate via:\nCard 1: 7635-5631-8613-6219\nCard 2: 6104-3376-2016-6494"),
            actions=[ft.TextButton("Close", on_click=lambda _: self.close_dialog())]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    # ---------- Stats View ----------
    def stats_view(self):
        self.apply_theme_to_page()
        stats = self.stats
        msg = f"📊 Game Statistics\n\n"
        msg += f"┌─────────────────────┐\n"
        msg += f"│ Total Games: {stats['games']:>8} │\n"
        msg += f"│ Wins:        {stats['wins']:>8} │\n"
        msg += f"│ Losses:      {stats['losses']:>8} │\n"
        msg += f"│ Draws:       {stats['draws']:>8} │\n"
        if stats['games'] > 0:
            win_rate = (stats['wins'] / stats['games']) * 100
            msg += f"│ Win Rate:    {win_rate:>7.1f}% │\n"
        msg += f"└─────────────────────┘"
        
        if is_grandmaster(stats) and not self.settings.get('vip', False):
            self.settings['vip'] = True
            save_settings(self.settings)
            msg += "\n🎉 Congratulations! You have reached Grandmaster rank!\n🌟 VIP features unlocked for FREE!"
        
        content = ft.Column([
            ft.Text("📊 Statistics", size=32, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Text(msg, size=16, color=self.theme['text'], selectable=True),
            ft.ElevatedButton("← Back", on_click=lambda _: self.page.go('/'), width=150)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        return ft.View(route='/stats', controls=[self.themed_container(content)], bgcolor=self.theme['bg'])
    
    # ---------- Leaderboard ----------
    def leaderboard_view(self):
        self.apply_theme_to_page()
        level = get_ranking_level(self.stats)
        msg = f"🏅 Player Ranking\n\n"
        msg += f"Level: {level}\n"
        msg += f"Games: {self.stats['games']}\n"
        msg += f"Wins: {self.stats['wins']}\n"
        win_rate = (self.stats['wins']/self.stats['games']*100 if self.stats['games']>0 else 0)
        msg += f"Win Rate: {win_rate:.1f}%\n\n"
        msg += "To improve your rank:\n"
        msg += "• Play more games\n"
        msg += "• Increase your win rate\n"
        msg += "• Aim for higher levels!"
        content = ft.Column([
            ft.Text("🏅 Leaderboard", size=32, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Text(msg, size=16, color=self.theme['text'], selectable=True),
            ft.ElevatedButton("← Back", on_click=lambda _: self.page.go('/'), width=150)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        return ft.View(route='/leaderboard', controls=[self.themed_container(content)], bgcolor=self.theme['bg'])
    
    # ---------- Settings ----------
    def settings_view(self):
        self.apply_theme_to_page()
        vip = self.settings.get('vip', False)
        
        # Theme dropdown
        theme_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(t) for t in ['dark','light','classic']],
            value=self.settings.get('theme', 'dark'),
            on_change=self.save_theme,
            disabled=not vip,
            width=150
        )
        # AI level
        level_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option('easy'), ft.dropdown.Option('medium'), ft.dropdown.Option('hard')],
            value=self.settings.get('ai_level', 'easy'),
            on_change=self.save_level,
            width=150
        )
        # Timer
        timer_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option('3'), ft.dropdown.Option('5'), ft.dropdown.Option('10')],
            value=str(self.settings.get('timer_minutes', 3)),
            on_change=self.save_timer,
            width=100
        )
        # Sound toggle
        sound_switch = ft.Switch(
            value=self.settings.get('sound', True),
            on_change=self.toggle_sound,
        )
        # Ads removed
        ads_switch = ft.Switch(
            value=self.settings.get('ads_removed', False),
            on_change=self.toggle_ads,
            disabled=True  # implement later
        )
        
        # VIP code entry
        vip_code_entry = ft.TextField(label="Activation Code", width=200)
        def activate_vip(e):
            code = vip_code_entry.value.strip()
            if not code:
                self.show_snackbar("Please enter a code.")
                return
            if VIPCodeManager.use_code(code):
                self.settings['vip'] = True
                save_settings(self.settings)
                self.show_snackbar("🎉 VIP activated successfully!")
                self.page.go('/settings')  # refresh
            else:
                self.show_snackbar("Invalid or used code.")
        
        # Referral
        user_id = self.settings.get('user_id', '')
        ref_code = ReferralSystem.register_referral(user_id)
        ref_code_text = ft.Text(f"Your Code: {ref_code}", size=16, color=self.theme['fg'])
        ref_entry = ft.TextField(label="Enter Referral Code", width=200)
        def use_referral(e):
            code = ref_entry.value.strip()
            if not code:
                self.show_snackbar("Enter a code.")
                return
            success, msg = ReferralSystem.use_referral(code)
            self.show_snackbar(msg)
        # Daily code
        daily_code_text = ft.Text(f"Daily Code: {ReferralSystem.get_daily_code()}", size=14, color=self.theme['fg_secondary'])
        daily_entry = ft.TextField(label="Enter Daily Code", width=200)
        def check_daily(e):
            code = daily_entry.value.strip()
            success, msg = ReferralSystem.check_daily_code(code)
            self.show_snackbar(msg)
        
        # Suggestions
        sug_name = ft.TextField(label="Your Name", width=200)
        sug_text = ft.TextField(label="Suggestion", width=300, multiline=True)
        def submit_suggestion(e):
            name = sug_name.value.strip() or "Anonymous"
            suggestion = sug_text.value.strip()
            if not suggestion:
                self.show_snackbar("Please enter a suggestion.")
                return
            ReferralSystem.submit_suggestion(name, suggestion)
            self.show_snackbar("✅ Submitted! Gmail opened.")
            sug_text.value = ""
            sug_name.value = ""
            self.page.update()
        
        # Build UI
        settings_content = ft.Column([
            ft.Text("⚙️ Settings", size=32, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Row([ft.Text("VIP Status:", size=16), ft.Text("Active ✅" if vip else "Free (Limited)", size=16, color=self.theme['success'] if vip else self.theme['warning'])]),
            ft.Divider(height=10),
            ft.Row([ft.Text("Theme:", size=16), theme_dropdown]),
            ft.Row([ft.Text("AI Level:", size=16), level_dropdown]),
            ft.Row([ft.Text("Timer (min):", size=16), timer_dropdown]),
            ft.Row([ft.Text("Sound:", size=16), sound_switch]),
            ft.Row([ft.Text("Remove Ads:", size=16), ads_switch]),
            ft.Divider(height=10),
            ft.Text("💳 Upgrade to VIP (45,000 Toman)", size=18, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Text("To activate VIP, send 45,000 Toman to one of the following cards:", size=14),
            ft.Text("Cards: 7635-5631-8613-6219 | 6104-3376-2016-6494", size=14, weight=ft.FontWeight.BOLD),
            ft.Row([vip_code_entry, ft.ElevatedButton("✅ Activate VIP", on_click=activate_vip)]),
            ft.Divider(height=10),
            ft.Text("🎁 Referral & Rewards", size=18, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Row([ref_code_text, ft.IconButton(icon=ft.icons.CONTENT_COPY, on_click=lambda _: self.copy_to_clipboard(ref_code))]),
            ft.Row([ref_entry, ft.ElevatedButton("✅ Use", on_click=use_referral)]),
            ft.Row([daily_code_text, daily_entry, ft.ElevatedButton("🎯 Check", on_click=check_daily)]),
            ft.Divider(height=10),
            ft.Text("💡 Suggestions", size=18, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Row([sug_name, sug_text, ft.ElevatedButton("📩 Send", on_click=submit_suggestion)]),
            ft.Divider(height=10),
            ft.Text("🏆 Weekly Puzzle: White to move, mate in 2", size=16),
            ft.Row([
                ft.TextField(label="Your Answer", width=150),
                ft.ElevatedButton("🏆 Submit", on_click=self.check_puzzle)
            ]),
            ft.ElevatedButton("← Back", on_click=lambda _: self.page.go('/'), width=150)
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        return ft.View(route='/settings', controls=[self.themed_container(settings_content, padding=20)], bgcolor=self.theme['bg'])
    
    def copy_to_clipboard(self, text):
        self.page.set_clipboard(text)
        self.show_snackbar("✅ Copied!")
    
    def show_snackbar(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
    
    def save_theme(self, e):
        self.settings['theme'] = e.control.value
        save_settings(self.settings)
        self.theme = THEMES[self.settings['theme']]
        self.apply_theme_to_page()
        self.page.go('/settings')  # refresh
    
    def save_level(self, e):
        level = e.control.value
        self.settings['ai_level'] = level
        save_settings(self.settings)
        self.ai.set_level(level)
        self.show_snackbar(f"AI level set to {level.capitalize()}")
    
    def save_timer(self, e):
        self.settings['timer_minutes'] = int(e.control.value)
        save_settings(self.settings)
    
    def toggle_sound(self, e):
        self.settings['sound'] = e.control.value
        save_settings(self.settings)
    
    def toggle_ads(self, e):
        # Not implemented fully; placeholder
        self.show_snackbar("Ads removal not implemented in this demo.")
    
    def check_puzzle(self, e):
        # dummy puzzle check
        self.show_snackbar("Puzzle answer not checked in demo.")
    
    def apply_theme_to_page(self):
        # Update page background and theme
        self.page.bgcolor = self.theme['bg']
        self.page.update()
    
    # ---------- Game View ----------
    def game_view(self):
        self.apply_theme_to_page()
        # Pass the app instance and any saved state if needed
        game = GameBoard(self, state=self.game_state)
        return ft.View(route='/game', controls=[game.container], bgcolor=self.theme['bg'])
    
    # ---------- Weekly Challenge ----------
    def weekly_challenge_view(self):
        self.apply_theme_to_page()
        # Simplified: just a placeholder
        content = ft.Column([
            ft.Text("🏆 Weekly Challenge", size=32, weight=ft.FontWeight.BOLD, color=self.theme['fg']),
            ft.Text("Coming soon...", size=18, color=self.theme['text_muted']),
            ft.ElevatedButton("← Back", on_click=lambda _: self.page.go('/'), width=150)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        return ft.View(route='/weekly', controls=[self.themed_container(content)], bgcolor=self.theme['bg'])

# =============================================
# Game Board (Flet version)
# =============================================
class GameBoard:
    def __init__(self, app: ChessApp, state=None):
        self.app = app
        self.page = app.page
        self.theme = app.theme
        self.ai = app.ai
        
        # Initialize board
        if state:
            self.board = chess.Board(state['fen'])
            self.turn = state['turn']
            self.move_history = state['move_history'].copy()
            self.two_player_mode = state['two_player_mode']
            self.ai.set_level(state['ai_level'])
            self.game_over = state['game_over']
            self.timer_white = state['timer_white']
            self.timer_black = state['timer_black']
            self.paused = state.get('paused', False)
            self.last_move = state.get('last_move', None)
            self.result_recorded = state.get('result_recorded', False)
        else:
            self.board = chess.Board()
            self.turn = 'w'
            self.move_history = []
            self.two_player_mode = False
            self.game_over = False
            self.timer_white = self.app.settings.get('timer_minutes', 3) * 60
            self.timer_black = self.app.settings.get('timer_minutes', 3) * 60
            self.paused = False
            self.last_move = None
            self.result_recorded = False
        
        self.selected = None  # (row, col)
        self.legal_moves = []  # list of (row, col)
        self.ai_thinking = False
        self.timer_running = False
        self.timer_id = None
        self.error_timer = None
        
        # Build UI
        self.container = ft.Container(
            content=self.build_layout(),
            bgcolor=self.theme['bg'],
            expand=True,
            padding=10
        )
        self.update_board()
        self.start_timer()
        if not self.two_player_mode and self.turn == 'b' and not self.game_over:
            self.page.after(500, self.do_ai_move)
    
    def build_layout(self):
        # Main row: board + history
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.create_status_bar(),
                        self.create_timer_display(),
                        self.create_top_buttons(),
                        self.create_board(),
                        self.create_bottom_buttons(),
                        self.create_info_bar(),
                        self.create_error_label(),
                        self.create_ad_banner() if not self.app.settings.get('ads_removed', False) else ft.Container(height=0)
                    ],
                    spacing=5,
                    expand=True
                ),
                self.create_history_panel()
            ],
            expand=True
        )
    
    def create_status_bar(self):
        self.turn_indicator = ft.Text("♔ White", size=18, weight=ft.FontWeight.BOLD, color=self.theme['fg'])
        self.piece_count = ft.Text("♔ 16  ♚ 16", size=14, color=self.theme['text_muted'])
        self.last_move_text = ft.Text("Last: -", size=14, color=self.theme['text_muted'])
        self.check_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=self.theme['error'])
        return ft.Row(
            controls=[self.turn_indicator, self.piece_count, self.last_move_text, self.check_text],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        )
    
    def create_timer_display(self):
        self.timer_label = ft.Text("⏱ White: 05:00  Black: 05:00", size=16, weight=ft.FontWeight.BOLD, color=self.theme['fg'])
        return ft.Row([self.timer_label], alignment=ft.MainAxisAlignment.CENTER)
    
    def create_top_buttons(self):
        self.pause_btn = ft.ElevatedButton("⏸ Pause", on_click=self.toggle_pause, bgcolor=self.theme['button_bg'], color=ft.colors.WHITE)
        return ft.Row([
            ft.ElevatedButton("Menu", on_click=lambda _: self.go_to_menu(), bgcolor=self.theme['button_bg'], color=ft.colors.WHITE),
            ft.ElevatedButton("Settings", on_click=lambda _: self.go_to_settings(), bgcolor=self.theme['button_bg'], color=ft.colors.WHITE),
            self.pause_btn
        ], spacing=10)
    
    def create_board(self):
        # Use a GridView for the board
        self.board_grid = ft.GridView(
            expand=1,
            runs_count=8,
            max_extent=CELL_SIZE,
            spacing=0,
            run_spacing=0,
            padding=0
        )
        self.board_containers = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                is_light = (r + c) % 2 == 0
                color = self.theme['board_light'] if is_light else self.theme['board_dark']
                container = ft.Container(
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    bgcolor=color,
                    data=(r, c),
                    on_click=self.on_click,
                    content=ft.Text("", size=32, text_align=ft.TextAlign.CENTER),
                    border=ft.border.all(0, 'transparent')
                )
                self.board_containers[r][c] = container
                self.board_grid.controls.append(container)
        # Wrap in a Container with border
        return ft.Container(
            content=self.board_grid,
            border=ft.border.all(4, self.theme['board_border']),
            border_radius=5,
            width=BOARD_SIZE,
            height=BOARD_SIZE
        )
    
    def create_bottom_buttons(self):
        row = ft.Row(spacing=5)
        row.controls.append(ft.ElevatedButton("NEW", on_click=self.reset_game, bgcolor=self.theme['button_green'], color=ft.colors.WHITE))
        if self.app.settings.get('vip', False):
            row.controls.append(ft.ElevatedButton("2P", on_click=self.toggle_two_player, bgcolor=self.theme['button_bg'], color=ft.colors.WHITE))
        for level in ['Easy', 'Medium', 'Hard']:
            row.controls.append(ft.ElevatedButton(level, on_click=lambda e, l=level.lower(): self.set_level(l), bgcolor=self.theme['button_bg'], color=ft.colors.WHITE))
        return row
    
    def create_info_bar(self):
        self.level_label = ft.Text(f"Level: {self.ai.level.capitalize()}", size=12, color=self.theme['text_muted'])
        self.mode_label = ft.Text("Mode: vs AI", size=12, color=self.theme['text_muted'])
        return ft.Row([self.level_label, self.mode_label], spacing=20)
    
    def create_error_label(self):
        self.error_label = ft.Text("", size=12, color=self.theme['error'])
        return self.error_label
    
    def create_ad_banner(self):
        # Simple ad banner placeholder
        return ft.Container(
            content=ft.Text("📢 Ad: Buy Chessboard at Digikala", size=12, color=self.theme['ad_fg']),
            bgcolor=self.theme['ad_bg'],
            padding=5,
            border_radius=5
        )
    
    def create_history_panel(self):
        self.history_list = ft.ListView(spacing=2, padding=10, auto_scroll=True)
        heading = ft.Text("📜 History", size=18, weight=ft.FontWeight.BOLD, color=self.theme['fg'])
        container = ft.Container(
            content=ft.Column([heading, self.history_list], expand=True),
            bgcolor=self.theme['history_bg'],
            border=ft.border.all(1, self.theme['board_border']),
            width=200,
            expand=True,
            padding=5
        )
        return container
    
    # =============================================
    # Board update
    # =============================================
    def update_board(self):
        # Clear all borders first
        for r in range(8):
            for c in range(8):
                container = self.board_containers[r][c]
                container.border = ft.border.all(0, 'transparent')
                is_light = (r + c) % 2 == 0
                container.bgcolor = self.theme['board_light'] if is_light else self.theme['board_dark']
                square = chess.square(c, 7 - r)
                piece = self.board.piece_at(square)
                if piece:
                    unicode_map = {
                        (chess.WHITE, chess.KING): '♔', (chess.WHITE, chess.QUEEN): '♕',
                        (chess.WHITE, chess.ROOK): '♖', (chess.WHITE, chess.BISHOP): '♗',
                        (chess.WHITE, chess.KNIGHT): '♘', (chess.WHITE, chess.PAWN): '♙',
                        (chess.BLACK, chess.KING): '♚', (chess.BLACK, chess.QUEEN): '♛',
                        (chess.BLACK, chess.ROOK): '♜', (chess.BLACK, chess.BISHOP): '♝',
                        (chess.BLACK, chess.KNIGHT): '♞', (chess.BLACK, chess.PAWN): '♟',
                    }
                    symbol = unicode_map.get((piece.color, piece.piece_type), '?')
                    container.content = ft.Text(symbol, size=32, color='#000' if piece.color == chess.BLACK else '#fff')
                else:
                    container.content = ft.Text("")
        
        # Highlight selected and legal moves
        if self.selected:
            sr, sc = self.selected
            self.board_containers[sr][sc].border = ft.border.all(2, self.theme['highlight'])
            for tr, tc in self.legal_moves:
                self.board_containers[tr][tc].border = ft.border.all(2, self.theme['legal_move'])
        
        # Highlight last move
        if self.last_move:
            from_sq, to_sq = self.last_move
            for sq in (from_sq, to_sq):
                r = 7 - chess.square_rank(sq)
                c = chess.square_file(sq)
                self.board_containers[r][c].border = ft.border.all(3, self.theme['highlight_move'])
        
        # Check glow
        if self.board.is_check():
            king_color = chess.WHITE if self.turn == 'b' else chess.BLACK
            king_square = self.board.king(king_color)
            if king_square:
                r = 7 - chess.square_rank(king_square)
                c = chess.square_file(king_square)
                self.board_containers[r][c].border = ft.border.all(3, self.theme['check_glow'])
        
        self.update_status()
        self.page.update()
    
    def update_status(self):
        turn_text = 'White' if self.turn == 'w' else 'Black'
        turn_icon = '♔' if self.turn == 'w' else '♚'
        if self.paused:
            self.turn_indicator.value = "⏸ Paused"
            self.turn_indicator.color = self.theme['warning']
        else:
            self.turn_indicator.value = f"{turn_icon} {turn_text}"
            self.turn_indicator.color = self.theme['fg']
        w = len(self.board.pieces(chess.KING, chess.WHITE)) + len(self.board.pieces(chess.QUEEN, chess.WHITE)) + \
            len(self.board.pieces(chess.ROOK, chess.WHITE)) + len(self.board.pieces(chess.BISHOP, chess.WHITE)) + \
            len(self.board.pieces(chess.KNIGHT, chess.WHITE)) + len(self.board.pieces(chess.PAWN, chess.WHITE))
        b = len(self.board.pieces(chess.KING, chess.BLACK)) + len(self.board.pieces(chess.QUEEN, chess.BLACK)) + \
            len(self.board.pieces(chess.ROOK, chess.BLACK)) + len(self.board.pieces(chess.BISHOP, chess.BLACK)) + \
            len(self.board.pieces(chess.KNIGHT, chess.BLACK)) + len(self.board.pieces(chess.PAWN, chess.BLACK))
        self.piece_count.value = f"♔ {w}  ♚ {b}"
        last = self.move_history[-1] if self.move_history else '-'
        self.last_move_text.value = f"Last: {last}"
        self.check_text.value = "⚠️ Check!" if self.board.is_check() else ""
        self.page.update()
    
    # =============================================
    # Click handler
    # =============================================
    def on_click(self, e):
        if self.game_over or self.ai_thinking or self.paused:
            return
        if not self.two_player_mode and self.turn == 'b':
            return
        r, c = e.control.data
        square = chess.square(c, 7 - r)
        
        if self.selected is None:
            piece = self.board.piece_at(square)
            if piece and ((self.turn == 'w' and piece.color == chess.WHITE) or
                          (self.turn == 'b' and piece.color == chess.BLACK)):
                self.selected = (r, c)
                self.legal_moves = self.get_legal_moves(r, c)
                self.update_board()
            else:
                self.show_error("❌ Invalid selection!")
            return
        
        if self.selected == (r, c):
            self.selected = None
            self.legal_moves = []
            self.update_board()
            return
        
        fr, fc = self.selected
        from_sq = chess.square(fc, 7 - fr)
        to_sq = square
        piece = self.board.piece_at(from_sq)
        move = None
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(to_sq) in [0, 7]:
            move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
        else:
            move = chess.Move(from_sq, to_sq)
        
        if move in self.board.legal_moves:
            self.board.push(move)
            self.selected = None
            self.legal_moves = []
            self.last_move = (from_sq, to_sq)
            is_white = self.turn == 'w'
            self.add_move_to_history(move.uci(), is_white)
            self.turn = 'b' if self.turn == 'w' else 'w'
            self.update_board()
            self.check_game_over()
            if not self.game_over and not self.two_player_mode and self.turn == 'b':
                self.page.after(300, self.do_ai_move)
        else:
            self.show_error("❌ Invalid move!")
            self.selected = None
            self.legal_moves = []
            self.update_board()
    
    def get_legal_moves(self, row, col):
        square = chess.square(col, 7 - row)
        moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                to_row = 7 - chess.square_rank(move.to_square)
                to_col = chess.square_file(move.to_square)
                moves.append((to_row, to_col))
        return moves
    
    # =============================================
    # AI
    # =============================================
    def do_ai_move(self):
        if self.game_over or self.ai_thinking or self.two_player_mode or self.paused:
            return
        self.ai_thinking = True
        self.turn_indicator.value = "🤖 Thinking..."
        self.page.update()
        # Use threading to avoid blocking UI
        threading.Thread(target=self._ai_thread, daemon=True).start()
    
    def _ai_thread(self):
        move = self.ai.get_best_move(self.board, self.turn == 'w')
        self.page.after(0, lambda: self._apply_ai_move(move))
    
    def _apply_ai_move(self, move):
        self.ai_thinking = False
        if move and not self.game_over:
            from_sq = move.from_square
            to_sq = move.to_square
            from_r = 7 - chess.square_rank(from_sq)
            from_c = chess.square_file(from_sq)
            to_r = 7 - chess.square_rank(to_sq)
            to_c = chess.square_file(to_sq)
            self.board.push(move)
            self.last_move = (from_sq, to_sq)
            is_white = self.turn == 'w'
            self.add_move_to_history(move.uci(), is_white)
            self.turn = 'w' if self.turn == 'b' else 'b'
            self.update_board()
            self.check_game_over()
        else:
            if not move:
                self.show_error("AI could not find a move!")
    
    # =============================================
    # Game over check
    # =============================================
    def check_game_over(self):
        if self.board.is_game_over():
            self.game_over = True
            self.stop_timer()
            if self.board.is_checkmate():
                result = 'loss' if self.turn == 'w' else 'win'
                winner = 'Black' if self.turn == 'w' else 'White'
                self.record_result(result)
                self.show_game_over_dialog(f"🏆 Checkmate!", f"{winner} wins!", result)
            else:
                self.record_result('draw')
                self.show_game_over_dialog("🤝 Draw!", "Game ended in a draw!", 'draw')
    
    def show_game_over_dialog(self, title, message, result):
        color = self.theme['success'] if result == 'win' else self.theme['error'] if result == 'loss' else self.theme['warning']
        dialog = ft.AlertDialog(
            title=ft.Text(title, color=color),
            content=ft.Text(message),
            actions=[
                ft.TextButton("New Game", on_click=self.close_dialog_and_reset)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def close_dialog_and_reset(self, e):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.reset_game()
    
    def record_result(self, result):
        if self.result_recorded:
            return
        self.result_recorded = True
        stats = self.app.stats
        stats['games'] += 1
        if result == 'win':
            stats['wins'] += 1
        elif result == 'loss':
            stats['losses'] += 1
        else:
            stats['draws'] += 1
        save_stats(stats)
        self.app.stats = stats
    
    # =============================================
    # History
    # =============================================
    def add_move_to_history(self, move_uci, is_white):
        self.move_history.append(move_uci)
        self.update_history_display()
    
    def update_history_display(self):
        self.history_list.controls.clear()
        for i in range(0, len(self.move_history), 2):
            move_num = i//2 + 1
            white_move = self.move_history[i] if i < len(self.move_history) else ''
            black_move = self.move_history[i+1] if i+1 < len(self.move_history) else ''
            line = f"{move_num:2d}. {white_move}"
            if black_move:
                line += f"  {black_move}"
            self.history_list.controls.append(ft.Text(line, size=12, color=self.theme['history_fg']))
        self.history_list.update()
    
    # =============================================
    # Timer
    # =============================================
    def start_timer(self):
        if self.game_over or self.paused:
            return
        if not self.timer_running:
            self.timer_running = True
            self.update_timer_loop()
    
    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.page.after_cancel(self.timer_id)
            self.timer_id = None
    
    def update_timer_loop(self):
        if not self.timer_running or self.paused or self.game_over:
            return
        if self.turn == 'w':
            self.timer_white -= 1
        else:
            self.timer_black -= 1
        self.update_timer_display()
        if self.timer_white <= 0:
            self.timer_white = 0
            self.game_over = True
            self.stop_timer()
            self.record_result('loss')
            self.show_game_over_dialog("⏱ Time Out", "Black wins on time!", "loss")
            return
        if self.timer_black <= 0:
            self.timer_black = 0
            self.game_over = True
            self.stop_timer()
            self.record_result('win')
            self.show_game_over_dialog("⏱ Time Out", "White wins on time!", "win")
            return
        self.timer_id = self.page.after(1000, self.update_timer_loop)
    
    def update_timer_display(self):
        w_min, w_sec = divmod(self.timer_white, 60)
        b_min, b_sec = divmod(self.timer_black, 60)
        self.timer_label.value = f"⏱ White: {w_min:02d}:{w_sec:02d}  Black: {b_min:02d}:{b_sec:02d}"
        self.timer_label.update()
    
    # =============================================
    # Pause / Reset / Settings / Navigation
    # =============================================
    def toggle_pause(self, e):
        self.paused = not self.paused
        if self.paused:
            self.stop_timer()
            self.pause_btn.text = "▶️ Resume"
            self.pause_btn.bgcolor = self.theme['warning']
            self.turn_indicator.value = "⏸ Paused"
            self.turn_indicator.color = self.theme['warning']
        else:
            self.start_timer()
            self.pause_btn.text = "⏸ Pause"
            self.pause_btn.bgcolor = self.theme['button_bg']
            self.update_status()
        self.page.update()
    
    def reset_game(self, e=None):
        self.stop_timer()
        self.board = chess.Board()
        self.turn = 'w'
        self.selected = None
        self.legal_moves = []
        self.game_over = False
        self.ai_thinking = False
        self.move_history = []
        self.last_move = None
        self.result_recorded = False
        self.paused = False
        self.pause_btn.text = "⏸ Pause"
        self.pause_btn.bgcolor = self.theme['button_bg']
        self.history_list.controls.clear()
        self.error_label.value = ""
        self.check_text.value = ""
        timer_min = self.app.settings.get('timer_minutes', 3)
        self.timer_white = timer_min * 60
        self.timer_black = timer_min * 60
        self.update_timer_display()
        self.update_board()
        self.start_timer()
        if not self.two_player_mode and self.turn == 'b':
            self.page.after(500, self.do_ai_move)
    
    def set_level(self, level):
        self.ai.set_level(level)
        self.level_label.value = f"Level: {level.capitalize()}"
        self.app.settings['ai_level'] = level
        save_settings(self.app.settings)
        self.reset_game()
    
    def toggle_two_player(self, e):
        self.two_player_mode = not self.two_player_mode
        self.mode_label.value = "Mode: 2 Players" if self.two_player_mode else "Mode: vs AI"
        self.reset_game()
    
    def go_to_menu(self):
        self.stop_timer()
        self.app.game_state = self.save_state()
        self.page.go('/')
    
    def go_to_settings(self):
        self.stop_timer()
        self.app.game_state = self.save_state()
        self.page.go('/settings')
    
    def save_state(self):
        return {
            'fen': self.board.fen(),
            'turn': self.turn,
            'move_history': self.move_history.copy(),
            'two_player_mode': self.two_player_mode,
            'ai_level': self.ai.level,
            'game_over': self.game_over,
            'timer_white': self.timer_white,
            'timer_black': self.timer_black,
            'paused': self.paused,
            'last_move': self.last_move,
            'result_recorded': self.result_recorded
        }
    
    def show_error(self, message):
        self.error_label.value = message
        self.error_label.update()
        if self.error_timer:
            self.page.after_cancel(self.error_timer)
        self.error_timer = self.page.after(2000, lambda: setattr(self.error_label, 'value', '') or self.error_label.update())

# =============================================
# Main entry point
# =============================================
def main(page: ft.Page):
    app = ChessApp(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
