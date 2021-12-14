# 太鼓さん次郎GAアプリ メイン処理

from training_data import make_training_data
from jiro import play_chart
from ga import GA
from const_val import *

# メイン処理
def main():
    # TODO: コマンドライン引数にする
    tja_path = 'C:\\Users\\enc91\\Desktop\\hobby\\taiko\\sample_tja\\release.tja'
    training_data = make_training_data(tja_path)
    g = GA(training_data=training_data)
    gene = g.genes[0]
    score = g.scores[0]
    chart = []
    timing = 0.0
    for note in gene:
        if note != NOTE_NONE:
            chart.append((note, timing))
        timing += SEC_PER_FRAME

    print(f'Expected score: {score}')
    play_chart(chart, tja_path)

if __name__ == '__main__':
    main()
