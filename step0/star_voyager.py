# star_voyager.py
# step0 フェーズ6: 矢印キーで宇宙船を動かす

import random
import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

TITLE = "STAR VOYAGER"
GUIDE = "PRESS ESC TO QUIT"

STAR_COUNT = 40         # 星の数
STAR_SPEED_MIN = 0.3    # 星の速さの下限（ドット／フレーム）
STAR_SPEED_MAX = 1.8    # 星の速さの上限

SHIP_U = 0              # 台紙のどこから切り出すか（横）
SHIP_V = 0              # 台紙のどこから切り出すか（縦）
SHIP_WIDTH = 16         # 宇宙船の幅
SHIP_HEIGHT = 16        # 宇宙船の高さ
SHIP_SPEED = 2          # 1 フレームに進むドット数

class App:
    """このゲーム全体を受け持つ箱"""

    def __init__(self):
        """箱が作られるときに1回だけ呼ばれる。ここで準備をすませる"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Star Voyager")
        pyxel.load("assets.pyxres")     # 絵と音のファイルを読み込む

        self.stars = []     # 星をぜんぶ入れるリスト
        self.make_stars()

        # 宇宙船の位置を覚えておく
        self.ship_x = (SCREEN_WIDTH - SHIP_WIDTH) // 2      # 横は画面の中央
        self.ship_y = 80                                    # 縦は下の方

        self.bgm_on = True                                  # BGM が鳴っているかどうか
        pyxel.playm(0, loop=True)                           # BGM をループ再生する

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

    def move_ship(self):
        """矢印キーで宇宙船を動かす。画面の外へは出さない"""
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.ship_x -= SHIP_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.ship_x += SHIP_SPEED
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.ship_y -= SHIP_SPEED
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.ship_y += SHIP_SPEED

        # 画面の外へ出ないように、行きすぎた分を押し戻す
        self.ship_x = max(0, min(self.ship_x, SCREEN_WIDTH - SHIP_WIDTH))
        self.ship_y = max(0, min(self.ship_y, SCREEN_HEIGHT - SHIP_HEIGHT))

    def update(self):
        """フレーム毎の更新処理"""
        if pyxel.btnp(pyxel.KEY_M):                             # M を押した瞬間だけ
            if self.bgm_on:
                pyxel.stop()                                    # 鳴っていたら止める
            else:
                pyxel.playm(0, loop = True)                     # 止まっていたら鳴らす
            self.bgm_on = not self.bgm_on                       # 状態を反転させる
            
        self.move_ship()
        
        for star in self.stars:
            star[1] += star[2]                                  # y に速さを足す

            if star[1] >= SCREEN_HEIGHT:                        # 画面の下に出たら
                star[0] = random.randint(0, SCREEN_WIDTH - 1)   # x を引き直して
                star[1] = 0                                     # いちばん上に戻す

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(0)

        # 1. 星（いちばん奥）
        for star in self.stars:
            pyxel.pset(star[0], star[1], self.star_color(star[2]))

        # 2. 宇宙船（星より手前）
        pyxel.blt(
            self.ship_x, self.ship_y,   # 画面のどこに貼るか
            0,                          # どのイメージバンクから取るか
            SHIP_U, SHIP_V,             # 台紙のどこから切り出すか
            SHIP_WIDTH, SHIP_HEIGHT,    # 何ドット分取り出すか
            pyxel.COLOR_BLACK,          # この色は塗らない（透過色）
        )

        # 3. 文字（いちばん手前）
        self.text_center(20, TITLE, pyxel.COLOR_YELLOW)
        self.text_center(34, GUIDE, pyxel.COLOR_GRAY)

App()
