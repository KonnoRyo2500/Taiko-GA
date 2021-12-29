# 太鼓さん次郎GAアプリ メイン処理

import argparse
import os.path as op

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
    parser.add_argument(
        '--num_generation',
        '-g',
        type=int,
        default=100,
        help='何世代学習を続けるか。')
    parser.add_argument(
        '--save_ckpt',
        '-c',
        action='store_true',
        help='遺伝子情報の書き出しを有効化する。'
    )
    parser.add_argument(
        '--ckpt_save_period',
        '-p',
        type=int,
        default=10,
        help='遺伝子情報を何世代ごとに書き出すか。')
    parser.add_argument(
        '--ckpt_out_dir',
        '-o',
        type=str,
        default=op.join('..', 'ckpt'),
        help='各世代の遺伝子情報を書き出すディレクトリ。')
    args = parser.parse_args()

    return args

# メイン処理
def main():
    args = parse_args()

    training_data = make_training_data(args.tja_path)
    g = GA(training_data=training_data, n_genes=NUM_GENES_IN_GENERATION)
    for gen in range(1, args.num_generation):
        if (args.save_ckpt) and (gen % args.ckpt_save_period == 0):
            g.save_generation(dir=args.ckpt_out_dir)
        g.go_to_next_generation()

    play_chart(g.get_gene_as_chart(), args.tja_path)

if __name__ == '__main__':
    main()
