# 太鼓さん次郎GAアプリ メイン処理

import argparse

from training_data import make_training_data
from jiro import play_chart
from ga import GA
from const_val import *

# コマンドライン引数の解析
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tja_path',
        '-t',
        type=str,
        required=True,
        help='譜面ファイル(.tja)のパス。')
    args = parser.parse_args()

    return args

# メイン処理
def main():
    args = parse_args()

    training_data = make_training_data(args.tja_path)
    g = GA(training_data=training_data, n_genes=NUM_GENES_IN_GENERATION)
    gen = 1
    while gen < 100:
        g.go_to_next_generation()
        gen += 1

    play_chart(g.get_gene_as_chart(), args.tja_path)

if __name__ == '__main__':
    main()
