# candy_hunt.py
# step1 フェーズ5：お化けに追いかけさせる

import random

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

BOY_SIZE = 8            # 男の子の絵の大きさ（縦横とも 8 ドット）
BOY_SPEED = 2           # 1 フレームで進むドット数

CANDY_SIZE = 8          # お菓子の絵の大きさ

GHOST_SIZE = 8          # お化けの絵の大きさ
GHOST_SPEED = 1         # 1 フレームで進むドット数（男の子の半分）

HIT_SIZE = 4            # 当たり判定に使う四角の大きさ（絵の中央だけを見る）
HIT_OFFSET = (BOY_SIZE - HIT_SIZE) // 2     # 絵の左上から、判定の四角までの距離（= 2）

SCENE_PLAY = 0          # あそんでいる画面
SCENE_GAMEOVER = 1      # ゲームオーバーの画面

def is_hit(x1, y1, size1, x2, y2, size2):
    """2 つの四角が重なっていれば True を返す"""
    return (x1 < x2 + size2 and x2 < x1 + size1 and
            y1 < y2 + size2 and y2 < y1 + size1)

def draw_center(s, y, col):
    """文字列を画面の横中央に描く"""
    x = (SCREEN_WIDTH - len(s) *4) // 2     # 4 は1文字分のフォント幅
    pyxel.text(x, y, s, col)

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Candy Hunt")
        pyxel.load("candy_hunt.pyxres")

        self.scene = SCENE_PLAY
        self.boy_x = SCREEN_WIDTH // 2 - BOY_SIZE // 2
        self.boy_y = SCREEN_HEIGHT // 2 - BOY_SIZE // 2
        self.ghost_x = 0
        self.ghost_y = 0
        self.score = 0
        self.place_candy()

        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム毎の更新処理"""
        if self.scene == SCENE_PLAY:
            self.update_play()

    def update_play(self):
        """あそんでいる間の更新"""
        self.move_boy()
        self.move_ghost()
        self.check_candy()
        self.check_ghost()

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

    def move_ghost(self):
        """お化けを男の子に近づける"""
        if self.ghost_x < self.boy_x:
            self.ghost_x += GHOST_SPEED
        elif self.ghost_x > self.boy_x:
            self.ghost_x -= GHOST_SPEED

        if self.ghost_y < self.boy_y:
            self.ghost_y += GHOST_SPEED
        elif self.ghost_y > self.boy_y:
            self.ghost_y -= GHOST_SPEED

    def place_candy(self):
        """男の子と重ならない場所へ、お菓子を置きなおす"""
        while True:
            self.candy_x = random.randint(0, SCREEN_WIDTH - CANDY_SIZE)
            self.candy_y = random.randint(0, SCREEN_HEIGHT - CANDY_SIZE)
            if not is_hit(self.boy_x, self.boy_y, BOY_SIZE,
                          self.candy_x, self.candy_y, CANDY_SIZE):
                break

    def check_candy(self):
        """お菓子がしっかり重なったら、スコアを増やして次の場所に置きなおす"""
        if is_hit(self.boy_x + HIT_OFFSET, self.boy_y + HIT_OFFSET, HIT_SIZE,
                  self.candy_x + HIT_OFFSET, self.candy_y + HIT_OFFSET, HIT_SIZE):
            self.score += 1
            self.place_candy()

    def check_ghost(self):
        """お化けに捕まったらゲームオーバーにする"""
        if is_hit(self.boy_x + HIT_OFFSET, self.boy_y + HIT_OFFSET, HIT_SIZE,
                  self.ghost_x + HIT_OFFSET, self.ghost_y + HIT_OFFSET, HIT_SIZE):
            self.scene = SCENE_GAMEOVER
            self.gameover_frame = pyxel.frame_count     # 捕まった時刻を覚えておく

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_play()

        if self.scene == SCENE_GAMEOVER:
            self.draw_gameover()

    def draw_play(self):
        """あそんでいる画面を描く"""
        pyxel.blt(self.candy_x, self.candy_y, 0, 16, 0,
                  CANDY_SIZE, CANDY_SIZE, pyxel.COLOR_BLACK)    # お菓子
        pyxel.blt(self.ghost_x, self.ghost_y, 0, 8, 0,
                  GHOST_SIZE, GHOST_SIZE, pyxel.COLOR_BLACK)    # お化け
        pyxel.blt(self.boy_x, self.boy_y, 0, 0, 0,
                  BOY_SIZE, BOY_SIZE, pyxel.COLOR_BLACK)        # 男の子
        pyxel.text(4, 4, f"SCORE {self.score}", pyxel.COLOR_WHITE)               # スコア

    def draw_gameover(self):
        """ゲームオーバーの文字を重ねて描く"""
        if pyxel.frame_count - self.gameover_frame < 15:    # 0.5 秒は文字を出さない
            return
        
        if pyxel.frame_count % 30 < 20:     # 30 フレームのうち 20 だけ描く（点滅したようにみせる）
            draw_center("GAME OVER", 52, pyxel.COLOR_RED)

        draw_center(f"SCORE {self.score}", 66, pyxel.COLOR_WHITE)

App()
