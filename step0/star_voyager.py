# star_voyager.py
# step0 フェーズ4: 素材を描き、クラスにまとめる

import random
import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

TITLE = "STAR VOYAGER"
GUIDE = "PRESS ESC TO QUIT"

STAR_COUNT = 40         # 星の数
STAR_SPEED_MIN = 0.3    # 星の速さの下限（ドット／フレーム）
STAR_SPEED_MAX = 1.8    # 星の速さの上限

class App:
    """このゲーム全体を受け持つ箱"""

    def __init__(self):
        """箱が作られるときに1回だけ呼ばれる。ここで準備をすませる"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Star Voyager")
        self.stars = []     # 星をぜんぶ入れるリスト
        self.make_stars()
        pyxel.run(self.update, self.draw)

    def make_stars(self):
        """星を STAR_COUNT 個ぶん作って self.stars に入れる"""
        for i in range(STAR_COUNT):
            x = random.randint(0, SCREEN_WIDTH - 1)
            y = random.randint(0, SCREEN_HEIGHT - 1)
            speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
            self.stars.append([x, y, speed])

    def star_color(self, speed):
        """速い星ほど明るい色にして、奥行きを表す"""
        if speed > 1.2:
            return pyxel.COLOR_WHITE
        if speed > 0.7:
            return pyxel.COLOR_GRAY
        return pyxel.COLOR_DARK_BLUE

    def text_center(self, y, s, col):
        """文字列 s を、画面の横中央に来るように描く"""
        x = (SCREEN_WIDTH - len(s) * pyxel.FONT_WIDTH) // 2
        pyxel.text(x, y, s, col)

    def update(self):
        """フレーム毎の更新処理。星を下へ動かす"""
        for star in self.stars:
            star[1] += star[2]                                  # y に速さを足す

            if star[1] >= SCREEN_HEIGHT:                        # 画面の下に出たら
                star[0] = random.randint(0, SCREEN_WIDTH - 1)   # x を引き直して
                star[1] = 0                                     # いちばん上に戻す

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(0)

        for star in self.stars:
            pyxel.pset(star[0], star[1], self.star_color(star[2]))

        self.text_center(20, TITLE, pyxel.COLOR_YELLOW)
        self.text_center(34, GUIDE, pyxel.COLOR_GRAY)

App()
