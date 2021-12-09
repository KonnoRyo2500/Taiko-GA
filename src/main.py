# 太鼓さん次郎GAアプリ メイン処理

from training_data import make_training_data
from jiro import play_chart

# メイン処理
def main():
    # TODO: コマンドライン引数にする
    tja_path = 'C:\\Users\\enc91\\Desktop\\hobby\\taiko\\sample_tja\\release.tja'
    training_data = make_training_data(tja_path)
    play_chart(training_data, tja_path)

if __name__ == '__main__':
    main()
