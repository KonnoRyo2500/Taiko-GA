# 太鼓さん次郎GAアプリ 太鼓さん次郎演奏処理

import time

import pywinauto as pwa
import ctypes

from const_val import *

# TODO: 設定ファイルで指定できるようにする
JIRO_PATH = 'C:\\Users\\enc91\\Downloads\\taikojiro292\\taikojiro292\\taikojiro.exe'

# 与えられたシーケンス形式の譜面を太鼓さん次郎で演奏する
def play_chart(chart, tja_path):
    # 太鼓さん次郎の起動
    pwa.Application(backend='uia').start(f'{JIRO_PATH} {tja_path}')

    # オートOFFで演奏開始
    # TJAファイルが読み込まれるまでに少し時間がかかるため、完了するまで待つ
    time.sleep(2)
    pwa.keyboard.send_keys('{F1} {SPACE}')

    # 演奏の実行
    start_time = time.time()
    now = time.time()
    for note_info in chart:
        note_type, timing = note_info
        wait_time = timing - now + start_time
        time.sleep(wait_time)
        _play_note(note_type)
        now = time.time()

# キーを押下し、指定された音符を1つ演奏する
def _play_note(note_type):
    play_func = {
        NOTE_DON: _play_normal_note,
        NOTE_KATSU: _play_normal_note,
        NOTE_DON_LARGE: _play_large_note,
        NOTE_KATSU_LARGE: _play_large_note,
    }[note_type]

    play_func(note_type)

# 通常の(=大音符でない)音符を1つ演奏する
def _play_normal_note(note_type):
    code = {
        NOTE_DON: KEYCODE_J,
        NOTE_KATSU: KEYCODE_K,
    }[note_type]

    _press_single_key(code)

# 大音符を1つ演奏する
def _play_large_note(note_type):
    codes = {
        NOTE_DON_LARGE: [KEYCODE_F, KEYCODE_J],
        NOTE_KATSU_LARGE: [KEYCODE_D, KEYCODE_K],
    }[note_type]

    for code in codes:
        _press_single_key(code)

# キーを1つ押下する
def _press_single_key(code):
    # キーの押下
    ctypes.windll.user32.keybd_event(code, 0, 0, 0)

    # キーを一瞬でリリースしてしまうとうまく判定されないため、わずかな遅延を加える
    time.sleep(0.001)

    # キーのリリース
    ctypes.windll.user32.keybd_event(code, 0, 2, 0)
