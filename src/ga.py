# 太鼓さん次郎GAアプリ GAクラス

import random

from const_val import *

# GAを用いて、指定された譜面を攻略するためのシーケンスを生成するクラス
class GA:
    # 遺伝子は、1フレームごとに叩く音符を並べた1次元配列とする。
    # フレームレートは60fps固定。したがって、60要素で1秒分の譜面となる。

    # コンストラクタ
    def __init__(self, n_genes=100, gene_length=60*120):
        self.genes = [] # 現世代での遺伝子
        self.fits = [] # 適合度

        self._generate_initial_genes(n_genes, gene_length)

    # 初期遺伝子を指定された個数生成
    def _generate_initial_genes(self, n_genes, gene_length):
        self.genes = [self._generate_initial_gene(gene_length) for _ in range(n_genes + 1)]
        self.fits = [None for _ in range(n_genes + 1)]

    # 初期遺伝子を1つ生成
    def _generate_initial_gene(self, gene_length):
        return [random.randint(NOTE_NONE, NOTE_KATSU_LARGE) for _ in range(gene_length + 1)]
