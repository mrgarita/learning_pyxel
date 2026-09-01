# -*- coding: utf-8 -*-
import pyxel
import random
from datetime import datetime

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 64

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
        # 魚の初期設定
        self.fish_x = SCREEN_WIDTH
        self.fish_y = 8
        self.fish_speed = FISH_SPEED
        self.fish_direction = DIRECTION_LEFT

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="dot_fish", fps=15)
        pyxel.load("fish_clock.pyxres")
        
        pyxel.run(self.update, self.draw)

    def change_fish_direction(self):
        """魚の移動方向を反転させる"""
        self.fish_direction = -self.fish_direction
        self.fish_y = random.randint(0, SCREEN_HEIGHT - FISH_HEIGHT // 2)   # Y 座標はその都度変える

    def update(self):
        """フレーム毎の更新処理"""
        # 現在時刻取得
        self.today = datetime.now()
        self.hour = self.today.hour
        self.minute = self.today.minute

        # 端まで行ったら向きを変える
        if self.fish_x < FISH_X_MIN:        # 左端
            self.fish_x = FISH_X_MIN
            self.change_fish_direction()
        if self.fish_x > FISH_X_MAX:        # 右端
            self.fish_x = FISH_X_MAX
            self.change_fish_direction()

        # 魚の移動
        self.fish_x = self.fish_x + self.fish_speed * self.fish_direction

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

        # 時計の「:」をチカチカさせる
        if pyxel.frame_count % 15 == 0:
            mytime = f"{self.hour:02} {self.minute:02}"
        else:
            mytime = f"{self.hour:02}:{self.minute:02}"

        # 画面中央に時計を表示
        time_x = (SCREEN_WIDTH - len(mytime) * pyxel.FONT_WIDTH) // 2
        time_y = (SCREEN_HEIGHT - pyxel.FONT_HEIGHT) // 2 
        pyxel.text(time_x, time_y, mytime, pyxel.COLOR_YELLOW)
  
App()
