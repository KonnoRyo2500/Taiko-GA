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
        self.n_generation = 1

        # 遺伝子の長さの決定
        training_final_note_time = training_data[-1][1]
        gene_final_note_time = training_final_note_time + (JUDGE_RANGE_FUKA_LATE / 1000.0) # ms -> sに変換
        gene_length = int(gene_final_note_time // SEC_PER_SAMPLING)

        # 初期世代の生成
        self._generate_initial_genes(n_genes, gene_length)
        self.scores = eval_genes(self.genes, self.training_data)

        self._print_generation_info()

    # 世代を1つ進める
    def go_to_next_generation(self):
        genes_in_next_gen = []
        # 交叉で遺伝子生成
        while len(genes_in_next_gen) < NUM_GENES_FROM_CROSSOVER:
            # 交叉させる遺伝子を決定
            gene1_idx, gene2_idx = random.randint(0, len(self.genes) - 1),\
                                   random.randint(0, len(self.genes) - 1)
            if gene1_idx == gene2_idx:
                continue
            gene1, gene2 = self.genes[gene1_idx], self.genes[gene2_idx]

            # 交叉で新遺伝子を生成
            gene_from_crossover = self._crossover(gene1, gene2, method=CrossoverMethod.UNIFORM)
            genes_in_next_gen.append(gene_from_crossover)

        # 選択で遺伝子生成
        genes_from_selection = self._selection(
                                    n_genes=NUM_GENES_FROM_SELECTION,
                                    method=SelectionMethod.ELITE)
        genes_in_next_gen.extend(genes_from_selection)

        # 突然変異を適用
        genes_in_next_gen = [self._mutation(gene, MUTATION_PROBABILITY) for gene in genes_in_next_gen]

        # 評価
        scores_in_next_gen = eval_genes(genes_in_next_gen, self.training_data)

        # メンバ変数を更新
        self.genes = genes_in_next_gen
        self.scores = scores_in_next_gen
        self.n_generation += 1

        self._print_generation_info()

    # 交叉
    def _crossover(self, gene1, gene2, method=CrossoverMethod.ONE_POINT):
        crossover_func = {
            CrossoverMethod.ONE_POINT: self._one_point_crossover,
            CrossoverMethod.TWO_POINT: self._two_point_crossover,
            CrossoverMethod.MULTI_POINT: self._multi_point_crossover,
            CrossoverMethod.UNIFORM: self._uniform_crossover,
        }[method]

        new_gene = crossover_func(gene1, gene2)

        return new_gene

    # 一点交叉
    def _one_point_crossover(self, gene1, gene2):
        raise NotImplementedError('一点交叉は未実装です。')

    # 二点交叉
    def _two_point_crossover(self, gene1, gene2):
        raise NotImplementedError('二点交叉は未実装です。')

    # 多点交叉
    def _multi_point_crossover(self, gene1, gene2, n_point):
        raise NotImplementedError('多点交叉は未実装です。')

    # 一様交叉
    def _uniform_crossover(self, gene1, gene2):
        new_gene = []
        for x1, x2 in zip(gene1, gene2):
            which = random.randint(0, 1)
            new_gene.append(x1 if which == 0 else x2)

        return new_gene

    # 選択
    def _selection(self, n_genes, method=SelectionMethod.ELITE):
        selection_func = {
            SelectionMethod.ELITE: self._elite_selection,
            SelectionMethod.ROULETTE: self._roulette_selection,
            SelectionMethod.RANKING: self._ranking_selection,
            SelectionMethod.TOURNAMENT: self._tournament_selection,
        }[method]

        new_genes = selection_func(n_genes)

        return new_genes

    # エリート選択
    def _elite_selection(self, n_genes):
        new_genes = []
        elite_genes_idx = [self.scores.index(sc) for sc in sorted(self.scores, reverse=True)]
        for idx in elite_genes_idx:
            if len(new_genes) == n_genes:
                break

            elite_gene = self.genes[idx]
            new_genes.append(elite_gene)

        return new_genes

    # ルーレット選択
    def _roulette_selection(self, n_genes):
        raise NotImplementedError('ルーレット選択は未実装です。')

    # ランキング選択
    def _ranking_selection(self, n_genes):
        raise NotImplementedError('ランキング選択は未実装です。')

    # トーナメント選択
    def _tournament_selection(self, n_genes):
        raise NotImplementedError('トーナメント選択は未実装です。')

    # 突然変異
    def _mutation(self, gene, probability):
        for i, _ in enumerate(gene):
            v = random.random()
            if v > probability:
                continue

            note_list = [n for n in range(NOTE_NONE, NOTE_KATSU_LARGE + 1)]
            note_list.remove(gene[i])
            gene[i] = note_list[random.randint(0, len(note_list) - 1)]

        return gene

    # 初期遺伝子を指定された個数生成
    def _generate_initial_genes(self, n_genes, gene_length):
        self.genes = [self._generate_initial_gene(gene_length) for _ in range(n_genes)]
        self.scores = [None] * n_genes

    # 初期遺伝子を1つ生成
    def _generate_initial_gene(self, gene_length):
        return [random.randint(NOTE_NONE, NOTE_KATSU_LARGE) for _ in range(gene_length)]

    # 世代情報を出力
    def _print_generation_info(self):
        print('-' * 10 + f'Generation {self.n_generation}' + '-' * 10)
        print(f'Max score: {max(self.scores)}')
        print(f'Avg score: {sum(self.scores) / len(self.scores)}')
