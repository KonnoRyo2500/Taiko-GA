# 太鼓さん次郎GAアプリ 教師データの作成処理

from const_val import *

# 教師データを作成する
def make_training_data(tja_path):
    with open(tja_path, 'r') as tja:
        current_bpm, offset = _read_bpm_and_offset(tja)

# ヘッダーからBPMとオフセットを取得する
def _read_bpm_and_offset(tja):
    bpm, offset = None, None
    while True:
        line = _read_tja_line(tja)
        if (line is None) or (line.startswith(CMD_START)):
            break

        # BPMとオフセットさえ取得できれば良いので、あまり凝った処理にはしない
        if line.startswith(HEADER_BPM):
            bpm = line.split(':')[1]
        elif line.startswith(HEADER_OFFSET):
            offset = line.split(':')[1]

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
