# star_voyager.py
# step0 フェーズ2:タイトル文字を表示する

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

TITLE = "STAR VOYAGER"
GUIDE = "PRESS ESC TO QUIT"

def text_center(y, s, col):
    """文字列sを、画面の横中央に来るように描く"""
    x = (SCREEN_WIDTH - len(s) * pyxel.FONT_WIDTH) // 2
    pyxel.text(x, y, s, col)


def update():
    """フレーム毎の更新処理。まだ何もしない"""
    pass

def draw():
    """フレーム毎の描画処理"""
    pyxel.cls(0)                                # 画面を黒で塗りつぶす
    text_center(20, TITLE, pyxel.COLOR_YELLOW)  # タイトル
    text_center(34, GUIDE, pyxel.COLOR_GRAY)    # 操作説明

pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Star Voyager")
pyxel.run(update, draw)
