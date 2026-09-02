# candy_hunt.py
# step1 フェーズ1：描いた 3 つの絵を並べて表示する

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Candy Hunt")
        pyxel.load("candy_hunt.pyxres")     # pyxel.init のあとにリソースファイルは読み込み可能
        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム毎の更新処理：まだ何もしない"""
        pass

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)

        pyxel.blt(40, 56, 0, 0, 0, 8, 8, pyxel.COLOR_BLACK)     # 男の子
        pyxel.blt(76, 56, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)     # お化け
        pyxel.blt(112, 56, 0, 16, 0, 8, 8, pyxel.COLOR_BLACK)   # お菓子

App()
