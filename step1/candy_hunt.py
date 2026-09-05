# candy_hunt.py
# step1 フェーズ9：効果音と BGM をつける

import random

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

BOY_SIZE = 8            # 男の子の絵の大きさ（縦横とも 8 ドット）
BOY_SPEED = 2           # 1 フレームで進むドット数

CANDY_SIZE = 8          # お菓子の絵の大きさ

GHOST_SIZE = 8          # お化けの絵の大きさ
GHOST_MOVE_EVERY = [2, 4, 1, 3, 5]     # 出てくる順に「何フレームに 1 回動くか」
GHOST_SPAWN_SCORE = 5   # お菓子を何個取るごとに 1 体増やすか

HIT_SIZE = 4            # 当たり判定に使う四角の大きさ（絵の中央だけを見る）
HIT_OFFSET = (BOY_SIZE - HIT_SIZE) // 2     # 絵の左上から、判定の四角までの距離（= 2）

SCENE_PLAY = 0          # あそんでいる画面
SCENE_GAMEOVER = 1      # ゲームオーバーの画面
SCENE_TITLE = 2         # タイトル画面

GAMEOVER_WAIT = 20      # 捕まってから文字を出すまでのフレーム数（0.67秒）
BLINK_CYCLE = 30        # 点滅 1 周期のフレーム数（1秒）
BLINK_ON = 20           # そのうち文字が見えているフレーム数

SOUND_CANDY = 0         # お菓子を取った音
SOUND_CAUGHT = 1        # 捕まった音
SOUND_GHOST = 2         # お化けが増えた音
MUSIC_BGM = 0           # BGM（チャンネル 0 と 1 を使う）
MUSIC_GAMEOVER = 1      # ゲームオーバーの BGM

CH_SE = 2               # 効果音を鳴らすチャンネル
CH_EVENT = 3            # お化けが増えた音だけ別のチャンネルにする

CORNERS = [             # お化けが出てくる 4 隅
    (0, 0),
    (SCREEN_WIDTH - GHOST_SIZE, 0),
    (0, SCREEN_HEIGHT - GHOST_SIZE),
    (SCREEN_WIDTH - GHOST_SIZE, SCREEN_HEIGHT - GHOST_SIZE),
]

def is_hit(x1, y1, size1, x2, y2, size2):
    """2 つの四角が重なっていれば True を返す"""
    return (x1 < x2 + size2 and x2 < x1 + size1 and
            y1 < y2 + size2 and y2 < y1 + size1)

def draw_center(s, y, col):
    """文字列を画面の横中央に描く"""
    x = (SCREEN_WIDTH - len(s) * 4) // 2     # 4 は1文字分のフォント幅
    pyxel.text(x, y, s, col)

def is_blink_on():
    """点滅の「見えている」タイミングなら True を返す"""
    return pyxel.frame_count % BLINK_CYCLE < BLINK_ON

def far_corner(x, y):
    """(x, y) からいちばん遠い隅を返す"""
    best_x, best_y = CORNERS[0]
    best_distance = -1

    for corner_x, corner_y in CORNERS:
        distance = abs(corner_x - x) + abs(corner_y -y)
        if distance > best_distance:
            best_x, best_y = corner_x, corner_y
            best_distance = distance

    return best_x, best_y

class Ghost:
    """お化け 1 体ぶんの場所と動き"""

    def __init__(self, x, y, move_every):
        """1 体作るときに、置く場所と動く間隔を決める"""
        self.x = x
        self.y = y
        self.move_every = move_every
        self.born_frame = pyxel.frame_count     # 生まれた時刻を覚えておく

    def move(self, target_x, target_y):
        """自分の番のフレームだけ、目標へ 1 ドット近づく"""
        if pyxel.frame_count % self.move_every != 0:
            return

        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Candy Hunt")
        pyxel.load("candy_hunt.pyxres")

        self.scene = SCENE_TITLE
        self.reset_game()

        pyxel.run(self.update, self.draw)

    def start_game(self):
        """ゲームを始める。中身を初期化して BGM を鳴らし始める"""
        self.reset_game()
        self.scene = SCENE_PLAY
        pyxel.playm(MUSIC_BGM, loop=True)

    def reset_game(self):
        """ゲームの中身を、最初の状態に戻す"""
        self.boy_x = SCREEN_WIDTH // 2 - BOY_SIZE // 2
        self.boy_y = SCREEN_HEIGHT // 2 - BOY_SIZE // 2
        self.score = 0
        self.ghosts = []
        self.add_ghost()
        self.place_candy()

    def add_ghost(self):
        """男の子からいちばん遠い隅に、お化けを 1 体足す"""
        move_every = GHOST_MOVE_EVERY[len(self.ghosts)]
        x, y = far_corner(self.boy_x, self.boy_y)
        self.ghosts.append(Ghost(x, y, move_every))

    def update(self):
        """フレーム毎の更新処理"""
        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_PLAY:
            self.update_play()
        else:
            self.update_gameover()

    def update_title(self):
        """タイトル画面。Enter でゲームを始める"""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game()

    def update_gameover(self):
        """ゲームオーバー画面。少し待ってから、Enter でゲームを再び始める"""
        elapsed = pyxel.frame_count - self.gameover_frame

        if elapsed == GAMEOVER_WAIT:        # ちょうどこのフレームだけ通る
            pyxel.playm(MUSIC_GAMEOVER)     # 捕まった音が終わってからジングル

        if elapsed < GAMEOVER_WAIT:
            return

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game()

    def update_play(self):
        """あそんでいる間の更新"""
        self.move_boy()
        self.move_ghosts()
        self.check_candy()
        self.check_ghosts()

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

    def move_ghosts(self):
        """お化けを男の子に近づける"""
        for ghost in self.ghosts:
            ghost.move(self.boy_x, self.boy_y)

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
            pyxel.play(CH_SE, SOUND_CANDY)          # 取った音
            self.place_candy()

            if (self.score % GHOST_SPAWN_SCORE == 0
                and len(self.ghosts) < len(GHOST_MOVE_EVERY)):
                self.add_ghost()
                pyxel.play(CH_EVENT, SOUND_GHOST)     # 増えた音

    def check_ghosts(self):
        """どれか 1 体にでも捕まったらゲームオーバーにする"""
        for ghost in self.ghosts:
            if is_hit(self.boy_x + HIT_OFFSET, self.boy_y + HIT_OFFSET, HIT_SIZE,
                    ghost.x + HIT_OFFSET, ghost.y + HIT_OFFSET, HIT_SIZE):
                self.scene = SCENE_GAMEOVER
                self.gameover_frame = pyxel.frame_count     # 捕まった時刻を覚えておく
                pyxel.stop()                                # BGM を止めてから
                pyxel.play(CH_SE, SOUND_CAUGHT)             # 捕まった音
                return

    def draw(self):
        """フレーム毎の描画処理"""
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.scene == SCENE_TITLE:
            self.draw_title()
            return
        
        self.draw_play()

        if self.scene == SCENE_GAMEOVER:
            self.draw_gameover()

    def draw_title(self):
        """タイトル画面を描く"""
        draw_center("CANDY HUNT", 44, pyxel.COLOR_YELLOW)

        if is_blink_on():
            draw_center("PRESS ENTER", 68, pyxel.COLOR_WHITE)

    def draw_play(self):
        """あそんでいる画面を描く"""
        pyxel.blt(self.candy_x, self.candy_y, 0, 16, 0,
                  CANDY_SIZE, CANDY_SIZE, pyxel.COLOR_BLACK)    # お菓子

        for ghost in self.ghosts:                               # お化けは何体でも
            if pyxel.frame_count - ghost.born_frame < 30 and not is_blink_on():
                continue                # 出てきて 1 秒は、点滅の消える側で描かない

            pyxel.blt(ghost.x, ghost.y, 0, 8, 0,
                      GHOST_SIZE, GHOST_SIZE, pyxel.COLOR_BLACK)
            
        pyxel.blt(self.boy_x, self.boy_y, 0, 0, 0,
                  BOY_SIZE, BOY_SIZE, pyxel.COLOR_BLACK)        # 男の子

        pyxel.text(4, 4, f"SCORE {self.score}", pyxel.COLOR_WHITE)               # スコア

    def draw_gameover(self):
        """ゲームオーバーの文字を重ねて描く"""
        elapsed = pyxel.frame_count - self.gameover_frame       # 捕まってからの経過
        if elapsed < GAMEOVER_WAIT:
            return
        
        if elapsed % BLINK_CYCLE < BLINK_ON:
            draw_center("GAME OVER", 52, pyxel.COLOR_RED)
            draw_center("PRESS ENTER TO RETRY", 80, pyxel.COLOR_GRAY)

        draw_center(f"SCORE {self.score}", 66, pyxel.COLOR_WHITE)

App()
