# 太鼓さん次郎GAアプリ 定数一覧

# ヘッダ
HEADER_BPM = 'BPM'
HEADER_OFFSET = 'OFFSET'

# 命令
CMD_START = '#START'
CMD_END = '#END'
CMD_BPMCHANGE = '#BPMCHANGE'
# HS変化やその他命令に関しては叩くタイミングには関係ないので考慮しない

# 音符の種類
NOTE_NONE = 0
NOTE_DON = 1
NOTE_KATSU = 2
NOTE_DON_LARGE = 3
NOTE_KATSU_LARGE = 4
# TODO: 連打に対応できるようになったら、連打系の音符も定義する

# 押下するキーのキーコード
KEYCODE_D = 68
KEYCODE_F = 70
KEYCODE_J = 74
KEYCODE_K = 75
