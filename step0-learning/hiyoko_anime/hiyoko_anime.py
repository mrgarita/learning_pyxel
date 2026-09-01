# hiyoko_anime.py
# step0 で学んだことの復習：ヒヨコを動かしてBGMを鳴らす

import pyxel
import random

SCREEN_WIDTH = 240
SCREEN_HEIGHT = 128

HIYOKO_U = 0            # ヒヨコ画像の切り出し位置X
HIYOKO_V = 0            # ヒヨコ画像の切り出し位置Y
HIYOKO_WIDTH = 16       # ヒヨコ画像の幅
HIYOKO_HEIGHT = 16      # ヒヨコ画像の高さ
HIYOKO_SPEED = 1        # ヒヨコの移動速度
HIYOKO_SCALE_MAX = 16   # ヒヨコの大きさの上限
GROUND_Y = 111          # ヒヨコの足元を置くY座標

class App:
    def __init__(self):
        """初期化処理"""

        self.flowers = []
        
        # 画面生成
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title = "Hiyoko Anime")

        # リソース読み込み
        pyxel.load("hiyoko_anime.pyxres")
        pyxel.playm(0, loop = True)     # BGM を鳴らす

        # ヒヨコの初期位置
        self.hiyoko_x = (SCREEN_WIDTH - HIYOKO_WIDTH) // 2
        self.hiyoko_direction = 1       # ヒヨコ 画像の向き（1: 順方向 -1: 左右反転）
        self.hiyoko_scale = 1           # ヒヨコ の大きさ
        self.put_on_ground()            # 足元を地面に合わせる

        # 実行
        pyxel.run(self.update, self.draw)

    def put_on_ground(self):
        """ヒヨコの足元が地面につくようにY座標を決める"""
        self.hiyoko_y = GROUND_Y - HIYOKO_HEIGHT * (self.hiyoko_scale + 1) / 2

    def grow_hiyoko(self):
        """ヒヨコを1段階大きくする（上限まで）"""
        self.hiyoko_scale = min(self.hiyoko_scale + 0.2, HIYOKO_SCALE_MAX)
        self.put_on_ground()

    def move_hiyoko(self):
        """ヒヨコの移動処理"""
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.hiyoko_x -= HIYOKO_SPEED
            self.hiyoko_direction = 1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.hiyoko_x += HIYOKO_SPEED
            self.hiyoko_direction = -1

        # ヒヨコ が画面の端で出ないようにする
        self.hiyoko_x = max(-HIYOKO_WIDTH // 2, min(self.hiyoko_x, SCREEN_WIDTH - HIYOKO_WIDTH // 2))

    def make_flower(self):
        """花 の生成処理"""
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            x = random.randint(0, SCREEN_WIDTH - 3)
            y = 0
            vx = random.randint(-2, 2)
            vy = random.randint(1, 5)
            self.flowers.append([x, y, vx, vy])

    def move_flowers(self):
        """花 の移動処理"""
        alive = []
        for flower in self.flowers:
            x, y, vx, vy = flower

            x += vx
            y += vy

            #ヒヨコ にぶつかったら消える
            if pyxel.pget(x+1, y+2) == pyxel.COLOR_YELLOW:
                self.grow_hiyoko()        # ヒヨコが大きくなる
                continue

            # 花 草にぶつかったら止まる
            if pyxel.pget(x+1, y+3) == pyxel.COLOR_GREEN:
                vx = 0
                vy = 0

            if y <= SCREEN_HEIGHT:
                alive.append([x, y, vx, vy])

        self.flowers[:] = alive     # self.flowers の中身を alive に入れ替える

    def update(self):
        """更新処理"""
        self.make_flower()
        self.move_flowers()
        self.move_hiyoko()

        # --- info ---
        if pyxel.frame_count % 30 == 0:
            print(f"flowers: {len(self.flowers)} scale: {self.hiyoko_scale}")

    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)

        # 雲
        pyxel.blt(20, 20, 0, 0, 32, 32, 32, pyxel.COLOR_BLACK)
        pyxel.blt(180, -10, 0, 0, 32, 32, 32, pyxel.COLOR_BLACK)

        # 地面
        for i in range(0, SCREEN_WIDTH, 16):
            pyxel.blt(i, 112, 0, 0, 16, 16, 16, pyxel.COLOR_BLACK)

        # ヒヨコ
        pyxel.blt(
            self.hiyoko_x, self.hiyoko_y,                           # ヒヨコ の表示位置XY
            0,                                                      # イメージバンク番号
            HIYOKO_U + (pyxel.frame_count // 5) % 2 * HIYOKO_WIDTH, HIYOKO_V,  # 切り出し位置XY
            HIYOKO_WIDTH * self.hiyoko_direction, HIYOKO_HEIGHT,    # 切り出す幅（向きを考慮）と高さ
            pyxel.COLOR_BLACK,                                      # 透過色
            0,                                                      # 回転角
            self.hiyoko_scale                                       # スケール
        )

        # 草
        for i in range(0, SCREEN_WIDTH, 8):
            pyxel.blt(i, 108, 0, 16, 16, 8, 4, pyxel.COLOR_BLACK)

        # 花
        for flower in self.flowers:
            x, y, vx, vy = flower
            pyxel.blt(x, y, 0, 16, 20, 3, 3, pyxel.COLOR_BLACK)


App()
