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

# 遺伝子の各要素に与えるスコア
SCORE_TOKURYO = 2.5
SCORE_TOKUKA = 1.5
SCORE_RYO = 2.0
SCORE_KA = 1.0
SCORE_FUKA = -2.0
SCORE_NONE = 0

# 太鼓さん次郎の仮想フレームレート
JIRO_FPS = 60
SEC_PER_FRAME = 1.0 / JIRO_FPS # 1フレーム当たりの秒数

# 判定範囲
# 真のタイミングから何秒ズレているか(早い側をマイナスとする)
JUDGE_RANGE_FUKA_EARLY = -12 * SEC_PER_FRAME
JUDGE_RANGE_KA_EARLY = -8 * SEC_PER_FRAME
JUDGE_RANGE_RYO_EARLY = -4 * SEC_PER_FRAME
JUDGE_RANGE_RYO_LATE = 4 * SEC_PER_FRAME
JUDGE_RANGE_KA_LATE = 8 * SEC_PER_FRAME
JUDGE_RANGE_FUKA_LATE = 12 * SEC_PER_FRAME
