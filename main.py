"""
CHESS — Ultimate Chess Client
Version 0.3.0 — Daily Challenges & Enhanced Move History
"""

import sys
import os
import json
import random
import threading
import time
import uuid
import warnings
import webbrowser
import shutil
import socket
import re
from enum import Enum
from typing import Optional, Dict, List, Tuple, Any, Union
from datetime import datetime

import chess
import chess.engine
import pygame

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QListWidget, QFrame, QGroupBox,
    QCheckBox, QMessageBox, QStackedWidget, QProgressBar, QScrollArea,
    QInputDialog, QDialog, QDialogButtonBox, QVBoxLayout as QVBoxLayoutDlg,
    QSizePolicy, QSpacerItem, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QShortcut, QSlider, QGraphicsDropShadowEffect,
    QLineEdit, QButtonGroup, QTabWidget
)
from PyQt5.QtCore import (
    Qt, QTimer, pyqtSignal, QEasingCurve, QPropertyAnimation, QPoint, QRect,
    QSize, QThread, QObject, QEventLoop, pyqtSlot, QMetaObject,
    Q_ARG, QByteArray, pyqtProperty
)
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QPixmap, QImage, QPen, QBrush, QIcon, QPalette,
    QLinearGradient, QRadialGradient, QKeySequence, QPainterPath, QCursor
)
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PIL import Image

warnings.filterwarnings("ignore", category=UserWarning, module="pygame")


# ============================================================================
# CONSTANTS & HELPERS
# ============================================================================
def resource_path(relative_path: str) -> str:
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_appdata_path(filename: str) -> str:
    home = os.path.expanduser("~")
    app_dir = os.path.join(home, ".chess_app")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, filename)


SETTINGS_FILE = get_appdata_path("settings.json")
STATS_FILE = get_appdata_path("stats.json")

DEFAULT_SETTINGS = {
    'ai_level': 'easy',
    'sound': True,
    'timer_minutes': 3,
    'theme': 'dark',
    'ads_removed': False,
    'vip': False,
    'user_id': '',
    'volume': 0.8,
    'piece_set': 'free',
    'flipped': False,
}

# Animation constants
ANIMATION_STEPS = 20
ANIMATION_DELAY = 8


# ============================================================================
# DESIGN SYSTEM
# ============================================================================
class Design:
    COLORS = {
        'dark': {
            'bg': '#0A0A14',
            'bg_secondary': '#111122',
            'surface': '#18182A',
            'surface_hover': '#22223A',
            'surface_active': '#2A2A48',
            'surface_elevated': '#20203A',
            'accent': '#E6C229',
            'accent_light': '#F5D83A',
            'accent_dark': '#C4A020',
            'accent_glow': 'rgba(230,194,41,0.15)',
            'success': '#38D39F',
            'success_glow': 'rgba(56,211,159,0.15)',
            'danger': '#FF5C68',
            'danger_glow': 'rgba(255,92,104,0.15)',
            'warning': '#F5B941',
            'warning_glow': 'rgba(245,185,65,0.15)',
            'text_primary': '#F5F5F7',
            'text_secondary': '#A6A6B8',
            'text_muted': '#707084',
            'board_light': '#F0D9B5',
            'board_dark': '#B58863',
            'board_light_shadow': '#D4BFA0',
            'board_dark_shadow': '#9C7A4A',
            'shadow': '0 16px 60px rgba(0,0,0,0.5)',
            'shadow_small': '0 4px 20px rgba(0,0,0,0.3)',
            'card_border': 'rgba(255,255,255,0.04)',
            'divider': 'rgba(255,255,255,0.06)',
        },
        'light': {
            'bg': '#F5F3EE',
            'bg_secondary': '#E8E4DA',
            'surface': '#F0EDE5',
            'surface_hover': '#E8E4DA',
            'surface_active': '#DDD8CC',
            'surface_elevated': '#F8F5ED',
            'accent': '#B8860B',
            'accent_light': '#D4A017',
            'accent_dark': '#A0730A',
            'accent_glow': 'rgba(184,134,11,0.12)',
            'success': '#27AE60',
            'success_glow': 'rgba(39,174,96,0.12)',
            'danger': '#C0392B',
            'danger_glow': 'rgba(192,57,43,0.12)',
            'warning': '#F39C12',
            'warning_glow': 'rgba(243,156,18,0.12)',
            'text_primary': '#1A1A1A',
            'text_secondary': '#4A4A4A',
            'text_muted': '#888888',
            'board_light': '#F0D9B5',
            'board_dark': '#B58863',
            'board_light_shadow': '#D4BFA0',
            'board_dark_shadow': '#9C7A4A',
            'shadow': '0 16px 60px rgba(0,0,0,0.08)',
            'shadow_small': '0 4px 20px rgba(0,0,0,0.05)',
            'card_border': 'rgba(0,0,0,0.04)',
            'divider': 'rgba(0,0,0,0.06)',
        },
        'classic': {
            'bg': '#2B241C',
            'bg_secondary': '#3D3228',
            'surface': '#4A3D31',
            'surface_hover': '#55483C',
            'surface_active': '#605348',
            'surface_elevated': '#524438',
            'accent': '#D4A373',
            'accent_light': '#E0B88A',
            'accent_dark': '#B8895A',
            'accent_glow': 'rgba(212,163,115,0.15)',
            'success': '#6B8E23',
            'success_glow': 'rgba(107,142,35,0.15)',
            'danger': '#8B3A3A',
            'danger_glow': 'rgba(139,58,58,0.15)',
            'warning': '#D4A373',
            'warning_glow': 'rgba(212,163,115,0.15)',
            'text_primary': '#F5E6D3',
            'text_secondary': '#C4B5A5',
            'text_muted': '#8A7B6B',
            'board_light': '#E8D3AA',
            'board_dark': '#B4875B',
            'board_light_shadow': '#C8B890',
            'board_dark_shadow': '#9C7A4A',
            'shadow': '0 16px 60px rgba(0,0,0,0.4)',
            'shadow_small': '0 4px 20px rgba(0,0,0,0.25)',
            'card_border': 'rgba(255,255,255,0.04)',
            'divider': 'rgba(255,255,255,0.06)',
        }
    }

    SPACING = {'xs': 4, 'sm': 8, 'md': 12, 'lg': 18, 'xl': 24, 'xxl': 32, 'xxxl': 48, 'xxxxl': 64}
    RADIUS = {'xs': 4, 'sm': 8, 'md': 12, 'lg': 16, 'xl': 20, 'xxl': 28, 'full': 9999}
    FONT = {
        'display': 56, 'logo': 48, 'h1': 30, 'h2': 22, 'h3': 18,
        'body': 14, 'small': 12, 'micro': 11, 'clock': 32, 'clock_small': 22,
        'mono': 'Consolas, monospace'
    }
    SHADOW = {'none': (0,0,0,0), 'small': (0,4,12,0.15), 'medium': (0,8,30,0.22),
              'large': (0,16,50,0.30), 'glow': (0,0,40,0.15)}
    ANIM = {'instant':0, 'fast':80, 'normal':180, 'slow':300, 'page':400, 'move':160, 'dialog':220}
    EASING = {'in': QEasingCurve.InCubic, 'out': QEasingCurve.OutCubic,
              'inout': QEasingCurve.InOutCubic, 'outback': QEasingCurve.OutBack}
    BUTTON_HEIGHT = 44
    ICON_SIZE = 20

    @classmethod
    def get_color(cls, theme: str, key: str) -> str:
        return cls.COLORS.get(theme, cls.COLORS['dark']).get(key, '#FFFFFF')

    @classmethod
    def get_font(cls, style: str) -> int:
        return cls.FONT.get(style, 14)


# ============================================================================
# THEMES
# ============================================================================
THEMES = {}
for theme_name, colors in Design.COLORS.items():
    THEMES[theme_name] = {
        'bg': colors['bg'],
        'bg_secondary': colors['bg_secondary'],
        'surface': colors['surface'],
        'surface_hover': colors['surface_hover'],
        'surface_active': colors['surface_active'],
        'surface_elevated': colors['surface_elevated'],
        'accent': colors['accent'],
        'accent_light': colors['accent_light'],
        'accent_dark': colors['accent_dark'],
        'accent_glow': colors['accent_glow'],
        'success': colors['success'],
        'success_glow': colors['success_glow'],
        'danger': colors['danger'],
        'danger_glow': colors['danger_glow'],
        'warning': colors['warning'],
        'warning_glow': colors['warning_glow'],
        'text_primary': colors['text_primary'],
        'text_secondary': colors['text_secondary'],
        'text_muted': colors['text_muted'],
        'board_light': colors['board_light'],
        'board_dark': colors['board_dark'],
        'board_light_shadow': colors['board_light_shadow'],
        'board_dark_shadow': colors['board_dark_shadow'],
        'shadow': colors['shadow'],
        'shadow_small': colors['shadow_small'],
        'card_border': colors['card_border'],
        'divider': colors['divider'],
        'highlight': (230, 194, 41, 65),
        'highlight_move': (230, 194, 41, 35),
        'legal_move': (56, 211, 159, 120),
        'legal_capture': (255, 92, 104, 100),
        'check_glow': colors['danger'],
    }

REQUIRED_THEME_KEYS = list(THEMES['dark'].keys())
for name, theme in THEMES.items():
    missing = set(REQUIRED_THEME_KEYS) - set(theme.keys())
    if missing:
        raise ValueError(f"Theme '{name}' missing keys: {sorted(missing)}")


# ============================================================================
# SETTINGS & STATS I/O
# ============================================================================
def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        if not isinstance(settings, dict):
            raise ValueError("Invalid settings format")
        for key in DEFAULT_SETTINGS:
            settings.setdefault(key, DEFAULT_SETTINGS[key])
        if settings['theme'] not in THEMES:
            settings['theme'] = 'dark'
        if settings['ai_level'] not in ['easy', 'medium', 'hard']:
            settings['ai_level'] = 'easy'
        if not isinstance(settings['timer_minutes'], int) or settings['timer_minutes'] <= 0:
            settings['timer_minutes'] = 3
        if not settings.get('user_id'):
            settings['user_id'] = str(uuid.uuid4())[:8]
        if not isinstance(settings.get('volume'), (int, float)) or settings['volume'] < 0 or settings['volume'] > 1:
            settings['volume'] = 0.8
        if not isinstance(settings.get('flipped'), bool):
            settings['flipped'] = False
        save_settings(settings)
        return settings
    except Exception as e:
        print(f"Settings load error: {e}")
        settings = DEFAULT_SETTINGS.copy()
        settings['user_id'] = str(uuid.uuid4())[:8]
        save_settings(settings)
        return settings


def save_settings(settings: dict) -> bool:
    try:
        temp = SETTINGS_FILE + ".tmp"
        with open(temp, 'w') as f:
            json.dump(settings, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, SETTINGS_FILE)
        return True
    except Exception as e:
        print(f"Settings save error: {e}")
        return False


def load_stats() -> dict:
    try:
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
        if not isinstance(stats, dict):
            raise ValueError("Invalid stats format")
        for key in ['games', 'wins', 'losses', 'draws']:
            stats.setdefault(key, 0)
        if stats['wins'] + stats['losses'] + stats['draws'] > stats['games']:
            stats['games'] = stats['wins'] + stats['losses'] + stats['draws']
        return stats
    except Exception as e:
        print(f"Stats load error: {e}")
        stats = {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0}
        save_stats(stats)
        return stats


def save_stats(stats: dict) -> bool:
    try:
        temp = STATS_FILE + ".tmp"
        with open(temp, 'w') as f:
            json.dump(stats, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, STATS_FILE)
        return True
    except Exception as e:
        print(f"Stats save error: {e}")
        return False


# ============================================================================
# SOUND MANAGER
# ============================================================================
class SoundManager:
    def __init__(self, settings: dict):
        self.sound_enabled = settings.get('sound', True)
        self.volume = settings.get('volume', 0.8)
        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self._init_mixer()

    def _init_mixer(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Sound init failed: {e}")
            self.sound_enabled = False
            return
        self.load_sounds()

    def load_sounds(self):
        base_path = resource_path('sounds')
        sound_names = [
            'click', 'move', 'check', 'checkmate', 'draw', 'error',
            'timeout', 'capture', 'castling', 'promotion'
        ]
        for name in sound_names:
            path = os.path.join(base_path, f'{name}.ogg')
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.volume)
                except Exception as e:
                    print(f"Could not load {name}: {e}")
                    self.sounds[name] = None
            else:
                self.sounds[name] = None

    def play(self, name: str):
        if not self.sound_enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"Error playing {name}: {e}")

    def toggle(self) -> bool:
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
        for s in self.sounds.values():
            if s:
                s.set_volume(self.volume)

    def quit(self):
        try:
            pygame.mixer.quit()
        except:
            pass


# ============================================================================
# UI COMPONENTS
# ============================================================================
class PremiumButton(QPushButton):
    def __init__(self, text: str, parent=None, primary: bool = False, danger: bool = False,
                 icon: Optional[str] = None, subtitle: Optional[str] = None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(Design.BUTTON_HEIGHT)
        self.setFont(QFont('Segoe UI', Design.FONT['body'], QFont.Bold if primary or danger else QFont.Normal))
        if primary:
            self.setProperty('class', 'primary')
        elif danger:
            self.setProperty('class', 'danger')
        else:
            self.setProperty('class', 'secondary')
        self.subtitle = subtitle
        self._setup_style()
        self._shadow_effect = None

    def _setup_style(self):
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        style = f"""
            QPushButton {{
                background-color: {theme['surface'] if self.property('class') not in ('primary', 'danger') else theme['accent'] if self.property('class') == 'primary' else theme['danger']};
                color: {theme['text_primary'] if self.property('class') not in ('primary', 'danger') else '#080812' if self.property('class') == 'primary' else 'white'};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 6px 18px;
                font-weight: 600;
                font-size: {Design.FONT['body']}px;
            }}
            QPushButton:hover {{
                background-color: {theme['surface_hover'] if self.property('class') not in ('primary', 'danger') else theme['accent_light'] if self.property('class') == 'primary' else theme['danger']};
            }}
            QPushButton:pressed {{
                background-color: {theme['surface_active'] if self.property('class') not in ('primary', 'danger') else theme['accent_dark'] if self.property('class') == 'primary' else theme['danger']};
            }}
            QPushButton:disabled {{
                opacity: 0.4;
            }}
        """
        self.setStyleSheet(style)

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.property('class') == 'primary':
            theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(24)
            shadow.setColor(QColor(theme['accent']))
            shadow.setOffset(0, 4)
            self.setGraphicsEffect(shadow)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setGraphicsEffect(None)


class StatusChip(QLabel):
    def __init__(self, text: str, status: str = 'offline', parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setFont(QFont('Segoe UI', Design.FONT['small'], QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(26)
        self.set_status(status)

    def set_status(self, status: str):
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        colors = {
            'offline': (theme['text_muted'], theme['surface']),
            'online': (theme['success'], theme['surface']),
            'waiting': (theme['warning'], theme['surface']),
            'connecting': (theme['warning'], theme['surface']),
            'error': (theme['danger'], theme['surface']),
        }
        if status in colors:
            self.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors[status][1]};
                    color: {colors[status][0]};
                    border: 1px solid {colors[status][0]};
                    border-radius: {Design.RADIUS['full']}px;
                    padding: 0 14px;
                }}
            """)


class AnimatedToggle(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked: bool = False):
        super().__init__(parent)
        self.checked = checked
        self.setFixedSize(48, 26)
        self.setCursor(Qt.PointingHandCursor)
        self._handle_pos = 26 if checked else 3
        self.anim = None
        self._setup_style()

    @pyqtProperty(float)
    def handle_pos(self):
        return self._handle_pos

    @handle_pos.setter
    def handle_pos(self, value):
        self._handle_pos = value
        self.update()

    def _setup_style(self):
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme['surface']};
                border-radius: {Design.RADIUS['full']}px;
            }}
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        bg_color = theme['accent'] if self.checked else theme['text_muted']
        painter.setBrush(QBrush(QColor(bg_color)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 48, 26, 13, 13)

        painter.setBrush(QBrush(QColor(theme['bg'])))
        painter.drawEllipse(int(self._handle_pos), 3, 20, 20)

    def mousePressEvent(self, event):
        self.checked = not self.checked
        target = 26 if self.checked else 3
        self.anim = QPropertyAnimation(self, b"handle_pos")
        self.anim.setDuration(180)
        self.anim.setStartValue(self._handle_pos)
        self.anim.setEndValue(target)
        self.anim.valueChanged.connect(lambda val: self.update())
        self.anim.finished.connect(lambda: self.toggled.emit(self.checked))
        self.anim.start()

    def isChecked(self) -> bool:
        return self.checked

    def setChecked(self, checked: bool):
        if self.checked != checked:
            self.checked = checked
            self._handle_pos = 26 if checked else 3
            self.update()
            self.toggled.emit(checked)


ToggleSwitch = AnimatedToggle


class Toast(QFrame):
    def __init__(self, parent, message: str, duration: int = 2800, type_: str = "info"):
        super().__init__(parent)
        self.type = type_
        self.parent_ref = parent
        self._update_style()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        self.label = QLabel(message)
        layout.addWidget(self.label)
        self.setFixedHeight(46)
        self.hide()
        self.duration = duration
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        self.setWindowOpacity(0)

    def _update_style(self):
        theme = self.parent_ref.theme if hasattr(self.parent_ref, 'theme') else THEMES['dark']
        colors = {
            'success': theme['success'],
            'error': theme['danger'],
            'warning': theme['warning'],
            'info': theme['accent']
        }
        color = colors.get(self.type, theme['text_primary'])
        if hasattr(self, 'label'):
            self.label.setStyleSheet(f"color: {color};")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(24,24,42,0.92);
                border: 1px solid {theme['accent']};
                border-radius: 12px;
                padding: 8px 18px;
            }}
            QLabel {{
                color: {color};
                font-size: 14px;
            }}
        """)

    def show_toast(self):
        parent = self.parent()
        if not parent:
            return
        self.setGeometry(
            (parent.width() - 440) // 2,
            parent.height() - 90,
            440,
            46
        )
        self.show()
        self.timer.start(self.duration)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(Design.ANIM['normal'])
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

    def fade_out(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(Design.ANIM['normal'])
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.finished.connect(self.hide)
        anim.start()


# ============================================================================
# DIALOGS
# ============================================================================
class PremiumDialog(QDialog):
    def __init__(self, parent, title: str, message: str, action: str = "close", callback=None):
        super().__init__(parent)
        self.parent_ref = parent
        self.callback = callback
        self.setWindowTitle("")
        self.setModal(True)
        self.setFixedSize(460, 320)
        theme = parent.theme if parent else THEMES['dark']
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['bg_secondary']};
                border: 1px solid {theme['accent']};
                border-radius: {Design.RADIUS['xl']}px;
            }}
            QLabel {{
                color: {theme['text_primary']};
            }}
            QPushButton {{
                background-color: {theme['surface']};
                color: {theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 10px 26px;
                font-weight: 600;
                font-size: {Design.FONT['body']}px;
            }}
            QPushButton:hover {{
                background-color: {theme['surface_hover']};
            }}
            QPushButton#primary {{
                background-color: {theme['accent']};
                color: #080812;
            }}
            QPushButton#primary:hover {{
                background-color: {theme['accent_light']};
            }}
            QPushButton#danger {{
                background-color: {theme['danger']};
                color: white;
            }}
            QPushButton#danger:hover {{
                background-color: #FF7A85;
            }}
        """)
        layout = QVBoxLayoutDlg(self)
        layout.setSpacing(Design.SPACING['md'])
        layout.setContentsMargins(Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'])

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title_label.setStyleSheet(f"color: {theme['accent']};")
        layout.addWidget(title_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet(f"color: {theme['text_secondary']}; font-size: 15px;")
        layout.addWidget(msg_label)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Design.SPACING['md'])
        if action == "new_game":
            new_btn = QPushButton("New Game")
            new_btn.setObjectName("primary")
            new_btn.clicked.connect(lambda: (self.accept(), parent.reset_board()))
            btn_layout.addWidget(new_btn)
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.reject)
            btn_layout.addWidget(close_btn)
        elif action == "resign":
            confirm_btn = QPushButton("Resign")
            confirm_btn.setObjectName("danger")
            confirm_btn.clicked.connect(lambda: (self.accept(), parent.resign_game()))
            btn_layout.addWidget(confirm_btn)
            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(cancel_btn)
        elif action == "draw":
            confirm_btn = QPushButton("Offer Draw")
            confirm_btn.setObjectName("primary")
            confirm_btn.clicked.connect(lambda: (self.accept(), parent.offer_draw()))
            btn_layout.addWidget(confirm_btn)
            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(cancel_btn)
        else:
            close_btn = QPushButton("OK")
            close_btn.setObjectName("primary")
            close_btn.clicked.connect(self.accept)
            btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)
        self.exec_()


class PromotionDialog(QDialog):
    def __init__(self, parent=None, color=chess.WHITE):
        super().__init__(parent)
        self.setWindowTitle("")
        self.setModal(True)
        self.selected = None
        self.setFixedSize(420, 280)
        theme = parent.theme if parent else THEMES['dark']
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['bg_secondary']};
                border: 1px solid {theme['accent']};
                border-radius: {Design.RADIUS['xl']}px;
            }}
            QLabel {{
                color: {theme['text_primary']};
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {theme['surface']};
                color: {theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 8px;
                min-width: 76px;
                min-height: 76px;
            }}
            QPushButton:hover {{
                background-color: {theme['surface_hover']};
                border: 2px solid {theme['accent']};
            }}
        """)
        layout = QVBoxLayoutDlg(self)
        layout.setSpacing(Design.SPACING['md'])
        title = QLabel("PROMOTION")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title.setStyleSheet(f"color: {theme['accent']};")
        layout.addWidget(title)

        sub = QLabel("Choose your piece")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet(f"color: {theme['text_muted']}; font-size: 14px;")
        layout.addWidget(sub)

        board_widget = parent.board_widget if parent and hasattr(parent, 'board_widget') else None

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Design.SPACING['md'])

        piece_types = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        piece_names = {chess.QUEEN:'queen', chess.ROOK:'rook', chess.BISHOP:'bishop', chess.KNIGHT:'knight'}

        for pt in piece_types:
            btn = QPushButton()
            btn.setFixedSize(78, 78)
            if board_widget:
                temp_piece = chess.Piece(pt, color)
                pixmap = board_widget.get_piece_pixmap(temp_piece)
                if pixmap:
                    icon = QIcon(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    btn.setIcon(icon)
                    btn.setIconSize(QSize(64, 64))
                else:
                    symbol = {chess.QUEEN: '♛', chess.ROOK: '♜', chess.BISHOP: '♝', chess.KNIGHT: '♞'}[pt]
                    btn.setText(symbol)
            else:
                btn.setText(piece_names[pt][0].upper())
            btn.clicked.connect(lambda checked, p=pt: self.select_piece(p))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def select_piece(self, piece_type: int):
        self.selected = piece_type
        self.accept()


class LANDialog(QDialog):
    def __init__(self, parent, mode: str = 'join'):
        super().__init__(parent)
        self.setWindowTitle("")
        self.setModal(True)
        self.mode = mode
        self.ip = ""
        self.setFixedSize(420, 280)
        theme = parent.theme if parent else THEMES['dark']
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['bg_secondary']};
                border: 1px solid {theme['accent']};
                border-radius: {Design.RADIUS['xl']}px;
            }}
            QLabel {{
                color: {theme['text_primary']};
            }}
            QLineEdit {{
                background-color: {theme['surface']};
                color: {theme['text_primary']};
                border: 1px solid {theme['card_border']};
                border-radius: {Design.RADIUS['md']}px;
                padding: 8px 14px;
                font-size: {Design.FONT['body']}px;
            }}
            QLineEdit:focus {{
                border: 1px solid {theme['accent']};
            }}
            QPushButton {{
                background-color: {theme['surface']};
                color: {theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: {Design.FONT['body']}px;
            }}
            QPushButton:hover {{
                background-color: {theme['surface_hover']};
            }}
            QPushButton#primary {{
                background-color: {theme['accent']};
                color: #080812;
            }}
            QPushButton#primary:hover {{
                background-color: {theme['accent_light']};
            }}
        """)
        layout = QVBoxLayoutDlg(self)
        layout.setSpacing(Design.SPACING['lg'])
        layout.setContentsMargins(Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'])

        title = QLabel("JOIN GAME" if mode == 'join' else "HOST GAME")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title.setStyleSheet(f"color: {theme['accent']};")
        layout.addWidget(title)

        if mode == 'join':
            ip_layout = QVBoxLayout()
            ip_label = QLabel("Host IP Address")
            ip_label.setStyleSheet(f"color: {theme['text_secondary']};")
            ip_layout.addWidget(ip_label)
            self.ip_input = QLineEdit()
            self.ip_input.setPlaceholderText("192.168.1.10")
            ip_layout.addWidget(self.ip_input)
            layout.addLayout(ip_layout)

            btn_layout = QHBoxLayout()
            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(cancel_btn)
            connect_btn = QPushButton("Connect")
            connect_btn.setObjectName("primary")
            connect_btn.clicked.connect(self.accept_join)
            btn_layout.addWidget(connect_btn)
            layout.addLayout(btn_layout)
        else:
            info = QLabel("Server will start on port 5000")
            info.setAlignment(Qt.AlignCenter)
            info.setStyleSheet(f"color: {theme['text_secondary']};")
            layout.addWidget(info)

            btn_layout = QHBoxLayout()
            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(cancel_btn)
            host_btn = QPushButton("Host")
            host_btn.setObjectName("primary")
            host_btn.clicked.connect(self.accept)
            btn_layout.addWidget(host_btn)
            layout.addLayout(btn_layout)

    def accept_join(self):
        ip = self.ip_input.text().strip()
        if ip:
            self.ip = ip
            self.accept()


# ============================================================================
# CHESS AI
# ============================================================================
class ChessAI:
    def __init__(self, level: str = 'easy', engine=None):
        self.engine = engine
        self.engine_lock = threading.RLock()
        self.set_level(level)
        if self.engine is None:
            self._init_engine()

    def _init_engine(self):
        try:
            possible_paths = [
                resource_path("stockfish.exe"),
                "/usr/games/stockfish",
                "/usr/bin/stockfish",
                shutil.which("stockfish")
            ]
            for path in possible_paths:
                if path and os.path.exists(path):
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    break
        except Exception as e:
            print(f"Stockfish init failed: {e}")
            self.engine = None

    def close_engine(self):
        if self.engine:
            with self.engine_lock:
                try:
                    self.engine.quit()
                except:
                    pass
                self.engine = None

    def set_level(self, level: str):
        self.level = level
        if level == 'easy':
            self.depth = 2
            self.mistake_chance = 0.4
            self.time_limit = 0.5
        elif level == 'medium':
            self.depth = 4
            self.mistake_chance = 0.15
            self.time_limit = 1.5
        elif level == 'hard':
            self.depth = 6
            self.mistake_chance = 0.0
            self.time_limit = 3.0
        else:
            self.depth = 2
            self.mistake_chance = 0.4
            self.time_limit = 0.5

    def get_best_move(self, board):
        move = None
        if self.engine:
            with self.engine_lock:
                try:
                    result = self.engine.play(board, chess.engine.Limit(time=self.time_limit, depth=self.depth))
                    move = result.move
                except Exception as e:
                    print(f"Engine error: {e}")
                    move = self._minimax_move(board)
        else:
            move = self._minimax_move(board)
        if move is None:
            legal = list(board.legal_moves)
            if legal:
                move = random.choice(legal)
        if move and self.mistake_chance > 0 and random.random() < self.mistake_chance:
            moves = list(board.legal_moves)
            if moves:
                return random.choice(moves[-5:]) if len(moves) > 5 else random.choice(moves)
        return move

    def _minimax_move(self, board):
        _, move = self._minimax(board, self.depth, -float('inf'), float('inf'), board.turn == chess.WHITE)
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
                board.push(move)
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, False)
                board.pop()
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
                board.push(move)
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, True)
                board.pop()
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
        values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900,
                  chess.KING: 20000}
        for pt in values:
            score += len(board.pieces(pt, chess.WHITE)) * values[pt]
            score -= len(board.pieces(pt, chess.BLACK)) * values[pt]
        return score


# ============================================================================
# AI WORKER (QThread)
# ============================================================================
class AIWorker(QObject):
    finished = pyqtSignal(object, int)  # (move, generation)

    def __init__(self, board_fen: str, level: str, engine, generation: int):
        super().__init__()
        self.board_fen = board_fen
        self.level = level
        self.engine = engine
        self.generation = generation

    @pyqtSlot()
    def run(self):
        try:
            board = chess.Board(self.board_fen)
            ai = ChessAI(self.level, self.engine)
            move = ai.get_best_move(board)
            self.finished.emit(move, self.generation)
        except Exception as e:
            print(f"AI worker error: {e}")
            self.finished.emit(None, self.generation)


# ============================================================================
# CHESS BOARD WIDGET
# ============================================================================
class ChessBoardWidget(QWidget):
    move_made = pyqtSignal(object)
    animation_finished = pyqtSignal()

    BASE_TO_KEY = {
        'bb': ('black', 'bishop'),
        'bk': ('black', 'king'),
        'bn': ('black', 'knight'),
        'bp': ('black', 'pawn'),
        'bq': ('black', 'queen'),
        'br': ('black', 'rook'),
        'wb': ('white', 'bishop'),
        'wk': ('white', 'king'),
        'wn': ('white', 'knight'),
        'wp': ('white', 'pawn'),
        'wq': ('white', 'queen'),
        'wr': ('white', 'rook'),
        'black_bishop': ('black', 'bishop'),
        'black_king': ('black', 'king'),
        'black_knight': ('black', 'knight'),
        'black_pawn': ('black', 'pawn'),
        'black_queen': ('black', 'queen'),
        'black_rook': ('black', 'rook'),
        'white_bishop': ('white', 'bishop'),
        'white_king': ('white', 'king'),
        'white_knight': ('white', 'knight'),
        'white_pawn': ('white', 'pawn'),
        'white_queen': ('white', 'queen'),
        'white_rook': ('white', 'rook'),
    }

    @staticmethod
    def discover_sets():
        base_dir = resource_path('assets')
        sets = {}
        order = []
        free_dir = os.path.join(base_dir, 'free', 'classic')
        if os.path.exists(free_dir) and ChessBoardWidget._is_valid_set(free_dir):
            sets['free'] = free_dir
            order.append('free')
        premium_dir = os.path.join(base_dir, 'premium')
        if os.path.exists(premium_dir):
            for item in sorted(os.listdir(premium_dir)):
                sub_path = os.path.join(premium_dir, item)
                if os.path.isdir(sub_path) and ChessBoardWidget._is_valid_set(sub_path):
                    set_id = str(len(sets))
                    sets[set_id] = sub_path
                    order.append(set_id)
        if 'free' not in sets:
            alt_free = os.path.join(base_dir, 'pieces')
            if os.path.exists(alt_free) and ChessBoardWidget._is_valid_set(alt_free):
                sets['free'] = alt_free
                order.insert(0, 'free')
        return sets, order

    @staticmethod
    def _is_valid_set(folder):
        pattern = re.compile(
            r'^([a-zA-Z_]+?)(?:\s*\(\d+\))?\.png$|^([wb])([krnbpq])(\d+)\.png$',
            re.IGNORECASE
        )
        found = set()
        for f in os.listdir(folder):
            m = pattern.match(f)
            if m:
                if m.group(1):
                    base = m.group(1)
                else:
                    base = m.group(2) + m.group(3)
                if base in ChessBoardWidget.BASE_TO_KEY:
                    found.add(base)
        required = {'bb','bk','bn','bp','bq','br','wb','wk','wn','wp','wq','wr'}
        # Require ALL 12 pieces
        return required.issubset(found)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.last_move = None
        self.flipped = False
        self.turn = chess.WHITE

        self.piece_pixmaps = {}
        self.available_sets = {}
        self.set_order = []

        self._scaled_cache = {}
        self._max_cache = 100
        self._bg_cache = None
        self._bg_cache_cell = 0
        self._bg_cache_flipped = False

        self.animating = False
        self.anim_king_from = None
        self.anim_king_to = None
        self.anim_king_piece = None
        self.anim_rook_from = None
        self.anim_rook_to = None
        self.anim_rook_piece = None
        self.anim_progress = 0
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._animate_step)

        self.dragging_square = None
        self.drag_start_pos = None
        self.drag_current_pos = None
        self.drag_piece = None
        self.is_dragging = False
        self.click_selection = None
        self.hover_square = None

        self._theme = None
        self._themed_cursor = None

        self.load_piece_set('free')
        self._preload_background()
        self._update_cursor_theme()

    def _get_scaled_pixmap(self, piece, cell):
        if not piece:
            return None
        color = 'white' if piece.color == chess.WHITE else 'black'
        piece_names = {
            chess.KING: 'king', chess.QUEEN: 'queen', chess.ROOK: 'rook',
            chess.BISHOP: 'bishop', chess.KNIGHT: 'knight', chess.PAWN: 'pawn'
        }
        key = f"{color}_{piece_names.get(piece.piece_type, '')}"
        cache_key = (key, cell)
        if cache_key in self._scaled_cache:
            return self._scaled_cache[cache_key]
        raw = self.piece_pixmaps.get(key)
        if raw:
            psize = min(cell - 8, raw.width(), raw.height())
            scaled = raw.scaled(psize, psize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if len(self._scaled_cache) >= self._max_cache:
                self._scaled_cache.pop(next(iter(self._scaled_cache)))
            self._scaled_cache[cache_key] = scaled
            return scaled
        return None

    def _build_themed_cursor(self, theme, size=22):
        pm = QPixmap(size, size)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(theme['accent']))
        p.setPen(QPen(QColor(theme['bg']), 1.5))
        p.drawEllipse(2, 2, size - 4, size - 4)
        p.end()
        return QCursor(pm, size // 2, size // 2)

    def _update_cursor_theme(self):
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        self._theme = theme
        self._themed_cursor = self._build_themed_cursor(theme)

    def _cursor_for_square(self, row_col):
        if row_col is None:
            return self._themed_cursor
        row, col = row_col
        sq = self._to_square(row, col)
        piece = self.board.piece_at(sq)
        if piece and piece.color == self.board.turn:
            return QCursor(Qt.OpenHandCursor)
        return self._themed_cursor

    def load_piece_set(self, set_id):
        self.available_sets, self.set_order = self.discover_sets()
        if set_id not in self.available_sets:
            set_id = 'free' if 'free' in self.available_sets else (self.set_order[0] if self.set_order else None)
            if set_id is None:
                self.piece_pixmaps = {}
                self._clear_cache()
                return
        folder = self.available_sets[set_id]
        self.piece_pixmaps = {}
        pattern = re.compile(
            r'^([a-zA-Z_]+?)(?:\s*\(\d+\))?\.png$|^([wb])([krnbpq])(\d+)\.png$',
            re.IGNORECASE
        )
        for filename in os.listdir(folder):
            if not filename.lower().endswith('.png'):
                continue
            m = pattern.match(filename)
            if not m:
                continue
            if m.group(1):
                base = m.group(1)
            else:
                base = m.group(2) + m.group(3)
            if base not in self.BASE_TO_KEY:
                continue
            color_name, piece_name = self.BASE_TO_KEY[base]
            standard_key = f"{color_name}_{piece_name}"
            try:
                img = Image.open(os.path.join(folder, filename))
                img = img.convert("RGBA")
                data = img.tobytes("raw", "RGBA")
                qimage = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)
                self.piece_pixmaps[standard_key] = pixmap
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        self._clear_cache()
        self.update()

    def _clear_cache(self):
        self._scaled_cache.clear()
        self._bg_cache = None
        self._bg_cache_cell = 0

    def _preload_background(self):
        self._bg_cache = None
        self._bg_cache_cell = 0
        self._bg_cache_flipped = self.flipped

    def get_piece_pixmap(self, piece):
        if not piece:
            return None
        color = 'white' if piece.color == chess.WHITE else 'black'
        piece_names = {
            chess.KING: 'king', chess.QUEEN: 'queen', chess.ROOK: 'rook',
            chess.BISHOP: 'bishop', chess.KNIGHT: 'knight', chess.PAWN: 'pawn'
        }
        key = f"{color}_{piece_names.get(piece.piece_type, '')}"
        return self.piece_pixmaps.get(key)

    def set_flipped(self, flipped):
        if self.flipped != flipped:
            self.flipped = flipped
            self._preload_background()
            self.update()

    def toggle_flipped(self):
        self.set_flipped(not self.flipped)

    def _screen_pos(self, square):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if self.flipped:
            return rank, 7 - file
        return 7 - rank, file

    def _to_square(self, row, col):
        if self.flipped:
            return chess.square(7 - col, row)
        return chess.square(col, 7 - row)

    def set_board(self, board):
        self.board = board
        self.selected_square = None
        self.legal_moves = []
        self.click_selection = None
        self.update()

    def set_selected(self, square):
        self.selected_square = square
        self.legal_moves = self._get_legal_moves(square) if square is not None else []
        self.update()

    def set_legal_moves(self, moves):
        self.legal_moves = moves
        self.update()

    def set_last_move(self, move):
        self.last_move = move
        self.update()

    def set_turn(self, turn):
        self.turn = turn

    def animate_move(self, king_from, king_to, king_piece, rook_from=None, rook_to=None, rook_piece=None):
        self.cancel_animation()
        self.animating = True
        self.anim_king_from = king_from
        self.anim_king_to = king_to
        self.anim_king_piece = king_piece
        self.anim_rook_from = rook_from
        self.anim_rook_to = rook_to
        self.anim_rook_piece = rook_piece
        self.anim_progress = 0
        self.anim_timer.start(ANIMATION_DELAY)

    def _animate_step(self):
        self.anim_progress += 1
        if self.anim_progress >= ANIMATION_STEPS:
            self.anim_timer.stop()
            self.animating = False
            self.anim_king_from = None
            self.anim_king_to = None
            self.anim_king_piece = None
            self.anim_rook_from = None
            self.anim_rook_to = None
            self.anim_rook_piece = None
            self.update()
            self.animation_finished.emit()
        else:
            self.update()

    def cancel_animation(self):
        self.anim_timer.stop()
        self.animating = False
        self.anim_king_from = None
        self.anim_king_to = None
        self.anim_king_piece = None
        self.anim_rook_from = None
        self.anim_rook_to = None
        self.anim_rook_piece = None
        self.update()

    def _get_legal_moves(self, square):
        moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                r, c = self._screen_pos(move.to_square)
                moves.append((r, c))
        return moves

    def _pos_to_square(self, x, y):
        w = self.width()
        h = self.height()
        size = min(w, h) - 16
        margin = size // 16
        cell = (size - 2 * margin) // 8
        total = cell * 8
        ox = (w - total) // 2
        oy = (h - total) // 2
        if x < ox or x >= ox + total or y < oy or y >= oy + total:
            return None
        col = (x - ox) // cell
        row = (y - oy) // cell
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None

    def mousePressEvent(self, event):
        if self.animating:
            return
        if event.button() == Qt.LeftButton:
            pos = self._pos_to_square(event.x(), event.y())
            if pos is None:
                return
            row, col = pos
            sq = self._to_square(row, col)
            piece = self.board.piece_at(sq)

            if piece and piece.color == self.board.turn:
                self.dragging_square = sq
                self.drag_start_pos = event.pos()
                self.drag_piece = piece
                self.is_dragging = True
                self.setCursor(Qt.ClosedHandCursor)

                self.selected_square = sq
                self.legal_moves = self._get_legal_moves(sq)
                self.click_selection = sq
                self.update()
            else:
                if self.selected_square is not None:
                    from_sq = self.selected_square
                    to_sq = sq
                    move = None
                    for m in self.board.legal_moves:
                        if m.from_square == from_sq and m.to_square == to_sq:
                            move = m
                            break
                    if move:
                        piece = self.board.piece_at(from_sq)
                        if piece and piece.piece_type == chess.PAWN and chess.square_rank(to_sq) in (0, 7):
                            dlg = PromotionDialog(self.parent(), piece.color)
                            if dlg.exec_() == QDialog.Accepted and dlg.selected:
                                move = chess.Move(from_sq, to_sq, promotion=dlg.selected)
                            else:
                                self.selected_square = None
                                self.legal_moves = []
                                self.update()
                                return
                        self.move_made.emit(move)
                        self.selected_square = None
                        self.legal_moves = []
                        self.update()
                        return
                    else:
                        self.selected_square = None
                        self.legal_moves = []
                        self.update()
                else:
                    if hasattr(self.parent(), 'sound_manager'):
                        self.parent().sound_manager.play('error')
        elif event.button() == Qt.RightButton:
            self.selected_square = None
            self.legal_moves = []
            self.click_selection = None
            self.update()

    def mouseMoveEvent(self, event):
        pos = self._pos_to_square(event.x(), event.y())
        new_hover = pos if pos else None

        if new_hover != self.hover_square:
            self.hover_square = new_hover
            if self.is_dragging:
                self.setCursor(Qt.ClosedHandCursor)
            else:
                self.setCursor(self._cursor_for_square(new_hover))
            self.update()

        if self.is_dragging:
            self.drag_current_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_dragging:
            moved = (event.pos() - self.drag_start_pos).manhattanLength()
            if moved < 6:
                self.is_dragging = False
                self.dragging_square = None
                self.drag_piece = None
                self.drag_current_pos = None
                self.setCursor(self._cursor_for_square(self.hover_square))
                self.update()
                return

            pos = self._pos_to_square(event.x(), event.y())
            if pos:
                row, col = pos
                to_sq = self._to_square(row, col)
                from_sq = self.dragging_square
                if from_sq is not None:
                    move = None
                    for m in self.board.legal_moves:
                        if m.from_square == from_sq and m.to_square == to_sq:
                            move = m
                            break
                    if move:
                        piece = self.board.piece_at(from_sq)
                        if piece and piece.piece_type == chess.PAWN and chess.square_rank(to_sq) in (0, 7):
                            dlg = PromotionDialog(self.parent(), piece.color)
                            if dlg.exec_() == QDialog.Accepted and dlg.selected:
                                move = chess.Move(from_sq, to_sq, promotion=dlg.selected)
                            else:
                                self.is_dragging = False
                                self.dragging_square = None
                                self.drag_piece = None
                                self.drag_current_pos = None
                                self.setCursor(Qt.ArrowCursor)
                                self.selected_square = None
                                self.legal_moves = []
                                self.update()
                                return
                        self.move_made.emit(move)
                        self.selected_square = None
                        self.legal_moves = []
                    else:
                        self.selected_square = None
                        self.legal_moves = []
                else:
                    self.selected_square = None
                    self.legal_moves = []
            else:
                self.selected_square = None
                self.legal_moves = []

            self.is_dragging = False
            self.dragging_square = None
            self.drag_piece = None
            self.drag_current_pos = None
            self.setCursor(Qt.ArrowCursor)
            self.update()

    def leaveEvent(self, event):
        if not self.is_dragging:
            self.hover_square = None
            self.setCursor(self._themed_cursor)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        size = min(w, h) - 16
        margin = size // 16
        cell = (size - 2 * margin) // 8
        total = cell * 8
        ox = (w - total) // 2
        oy = (h - total) // 2

        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']

        painter.setBrush(QColor(0, 0, 0, 40))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(ox - 4, oy - 4, total + 8, total + 8, Design.RADIUS['lg'], Design.RADIUS['lg'])

        painter.setBrush(QColor(theme['surface']))
        painter.drawRoundedRect(ox - 2, oy - 2, total + 4, total + 4, Design.RADIUS['lg'], Design.RADIUS['lg'])

        bg = self._get_bg_cache(cell)
        if bg:
            painter.drawPixmap(ox, oy, bg)
        else:
            for r in range(8):
                for c in range(8):
                    is_light = (r + c) % 2 == 0
                    base = QColor(theme['board_light']) if is_light else QColor(theme['board_dark'])
                    grad = QLinearGradient(ox + c*cell, oy + r*cell, ox + (c+1)*cell, oy + (r+1)*cell)
                    grad.setColorAt(0, base)
                    grad.setColorAt(1, base.lighter(108) if is_light else base.darker(108))
                    painter.fillRect(ox + c*cell, oy + r*cell, cell, cell, grad)

        if self.hover_square is not None and not self.is_dragging:
            r, c = self.hover_square
            painter.setBrush(QColor(255, 255, 255, 30))
            painter.setPen(Qt.NoPen)
            painter.fillRect(ox + c*cell, oy + r*cell, cell, cell, QColor(255, 255, 255, 30))

        for (tr, tc) in self.legal_moves:
            x = ox + tc*cell + cell//2
            y = oy + tr*cell + cell//2
            sq = self._to_square(tr, tc)
            if self.board.piece_at(sq):
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor(*theme['legal_capture']), 2.5))
                painter.drawEllipse(x - 15, y - 15, 30, 30)
            else:
                painter.setBrush(QBrush(QColor(*theme['legal_move']), Qt.SolidPattern))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(x - 6, y - 6, 12, 12)

        if self.last_move:
            for sq in self.last_move:
                r, c = self._screen_pos(sq)
                painter.fillRect(ox + c*cell, oy + r*cell, cell, cell, QColor(*theme['highlight_move']))

        if self.selected_square is not None:
            r, c = self._screen_pos(self.selected_square)
            painter.fillRect(ox + c*cell, oy + r*cell, cell, cell, QColor(*theme['highlight']))
            painter.setPen(QPen(QColor(theme['accent']), 2.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(ox + c*cell + 2, oy + r*cell + 2, cell - 4, cell - 4)
            grad = QRadialGradient(ox + c*cell + cell/2, oy + r*cell + cell/2, cell/2)
            grad.setColorAt(0, QColor(230,194,41,40))
            grad.setColorAt(1, QColor(230,194,41,0))
            painter.setBrush(grad)
            painter.setPen(Qt.NoPen)
            painter.drawRect(ox + c*cell + 2, oy + r*cell + 2, cell - 4, cell - 4)

        if self.board.is_check():
            king_color = self.board.turn
            king_square = self.board.king(king_color)
            if king_square is not None:
                r, c = self._screen_pos(king_square)
                grad = QRadialGradient(ox + c*cell + cell/2, oy + r*cell + cell/2, cell*1.2)
                grad.setColorAt(0, QColor(255,92,104,80))
                grad.setColorAt(1, QColor(255,92,104,0))
                painter.setBrush(grad)
                painter.setPen(Qt.NoPen)
                painter.drawRect(ox + c*cell, oy + r*cell, cell, cell)
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor(theme['check_glow']), 3))
                painter.drawRect(ox + c*cell + 2, oy + r*cell + 2, cell - 4, cell - 4)
                pulse = (abs((time.time() * 2) % 2 - 1)) * 0.4 + 0.1
                painter.setPen(QPen(QColor(255,92,104,int(pulse*200)), 2))
                painter.drawRect(ox + c*cell + 4, oy + r*cell + 4, cell - 8, cell - 8)

        if self.animating:
            self._draw_animated_pieces(painter, ox, oy, cell)
        else:
            self._draw_static_pieces(painter, ox, oy, cell)

        if self.is_dragging and self.drag_piece and self.drag_current_pos is not None:
            x = self.drag_current_pos.x() - cell//2
            y = self.drag_current_pos.y() - cell//2
            pixmap = self._get_scaled_pixmap(self.drag_piece, cell)
            if pixmap:
                painter.setOpacity(0.85)
                painter.drawPixmap(x, y, pixmap)
                painter.setOpacity(1.0)

        if self.is_dragging and self.hover_square:
            r, c = self.hover_square
            to_sq = self._to_square(r, c)
            if self.dragging_square is not None:
                valid = any(m.from_square == self.dragging_square and m.to_square == to_sq for m in self.board.legal_moves)
                if valid:
                    painter.setPen(QPen(QColor(theme['success']), 3))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawRoundedRect(ox + c*cell + 3, oy + r*cell + 3, cell - 6, cell - 6, 6, 6)

        painter.setPen(QColor(theme['text_muted']))
        font = painter.font()
        font.setPointSize(max(10, int(cell * 0.2)))
        painter.setFont(font)
        for i in range(8):
            if self.flipped:
                rank_label = str(i + 1)
                file_label = chr(ord('h') - i)
            else:
                rank_label = str(8 - i)
                file_label = chr(ord('a') + i)
            painter.drawText(ox - 20, oy + i*cell + cell//2 + 5, rank_label)
            painter.drawText(ox + i*cell + cell//2 - 6, oy + total + 24, file_label)

    def _get_bg_cache(self, cell):
        if self._bg_cache is not None and self._bg_cache_cell == cell and self._bg_cache_flipped == self.flipped:
            return self._bg_cache
        theme = self.parent().theme if hasattr(self.parent(), 'theme') else THEMES['dark']
        pix = QPixmap(8*cell, 8*cell)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        for r in range(8):
            for c in range(8):
                dr = r if not self.flipped else 7 - r
                dc = c if not self.flipped else 7 - c
                is_light = (dr + dc) % 2 == 0
                base = QColor(theme['board_light']) if is_light else QColor(theme['board_dark'])
                grad = QLinearGradient(c*cell, r*cell, (c+1)*cell, (r+1)*cell)
                grad.setColorAt(0, base)
                grad.setColorAt(1, base.lighter(108) if is_light else base.darker(108))
                p.fillRect(c*cell, r*cell, cell, cell, grad)
        p.end()
        self._bg_cache = pix
        self._bg_cache_cell = cell
        self._bg_cache_flipped = self.flipped
        return self._bg_cache

    def _draw_piece_shadow(self, painter, row, col, ox, oy, cell):
        shadow_w = int(cell * 0.55)
        shadow_h = int(cell * 0.18)
        cx = ox + col * cell + cell // 2
        cy = oy + row * cell + int(cell * 0.82)
        grad = QRadialGradient(cx, cy, shadow_w / 2)
        grad.setColorAt(0, QColor(0, 0, 0, 70))
        grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(grad)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - shadow_w//2, cy - shadow_h//2, shadow_w, shadow_h)

    def _draw_piece_at(self, painter, piece, row, col, ox, oy, cell, opacity=1.0):
        self._draw_piece_shadow(painter, row, col, ox, oy, cell)
        pixmap = self._get_scaled_pixmap(piece, cell)
        if pixmap:
            if opacity < 1.0:
                painter.setOpacity(opacity)
            x = int(ox + col*cell + (cell - pixmap.width())//2)
            y = int(oy + row*cell + (cell - pixmap.height())//2)
            painter.drawPixmap(x, y, pixmap)
            painter.setOpacity(1.0)
        else:
            unicode_map = {
                (chess.WHITE, chess.KING): '♔', (chess.WHITE, chess.QUEEN): '♕',
                (chess.WHITE, chess.ROOK): '♖', (chess.WHITE, chess.BISHOP): '♗',
                (chess.WHITE, chess.KNIGHT): '♘', (chess.WHITE, chess.PAWN): '♙',
                (chess.BLACK, chess.KING): '♚', (chess.BLACK, chess.QUEEN): '♛',
                (chess.BLACK, chess.ROOK): '♜', (chess.BLACK, chess.BISHOP): '♝',
                (chess.BLACK, chess.KNIGHT): '♞', (chess.BLACK, chess.PAWN): '♟',
            }
            symbol = unicode_map.get((piece.color, piece.piece_type), '?')
            font = QFont()
            font.setFamilies(['Segoe UI Symbol', 'DejaVu Sans', 'Noto Sans Symbols', 'Arial Unicode MS', 'Segoe UI'])
            font.setPointSize(int(cell * 0.6))
            painter.setFont(font)
            painter.setPen(QColor('black' if piece.color == chess.BLACK else 'white'))
            painter.drawText(int(ox + col*cell), int(oy + (row+1)*cell), symbol)

    def _draw_static_pieces(self, painter, ox, oy, cell):
        for r in range(8):
            for c in range(8):
                sq = self._to_square(r, c)
                piece = self.board.piece_at(sq)
                if piece:
                    self._draw_piece_at(painter, piece, r, c, ox, oy, cell)

    def _draw_animated_pieces(self, painter, ox, oy, cell):
        for r in range(8):
            for c in range(8):
                sq = self._to_square(r, c)
                if (self.anim_king_from is not None and sq == self.anim_king_from) or \
                   (self.anim_king_to is not None and sq == self.anim_king_to) or \
                   (self.anim_rook_from is not None and sq == self.anim_rook_from) or \
                   (self.anim_rook_to is not None and sq == self.anim_rook_to):
                    continue
                piece = self.board.piece_at(sq)
                if piece:
                    self._draw_piece_at(painter, piece, r, c, ox, oy, cell)

        if self.anim_king_from is not None and self.anim_king_to is not None and self.anim_king_piece:
            fr, fc = self._screen_pos(self.anim_king_from)
            tr, tc = self._screen_pos(self.anim_king_to)
            t = self.anim_progress / ANIMATION_STEPS
            t_eased = 1 - pow(1 - t, 3)
            cur_r = fr + (tr - fr) * t_eased
            cur_c = fc + (tc - fc) * t_eased
            self._draw_piece_at(painter, self.anim_king_piece, cur_r, cur_c, ox, oy, cell)

        if self.anim_rook_from is not None and self.anim_rook_to is not None and self.anim_rook_piece:
            fr, fc = self._screen_pos(self.anim_rook_from)
            tr, tc = self._screen_pos(self.anim_rook_to)
            t = self.anim_progress / ANIMATION_STEPS
            t_eased = 1 - pow(1 - t, 3)
            cur_r = fr + (tr - fr) * t_eased
            cur_c = fc + (tc - fc) * t_eased
            self._draw_piece_at(painter, self.anim_rook_piece, cur_r, cur_c, ox, oy, cell)

    def sizeHint(self):
        return QSize(460, 460)

    def minimumSizeHint(self):
        return QSize(340, 340)


# ============================================================================
# LAN NETWORK
# ============================================================================
class ChessServer(QTcpServer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = None
        self.buffer = ""
        self._disconnecting = False
        self.newConnection.connect(self._on_new_connection)

    def start_server(self, port=5000):
        if not self.listen(QHostAddress.Any, port):
            return False
        return True

    def _on_new_connection(self):
        if self._disconnecting:
            return
        if self.client:
            self.client.close()
        self.client = self.nextPendingConnection()
        self.buffer = ""
        self.client.readyRead.connect(self._on_ready_read)
        self.client.disconnected.connect(self._on_disconnect)
        self.client.errorOccurred.connect(self._on_error)
        self.parent().on_connected(True, "Client connected")

    def _on_ready_read(self):
        if self._disconnecting:
            return
        try:
            data = self.client.readAll().data().decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Read error: {e}")
            return
        self.buffer += data
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            if not line:
                continue
            try:
                msg = json.loads(line.strip())
                if not isinstance(msg, dict):
                    continue
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue
            self.parent().on_data(msg)

    def _on_disconnect(self):
        if self._disconnecting:
            return
        self._disconnecting = True
        self.parent().on_connected(False, "Client disconnected")
        if self.client:
            self.client.close()
            self.client = None
        self.parent().on_disconnected()
        self._disconnecting = False

    def _on_error(self, error):
        if self._disconnecting:
            return
        self._disconnecting = True
        self.parent().on_connected(False, f"Error: {error}")
        if self.client:
            self.client.close()
            self.client = None
        self.parent().on_disconnected()
        self._disconnecting = False

    def send_message(self, msg_dict):
        if self.client and not self._disconnecting:
            try:
                self.client.write((json.dumps(msg_dict) + "\n").encode('utf-8'))
            except Exception as e:
                print(f"Send error: {e}")

    def close_connection(self):
        if self._disconnecting:
            if self.isListening():
                QTcpServer.close(self)
            return
        self._disconnecting = True
        if self.client:
            self.client.close()
            self.client = None
        if self.isListening():
            QTcpServer.close(self)
        self._disconnecting = False


class ChessClient(QTcpSocket):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buffer = ""
        self._disconnecting = False
        self.connected.connect(self._on_connected)
        self.readyRead.connect(self._on_ready_read)
        self.disconnected.connect(self._on_disconnect)
        self.errorOccurred.connect(self._on_error)

    def connect_to_host(self, host, port=5000):
        self.connectToHost(host, port)

    def _on_connected(self):
        self.parent().on_connected(True, "Connected to host")

    def _on_ready_read(self):
        if self._disconnecting:
            return
        try:
            data = self.readAll().data().decode('utf-8', errors='replace')
        except Exception as e:
            print(f"Read error: {e}")
            return
        self.buffer += data
        while "\n" in self.buffer:
            line, self.buffer = self.buffer.split("\n", 1)
            if not line:
                continue
            try:
                msg = json.loads(line.strip())
                if not isinstance(msg, dict):
                    continue
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue
            self.parent().on_data(msg)

    def _on_disconnect(self):
        if self._disconnecting:
            return
        self._disconnecting = True
        self.parent().on_connected(False, "Disconnected from host")
        self.parent().on_disconnected()
        self._disconnecting = False

    def _on_error(self, error):
        if self._disconnecting:
            return
        self._disconnecting = True
        self.parent().on_connected(False, f"Error: {error}")
        self.parent().on_disconnected()
        self._disconnecting = False

    def send_message(self, msg_dict):
        if not self._disconnecting:
            try:
                self.write((json.dumps(msg_dict) + "\n").encode('utf-8'))
            except Exception as e:
                print(f"Send error: {e}")

    def close_connection(self):
        if self._disconnecting:
            return
        self._disconnecting = True
        self.close()
        self._disconnecting = False


# ============================================================================
# TIMER MANAGER (with proper turn switching)
# ============================================================================
class TimerManager(QObject):
    timeout = pyqtSignal(str)  # 'white' or 'black'
    tick = pyqtSignal(float, float)  # white_time, black_time

    def __init__(self, initial_minutes: int = 3):
        super().__init__()
        self.minutes = initial_minutes
        self.white_time = initial_minutes * 60.0
        self.black_time = initial_minutes * 60.0
        self.running = False
        self.paused = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.last_tick = 0.0
        self.current_turn = chess.WHITE

    def start(self, turn: int = chess.WHITE):
        self.current_turn = turn
        self.running = True
        self.paused = False
        self.last_tick = time.monotonic()
        self.timer.start(100)

    def stop(self):
        self.running = False
        self.timer.stop()

    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.timer.stop()

    def resume(self):
        if self.running and self.paused:
            self.paused = False
            self.last_tick = time.monotonic()
            self.timer.start(100)

    def reset(self, minutes: int):
        self.minutes = minutes
        self.white_time = minutes * 60.0
        self.black_time = minutes * 60.0
        self.running = False
        self.paused = False
        self.timer.stop()
        self.current_turn = chess.WHITE

    def set_turn(self, turn: int):
        self.current_turn = turn

    def sync_times(self, white: float, black: float):
        self.white_time = white
        self.black_time = black

    def advance_turn(self, new_turn: int):
        """
        Advance timer: first settle current player's clock, then switch to new_turn.
        This ensures the correct player's time is decremented.
        """
        if not self.running or self.paused:
            self.current_turn = new_turn
            return
        # Settle current turn (deduct elapsed time)
        self._tick()
        # Switch to new turn
        self.current_turn = new_turn

    def _tick(self):
        if not self.running or self.paused:
            return
        now = time.monotonic()
        elapsed = now - self.last_tick
        self.last_tick = now
        if self.current_turn == chess.WHITE:
            self.white_time -= elapsed
            if self.white_time < 0:
                self.white_time = 0
                self.timeout.emit('white')
                return
        else:
            self.black_time -= elapsed
            if self.black_time < 0:
                self.black_time = 0
                self.timeout.emit('black')
                return
        self.tick.emit(self.white_time, self.black_time)

    def get_times(self) -> tuple:
        return self.white_time, self.black_time


# ============================================================================
# NETWORK MANAGER (fixed close bug)
# ============================================================================
class NetworkManager(QObject):
    connected = pyqtSignal(bool, str)
    data_received = pyqtSignal(dict)
    disconnected = pyqtSignal()
    send_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.server = None
        self.client = None
        self.is_host = False
        self.connected_flag = False

    def host_game(self, port: int = 5000):
        self.is_host = True
        self.server = ChessServer(self)
        if self.server.start_server(port):
            self.connected_flag = True
            self.connected.emit(True, f"Server started on port {port}")
        else:
            self.connected.emit(False, "Could not start server")

    def join_game(self, host: str, port: int = 5000):
        self.is_host = False
        self.client = ChessClient(self)
        self.client.connect_to_host(host, port)

    def send_message(self, msg: dict):
        try:
            if self.is_host and self.server:
                self.server.send_message(msg)
            elif not self.is_host and self.client:
                self.client.send_message(msg)
            else:
                self.send_error.emit("No active connection")
        except Exception as e:
            self.send_error.emit(f"Send error: {str(e)}")

    def close(self):
        if self.is_host and self.server:
            self.server.close_connection()
            self.server = None
        elif not self.is_host and self.client:
            self.client.close_connection()
            self.client = None
        was_connected = self.connected_flag
        self.connected_flag = False
        if was_connected:
            self.disconnected.emit()

    def on_connected(self, success: bool, msg: str):
        self.connected_flag = success
        self.connected.emit(success, msg)

    def on_data(self, data: dict):
        self.data_received.emit(data)

    def on_disconnected(self):
        self.connected_flag = False
        self.disconnected.emit()


# ============================================================================
# GAME STATE
# ============================================================================
class GameState:
    def __init__(self):
        self.board = chess.Board()
        self.move_stack: List[chess.Move] = []
        self.move_history: List[str] = []
        self.game_over = False
        self.paused = False
        self.result = None
        self.timer_white = 180.0
        self.timer_black = 180.0
        self.turn = chess.WHITE

    def reset(self, minutes: int = 3):
        self.board = chess.Board()
        self.move_stack = []
        self.move_history = []
        self.game_over = False
        self.paused = False
        self.result = None
        self.timer_white = minutes * 60.0
        self.timer_black = minutes * 60.0
        self.turn = chess.WHITE

    def push_move(self, move: chess.Move) -> str:
        san = self.board.san(move)
        self.board.push(move)
        self.move_stack.append(move)
        self.move_history.append(san)
        self.turn = self.board.turn
        if self.board.is_game_over():
            self.game_over = True
            if self.board.is_checkmate():
                self.result = 'win' if self.board.turn == chess.BLACK else 'loss'
            else:
                self.result = 'draw'
        return san

    def to_dict(self) -> dict:
        return {
            'fen': self.board.fen(),
            'moves': [m.uci() for m in self.move_stack],
            'move_history': self.move_history,
            'game_over': self.game_over,
            'paused': self.paused,
            'result': self.result,
            'timer_white': self.timer_white,
            'timer_black': self.timer_black,
            'turn': self.turn
        }

    def from_dict(self, data: dict):
        self.board = chess.Board(data['fen'])
        self.move_stack = [chess.Move.from_uci(u) for u in data['moves']]
        self.move_history = data['move_history']
        self.game_over = data['game_over']
        self.paused = data['paused']
        self.result = data['result']
        self.timer_white = data['timer_white']
        self.timer_black = data['timer_black']
        self.turn = data['turn']


# ============================================================================
# GAME CONTROLLER — Fixed (QThread lifecycle, timer, capture, game over)
# ============================================================================
class GameController(QObject):
    board_updated = pyqtSignal()
    history_updated = pyqtSignal()
    player_cards_updated = pyqtSignal()
    game_over_signal = pyqtSignal(str, str)  # title, message
    toast = pyqtSignal(str, str)  # message, type
    board_flipped = pyqtSignal(bool)

    def __init__(self, main_window, shared_engine, sound_manager):
        super().__init__()
        self.main_window = main_window
        self.settings = main_window.settings
        self.stats = main_window.stats
        self.sound_manager = sound_manager
        self.vip = self.settings.get('vip', False)
        self.two_player_mode = False
        self.lan_mode = False
        self.is_host = False
        self.lan_color = None

        self.state = GameState()
        self.timer_minutes = self.settings.get('timer_minutes', 3)
        self.state.reset(self.timer_minutes)

        self.ai = ChessAI(self.settings.get('ai_level', 'easy'), engine=shared_engine)

        self.timer_manager = TimerManager(self.timer_minutes)
        self.timer_manager.timeout.connect(self._on_timeout)
        self.timer_manager.tick.connect(self._on_timer_tick)

        self.network = NetworkManager()
        self.network.connected.connect(self._on_network_connected)
        self.network.data_received.connect(self._on_network_data)
        self.network.disconnected.connect(self._on_network_disconnected)
        self.network.send_error.connect(lambda msg: self.toast.emit(f"Network error: {msg}", "error"))

        # AI thread management
        self.ai_thread = None
        self.ai_worker = None
        self.ai_generation = 0
        self.ai_thinking = False

        self.selected_square = None
        self.legal_moves = []
        self.last_move = None
        self.paused = False
        self.game_over = False
        self._game_finished = False
        self.result_recorded = False
        self.settings_open = False
        self._closing = False

        self.start_timer()

        if not self.two_player_mode and not self.lan_mode and self.state.board.turn == chess.BLACK:
            QTimer.singleShot(500, self.do_ai_move)

    # ---------- Game Logic ----------
    def make_move(self, move: chess.Move, send_network: bool = True) -> bool:
        if self.game_over or self.ai_thinking or self.paused or self.settings_open:
            return False
        if self.lan_mode and self.is_host and self.state.board.turn != chess.WHITE:
            return False
        if self.lan_mode and not self.is_host and self.state.board.turn != chess.BLACK:
            return False
        if move not in self.state.board.legal_moves:
            return False

        self._commit_move(move, send_network)
        return True

    def _commit_move(self, move: chess.Move, send_network: bool = True):
        # Pre-move: detect capture/castling/promotion BEFORE board mutation
        is_capture = self.state.board.is_capture(move)
        is_castling = self.state.board.is_castling(move)
        is_promotion = move.promotion is not None

        # Settle current player's clock BEFORE the move
        self.timer_manager.advance_turn(self.state.board.turn)

        # Push the move
        from_sq = move.from_square
        to_sq = move.to_square
        san = self.state.push_move(move)
        self.last_move = (from_sq, to_sq)

        # AFTER move: switch timer to the new turn
        self.timer_manager.set_turn(self.state.board.turn)

        # Sounds based on pre-move state
        if is_capture:
            self.sound_manager.play('capture')
        elif is_promotion:
            self.sound_manager.play('promotion')
        elif is_castling:
            self.sound_manager.play('castling')
        else:
            self.sound_manager.play('move')

        if self.state.board.is_check() and not self.state.board.is_checkmate():
            self.sound_manager.play('check')
        if self.state.board.is_checkmate():
            self.sound_manager.play('checkmate')

        # Update UI
        self.board_updated.emit()
        self.history_updated.emit()
        self.player_cards_updated.emit()

        # Network sync
        if send_network and self.lan_mode:
            self.network.send_message({
                "type": "move",
                "uci": move.uci(),
                "ply": len(self.state.move_stack),
                "white_time": int(self.state.timer_white),
                "black_time": int(self.state.timer_black)
            })

        # Check game over (DO NOT auto-reset)
        if self.state.board.is_game_over():
            self._finish_game()
            return

        # AI turn
        if not self.game_over and not self.two_player_mode and not self.lan_mode and self.state.board.turn == chess.BLACK:
            QTimer.singleShot(300, self.do_ai_move)

    def _finish_game(self):
        """Handle game over WITHOUT auto-resetting the board."""
        self.game_over = True
        self._game_finished = True
        self.timer_manager.stop()

        if self.state.board.is_checkmate():
            winner = 'White' if self.state.board.turn == chess.BLACK else 'Black'
            result = 'win' if winner == 'White' else 'loss'
            if not self.two_player_mode and not self.lan_mode:
                self.record_result(result)
            self.game_over_signal.emit("Checkmate", f"{winner} wins!")
            if self.lan_mode:
                self.network.send_message({
                    "type": "game_over",
                    "result": "checkmate",
                    "winner": winner.lower()
                })
        else:
            if not self.two_player_mode and not self.lan_mode:
                self.record_result('draw')
            self.game_over_signal.emit("Draw", "Game ended in a draw!")
            if self.lan_mode:
                self.network.send_message({
                    "type": "game_over",
                    "result": "draw"
                })

    def record_result(self, result: str):
        if self.result_recorded:
            return
        self.result_recorded = True
        self.stats['games'] += 1
        if result == 'win':
            self.stats['wins'] += 1
        elif result == 'loss':
            self.stats['losses'] += 1
        else:
            self.stats['draws'] += 1
        save_stats(self.stats)
        self.main_window.stats = self.stats

    # ---------- AI (with proper QThread lifecycle) ----------
    def do_ai_move(self):
        if (
            self.game_over
            or self.ai_thinking
            or self.two_player_mode
            or self.lan_mode
            or self.paused
            or self.settings_open
        ):
            return

        if self.state.board.turn != chess.BLACK:
            return

        # Clear stale thread reference
        if self.ai_thread is not None:
            try:
                if self.ai_thread.isRunning():
                    return
            except RuntimeError:
                self.ai_thread = None
                self.ai_worker = None

        self.ai_thinking = True
        self.ai_generation += 1
        gen = self.ai_generation

        thread = QThread(self)
        worker = AIWorker(
            self.state.board.fen(),
            self.settings.get('ai_level', 'easy'),
            self.ai.engine,
            gen
        )

        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(self._on_ai_finished)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(lambda: self._clear_ai_thread(thread))

        self.ai_thread = thread
        self.ai_worker = worker

        thread.start()

    def _clear_ai_thread(self, thread):
        if self.ai_thread is thread:
            self.ai_thread = None
            self.ai_worker = None

    def _on_ai_finished(self, move, gen):
        if gen != self.ai_generation:
            return

        self.ai_thinking = False

        if self.paused or self.game_over or self.lan_mode or self.settings_open:
            return

        if move and move in self.state.board.legal_moves:
            self._commit_move(move, send_network=False)
        else:
            if not move:
                self.toast.emit("AI could not find a move", "error")

    # ---------- Timer ----------
    def start_timer(self):
        if self.game_over or self.paused or self.settings_open:
            return
        self.timer_manager.start(self.state.board.turn)

    def stop_timer(self):
        self.timer_manager.stop()

    def pause_timer(self):
        self.timer_manager.pause()

    def resume_timer(self):
        self.timer_manager.resume()

    def _on_timeout(self, color: str):
        self.game_over = True
        self._game_finished = True
        self.timer_manager.stop()
        self.sound_manager.play('timeout')

        winner = 'Black' if color == 'white' else 'White'
        result = 'loss' if color == 'white' else 'win'

        if not self.two_player_mode and not self.lan_mode:
            self.record_result(result)

        self.game_over_signal.emit("Time Out", f"{winner} wins on time!")

        if self.lan_mode:
            self.network.send_message({
                "type": "game_over",
                "result": "timeout",
                "winner": winner.lower()
            })

    def _on_timer_tick(self, white_time: float, black_time: float):
        self.state.timer_white = white_time
        self.state.timer_black = black_time
        self.player_cards_updated.emit()

    # ---------- Network ----------
    def host_game(self):
        if self.lan_mode:
            self.toast.emit("Already in a game", "error")
            return
        self.stop_timer()
        self.ai_generation += 1
        self.ai_thinking = False
        self.lan_mode = True
        self.is_host = True
        self.lan_color = "white"
        self.network.host_game()

    def join_game(self, ip: str):
        if self.lan_mode:
            self.toast.emit("Already in a game", "error")
            return
        self.stop_timer()
        self.ai_generation += 1
        self.ai_thinking = False
        self.lan_mode = True
        self.is_host = False
        self.lan_color = None
        self.network.join_game(ip)

    def _on_network_connected(self, success: bool, msg: str):
        if success:
            self.toast.emit(msg, "success")
            if self.is_host:
                self.network.send_message({
                    "type": "sync",
                    "fen": self.state.board.fen(),
                    "moves": [m.uci() for m in self.state.move_stack],
                    "white_time": int(self.state.timer_white),
                    "black_time": int(self.state.timer_black),
                    "ply": len(self.state.move_stack)
                })
                self.start_timer()
            else:
                QTimer.singleShot(3000, lambda: self._check_sync_timeout())
        else:
            self.toast.emit(msg, "error")
            self._on_network_disconnected()

    def _check_sync_timeout(self):
        if self.lan_mode and not self.lan_color:
            self.toast.emit("No sync received from host. Disconnecting.", "error")
            self.network.close()

    def _on_network_data(self, data: dict):
        typ = data.get('type')

        if typ == 'sync':
            if not self.is_host:
                fen = data.get('fen')
                moves_uci = data.get('moves', [])
                wt = data.get('white_time', self.state.timer_white)
                bt = data.get('black_time', self.state.timer_black)
                ply = data.get('ply', 0)

                if len(moves_uci) != ply:
                    return

                try:
                    b = chess.Board()
                    for u in moves_uci:
                        m = chess.Move.from_uci(u)
                        if m not in b.legal_moves:
                            raise ValueError("Invalid move")
                        b.push(m)

                    if b.fen() != fen:
                        raise ValueError("FEN mismatch")

                    self.state.board = chess.Board(fen)
                    self.state.move_stack = [chess.Move.from_uci(u) for u in moves_uci]
                    self.state.move_history = []
                    b2 = chess.Board()
                    for m in self.state.move_stack:
                        self.state.move_history.append(b2.san(m))
                        b2.push(m)

                    # Sync both GameState and TimerManager
                    self.state.timer_white = wt
                    self.state.timer_black = bt
                    self.timer_manager.sync_times(wt, bt)
                    self.timer_manager.set_turn(self.state.board.turn)

                    self.state.turn = self.state.board.turn
                    self.state.game_over = False
                    self.lan_color = "black"

                    # Reset UI state
                    self.selected_square = None
                    self.legal_moves = []
                    self.last_move = None

                    self.board_updated.emit()
                    self.history_updated.emit()
                    self.player_cards_updated.emit()
                    self.start_timer()
                    self.toast.emit("Game synchronized", "success")
                    self.board_flipped.emit(True)

                except Exception as e:
                    print(f"Sync error: {e}")
                    self._on_network_disconnected()
                    self.toast.emit("Sync failed", "error")

        elif typ == 'move':
            if self.lan_mode:
                uci = data.get('uci')
                ply = data.get('ply', 0)
                wt = data.get('white_time')
                bt = data.get('black_time')

                if ply != len(self.state.move_stack) + 1:
                    if self.is_host:
                        self.network.send_message({"type": "sync_request"})
                    return

                try:
                    move = chess.Move.from_uci(uci)
                    if move not in self.state.board.legal_moves:
                        return

                    if self.is_host and self.state.board.turn != chess.BLACK:
                        return
                    if not self.is_host and self.state.board.turn != chess.WHITE:
                        return

                    if wt is not None:
                        self.state.timer_white = wt
                        self.timer_manager.sync_times(wt, self.state.timer_black)
                    if bt is not None:
                        self.state.timer_black = bt
                        self.timer_manager.sync_times(self.state.timer_white, bt)

                    self._commit_move(move, send_network=False)

                except Exception as e:
                    print(f"Move error: {e}")

        elif typ == 'sync_request':
            if self.is_host:
                self.network.send_message({
                    "type": "sync",
                    "fen": self.state.board.fen(),
                    "moves": [m.uci() for m in self.state.move_stack],
                    "white_time": int(self.state.timer_white),
                    "black_time": int(self.state.timer_black),
                    "ply": len(self.state.move_stack)
                })

        elif typ == 'pause':
            paused = data.get('paused', False)
            if paused != self.paused:
                self.toggle_pause()

        elif typ == 'new_game':
            self._handle_new_game_request()

        elif typ == 'new_game_accept':
            self.reset_board(notify_peer=False)

        elif typ == 'new_game_decline':
            self.toast.emit("Opponent declined new game", "error")

        elif typ == 'resign':
            self.game_over = True
            self._game_finished = True
            self.game_over_signal.emit("Resign", "Opponent resigned. You win!")
            # DO NOT auto-reset

        elif typ == 'draw_offer':
            self._handle_draw_offer()

        elif typ == 'draw_accept':
            self.game_over = True
            self._game_finished = True
            self.record_result('draw')
            self.game_over_signal.emit("Draw", "Game drawn by agreement.")

        elif typ == 'draw_decline':
            self.toast.emit("Opponent declined draw", "error")

        elif typ == 'game_over':
            result = data.get('result')
            winner = data.get('winner')
            self.game_over = True
            self._game_finished = True
            self.stop_timer()

            if result == 'timeout':
                self.game_over_signal.emit("Time Out", f"{winner.capitalize()} wins on time!")
            elif result == 'checkmate':
                self.game_over_signal.emit("Checkmate", f"{winner.capitalize()} wins!")
            elif result == 'draw':
                self.game_over_signal.emit("Draw", "Game drawn!")

            # DO NOT auto-reset

    def _handle_new_game_request(self):
        reply = QMessageBox.question(
            self.main_window, "New Game",
            "Opponent wants a new game. Accept?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.network:
                self.network.send_message({"type": "new_game_accept"})
            self.reset_board(notify_peer=False)
        else:
            if self.network:
                self.network.send_message({"type": "new_game_decline"})

    def _handle_draw_offer(self):
        reply = QMessageBox.question(
            self.main_window, "Draw Offer",
            "Opponent offers a draw. Accept?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.network:
                self.network.send_message({"type": "draw_accept"})
            self.game_over = True
            self._game_finished = True
            self.record_result('draw')
            self.game_over_signal.emit("Draw", "Game drawn by agreement.")
        else:
            if self.network:
                self.network.send_message({"type": "draw_decline"})

    def _on_network_disconnected(self):
        if self._closing:
            return

        self.lan_mode = False
        self.is_host = False
        self.lan_color = None
        self.toast.emit("Connection lost", "error")
        self.reset_board(notify_peer=False)

    # ---------- Pause / Reset ----------
    def toggle_pause(self):
        if self.game_over:
            return

        self.paused = not self.paused
        if self.paused:
            self.timer_manager.pause()
            if self.lan_mode:
                self.network.send_message({"type": "pause", "paused": True})
        else:
            self.timer_manager.resume()
            self.start_timer()
            if self.lan_mode:
                self.network.send_message({"type": "pause", "paused": False})

        self.player_cards_updated.emit()

    def reset_board(self, notify_peer: bool = True):
        self.stop_timer()
        self.state.reset(self.timer_minutes)
        self.timer_manager.reset(self.timer_minutes)

        self.selected_square = None
        self.legal_moves = []
        self.last_move = None
        self.game_over = False
        self._game_finished = False
        self.result_recorded = False
        self.paused = False
        self.ai_generation += 1

        self.board_updated.emit()
        self.history_updated.emit()
        self.player_cards_updated.emit()
        self.start_timer()

        if self.lan_mode and notify_peer:
            self.network.send_message({"type": "new_game"})

        if not self.two_player_mode and not self.lan_mode and self.state.board.turn == chess.BLACK:
            QTimer.singleShot(500, self.do_ai_move)

    def resign_game(self):
        if self.game_over:
            return

        self.game_over = True
        self._game_finished = True

        if self.lan_mode:
            self.network.send_message({"type": "resign"})

        if not self.two_player_mode and not self.lan_mode:
            self.record_result('loss')

        self.game_over_signal.emit("Resign", "You resigned. Game over.")
        # DO NOT auto-reset

    def offer_draw(self):
        if self.game_over:
            return

        if self.lan_mode:
            self.network.send_message({"type": "draw_offer"})
            self.toast.emit("Draw offer sent", "success")
        else:
            self.game_over = True
            self._game_finished = True
            self.record_result('draw')
            self.game_over_signal.emit("Draw", "Game drawn by agreement.")

    # ---------- Two Player ----------
    def toggle_two_player(self):
        if self.lan_mode:
            self.toast.emit("Cannot switch while LAN active", "error")
            return
        if not self.vip:
            self.toast.emit("VIP required for 2P mode", "error")
            return

        self.two_player_mode = not self.two_player_mode
        self.reset_board(notify_peer=False)

    # ---------- Settings ----------
    def set_level(self, level: str):
        if self.ai_thinking or self.lan_mode:
            return

        self.ai.set_level(level)
        self.settings['ai_level'] = level
        save_settings(self.settings)
        self.reset_board(notify_peer=False)

    def set_timer_minutes(self, minutes: int):
        self.timer_minutes = minutes
        self.settings['timer_minutes'] = minutes
        save_settings(self.settings)

        self.state.timer_white = minutes * 60.0
        self.state.timer_black = minutes * 60.0
        self.timer_manager.reset(minutes)

    def cleanup(self):
        self._closing = True
        self.stop_timer()

        if self.network:
            self.network.close()

        self.ai_generation += 1
        self.ai_thinking = False

        # Clear AI thread if still running
        if self.ai_thread is not None:
            try:
                if self.ai_thread.isRunning():
                    self.ai_thread.quit()
                    self.ai_thread.wait(500)
            except RuntimeError:
                pass
            self.ai_thread = None
            self.ai_worker = None

    # ---------- Getters ----------
    def get_board(self):
        return self.state.board

    def get_move_history(self):
        return self.state.move_history

    def get_move_stack(self):
        return self.state.move_stack

    def get_timer_times(self):
        return self.timer_manager.get_times()


# ============================================================================
# ===== CHALLENGES (Daily) =====
# ============================================================================
class Challenge:
    def __init__(self, name: str, description: str, fen: str, solution_moves: List[str],
                 hint: str, explanation: str = ""):
        self.name = name
        self.description = description
        self.fen = fen
        self.board = chess.Board(fen)
        self.solution = [self.board.parse_san(m) for m in solution_moves]
        self.hint = hint
        self.explanation = explanation
        self.current_step = 0

    def get_position(self) -> chess.Board:
        return self.board

    def is_move_correct(self, move: chess.Move) -> bool:
        if self.current_step < len(self.solution):
            return move == self.solution[self.current_step]
        return False

    def advance(self) -> bool:
        self.current_step += 1
        if self.current_step < len(self.solution):
            self.board.push(self.solution[self.current_step])
            return True
        return False

    def reset(self):
        self.board = chess.Board(self.fen)
        self.current_step = 0

    def is_complete(self) -> bool:
        return self.current_step >= len(self.solution)


class ChallengeManager:
    def __init__(self):
        self.challenges: List[Challenge] = []
        self._load_challenges()

    def _load_challenges(self):
        challenges_data = [
            ("Fork",
             "Attack two pieces at once.",
             "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
             ["Qxf7+"],
             "Move queen to f7 forking king and rook.",
             "Qxf7+ gives check and attacks the rook."),
            ("Skewer",
             "Attack a valuable piece behind a less valuable one.",
             "r1bqkb1r/ppp2ppp/2n2n2/3pp3/2B1P3/2N5/PPPP1PPP/R1BQK1NR w KQkq - 6 5",
             ["Bxd5"],
             "Bishop takes d5, skewering queen.",
             "Bxd5 captures the knight and exposes the queen."),
            ("Pin",
             "Pin a piece to the king.",
             "rnbqkbnr/ppp2ppp/3p4/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 3",
             ["Bb5+"],
             "Bishop to b5 pins the knight on c6.",
             "Bb5+ pins the knight and gives check."),
            ("Sacrifice",
             "Sacrifice a piece to force mate.",
             "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
             ["Qxf7+"],
             "Queen sacrifice leads to mate.",
             "Qxf7+ is a sacrifice that forces checkmate."),
        ]
        for name, desc, fen, moves, hint, expl in challenges_data:
            self.challenges.append(Challenge(name, desc, fen, moves, hint, expl))

    def get_daily_challenge(self) -> Optional[Challenge]:
        """Return a challenge based on today's date (day of month) as seed."""
        if not self.challenges:
            return None
        day = datetime.now().day
        index = day % len(self.challenges)
        challenge = self.challenges[index]
        # Reset the challenge board each time we get it
        challenge.reset()
        return challenge


# ============================================================================
# ===== CHALLENGES SCREEN =====
# ============================================================================
class ChallengesScreen(QWidget):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.theme = main_window.theme
        self.sound_manager = main_window.sound_manager
        self.challenge_manager = ChallengeManager()
        self.current_challenge = None
        self.load_daily_challenge()

        self.setup_ui()
        self.update_challenge()

    def load_daily_challenge(self):
        self.current_challenge = self.challenge_manager.get_daily_challenge()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Design.SPACING['md'])
        layout.setContentsMargins(Design.SPACING['lg'], Design.SPACING['lg'],
                                  Design.SPACING['lg'], Design.SPACING['lg'])

        self.title_label = QLabel("♟ Daily Challenge")
        self.title_label.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        self.title_label.setStyleSheet(f"color: {self.theme['accent']};")
        layout.addWidget(self.title_label)

        self.date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
        self.date_label.setFont(QFont('Segoe UI', Design.FONT['body']))
        self.date_label.setStyleSheet(f"color: {self.theme['text_muted']};")
        layout.addWidget(self.date_label)

        self.desc_label = QLabel("")
        self.desc_label.setWordWrap(True)
        self.desc_label.setFont(QFont('Segoe UI', Design.FONT['body']))
        self.desc_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        layout.addWidget(self.desc_label)

        self.board_widget = ChessBoardWidget(self)
        self.board_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.board_widget, stretch=1)

        self.hint_label = QLabel("")
        self.hint_label.setWordWrap(True)
        self.hint_label.setStyleSheet(f"color: {self.theme['warning']}; font-style: italic;")
        layout.addWidget(self.hint_label)

        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet(f"color: {self.theme['success']}; font-weight: bold;")
        layout.addWidget(self.feedback_label)

        ctrl_layout = QHBoxLayout()
        self.reset_btn = PremiumButton("🔄 Reset", self)
        self.reset_btn.clicked.connect(self.reset_challenge)
        self.back_btn = PremiumButton("← Back to Menu", self)
        self.back_btn.clicked.connect(self.go_back)

        ctrl_layout.addWidget(self.reset_btn)
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(self.back_btn)
        layout.addLayout(ctrl_layout)

        self.board_widget.move_made.connect(self.on_move_made)

    def update_challenge(self):
        if self.current_challenge is None:
            self.desc_label.setText("No challenge available today.")
            return
        self.board_widget.set_board(self.current_challenge.get_position())
        self.desc_label.setText(f"{self.current_challenge.name}: {self.current_challenge.description}")
        self.hint_label.setText(f"💡 Hint: {self.current_challenge.hint}")
        self.feedback_label.setText("")

    def on_move_made(self, move: chess.Move):
        if self.current_challenge is None:
            return
        if self.current_challenge.is_move_correct(move):
            self.current_challenge.advance()
            self.board_widget.set_board(self.current_challenge.get_position())
            if self.current_challenge.is_complete():
                self.feedback_label.setText("✅ Excellent! Challenge complete.")
                if self.current_challenge.explanation:
                    QMessageBox.information(self, "Explanation", self.current_challenge.explanation)
            else:
                self.feedback_label.setText("✅ Correct! Continue.")
        else:
            self.feedback_label.setText("❌ Wrong move. Try again.")
            self.board_widget.set_board(self.current_challenge.get_position())

    def reset_challenge(self):
        if self.current_challenge:
            self.current_challenge.reset()
            self.board_widget.set_board(self.current_challenge.get_position())
            self.feedback_label.setText("")

    def go_back(self):
        self.main_window.switch_to_menu()


# ============================================================================
# ===== LESSONS (Rules & Piece Movements) =====
# ============================================================================
class LessonTopic:
    def __init__(self, title: str, description: str, fen: str, explanation: str = ""):
        self.title = title
        self.description = description
        self.fen = fen
        self.explanation = explanation
        self.board = chess.Board(fen)

    def get_board(self) -> chess.Board:
        return self.board


class LessonManager:
    def __init__(self):
        self.topics: List[LessonTopic] = []
        self._load_topics()

    def _load_topics(self):
        topics_data = [
            ("Pawn Movement",
             "Pawns move forward one square, but capture diagonally. On their first move, they may move two squares.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Pawns are the foot soldiers of chess."),
            ("Knight Movement",
             "Knights move in an L-shape: two squares in one direction and one perpendicular. They can jump over pieces.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Knights are the only pieces that can jump."),
            ("Bishop Movement",
             "Bishops move diagonally any number of squares, staying on the same color.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Bishops are long-range diagonal pieces."),
            ("Rook Movement",
             "Rooks move horizontally or vertically any number of squares.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Rooks are powerful on open files and ranks."),
            ("Queen Movement",
             "Queens combine the power of a rook and a bishop, moving any number of squares in any direction.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "The queen is the most powerful piece."),
            ("King Movement",
             "Kings move one square in any direction. They can also castle (see below).",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "The king is the most important piece."),
            ("Castling",
             "Castling is a special move where the king moves two squares towards a rook, and the rook jumps over it. It cannot be done if either piece has moved, if the king is in check, or if the king passes through check.",
             "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Castling is the only move that moves two pieces at once."),
            ("Promotion",
             "When a pawn reaches the last rank, it can be promoted to a queen, rook, bishop, or knight.",
             "8/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
             "Promotion usually chooses a queen."),
            ("Check",
             "A king is in check when it is attacked by an enemy piece. The player must get out of check immediately.",
             "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
             "White's queen gives check."),
            ("Checkmate",
             "Checkmate occurs when the king is in check and there is no legal move to escape.",
             "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
             "This position is checkmate."),
            ("Stalemate",
             "Stalemate is a draw where the player to move has no legal moves, but their king is not in check.",
             "7k/8/8/8/8/8/8/K7 w - - 0 1",
             "Black is stalemated."),
            ("En Passant",
             "En passant is a special pawn capture that can occur when a pawn moves two squares from its starting square and lands adjacent to an enemy pawn.",
             "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2",
             "White can capture en passant."),
        ]
        for title, desc, fen, expl in topics_data:
            self.topics.append(LessonTopic(title, desc, fen, expl))

    def get_all(self) -> List[LessonTopic]:
        return self.topics

    def get(self, index: int) -> Optional[LessonTopic]:
        if 0 <= index < len(self.topics):
            return self.topics[index]
        return None

    def count(self) -> int:
        return len(self.topics)


class LessonsWidget(QWidget):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.theme = main_window.theme
        self.lesson_manager = LessonManager()
        self.current_index = 0
        self.current_topic = self.lesson_manager.get(0)

        self.setup_ui()
        self.update_topic()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Design.SPACING['sm'])

        self.topic_list = QListWidget()
        self.topic_list.setMaximumHeight(100)
        self.topic_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                font-size: {Design.FONT['small']}px;
            }}
            QListWidget::item:selected {{
                background: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
        """)
        for topic in self.lesson_manager.get_all():
            self.topic_list.addItem(topic.title)
        self.topic_list.setCurrentRow(0)
        self.topic_list.currentRowChanged.connect(self.on_topic_selected)
        layout.addWidget(self.topic_list)

        self.board_widget = ChessBoardWidget(self)
        self.board_widget.setFixedSize(300, 300)
        self.board_widget.setEnabled(False)
        layout.addWidget(self.board_widget, alignment=Qt.AlignCenter)

        self.desc_label = QLabel("")
        self.desc_label.setWordWrap(True)
        self.desc_label.setFont(QFont('Segoe UI', Design.FONT['body']))
        self.desc_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        layout.addWidget(self.desc_label)

        self.explanation_label = QLabel("")
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setFont(QFont('Segoe UI', Design.FONT['small']))
        self.explanation_label.setStyleSheet(f"color: {self.theme['text_muted']}; font-style: italic;")
        layout.addWidget(self.explanation_label)

        layout.addStretch()

    def on_topic_selected(self, index):
        self.current_index = index
        self.current_topic = self.lesson_manager.get(index)
        self.update_topic()

    def update_topic(self):
        if self.current_topic is None:
            return
        self.board_widget.set_board(self.current_topic.get_board())
        self.desc_label.setText(self.current_topic.description)
        self.explanation_label.setText(self.current_topic.explanation)


# ============================================================================
# GAME UI (with enhanced history table and click-to-show move)
# ============================================================================
class GameUI(QWidget):
    def __init__(self, controller: GameController, main_window):
        super().__init__(main_window)
        self.controller = controller
        self.main_window = main_window
        self.settings = controller.settings
        self.theme = main_window.theme
        self.vip = controller.vip

        self.sound_manager = main_window.sound_manager

        self.controller.board_updated.connect(self.update_board)
        self.controller.history_updated.connect(self.update_history)
        self.controller.player_cards_updated.connect(self.update_player_cards)
        self.controller.game_over_signal.connect(self.show_game_over)
        self.controller.toast.connect(self.show_toast)
        self.controller.board_flipped.connect(self.on_board_flipped)

        self.board_widget = None
        self.history_table = None
        self.white_time_label = None
        self.black_time_label = None
        self.white_status = None
        self.black_status = None
        self.pause_btn = None
        self.network_status_label = None
        self.ad_timer = None
        self.ad_label = None
        self.ad_index = 0
        self.ad_links = [("Chess.com", "https://www.chess.com"), ("Lichess", "https://lichess.org"), ("Chessable", "https://www.chessable.com")]
        self.toast_widget = None
        self.history_empty = None
        self.two_player_btn = None
        self.ad_frame = None
        self.tab_widget = None

        self.setup_ui()
        self.update_board()
        self.update_history()
        self.update_player_cards()
        self._apply_themed_cursor()

        if not self.controller.two_player_mode and not self.controller.lan_mode and self.controller.state.board.turn == chess.BLACK:
            QTimer.singleShot(500, self.controller.do_ai_move)

    def _apply_themed_cursor(self):
        cursor = self._build_themed_cursor(self.theme)
        self.setCursor(cursor)

    def _build_themed_cursor(self, theme, size=22):
        pm = QPixmap(size, size)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(theme['accent']))
        p.setPen(QPen(QColor(theme['bg']), 1.5))
        p.drawEllipse(2, 2, size - 4, size - 4)
        p.end()
        return QCursor(pm, size // 2, size // 2)

    def get_stylesheet(self):
        return f"""
            QWidget {{
                background-color: {self.theme['bg']};
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 6px 16px;
                font-weight: 600;
                font-size: {Design.FONT['body']}px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['surface_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['surface_active']};
            }}
            QPushButton#primary {{
                background-color: {self.theme['accent']};
                color: #080812;
            }}
            QPushButton#primary:hover {{
                background-color: {self.theme['accent_light']};
            }}
            QPushButton#danger {{
                background-color: {self.theme['danger']};
                color: white;
            }}
            QPushButton#danger:hover {{
                background-color: #FF7A85;
            }}
            QTableWidget {{
                background: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                gridline-color: {self.theme['divider']};
                font-size: {Design.FONT['body']}px;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {self.theme['divider']};
            }}
            QTableWidget::item:selected {{
                background: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
            QHeaderView::section {{
                background: {self.theme['surface']};
                color: {self.theme['text_muted']};
                padding: 4px;
                border: none;
                font-weight: bold;
            }}
            QFrame#card {{
                background-color: {self.theme['surface']};
                border-radius: {Design.RADIUS['lg']}px;
                padding: 8px;
                border: 1px solid {self.theme['card_border']};
            }}
            QFrame#player-card {{
                background-color: {self.theme['surface']};
                border-radius: {Design.RADIUS['md']}px;
                padding: 8px 18px;
                border: 1px solid {self.theme['card_border']};
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 5px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme['text_muted']};
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme['text_secondary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QTabWidget::pane {{
                background: {self.theme['surface']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
            }}
            QTabBar::tab {{
                background: {self.theme['surface']};
                color: {self.theme['text_secondary']};
                padding: 6px 14px;
                border-top-left-radius: {Design.RADIUS['sm']}px;
                border-top-right-radius: {Design.RADIUS['sm']}px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
            QTabBar::tab:hover {{
                background: {self.theme['surface_hover']};
            }}
        """

    def setup_ui(self):
        self.setStyleSheet(self.get_stylesheet())

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Design.SPACING['xl'], Design.SPACING['lg'], Design.SPACING['xl'], Design.SPACING['lg'])
        main_layout.setSpacing(Design.SPACING['xl'])

        left_panel = QVBoxLayout()
        left_panel.setSpacing(Design.SPACING['md'])

        # Player Cards
        player_layout = QHBoxLayout()
        player_layout.setSpacing(Design.SPACING['lg'])

        self.white_card = QFrame()
        self.white_card.setObjectName("player-card")
        white_layout = QHBoxLayout(self.white_card)
        white_layout.setContentsMargins(Design.SPACING['md'], Design.SPACING['sm'], Design.SPACING['md'], Design.SPACING['sm'])
        white_left = QVBoxLayout()
        white_label = QLabel("♔ White")
        white_label.setFont(QFont('Segoe UI', Design.FONT['body'], QFont.Bold))
        white_left.addWidget(white_label)
        white_layout.addLayout(white_left)
        white_layout.addStretch()
        white_center = QVBoxLayout()
        white_center.setAlignment(Qt.AlignCenter)
        self.white_time_label = QLabel("05:00")
        self.white_time_label.setFont(QFont('Consolas', Design.FONT['clock'], QFont.Bold))
        self.white_time_label.setStyleSheet(f"color: {self.theme['text_primary']};")
        white_center.addWidget(self.white_time_label)
        white_layout.addLayout(white_center)
        white_layout.addStretch()
        white_right = QVBoxLayout()
        white_right.setAlignment(Qt.AlignRight)
        self.white_status = QLabel("● Your turn")
        self.white_status.setFont(QFont('Segoe UI', Design.FONT['small']))
        self.white_status.setStyleSheet(f"color: {self.theme['accent']};")
        white_right.addWidget(self.white_status)
        white_layout.addLayout(white_right)
        player_layout.addWidget(self.white_card)

        self.black_card = QFrame()
        self.black_card.setObjectName("player-card")
        black_layout = QHBoxLayout(self.black_card)
        black_layout.setContentsMargins(Design.SPACING['md'], Design.SPACING['sm'], Design.SPACING['md'], Design.SPACING['sm'])
        black_left = QVBoxLayout()
        black_label = QLabel("♚ Black")
        black_label.setFont(QFont('Segoe UI', Design.FONT['body'], QFont.Bold))
        black_left.addWidget(black_label)
        black_layout.addLayout(black_left)
        black_layout.addStretch()
        black_center = QVBoxLayout()
        black_center.setAlignment(Qt.AlignCenter)
        self.black_time_label = QLabel("05:00")
        self.black_time_label.setFont(QFont('Consolas', Design.FONT['clock'], QFont.Bold))
        self.black_time_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
        black_center.addWidget(self.black_time_label)
        black_layout.addLayout(black_center)
        black_layout.addStretch()
        black_right = QVBoxLayout()
        black_right.setAlignment(Qt.AlignRight)
        self.black_status = QLabel("● Waiting")
        self.black_status.setFont(QFont('Segoe UI', Design.FONT['small']))
        self.black_status.setStyleSheet(f"color: {self.theme['text_muted']};")
        black_right.addWidget(self.black_status)
        black_layout.addLayout(black_right)
        player_layout.addWidget(self.black_card)

        left_panel.addLayout(player_layout)

        # Board Container
        board_container = QFrame()
        board_container.setObjectName("card")
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(Design.SPACING['sm'], Design.SPACING['sm'], Design.SPACING['sm'], Design.SPACING['sm'])

        rotate_layout = QHBoxLayout()
        rotate_layout.addStretch()
        self.rotate_btn = QPushButton("⟲ Rotate Board")
        self.rotate_btn.setFixedHeight(28)
        self.rotate_btn.setFont(QFont('Segoe UI', 11))
        self.rotate_btn.setCursor(Qt.PointingHandCursor)
        self.rotate_btn.clicked.connect(self.toggle_board_flip)
        rotate_layout.addWidget(self.rotate_btn)
        board_layout.addLayout(rotate_layout)

        self.board_widget = ChessBoardWidget(self)
        piece_set = self.settings.get('piece_set', 'free')
        self.board_widget.load_piece_set(piece_set)
        self.board_widget.set_board(self.controller.state.board)
        self.board_widget.move_made.connect(self.on_move_made)
        board_layout.addWidget(self.board_widget)
        left_panel.addWidget(board_container)

        # Actions Row
        action_layout = QHBoxLayout()
        action_layout.setSpacing(Design.SPACING['sm'])

        self.new_btn = QPushButton("New")
        self.new_btn.setObjectName("primary")
        self.new_btn.setFixedHeight(Design.BUTTON_HEIGHT)
        self.new_btn.setCursor(Qt.PointingHandCursor)
        self.new_btn.clicked.connect(self.on_new_game)
        action_layout.addWidget(self.new_btn)

        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setFixedHeight(Design.BUTTON_HEIGHT)
        self.pause_btn.setCursor(Qt.PointingHandCursor)
        self.pause_btn.clicked.connect(self.on_pause_clicked)
        action_layout.addWidget(self.pause_btn)

        self.two_player_btn = QPushButton("👥 2P")
        self.two_player_btn.setFixedHeight(Design.BUTTON_HEIGHT)
        self.two_player_btn.setCursor(Qt.PointingHandCursor)
        self.two_player_btn.clicked.connect(self.on_two_player_clicked)
        action_layout.addWidget(self.two_player_btn)

        self.settings_btn = QPushButton("⚙ Settings")
        self.settings_btn.setFixedHeight(Design.BUTTON_HEIGHT)
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.clicked.connect(self.go_to_settings)
        action_layout.addWidget(self.settings_btn)

        self.menu_btn = QPushButton("Menu")
        self.menu_btn.setFixedHeight(Design.BUTTON_HEIGHT)
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.clicked.connect(self.go_to_menu)
        action_layout.addWidget(self.menu_btn)

        action_layout.addStretch()

        self.host_btn = QPushButton("Host")
        self.host_btn.setFixedHeight(32)
        self.host_btn.setFixedWidth(62)
        self.host_btn.setCursor(Qt.PointingHandCursor)
        self.host_btn.clicked.connect(self.on_host_clicked)
        action_layout.addWidget(self.host_btn)

        self.join_btn = QPushButton("Join")
        self.join_btn.setFixedHeight(32)
        self.join_btn.setFixedWidth(62)
        self.join_btn.setCursor(Qt.PointingHandCursor)
        self.join_btn.clicked.connect(self.on_join_clicked)
        action_layout.addWidget(self.join_btn)

        self.network_status_label = StatusChip("● Offline", "offline", self)
        action_layout.addWidget(self.network_status_label)

        action_layout.addStretch()

        self.resign_btn = QPushButton("Resign")
        self.resign_btn.setObjectName("danger")
        self.resign_btn.setFixedHeight(32)
        self.resign_btn.setCursor(Qt.PointingHandCursor)
        self.resign_btn.clicked.connect(self.on_resign_clicked)
        action_layout.addWidget(self.resign_btn)

        self.draw_btn = QPushButton("Draw")
        self.draw_btn.setFixedHeight(32)
        self.draw_btn.setCursor(Qt.PointingHandCursor)
        self.draw_btn.clicked.connect(self.on_draw_clicked)
        action_layout.addWidget(self.draw_btn)

        left_panel.addLayout(action_layout)

        # RIGHT PANEL
        right_panel = QVBoxLayout()
        right_panel.setSpacing(Design.SPACING['md'])

        # Tab widget: History | Lessons
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                background: {self.theme['surface']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
            }}
            QTabBar::tab {{
                background: {self.theme['surface']};
                color: {self.theme['text_secondary']};
                padding: 6px 14px;
                border-top-left-radius: {Design.RADIUS['sm']}px;
                border-top-right-radius: {Design.RADIUS['sm']}px;
            }}
            QTabBar::tab:selected {{
                background: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
            QTabBar::tab:hover {{
                background: {self.theme['surface_hover']};
            }}
        """)

        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(0)

        hist_header = QHBoxLayout()
        hist_title = QLabel("Moves")
        hist_title.setFont(QFont('Segoe UI', Design.FONT['h2'], QFont.Bold))
        hist_title.setStyleSheet(f"color: {self.theme['text_primary']};")
        hist_header.addWidget(hist_title)
        self.history_count = QLabel("0")
        self.history_count.setFont(QFont('Segoe UI', Design.FONT['body']))
        self.history_count.setStyleSheet(f"color: {self.theme['text_muted']};")
        hist_header.addWidget(self.history_count)
        hist_header.addStretch()
        history_layout.addLayout(hist_header)

        # Use QTableWidget for better history display
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["#", "White", "Black"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SingleSelection)
        self.history_table.setStyleSheet(f"""
            QTableWidget {{
                background: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                gridline-color: {self.theme['divider']};
                font-size: {Design.FONT['body']}px;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {self.theme['divider']};
            }}
            QTableWidget::item:selected {{
                background: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
            QHeaderView::section {{
                background: {self.theme['surface']};
                color: {self.theme['text_muted']};
                padding: 4px;
                border: none;
                font-weight: bold;
            }}
        """)
        self.history_table.itemClicked.connect(self.on_history_item_clicked)
        history_layout.addWidget(self.history_table)

        self.history_empty = QLabel("♟\n\nNo moves yet\nMake your first move")
        self.history_empty.setAlignment(Qt.AlignCenter)
        self.history_empty.setFont(QFont('Segoe UI', Design.FONT['body']))
        self.history_empty.setStyleSheet(f"color: {self.theme['text_muted']};")
        history_layout.addWidget(self.history_empty)

        self.tab_widget.addTab(history_tab, "History")

        # Lessons tab
        self.lessons_widget = LessonsWidget(self, self.main_window)
        self.tab_widget.addTab(self.lessons_widget, "Lessons")

        right_panel.addWidget(self.tab_widget)

        # Ad
        self.ad_frame = QFrame()
        self.ad_frame.setObjectName("card")
        self.ad_frame.setStyleSheet(f"""
            QFrame#card {{
                background-color: {self.theme['bg_secondary']};
                border-radius: {Design.RADIUS['md']}px;
                padding: 2px 14px;
            }}
        """)
        self.ad_frame.setVisible(not self.settings.get('ads_removed', False))
        ad_layout = QHBoxLayout(self.ad_frame)
        self.ad_label = QLabel(self.ad_links[0][0])
        self.ad_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-weight: 500;")
        self.ad_label.setCursor(Qt.PointingHandCursor)
        self.ad_label.mousePressEvent = lambda e: webbrowser.open(self.ad_links[self.ad_index][1])
        ad_layout.addWidget(self.ad_label)
        ad_sponsor = QLabel("Sponsored")
        ad_sponsor.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 11px;")
        ad_layout.addWidget(ad_sponsor, alignment=Qt.AlignRight)
        right_panel.addWidget(self.ad_frame)

        if not self.settings.get('ads_removed', False):
            self.ad_timer = QTimer(self)
            self.ad_timer.timeout.connect(self.rotate_ad)
            self.ad_timer.start(10000)

        right_panel.addStretch()
        main_layout.addLayout(left_panel, stretch=2)
        main_layout.addLayout(right_panel, stretch=1)

        self.toast_widget = Toast(self, "", 2800, "info")
        self.toast_widget.hide()

        if self.settings.get('flipped', False):
            self.board_widget.set_flipped(True)

    def rotate_ad(self):
        self.ad_index = (self.ad_index + 1) % len(self.ad_links)
        if self.ad_label:
            self.ad_label.setText(self.ad_links[self.ad_index][0])
            self.ad_label.mousePressEvent = lambda e: webbrowser.open(self.ad_links[self.ad_index][1])

    # ---------- UI Callbacks ----------
    def on_move_made(self, move):
        self.controller.make_move(move)

    def on_pause_clicked(self):
        self.controller.toggle_pause()
        if self.controller.paused:
            self.pause_btn.setText("▶ Resume")
        else:
            self.pause_btn.setText("⏸ Pause")

    def on_two_player_clicked(self):
        self.controller.toggle_two_player()
        if self.controller.two_player_mode:
            self.two_player_btn.setStyleSheet(f"background-color: {self.theme['accent']}; color: #080812;")
        else:
            self.two_player_btn.setStyleSheet("")

    def on_new_game(self):
        self.controller.reset_board(notify_peer=True)
        self.pause_btn.setText("⏸ Pause")

    def on_host_clicked(self):
        self.controller.host_game()

    def on_join_clicked(self):
        dlg = LANDialog(self, 'join')
        if dlg.exec_() == QDialog.Accepted and dlg.ip:
            self.controller.join_game(dlg.ip)

    def on_resign_clicked(self):
        if self.controller.game_over:
            return
        PremiumDialog(self, "Resign", "Are you sure you want to resign?", "resign")

    def on_draw_clicked(self):
        self.controller.offer_draw()

    def go_to_settings(self):
        self.controller.settings_open = True
        self.controller.stop_timer()
        self.board_widget.cancel_animation()
        self.main_window.switch_to_settings(from_game=True)

    def go_to_menu(self):
        if not self.controller.game_over and len(self.controller.state.move_stack) > 0:
            reply = QMessageBox.question(self, "Leave Game", "Are you sure you want to leave? Current game will be lost.", QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
        self.controller.cleanup()
        self.main_window.switch_to_menu()

    def toggle_board_flip(self):
        self.board_widget.toggle_flipped()
        self.settings['flipped'] = self.board_widget.flipped
        save_settings(self.settings)

    def on_board_flipped(self, flipped: bool):
        self.board_widget.set_flipped(flipped)
        self.settings['flipped'] = flipped
        save_settings(self.settings)

    # ---------- History Table Methods ----------
    def on_history_item_clicked(self, item):
        row = item.row()
        move_index = row * 2
        if item.column() == 2:
            move_index += 1
        if move_index >= len(self.controller.state.move_stack):
            return
        self.show_move_at_index(move_index)

    def show_move_at_index(self, index):
        """Restore board to position before move at given index and highlight that move."""
        board = chess.Board()
        for i in range(index):
            board.push(self.controller.state.move_stack[i])
        self.board_widget.set_board(board)
        if index > 0:
            last_move = self.controller.state.move_stack[index - 1]
            from_sq = last_move.from_square
            to_sq = last_move.to_square
            # For castling, we want to highlight both king and rook squares
            if board.is_castling(last_move):
                # Find the rook involved
                # For kingside castling: from_sq is king (e1 or e8), to_sq is g1 or g8
                # Rook moves from h1/h8 to f1/f8
                if to_sq in (chess.G1, chess.G8):
                    rook_from = chess.H1 if to_sq == chess.G1 else chess.H8
                    rook_to = chess.F1 if to_sq == chess.G1 else chess.F8
                    self.board_widget.set_last_move((from_sq, to_sq))
                    # Store both king and rook moves for highlight
                    # Our board widget supports only one last_move, but we can store tuple of tuples
                    # For simplicity, we set last_move to (from_sq, to_sq) and separately indicate castling
                    # But we want both pieces highlighted, so we store both squares in last_move as a tuple of four
                    self.board_widget.last_move = (from_sq, to_sq, rook_from, rook_to)
                else:
                    rook_from = chess.A1 if to_sq == chess.C1 else chess.A8
                    rook_to = chess.D1 if to_sq == chess.C1 else chess.D8
                    self.board_widget.set_last_move((from_sq, to_sq))
                    self.board_widget.last_move = (from_sq, to_sq, rook_from, rook_to)
            else:
                self.board_widget.set_last_move((from_sq, to_sq))
        else:
            self.board_widget.set_last_move(None)
        self.board_widget.update()

    # ---------- UI Update Methods ----------
    def update_board(self):
        self.board_widget.set_board(self.controller.state.board)
        self.board_widget.set_selected(self.controller.selected_square)
        self.board_widget.set_legal_moves(self.controller.legal_moves)
        self.board_widget.set_last_move(self.controller.last_move)
        self.update_status()
        self.update_player_cards()

    def update_history(self):
        self.history_table.setRowCount(0)
        if not self.controller.state.move_history:
            self.history_empty.setVisible(True)
            self.history_table.setVisible(False)
            return
        self.history_empty.setVisible(False)
        self.history_table.setVisible(True)

        moves = self.controller.state.move_history
        row_count = (len(moves) + 1) // 2
        self.history_table.setRowCount(row_count)

        for i in range(row_count):
            # Number
            item_num = QTableWidgetItem(str(i + 1))
            item_num.setTextAlignment(Qt.AlignCenter)
            item_num.setForeground(QColor(self.theme['text_muted']))
            self.history_table.setItem(i, 0, item_num)

            # White move
            white_move = moves[i*2] if i*2 < len(moves) else ""
            item_white = QTableWidgetItem(white_move)
            item_white.setTextAlignment(Qt.AlignCenter)
            if white_move:
                item_white.setForeground(QColor(self.theme['text_primary']))
            self.history_table.setItem(i, 1, item_white)

            # Black move
            black_move = moves[i*2+1] if i*2+1 < len(moves) else ""
            item_black = QTableWidgetItem(black_move)
            item_black.setTextAlignment(Qt.AlignCenter)
            if black_move:
                item_black.setForeground(QColor(self.theme['text_primary']))
            self.history_table.setItem(i, 2, item_black)

        # Scroll to bottom
        self.history_table.scrollToBottom()

    def update_player_cards(self):
        if self.controller.paused:
            return
        w_time, b_time = self.controller.get_timer_times()
        w_min, w_sec = divmod(int(w_time), 60)
        b_min, b_sec = divmod(int(b_time), 60)
        self.white_time_label.setText(f"{w_min:02d}:{w_sec:02d}")
        self.black_time_label.setText(f"{b_min:02d}:{b_sec:02d}")

        if not self.controller.paused:
            if self.controller.state.board.turn == chess.WHITE:
                self.white_time_label.setStyleSheet(f"color: {self.theme['accent']}; font-weight: bold;")
                self.black_time_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
            else:
                self.white_time_label.setStyleSheet(f"color: {self.theme['text_secondary']};")
                self.black_time_label.setStyleSheet(f"color: {self.theme['accent']}; font-weight: bold;")
        if w_time < 30 and w_time > 0:
            self.white_time_label.setStyleSheet(f"color: {self.theme['danger']}; font-weight: bold;")
        if b_time < 30 and b_time > 0:
            self.black_time_label.setStyleSheet(f"color: {self.theme['danger']}; font-weight: bold;")

    def update_status(self):
        if self.controller.paused:
            self.white_status.setText("⏸ Paused")
            self.white_status.setStyleSheet(f"color: {self.theme['warning']};")
            self.black_status.setText("⏸ Paused")
            self.black_status.setStyleSheet(f"color: {self.theme['warning']};")
            return
        if self.controller.state.board.turn == chess.WHITE:
            self.white_status.setText("● Your turn")
            self.white_status.setStyleSheet(f"color: {self.theme['accent']};")
            self.black_status.setText("● Waiting")
            self.black_status.setStyleSheet(f"color: {self.theme['text_muted']};")
        else:
            self.white_status.setText("● Waiting")
            self.white_status.setStyleSheet(f"color: {self.theme['text_muted']};")
            if self.controller.ai_thinking:
                self.black_status.setText("● Thinking...")
                self.black_status.setStyleSheet(f"color: {self.theme['warning']};")
            else:
                self.black_status.setText("● Your turn")
                self.black_status.setStyleSheet(f"color: {self.theme['accent']};")

    def show_game_over(self, title: str, message: str):
        PremiumDialog(self, title, message, "close")

    def show_toast(self, message: str, type_: str = "info"):
        if self.toast_widget:
            self.toast_widget.label.setText(message)
            self.toast_widget.type = type_
            self.toast_widget._update_style()
            self.toast_widget.show_toast()

    def closeEvent(self, event):
        self.controller.cleanup()
        if self.ad_timer:
            self.ad_timer.stop()
        event.accept()


# ============================================================================
# SETTINGS SCREEN
# ============================================================================
class SettingsScreen(QWidget):
    def __init__(self, main_window, from_game=False):
        super().__init__(main_window)
        self.main_window = main_window
        self.settings = main_window.settings
        self.theme = main_window.theme
        self.from_game = from_game
        self.current_page = 0
        self.setup_ui()

    def setup_ui(self):
        if self.layout():
            old = self.layout()
            while old.count():
                item = old.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    while item.layout().count():
                        child = item.layout().takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    item.layout().deleteLater()
            QWidget().setLayout(old)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg']};
                color: {self.theme['text_primary']};
                font-family: 'Segoe UI', sans-serif;
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 5px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.theme['text_muted']};
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {self.theme['text_secondary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        sidebar_widget = QFrame()
        sidebar_widget.setFixedWidth(240)
        sidebar_widget.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme['bg_secondary']};
                border-right: 1px solid {self.theme['divider']};
            }}
        """)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(Design.SPACING['md'], Design.SPACING['lg'], Design.SPACING['md'], Design.SPACING['lg'])
        sidebar_layout.setSpacing(Design.SPACING['sm'])

        search_box = QLineEdit()
        search_box.setPlaceholderText("Search settings...")
        search_box.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['card_border']};
                border-radius: {Design.RADIUS['md']}px;
                padding: 8px 14px;
                font-size: {Design.FONT['body']}px;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.theme['accent']};
            }}
        """)
        search_box.textChanged.connect(self.filter_sidebar)
        sidebar_layout.addWidget(search_box)

        self.sidebar_list = QListWidget()
        self.sidebar_list.setFixedWidth(220)
        self.sidebar_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                outline: none;
                font-size: {Design.FONT['body']}px;
                padding: 4px 0;
            }}
            QListWidget::item {{
                padding: 8px 14px;
                border-radius: {Design.RADIUS['sm']}px;
                margin: 2px 0;
                color: {self.theme['text_secondary']};
            }}
            QListWidget::item:hover {{
                background-color: {self.theme['surface_hover']};
                color: {self.theme['text_primary']};
            }}
            QListWidget::item:selected {{
                background-color: {self.theme['surface_active']};
                color: {self.theme['text_primary']};
                border-left: 3px solid {self.theme['accent']};
                padding-left: 11px;
            }}
        """)
        self.sidebar_data = [
            {"id": 0, "label": "Gameplay", "icon": "🎮", "color": "#4A90D9"},
            {"id": 1, "label": "Appearance", "icon": "🎨", "color": "#9B59B6"},
            {"id": 2, "label": "Audio", "icon": "🔊", "color": "#2ECC71"},
            {"id": 3, "label": "Premium", "icon": "✦", "color": "#F1C40F"},
            {"id": 4, "label": "Ads", "icon": "📢", "color": "#95A5A6"},
            {"id": 5, "label": "About", "icon": "ℹ", "color": "#5DADE2"},
        ]
        for item in self.sidebar_data:
            list_item = QListWidgetItem(f"{item['icon']}  {item['label']}")
            list_item.setData(Qt.UserRole, item['id'])
            self.sidebar_list.addItem(list_item)
        self.sidebar_list.setCurrentRow(0)
        self.sidebar_list.currentRowChanged.connect(self.switch_page)
        sidebar_layout.addWidget(self.sidebar_list)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar_widget)

        # CONTENT AREA
        content_widget = QFrame()
        content_widget.setStyleSheet(f"background-color: {self.theme['bg']};")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(Design.SPACING['xl'], Design.SPACING['lg'], Design.SPACING['xl'], Design.SPACING['lg'])
        content_layout.setSpacing(Design.SPACING['md'])

        header_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.theme['text_secondary']};
                border: none;
                padding: 6px 12px;
                font-size: {Design.FONT['body']}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                color: {self.theme['text_primary']};
                background-color: {self.theme['surface_hover']};
                border-radius: {Design.RADIUS['sm']}px;
            }}
        """)
        self.back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(self.back_btn)
        header_layout.addStretch()

        self.page_title = QLabel("GAMEPLAY")
        self.page_title.setFont(QFont('Segoe UI', Design.FONT['h2'], QFont.Bold))
        self.page_title.setStyleSheet(f"color: {self.theme['text_primary']};")
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")
        content_layout.addWidget(self.content_stack)

        self.pages = {}
        self.pages[0] = self.create_gameplay_page()
        self.pages[1] = self.create_appearance_page()
        self.pages[2] = self.create_audio_page()
        self.pages[3] = self.create_premium_page()
        self.pages[4] = self.create_ads_page()
        self.pages[5] = self.create_about_page()

        for idx, page in self.pages.items():
            self.content_stack.addWidget(page)
        self.content_stack.setCurrentIndex(0)

        main_layout.addWidget(content_widget, stretch=1)

    def filter_sidebar(self, text):
        text = text.lower()
        for i in range(self.sidebar_list.count()):
            item = self.sidebar_list.item(i)
            item.setHidden(text not in item.text().lower())

    def switch_page(self, index):
        if index < 0:
            return
        self.current_page = index
        self.page_title.setText(self.sidebar_data[index]['label'].upper())
        anim = QPropertyAnimation(self.content_stack, b"windowOpacity")
        anim.setDuration(150)
        anim.setStartValue(0.5)
        anim.setEndValue(1.0)
        self.content_stack.setCurrentIndex(index)
        anim.start()

    def _create_card(self):
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QFrame#card {{
                background-color: {self.theme['surface']};
                border-radius: {Design.RADIUS['lg']}px;
                padding: 16px 24px;
                border: 1px solid {self.theme['card_border']};
            }}
        """)
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        return card

    def _divider(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setStyleSheet(f"background-color: {self.theme['divider']}; max-height: 1px; margin: 4px 0;")
        return frame

    def create_gameplay_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['md'])

        title = QLabel("GAMEPLAY")
        title.setFont(QFont('Segoe UI', Design.FONT['small'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['text_muted']}; letter-spacing: 1.5px;")
        card_layout.addWidget(title)

        # Difficulty
        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Difficulty")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("How challenging the AI should be")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()

        diff_container = QFrame()
        diff_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme['surface']};
                border-radius: {Design.RADIUS['full']}px;
                padding: 3px;
            }}
        """)
        diff_layout = QHBoxLayout(diff_container)
        diff_layout.setSpacing(3)
        diff_layout.setContentsMargins(3, 3, 3, 3)

        diff_group = QButtonGroup(self)
        diff_group.setExclusive(True)

        for level in ['Easy', 'Medium', 'Hard']:
            btn = QPushButton(level)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self.theme['text_secondary']};
                    border: none;
                    border-radius: {Design.RADIUS['full']}px;
                    padding: 4px 16px;
                    font-size: {Design.FONT['body']}px;
                    font-weight: 500;
                }}
                QPushButton:checked {{
                    background-color: {self.theme['accent']};
                    color: #080812;
                }}
                QPushButton:hover:!checked {{
                    background-color: {self.theme['surface_hover']};
                }}
            """)
            if level.lower() == self.settings.get('ai_level', 'easy'):
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, l=level: self.save_level(l))
            diff_group.addButton(btn)
            diff_layout.addWidget(btn)
        row.addWidget(diff_container)
        card_layout.addLayout(row)
        card_layout.addWidget(self._divider())

        # Time Control
        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Time Control")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Time per player for the game")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()

        time_container = QFrame()
        time_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme['surface']};
                border-radius: {Design.RADIUS['full']}px;
                padding: 3px;
            }}
        """)
        time_layout = QHBoxLayout(time_container)
        time_layout.setSpacing(3)
        time_layout.setContentsMargins(3, 3, 3, 3)

        time_group = QButtonGroup(self)
        time_group.setExclusive(True)

        for t in ['3 min', '5 min', '10 min']:
            btn = QPushButton(t)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {self.theme['text_secondary']};
                    border: none;
                    border-radius: {Design.RADIUS['full']}px;
                    padding: 4px 16px;
                    font-size: {Design.FONT['body']}px;
                    font-weight: 500;
                }}
                QPushButton:checked {{
                    background-color: {self.theme['accent']};
                    color: #080812;
                }}
                QPushButton:hover:!checked {{
                    background-color: {self.theme['surface_hover']};
                }}
            """)
            if t == str(self.settings.get('timer_minutes', 3)) + ' min':
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, time=t: self.save_timer(time))
            time_group.addButton(btn)
            time_layout.addWidget(btn)
        row.addWidget(time_container)
        card_layout.addLayout(row)
        card_layout.addWidget(self._divider())

        # Sound
        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Sound")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Enable game sounds")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()
        switch = AnimatedToggle(self)
        switch.setChecked(self.main_window.sound_manager.sound_enabled)
        switch.toggled.connect(self.toggle_sound)
        row.addWidget(switch)
        card_layout.addLayout(row)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def create_appearance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['md'])

        title = QLabel("THEME")
        title.setFont(QFont('Segoe UI', Design.FONT['small'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['text_muted']}; letter-spacing: 1.5px;")
        card_layout.addWidget(title)

        theme_names = ['Dark', 'Light', 'Classic']
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(Design.SPACING['md'])
        for t in theme_names:
            tile = QFrame()
            tile.setFixedSize(130, 80)
            is_active = t.lower() == self.settings.get('theme', 'dark')
            tile.setStyleSheet(f"""
                QFrame {{
                    background-color: {THEMES[t.lower()]['surface']};
                    border: 2px solid {'transparent' if not is_active else self.theme['accent']};
                    border-radius: {Design.RADIUS['md']}px;
                    cursor: pointer;
                }}
                QFrame:hover {{
                    border: 2px solid {self.theme['accent']};
                }}
            """)
            tile.setToolTip(t)
            tile.mousePressEvent = lambda e, theme=t: self.save_theme(theme.lower())
            mini_layout = QVBoxLayout(tile)
            mini_layout.setContentsMargins(8, 8, 8, 8)
            mini = QLabel("♔ ♚")
            mini.setAlignment(Qt.AlignCenter)
            mini.setStyleSheet(f"color: {THEMES[t.lower()]['text_primary']}; font-size: 18px;")
            mini_layout.addWidget(mini)
            name_lbl = QLabel(t)
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"color: {THEMES[t.lower()]['text_secondary']}; font-size: 11px; font-weight: bold;")
            mini_layout.addWidget(name_lbl)
            theme_layout.addWidget(tile)
        card_layout.addLayout(theme_layout)
        card_layout.addWidget(self._divider())

        # Piece Set
        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Piece Set")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Premium sets available with VIP")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()

        self.piece_set_combo = QComboBox()
        self.piece_set_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['card_border']};
                border-radius: {Design.RADIUS['sm']}px;
                padding: 6px 12px;
                min-height: 32px;
                font-size: {Design.FONT['body']}px;
            }}
            QComboBox:hover {{ border-color: {self.theme['accent']}; }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                selection-background-color: {self.theme['surface_hover']};
                selection-color: {self.theme['text_primary']};
                border: none;
            }}
        """)
        self.piece_set_combo.blockSignals(True)
        self.update_piece_set_combo()
        self.piece_set_combo.blockSignals(False)
        self.piece_set_combo.currentIndexChanged.connect(self.save_piece_set)
        self.piece_set_combo.setFixedWidth(180)
        row.addWidget(self.piece_set_combo)
        card_layout.addLayout(row)

        card_layout.addWidget(self._divider())

        # Flip Board
        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Always flip for Black")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Auto-rotate board when playing as Black")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()
        flip_switch = AnimatedToggle(self)
        flip_switch.setChecked(self.settings.get('flipped', False))
        flip_switch.toggled.connect(self.save_flip)
        row.addWidget(flip_switch)
        card_layout.addLayout(row)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def update_piece_set_combo(self):
        self.piece_set_combo.clear()
        sets, order = ChessBoardWidget.discover_sets()
        if 'free' in sets:
            self.piece_set_combo.addItem("Classic", "free")
        if self.settings.get('vip', False):
            for set_id in order:
                if set_id != 'free':
                    self.piece_set_combo.addItem(f"Set {set_id}", set_id)
        current = self.settings.get('piece_set', 'free')
        idx = self.piece_set_combo.findData(current)
        if idx >= 0:
            self.piece_set_combo.setCurrentIndex(idx)

    def save_piece_set(self, index):
        data = self.piece_set_combo.currentData()
        if data:
            self.settings['piece_set'] = data
            save_settings(self.settings)
            if self.main_window.game_screen:
                self.main_window.game_screen.board_widget.load_piece_set(data)
                self.main_window.game_screen.update_board()

    def save_flip(self, enabled):
        self.settings['flipped'] = enabled
        save_settings(self.settings)
        if self.main_window.game_screen:
            self.main_window.game_screen.board_widget.set_flipped(enabled)

    def create_audio_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['md'])

        title = QLabel("AUDIO")
        title.setFont(QFont('Segoe UI', Design.FONT['small'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['text_muted']}; letter-spacing: 1.5px;")
        card_layout.addWidget(title)

        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Sound Effects")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Enable all game sounds")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()
        switch = AnimatedToggle(self)
        switch.setChecked(self.main_window.sound_manager.sound_enabled)
        switch.toggled.connect(self.toggle_sound)
        row.addWidget(switch)
        card_layout.addLayout(row)
        card_layout.addWidget(self._divider())

        row = QHBoxLayout()
        col = QVBoxLayout()
        lbl = QLabel("Master Volume")
        lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
        col.addWidget(lbl)
        desc = QLabel("Overall sound level")
        desc.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
        col.addWidget(desc)
        row.addLayout(col)
        row.addStretch()
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.settings.get('volume', 0.8) * 100))
        self.volume_slider.setFixedWidth(160)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_label = QLabel(f"{int(self.settings.get('volume', 0.8) * 100)}%")
        self.volume_label.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px; font-weight: 600; min-width: 40px;")
        row.addWidget(self.volume_slider)
        row.addWidget(self.volume_label)
        card_layout.addLayout(row)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def create_premium_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card.setStyleSheet(f"""
            QFrame#card {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 {self.theme['surface']},
                                            stop:1 {self.theme['surface_hover']});
                border: 1px solid {self.theme['accent']};
                border-radius: {Design.RADIUS['lg']}px;
                padding: 24px 28px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['md'])

        title = QLabel("✦ PREMIUM")
        title.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['accent']};")
        card_layout.addWidget(title)

        desc = QLabel("Unlock the complete chess experience")
        desc.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px;")
        card_layout.addWidget(desc)

        card_layout.addSpacing(Design.SPACING['sm'])

        features = [
            {"label": "Two Player Mode", "icon": "👥", "desc": "Play with friends on the same device"},
            {"label": "LAN Multiplayer", "icon": "🌐", "desc": "Connect and play over local network"},
            {"label": "Premium Piece Sets", "icon": "♛", "desc": "7 exclusive piece styles"},
            {"label": "Ad-Free Experience", "icon": "🚫", "desc": "No interruptions while playing"},
        ]
        for f in features:
            f_layout = QHBoxLayout()
            icon_lbl = QLabel(f["icon"])
            icon_lbl.setStyleSheet(f"font-size: 20px; min-width: 32px;")
            f_layout.addWidget(icon_lbl)
            col = QVBoxLayout()
            lbl = QLabel(f["label"])
            lbl.setStyleSheet(f"color: {self.theme['text_primary']}; font-size: {Design.FONT['body']}px; font-weight: 600;")
            col.addWidget(lbl)
            desc_lbl = QLabel(f["desc"])
            desc_lbl.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['small']}px;")
            col.addWidget(desc_lbl)
            f_layout.addLayout(col)
            f_layout.addStretch()
            card_layout.addLayout(f_layout)

        card_layout.addSpacing(Design.SPACING['md'])

        status_layout = QHBoxLayout()
        status_layout.addStretch()
        status_text = "ACTIVE ✅" if self.settings.get('vip', False) else "FREE"
        status_color = self.theme['accent'] if self.settings.get('vip', False) else self.theme['text_muted']
        status_badge = QLabel(status_text)
        status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color}22;
                color: {status_color};
                border: 1px solid {status_color};
                border-radius: {Design.RADIUS['full']}px;
                padding: 4px 16px;
                font-size: {Design.FONT['body']}px;
                font-weight: 600;
            }}
        """)
        status_layout.addWidget(status_badge)
        status_layout.addStretch()
        card_layout.addLayout(status_layout)

        if not self.settings.get('vip', False):
            price_layout = QHBoxLayout()
            price_layout.addStretch()
            price = QLabel("$2.99")
            price.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
            price.setStyleSheet(f"color: {self.theme['accent']};")
            price_layout.addWidget(price)
            price_layout.addStretch()
            card_layout.addLayout(price_layout)

            btn = QPushButton("Upgrade Now")
            btn.setObjectName("primary")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton#primary {{
                    background-color: {self.theme['accent']};
                    color: #080812;
                    border: none;
                    border-radius: {Design.RADIUS['md']}px;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: {Design.FONT['body']}px;
                }}
                QPushButton#primary:hover {{
                    background-color: {self.theme['accent_light']};
                }}
            """)
            btn.clicked.connect(self.upgrade_vip)
            card_layout.addWidget(btn)

            restore_btn = QPushButton("Restore Purchase")
            restore_btn.setCursor(Qt.PointingHandCursor)
            restore_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {self.theme['text_muted']};
                    border: none;
                    font-size: {Design.FONT['small']}px;
                    padding: 4px;
                }}
                QPushButton:hover {{
                    color: {self.theme['text_secondary']};
                }}
            """)
            restore_btn.clicked.connect(self.restore_purchase)
            card_layout.addWidget(restore_btn, alignment=Qt.AlignCenter)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def restore_purchase(self):
        if self.settings.get('vip', False):
            QMessageBox.information(self, "Restore", "Your premium status is already active.")
        else:
            QMessageBox.information(self, "Restore", "No previous purchase found.")

    def create_ads_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['md'])

        title = QLabel("ADVERTISEMENTS")
        title.setFont(QFont('Segoe UI', Design.FONT['small'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['text_muted']}; letter-spacing: 1.5px;")
        card_layout.addWidget(title)

        status_layout = QHBoxLayout()
        status_text = "REMOVED ✅" if self.settings.get('ads_removed', False) else "ACTIVE"
        status_color = self.theme['success'] if self.settings.get('ads_removed', False) else self.theme['warning']
        status_badge = QLabel(status_text)
        status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color}22;
                color: {status_color};
                border: 1px solid {status_color};
                border-radius: {Design.RADIUS['full']}px;
                padding: 4px 16px;
                font-size: {Design.FONT['body']}px;
                font-weight: 600;
            }}
        """)
        status_layout.addWidget(status_badge)
        status_layout.addStretch()
        card_layout.addLayout(status_layout)

        if not self.settings.get('ads_removed', False):
            btn = QPushButton("Remove Ads $1.99")
            btn.setObjectName("primary")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton#primary {{
                    background-color: {self.theme['accent']};
                    color: #080812;
                    border: none;
                    border-radius: {Design.RADIUS['md']}px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: {Design.FONT['body']}px;
                }}
                QPushButton#primary:hover {{
                    background-color: {self.theme['accent_light']};
                }}
            """)
            btn.clicked.connect(self.remove_ads)
            card_layout.addWidget(btn)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(Design.SPACING['lg'])

        card = self._create_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(Design.SPACING['sm'])
        card_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("♛ CHESS")
        title.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['accent']};")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        info = [
            "Version 0.3.0",
            "Built with PyQt5 & python-chess",
            "2025 — All Rights Reserved",
            "",
            "♔ Strategy • Intelligence • Victory ♚"
        ]
        for line in info:
            lbl = QLabel(line)
            lbl.setAlignment(Qt.AlignCenter)
            if line.startswith("♔"):
                lbl.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: {Design.FONT['body']}px; font-style: italic;")
            else:
                lbl.setStyleSheet(f"color: {self.theme['text_secondary']}; font-size: {Design.FONT['body']}px;")
            card_layout.addWidget(lbl)

        layout.addWidget(card)
        layout.addStretch()
        return page

    def save_theme(self, theme):
        self.settings['theme'] = theme
        save_settings(self.settings)
        self.main_window.apply_theme(theme)
        self.setStyleSheet(self.get_stylesheet())

    def save_level(self, level):
        level_lower = level.lower()
        self.settings['ai_level'] = level_lower
        save_settings(self.settings)
        if self.main_window.game_screen:
            self.main_window.game_screen.controller.set_level(level_lower)

    def save_timer(self, timer):
        minutes = int(timer.split()[0])
        self.settings['timer_minutes'] = minutes
        save_settings(self.settings)
        if self.main_window.game_screen:
            self.main_window.game_screen.controller.set_timer_minutes(minutes)
            self.main_window.game_screen.update_player_cards()

    def toggle_sound(self, enabled):
        self.main_window.sound_manager.sound_enabled = enabled
        self.settings['sound'] = enabled
        save_settings(self.settings)

    def change_volume(self, value):
        volume = value / 100.0
        self.main_window.sound_manager.set_volume(volume)
        self.settings['volume'] = volume
        save_settings(self.settings)
        self.volume_label.setText(f"{value}%")

    def upgrade_vip(self):
        reply = QMessageBox.question(self, "VIP Upgrade", "Upgrade to VIP for $2.99?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.settings['vip'] = True
            save_settings(self.settings)
            self.main_window.settings = self.settings
            if self.main_window.game_screen:
                self.main_window.game_screen.controller.vip = True
                self.main_window.game_screen.vip = True
            self.piece_set_combo.blockSignals(True)
            self.update_piece_set_combo()
            self.piece_set_combo.blockSignals(False)
            self.setup_ui()

    def remove_ads(self):
        reply = QMessageBox.question(self, "Remove Ads", "Remove ads for $1.99?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.main_window.game_screen and self.main_window.game_screen.ad_timer:
                self.main_window.game_screen.ad_timer.stop()
            self.settings['ads_removed'] = True
            save_settings(self.settings)
            self.main_window.settings = self.settings
            if self.main_window.game_screen:
                self.main_window.game_screen.ad_frame.setVisible(False)
                if self.main_window.game_screen.ad_timer:
                    self.main_window.game_screen.ad_timer.stop()
                self.main_window.game_screen.settings = self.main_window.settings
            self.setup_ui()
        else:
            if self.main_window.game_screen and self.main_window.game_screen.ad_timer:
                if not self.main_window.game_screen.ad_timer.isActive():
                    self.main_window.game_screen.ad_timer.start(10000)

    def go_back(self):
        if self.from_game and self.main_window.game_screen:
            self.main_window.game_screen.controller.settings_open = False
            self.main_window.game_screen.controller.start_timer()
            self.main_window.game_screen.update_board()
        self.main_window.switch_to_menu() if not self.from_game else self.main_window.switch_to_game()


# ============================================================================
# MAIN MENU
# ============================================================================
class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.theme = main_window.theme
        self.setup_ui()

    def setup_ui(self):
        if self.layout():
            old = self.layout()
            while old.count():
                item = old.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    while item.layout().count():
                        child = item.layout().takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    item.layout().deleteLater()
            QWidget().setLayout(old)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['bg']};
            }}
            QPushButton {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {self.theme['surface_hover']};
            }}
            QPushButton#primary {{
                background-color: {self.theme['accent']};
                color: #080812;
            }}
            QPushButton#primary:hover {{
                background-color: {self.theme['accent_light']};
            }}
            QPushButton#danger {{
                background-color: {self.theme['danger']};
                color: white;
            }}
            QPushButton#danger:hover {{
                background-color: #FF7A85;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(Design.SPACING['md'])
        layout.setContentsMargins(Design.SPACING['xxxl'], Design.SPACING['xxxl'], Design.SPACING['xxxl'], Design.SPACING['xxxl'])

        logo_frame = QFrame()
        logo_frame.setStyleSheet(f"""
            QFrame {{
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.6, fx:0.5, fy:0.5,
                                            stop:0 {self.theme['accent_glow']}, stop:1 transparent);
                border: none;
            }}
        """)
        logo_frame.setFixedHeight(200)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setAlignment(Qt.AlignCenter)

        logo = QLabel("♚ CHESS ♔")
        logo.setFont(QFont('Segoe UI', Design.FONT['display'], QFont.Bold))
        logo.setStyleSheet(f"color: {self.theme['accent']};")
        logo.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo)

        subtitle = QLabel("Strategy • Intelligence • Victory")
        subtitle.setFont(QFont('Segoe UI', Design.FONT['body'] + 2, QFont.StyleItalic))
        subtitle.setStyleSheet(f"color: {self.theme['text_muted']};")
        subtitle.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(subtitle)

        layout.addWidget(logo_frame)
        layout.addSpacing(Design.SPACING['xxl'])

        buttons = [
            ("♟  New Game", self.start_game, "primary"),
            ("♞  Daily Challenge", self.open_challenges, ""),
            ("📊 Statistics", self.show_stats, ""),
            ("⚙ Settings", self.open_settings, ""),
            ("🚪 Exit", self.main_window.close, "danger")
        ]

        for text, callback, style in buttons:
            btn = PremiumButton(text, self, primary=(style == "primary"), danger=(style == "danger"))
            btn.clicked.connect(callback)
            btn.setFixedWidth(300)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addStretch()

        footer = QLabel("v0.3.0 • Daily Challenges • Built with PyQt5")
        footer.setFont(QFont('Segoe UI', Design.FONT['small']))
        footer.setStyleSheet(f"color: {self.theme['text_muted']};")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setWindowOpacity(0)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(Design.ANIM['page'])
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

    def update_theme(self):
        self.theme = self.main_window.theme
        self.setup_ui()

    def start_game(self):
        self.main_window.switch_to_game()

    def open_challenges(self):
        self.main_window.switch_to_challenges()

    def show_stats(self):
        stats = self.main_window.stats
        total = stats["games"]
        wins = stats["wins"]
        losses = stats["losses"]
        draws = stats["draws"]
        win_rate = (wins / total * 100) if total else 0

        dlg = QDialog(self)
        dlg.setWindowTitle("")
        dlg.setModal(True)
        dlg.setFixedSize(520, 460)
        dlg.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme['bg_secondary']};
                border: 1px solid {self.theme['accent']};
                border-radius: {Design.RADIUS['xl']}px;
            }}
            QLabel {{
                color: {self.theme['text_primary']};
            }}
            QPushButton {{
                background-color: {self.theme['surface']};
                color: {self.theme['text_primary']};
                border: none;
                border-radius: {Design.RADIUS['md']}px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {self.theme['surface_hover']};
            }}
        """)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(Design.SPACING['md'])
        layout.setContentsMargins(Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'], Design.SPACING['xl'])

        title = QLabel("Statistics")
        title.setFont(QFont('Segoe UI', Design.FONT['h1'], QFont.Bold))
        title.setStyleSheet(f"color: {self.theme['accent']};")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        chart = QWidget()
        chart.setFixedSize(130, 130)
        chart.setStyleSheet("background: transparent;")
        chart.paintEvent = lambda e: self._draw_donut(chart, wins, losses, draws)
        layout.addWidget(chart, alignment=Qt.AlignCenter)

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(Design.SPACING['md'])
        for label, value, color in [("Games", total, self.theme['text_primary']),
                                     ("Wins", wins, "#38D39F"),
                                     ("Losses", losses, "#FF5C68"),
                                     ("Draws", draws, "#F5B941")]:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.theme['surface']};
                    border-radius: {Design.RADIUS['md']}px;
                    padding: 8px;
                }}
            """)
            card_layout2 = QVBoxLayout(card)
            val = QLabel(str(value))
            val.setFont(QFont('Segoe UI', 22, QFont.Bold))
            val.setAlignment(Qt.AlignCenter)
            val.setStyleSheet(f"color: {color};")
            card_layout2.addWidget(val)
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 11px;")
            card_layout2.addWidget(lbl)
            kpi_layout.addWidget(card)
        layout.addLayout(kpi_layout)

        rate_lbl = QLabel(f"Win Rate: {win_rate:.1f}%")
        rate_lbl.setFont(QFont('Segoe UI', 18, QFont.Bold))
        rate_lbl.setStyleSheet(f"color: {self.theme['accent']};")
        rate_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(rate_lbl)

        layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dlg.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        dlg.exec_()

    def _draw_donut(self, widget, wins, losses, draws):
        total = wins + losses + draws
        if total == 0:
            return
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = widget.rect().adjusted(10, 10, -10, -10)
        angles = [wins / total * 360, losses / total * 360, draws / total * 360]
        colors = ["#38D39F", "#FF5C68", "#F5B941"]
        start = 0
        for angle, col in zip(angles, colors):
            if angle > 0:
                painter.setBrush(QBrush(QColor(col)))
                painter.setPen(Qt.NoPen)
                painter.drawPie(rect, int(start * 16), int(angle * 16))
                start += angle
        painter.setBrush(QBrush(widget.palette().color(widget.backgroundRole())))
        painter.drawEllipse(rect.adjusted(rect.width() // 4, rect.height() // 4, -rect.width() // 4, -rect.height() // 4))

    def open_settings(self):
        self.main_window.switch_to_settings(from_game=False)


# ============================================================================
# MAIN WINDOW
# ============================================================================
class ChessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.stats = load_stats()
        self.theme_name = self.settings.get('theme', 'dark')
        self.theme = THEMES[self.theme_name]

        self.sound_manager = SoundManager(self.settings)

        self.setWindowTitle("CHESS")
        self.setMinimumSize(1100, 800)
        self.setStyleSheet(f"QMainWindow {{ background-color: {self.theme['bg']}; }}")

        self.shared_engine = None
        self._init_shared_engine()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.menu_widget = MainMenu(self)
        self.game_screen = None
        self.settings_widget = None
        self.challenges_screen = None

        self.central_widget.addWidget(self.menu_widget)
        self.switch_to_menu()

        try:
            self.setWindowIcon(QIcon(resource_path('assets/icon.png')))
        except:
            pass

        self.shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)
        self.shortcut_escape = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_escape.activated.connect(self.exit_fullscreen)
        self.shortcut_space = QShortcut(QKeySequence("Space"), self)
        self.shortcut_space.activated.connect(self.toggle_pause_global)

    def _init_shared_engine(self):
        try:
            possible_paths = [
                resource_path("stockfish.exe"),
                "/usr/games/stockfish",
                "/usr/bin/stockfish",
                shutil.which("stockfish")
            ]
            for path in possible_paths:
                if path and os.path.exists(path):
                    self.shared_engine = chess.engine.SimpleEngine.popen_uci(path)
                    break
        except Exception as e:
            print(f"Could not init Stockfish: {e}")
            self.shared_engine = None

    def close_shared_engine(self):
        if self.shared_engine:
            try:
                self.shared_engine.quit()
            except:
                pass
            self.shared_engine = None

    def apply_theme(self, theme_name):
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
        self.setStyleSheet(f"QMainWindow {{ background-color: {self.theme['bg']}; }}")
        if self.menu_widget:
            self.menu_widget.update_theme()
        if self.game_screen:
            self.game_screen.theme = self.theme
            self.game_screen.setStyleSheet(self.game_screen.get_stylesheet())
            self.game_screen.update_board()
            self.game_screen.update_player_cards()
            self.game_screen._apply_themed_cursor()
            self.game_screen.board_widget._update_cursor_theme()
        if self.settings_widget:
            self.settings_widget.theme = self.theme
            self.settings_widget.setup_ui()
        if self.challenges_screen:
            self.challenges_screen.theme = self.theme
            self.challenges_screen.setStyleSheet(f"background-color: {self.theme['bg']};")

    def switch_to_menu(self):
        if self.game_screen:
            self.game_screen.controller.cleanup()
        self.central_widget.setCurrentWidget(self.menu_widget)

    def switch_to_game(self):
        if self.game_screen:
            self.central_widget.setCurrentWidget(self.game_screen)
            return
        controller = GameController(self, self.shared_engine, self.sound_manager)
        self.game_screen = GameUI(controller, self)
        self.central_widget.addWidget(self.game_screen)
        self.central_widget.setCurrentWidget(self.game_screen)

    def switch_to_settings(self, from_game=False):
        if self.settings_widget is None:
            self.settings_widget = SettingsScreen(self, from_game)
        else:
            self.settings_widget.from_game = from_game
            self.settings_widget.theme = self.theme
            self.settings_widget.setup_ui()
        self.central_widget.addWidget(self.settings_widget)
        self.central_widget.setCurrentWidget(self.settings_widget)

    def switch_to_challenges(self):
        if self.challenges_screen is None:
            self.challenges_screen = ChallengesScreen(self, self)
            self.central_widget.addWidget(self.challenges_screen)
        self.central_widget.setCurrentWidget(self.challenges_screen)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()

    def toggle_pause_global(self):
        if self.game_screen and not self.game_screen.controller.game_over:
            self.game_screen.on_pause_clicked()

    def closeEvent(self, event):
        if self.game_screen:
            self.game_screen.controller.cleanup()
        if self.sound_manager:
            self.sound_manager.quit()
        QTimer.singleShot(100, self.close_shared_engine)
        event.accept()


# ============================================================================
# RUN
# ============================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ChessMainWindow()
    window.show()
    sys.exit(app.exec_())
