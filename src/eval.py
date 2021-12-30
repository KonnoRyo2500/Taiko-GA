# 太鼓さん次郎GAアプリ 適応度判定処理

from multiprocessing import Pool

from const_val import *

# 与えられた複数の遺伝子の適応度をそれぞれ計算する
def eval_genes(genes, training_data):
    # 本来であれば太鼓さん次郎で演奏を行い、そのスコアを適応度とするのが
    # 望ましいが、その方法だと学習に時間がかかるうえ、スコアの取得が難しい。
    # そこで、tjaファイルから本来の譜面を教師データとして抽出し、その譜面を用いて
    # 以下の方法で適応度を判定する。

    # 遺伝子中の各音符に対して、特良,特可,良,可,不可,判定なし(空打ち)
    # それぞれの判定について点数を与える。
    # 点数の合計をその遺伝子の適応度とする。

    with Pool(NUM_PROCESSES) as pl:
        eval_args = [(gene, training_data) for gene in genes]
        scores = pl.starmap(_eval_gene, eval_args)
    return scores

# 与えられた1つの遺伝子の適応度を計算する
def _eval_gene(gene, training_data):
    timing = 0.0
    gene_score = 0
    t_data_with_score = [[*t, SCORE_NONE] for t in training_data] # (種類, タイミング, 適応度)
    for note in gene:
        # 判定範囲内の音符について、今叩いた音符で処理できるものがないか調べる
        neighbor_t = [(i, t) for i, t in enumerate(t_data_with_score) if t[2] == SCORE_NONE and JUDGE_RANGE_FUKA_EARLY <= (t[1] - timing) * 1000 <= JUDGE_RANGE_FUKA_LATE]
        evaluated_note = []
        for i, nt in neighbor_t:
            # 1つの音符につき、同色の音符は先頭の1つしか見ない
            nt_note, nt_timing, nt_score = nt
            if nt_note in evaluated_note:
                continue
            else:
                if (nt_note == NOTE_DON) or (nt_note == NOTE_DON_LARGE):
                    evaluated_note.append(NOTE_DON)
                    evaluated_note.append(NOTE_DON_LARGE)
                elif (nt_note == NOTE_KATSU) or (nt_note == NOTE_KATSU_LARGE):
                    evaluated_note.append(NOTE_KATSU)
                    evaluated_note.append(NOTE_KATSU_LARGE)
            note_score = _eval_note(note, timing, nt_note, nt_timing)
            t_data_with_score[i][2] = note_score
            if note_score != SCORE_NONE:
                break
        timing += SEC_PER_SAMPLING

    # 見逃した音符はすべて不可判定にする
    for t in t_data_with_score:
        t_score = t[2]
        gene_score += t_score if t_score != SCORE_NONE else SCORE_FUKA

    return gene_score

# 与えられた音符の点数を決定する
def _eval_note(note, timing, t_note, t_timing):
    acceptable_note_pair = [
        (NOTE_DON, NOTE_DON),
        (NOTE_DON, NOTE_DON_LARGE),
        (NOTE_KATSU, NOTE_KATSU),
        (NOTE_KATSU, NOTE_KATSU_LARGE),
        (NOTE_DON_LARGE, NOTE_DON_LARGE),
        (NOTE_DON_LARGE, NOTE_DON),
        (NOTE_KATSU_LARGE, NOTE_KATSU_LARGE),
        (NOTE_KATSU_LARGE, NOTE_KATSU),
    ]
    if (note, t_note) not in acceptable_note_pair:
        return SCORE_NONE

    is_play_large_note_success = (note in [NOTE_DON_LARGE, NOTE_KATSU_LARGE]) and \
                                 (note == t_note)
    note_score = SCORE_NONE
    diff_timing_ms = (t_timing - timing) * 1000
    if JUDGE_RANGE_FUKA_EARLY <= diff_timing_ms < JUDGE_RANGE_KA_EARLY:
        note_score = SCORE_FUKA
    elif JUDGE_RANGE_KA_EARLY <= diff_timing_ms < JUDGE_RANGE_RYO_EARLY:
        note_score = SCORE_TOKUKA if is_play_large_note_success else SCORE_KA
    elif JUDGE_RANGE_RYO_EARLY <= diff_timing_ms <= JUDGE_RANGE_RYO_LATE:
        note_score = SCORE_TOKURYO if is_play_large_note_success else SCORE_RYO
    elif JUDGE_RANGE_RYO_LATE < diff_timing_ms <= JUDGE_RANGE_KA_LATE:
        note_score = SCORE_TOKUKA if is_play_large_note_success else SCORE_KA
    elif JUDGE_RANGE_KA_LATE < diff_timing_ms <= JUDGE_RANGE_FUKA_LATE:
        note_score = SCORE_FUKA

    return note_score

