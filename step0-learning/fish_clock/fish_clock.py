# -*- coding: utf-8 -*-
import pyxel
import random
from datetime import datetime

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 64

TITLE = "dot_fish"
TIME_COLOR = pyxel.COLOR_YELLOW

FISH_WIDTH = 8
FISH_HEIGHT = 8
FISH_SPEED = 0.5
FISH_X_MIN = 0 - FISH_WIDTH * 2
FISH_X_MAX = SCREEN_WIDTH + FISH_WIDTH

DIRECTION_RIGHT = 1
DIRECTION_LEFT = -1

class App:
    def __init__(self):
        """起動時の設定"""
        self.last_minute = datetime.now().minute    # 前回のフレームで見た「分」

        # 魚の初期設定
        self.fish_x = SCREEN_WIDTH
        self.fish_y = 8
        self.fish_speed = FISH_SPEED
        self.fish_direction = DIRECTION_LEFT

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, fps=15)
        pyxel.load("fish_clock.pyxres")
        
        pyxel.run(self.update, self.draw)

    def change_fish_direction(self):
        """魚の移動方向を反転させる"""
        self.fish_direction = -self.fish_direction
        self.fish_y = random.randint(0, SCREEN_HEIGHT - FISH_HEIGHT // 2)   # Y 座標はその都度変える

    def center_text(self, s, col):
        """画面中央に文字を配置"""
        x = (SCREEN_WIDTH - len(s) * pyxel.FONT_WIDTH) // 2
        y = (SCREEN_HEIGHT - pyxel.FONT_HEIGHT) // 2 
        pyxel.text(x, y, s, col)

    def play_chime(self):
        """時報を鳴らす"""
        pyxel.playm(0, loop=False)

    def set_time(self):
        """時刻の取得とチャイム設定"""
        self.today = datetime.now()
        self.hour = self.today.hour
        self.minute = self.today.minute

        # 分が変わった瞬間だけ判定する
        if self.minute != self.last_minute:
            if self.minute == 0:
                self.play_chime()           # 時報を鳴らす
            self.last_minute = self.minute  # これが無いと1分間鳴り続ける

    def move_fish(self):
        """魚をを泳がせ、端まで来たら向きを変える"""
        self.fish_x = self.fish_x + self.fish_speed * self.fish_direction

        # 動ける範囲の外に出たら、範囲内に戻して向きを変える
        if not FISH_X_MIN <= self.fish_x <= FISH_X_MAX:
            self.fish_x = max(FISH_X_MIN, min(self.fish_x, FISH_X_MAX))
            self.change_fish_direction()

    def update(self):
        """フレーム毎の更新処理"""
        self.set_time()
        self.move_fish()

    def draw(self):
        """描画処理"""
        pyxel.cls(pyxel.COLOR_NAVY)

        # 魚表示
        pyxel.blt(
              self.fish_x, self.fish_y,         # 表示位置XY
              0,                                # イメージバンク番号
              (pyxel.frame_count % 2) * 8, 0,   # 切り出し位置XY:フレーム毎にX座標をかえて2枚のドット絵を使って泳いでいるように見せる
              -self.fish_direction * 8, 8,      # 切り出し幅と高さ：幅は進行方向により変えている
              pyxel.COLOR_BLACK                 # 透過色
          )

        # 時刻を2桁で表示 ex) 10:05
        hours = f"{self.hour:02}"
        minutes = f"{self.minute:02}"

        # 時計の「:」をチカチカさせる
        if pyxel.frame_count % 15 == 0:
            sep = " "
        else:
            sep = ":"

        str_time = f"{hours}{sep}{minutes}"

        # 画面中央に時計を表示
        self.center_text(str_time, TIME_COLOR)

  
App()
