import stdqt
import threading
import re
import requests
import asyncio
import asyncqt
import httpx
import sys
import os
import functools
import random
import win32gui
import win32con
import pyautogui
import MCLikeCommandParser as mccmd
import psutil
import time
import keyboard
import math
import struct
import subprocess
import multiprocessing
import winreg as reg
from traceback import print_exception
from pathlib import Path
from collections import defaultdict

from ctypes import windll
from win32con import *
from win32gui import *
from threading import Thread
from stdqt import *
from typing import *

ALARM_WINDOW_TITLE = '!!!'
ANGRY_1_TIP = '不要扯人家! \n会痛的哦?'

DEFAULT_TIP = '又可以看伙伴画画了!\n人家可以帮你输哦?'
ANGRY_1_TIP = '不要扯人家! \n会痛的哦?'
RECOVER_FROM_ANGER_TIP = '快呀!'

LOG_PATH = os.getenv('APPDATA') + '/../LocalLow/Acureus/Draw_Guess/Player.log'

CYRENE_PINK = QColor(254, 223, 228)
TEST_RED = QColor(255, 0, 0)

global_timers = []

class AlarmWindow:
    instances = []
    def __init__(self, tip:str) -> None:
        AlarmWindow.instances += [self]

        self.alarm_window = QWidget()
        self.alarm_window.setFixedSize(800, 200)
        self.alarm_window.setWindowTitle(ALARM_WINDOW_TITLE)

        self.o_tip = QLabel(self.alarm_window)
        self.o_tip.setFixedWidth(self.alarm_window.width())
        self.o_tip.setMinimumHeight(100)
        self.o_tip.setWordWrap(True)
        self.o_tip.setTextFormat(Qt.RichText)
        _splited = tip.split(endl)
        self.tip = endl.join(_splited[:-1])
        self.err = _splited[-1]
        self.tiptext = f"""
        <head>
            <style>
                * {{
                    margin: 0px, 0px, 0px, 0px;
                }}
            </style>
        </head>
        <p>
            <font face=\"汉仪旗黑 75S\" size=\"48\">
                {self.tip}
            </font>
        </p>
        <p>
            <font face=\"汉仪旗黑 55S\" size=\"24\">
                {self.err}
            </font>
        </p>
        """
        self.o_tip.setText(self.tiptext)
        def _thread():
            try:
                with open('./global.css', 'r', encoding='utf-8') as f:
                    css = f.read()
                self.alarm_window.setStyleSheet(css)
            except Exception:
                pass
        Thread(target=_thread).start()

        self.alarm_window.show()
    def __del__(self) -> None:
        print('shan le!')

class CustomQThread(QThread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,  **kwargs)
        self.target_func = lambda : print('void function')
    def setTargetFunction(self, func) -> None:
        self.target_func = func
    def run(self) -> None:
        self.target_func()

class NormalAlarmWindow(QWidget):
    def __init__(self, tip:str) -> None:
        super().__init__()      
        self.is_angry_resize = False

        self.setGeometry(1920 - 400 - 20, 1080 - 200 - 70, 400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('PhiLia093 - Draw & Guess Remote Copy')

        self.o_cyrene = QLabel(self)
        self.o_cyrene.setStyleSheet(
            "border-image: url(./cyrene_small_handback.png); background-color: transparent;"
        )
        self.o_cyrene.setGeometry(self.width() - 200 *2// 3, self.height() - 283 *2// 3, 200 *2// 3, 283 *2// 3)

        self.tip = tip
        self.o_tip = QLabel(self)
        self.o_tip.setGeometry(20, 15, 400, 100)
        self.o_tip.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.o_tip.setFont(font_hyqh_55(18))
        self.o_tip.setText(tip)
    def show(self):
        self.o_tip.setText(self.tip)
        return super().show()
    def resizeEvent(self, a0):
        global global_timers
        if (a0.oldSize().width(), a0.oldSize().height()) != (-1, -1) and (a0.size().width(), a0.size().height()) != (400, 200):
            if not self.is_angry_resize:
                self.o_tip.setText(ANGRY_1_TIP)
            self.is_angry_resize = True
            recover_size_timer = QTimer(self)
            global_timers += [recover_size_timer]
            def _recover():
                nonlocal recover_size_timer
                self.resize(400, 200)
                recover_size_timer.stop()
                if recover_size_timer in global_timers:
                    global_timers.remove(recover_size_timer)
                del recover_size_timer
            recover_size_timer.timeout.connect(_recover)
            recover_size_timer.setSingleShot(True)
            recover_size_timer.start(1000)
        return super().resizeEvent(a0)

def disable(func):
    def _wrapper(*args, **kwargs):
        print(f"Disabled function calling of {func.__name__}()")
    return _wrapper
@disable
def _some_example():
    pass


def font_hyqh_75(size:int=24) -> QFont:
    return QFont('汉仪旗黑 75S', size)

def font_hyqh_55(size:int=24) -> QFont:
    return QFont('汉仪旗黑 55S', size)

endl = '\n'
__main__constname = '__main__'


gc_protected = []

def gc_protect(a) -> None:
    global gc_protected
    if a not in gc_protected:
        gc_protected += [a]

def cancle_gc_protect(a) -> None:
    global gc_protected
    if a in gc_protected:
        gc_protected.remove(a)

def qel_sleep(ms:int) -> None:
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()