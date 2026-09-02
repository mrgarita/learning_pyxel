# candy_hunt.py
# step1 フェーズ1：描いた 3 つの絵を並べて表示する

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

BOY_SIZE = 8            # 男の子の絵の大きさ（縦横とも 8 ドット）
BOY_SPEED = 2           # 1 フレームで進むドット数

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Candy Hunt")
        pyxel.load("candy_hunt.pyxres")

        self.boy_x = SCREEN_WIDTH // 2 - BOY_SIZE // 2
        self.boy_y = SCREEN_HEIGHT // 2 - BOY_SIZE // 2

        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム毎の更新処理"""
        self.move_boy()

    def move_boy(self):
        """矢印キーで男の子を動かす"""
        if pyxel.btn(pyxel.KEY_LEFT):
            self.boy_x -= BOY_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.boy_x += BOY_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.boy_y -= BOY_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.boy_y += BOY_SPEED

        # 画面の外へ出さない
        self.boy_x = max(0, min(self.boy_x, SCREEN_WIDTH - BOY_SIZE))
        self.boy_y = max(0, min(self.boy_y, SCREEN_HEIGHT - BOY_SIZE))

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)

        pyxel.blt(self.boy_x, self.boy_y, 0, 0, 0,
                  BOY_SIZE, BOY_SIZE, pyxel.COLOR_BLACK)     # 男の子

App()
