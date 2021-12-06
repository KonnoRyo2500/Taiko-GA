# 太鼓さん次郎GAアプリ 教師データの作成処理

from const_val import *

# 教師データを作成する
def make_training_data(tja_path):
    with open(tja_path, 'r') as tja:
        initial_bpm, offset = _read_bpm_and_offset(tja)
        training_data = _read_notes_timing(tja, initial_bpm, offset)

    return training_data

# ヘッダーからBPMとオフセットを取得する
def _read_bpm_and_offset(tja):
    bpm, offset = None, None
    while True:
        line = _read_tja_line(tja)
        if (line is None) or (line.startswith(CMD_START)):
            break

        # BPMとオフセットさえ取得できれば良いので、あまり凝った処理にはしない
        if line.startswith(HEADER_BPM):
            bpm = float(line.split(':')[1])
        elif line.startswith(HEADER_OFFSET):
            offset = float(line.split(':')[1])

    if (bpm is None) or (offset is None):
        raise RuntimeError('BPMとオフセットはヘッダーに必ず記載してください。')

    return bpm, offset

# TJAファイルの1行を読み込む
def _read_tja_line(tja):
    line = tja.readline()
    if line == '':
        return None

    # コメント部分の除去
    comment_begin_idx = line.find('//')
    if comment_begin_idx != -1:
        line = line[:comment_begin_idx]

    # いきなりstripしてしまうとlineが空文字列だった際、
    # ファイル終端と空行を判別できなくなってしまう
    # そのため、ファイル終端を判定してからstripする
    line = line.strip()

    return line

# 各音符を叩く正確なタイミング(=教師データ)を取得する
# TODO: 譜面分岐に対応する
# TODO: 複数の小節が1行に記載されているときにも正常に読み込めるようにする
def _read_notes_timing(tja, initial_bpm, offset):
    elapsed_time_sec = 0.0
    current_bpm = initial_bpm
    note_buf = ''
    training_data = []
    valid_notes = [1, 2, 3, 4]
    while True:
        line = _read_tja_line(tja)

        # 譜面部分終了
        if (line is None) or (line.startswith(CMD_END)):
            break
        # BPM変化
        elif line.startswith(CMD_BPMCHANGE):
            new_bpm = float(line.split()[1])
            current_bpm = new_bpm
            continue
        # その他の命令
        # 教師データの作成には関係ないので無視する
        elif line.startswith('#'):
            continue
        # 小節途中での改行
        # 次の行も読み込む
        elif not line.endswith(','):
            note_buf += line
            continue

        if note_buf != '':
            line = note_buf + line
        line = line[:-1] # 最後の','は音符ではないので削除

        for note in line:
            note = int(note)
            if note in valid_notes:
                training_data.append((note, elapsed_time_sec))
            # BPM = bのn分音符同士の間隔は 240 / bn 秒
            period_per_note = 240 / (current_bpm * len(line))
            elapsed_time_sec += period_per_note
        note_buf = ''

    return training_data
