# candy_hunt.py
# step1 フェーズ3：お菓子を置いて、重なったら次の場所へ移す

import random

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

BOY_SIZE = 8            # 男の子の絵の大きさ（縦横とも 8 ドット）
BOY_SPEED = 2           # 1 フレームで進むドット数

CANDY_SIZE = 8          # お菓子の絵の大きさ

def is_hit(x1, y1, size1, x2, y2, size2):
    """2 つの四角が重なっていれば True を返す"""
    return (x1 < x2 + size2 and x2 < x1 + size1 and
            y1 < y2 + size2 and y2 < y1 + size1)

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Candy Hunt")
        pyxel.load("candy_hunt.pyxres")

        self.boy_x = SCREEN_WIDTH // 2 - BOY_SIZE // 2
        self.boy_y = SCREEN_HEIGHT // 2 - BOY_SIZE // 2
        self.place_candy()

        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム毎の更新処理"""
        self.move_boy()
        self.check_candy()

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

    def place_candy(self):
        """男の子と重ならない場所へ、お菓子を置きなおす"""
        while True:
            self.candy_x = random.randint(0, SCREEN_WIDTH - CANDY_SIZE)
            self.candy_y = random.randint(0, SCREEN_HEIGHT - CANDY_SIZE)
            if not is_hit(self.boy_x, self.boy_y, BOY_SIZE,
                          self.candy_x, self.candy_y, CANDY_SIZE):
                break

    def check_candy(self):
        """お菓子に重なったら、次の場所へ置きなおす"""
        if is_hit(self.boy_x, self.boy_y, BOY_SIZE,
                  self.candy_x, self.candy_y, CANDY_SIZE):
            self.place_candy()

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)

        pyxel.blt(self.candy_x, self.candy_y, 0, 16, 0,
                  CANDY_SIZE, CANDY_SIZE, pyxel.COLOR_BLACK)    # お菓子
        pyxel.blt(self.boy_x, self.boy_y, 0, 0, 0,
                  BOY_SIZE, BOY_SIZE, pyxel.COLOR_BLACK)        # 男の子

App()
