# 太鼓さん次郎GAアプリ GAクラス

import random

from const_val import *
from eval import eval_genes

# GAを用いて、指定された譜面を攻略するためのシーケンスを生成するクラス
class GA:
    # 遺伝子は、一定時間ごとに叩く音符を並べた1次元配列とする。
    # 1秒間に何個の音符を叩くかを、const_val.pyのNOTE_SAMPLING_RATEで指定できる。

    # コンストラクタ
    def __init__(self, training_data, n_genes=100):
        self.genes = [] # 現世代での遺伝子
        self.scores = [] # 適合度
        self.training_data = training_data # 教師データ

        # 遺伝子の長さの決定
        training_final_note_time = training_data[-1][1]
        gene_final_note_time = training_final_note_time + (JUDGE_RANGE_FUKA_LATE / 1000.0) # ms -> sに変換
        gene_length = int(gene_final_note_time // SEC_PER_SAMPLING)

        # 初期世代の生成
        self._generate_initial_genes(n_genes, gene_length)
        self.scores = eval_genes(self.genes, self.training_data)

    # 初期遺伝子を指定された個数生成
    def _generate_initial_genes(self, n_genes, gene_length):
        self.genes = [self._generate_initial_gene(gene_length) for _ in range(n_genes)]
        self.scores = [None] * n_genes

    # 初期遺伝子を1つ生成
    def _generate_initial_gene(self, gene_length):
        return [random.randint(NOTE_NONE, NOTE_KATSU_LARGE) for _ in range(gene_length)]
