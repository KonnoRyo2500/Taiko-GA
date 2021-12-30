# 太鼓さん次郎GAアプリ 定数一覧

from enum import Enum, auto

### システム全般 ###
# 評価時に用いるプロセス数
NUM_PROCESSES = 16

### 太鼓さん次郎関連 ###
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

# 自動演奏時、1秒間にいくつの音符を配置(サンプリング)するか
NOTE_SAMPLING_RATE = 30
SEC_PER_SAMPLING = 1.0 / NOTE_SAMPLING_RATE # 1サンプリング当たりの秒数

# 判定範囲
# 真のタイミングから何ミリ秒ズレているか(早い側をマイナスとする)
JUDGE_RANGE_FUKA_EARLY = -150
JUDGE_RANGE_KA_EARLY = -100
JUDGE_RANGE_RYO_EARLY = -50
JUDGE_RANGE_RYO_LATE = -JUDGE_RANGE_RYO_EARLY
JUDGE_RANGE_KA_LATE = -JUDGE_RANGE_KA_EARLY
JUDGE_RANGE_FUKA_LATE = -JUDGE_RANGE_FUKA_EARLY

### GA関連 ###
# 遺伝子の各要素に与えるスコア
SCORE_TOKURYO = 2.5
SCORE_TOKUKA = 1.5
SCORE_RYO = 2.0
SCORE_KA = 1.0
SCORE_FUKA = -2.0
SCORE_NONE = 0

# 交叉のアルゴリズム
class CrossoverMethod(Enum):
    ONE_POINT = auto() # 一点交叉
    TWO_POINT = auto() # 二点交叉
    MULTI_POINT = auto() # 多点交叉
    UNIFORM = auto() # 一様交叉

# 選択のアルゴリズム
class SelectionMethod(Enum):
    ELITE = auto() # エリート選択
    ROULETTE = auto() # ルーレット選択
    RANKING = auto() # ランキング選択
    TOURNAMENT = auto() # トーナメント選択

# 突然変異の確率
MUTATION_PROBABILITY = 0.01

# 世代ごとの遺伝子の数
NUM_GENES_IN_GENERATION = 100
# 選択で生成する遺伝子の数
NUM_GENES_FROM_SELECTION = 20
# 交叉で生成する遺伝子の数
NUM_GENES_FROM_CROSSOVER = NUM_GENES_IN_GENERATION - NUM_GENES_FROM_SELECTION
