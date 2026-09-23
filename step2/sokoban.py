# sokoban.py
# step2 フェーズ6：ステージを 10 個にする

import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
TILE = 8                # 1 マスの大きさ（ドット）
HUD_HEIGHT = 12         # 画面の上、手数などを出すために空けておく高さ
MOVE_FRAMES = 8         # 隣のマスへ移りきるまでにかけるフレーム数

SCENE_TITLE = 0         # タイトル画面
SCENE_GAME = 1          # あそんでいる画面

BLINK_CYCLE = 30        # 点滅 1 周期のフレーム数（1 秒）
BLINK_ON = 20           # そのうち文字が見えているフレーム数

# イメージバンク 0 の、切り出し位置
V_TILE = 0              # タイルの段
V_PLAYER_A = 8          # 主人公の段（コマ A）
V_PLAYER_B = 16         # 主人公の段（コマ B・足を入れ替えた絵）
U_FLOOR = 0             # 床（歩ける）
U_WALL = 8              # 壁（歩けない）
U_GOAL = 16             # ゴール
U_BOX = 24              # 荷物
U_BOX_ON_GOAL = 32      # ゴールに乗っている荷物

# 向き。この番号がそのまま主人公の絵の切り出し位置になる
DIR_DOWN = 0
DIR_UP = 1
DIR_LEFT = 2
DIR_RIGHT = 3

# 向きごとの、1 歩ぶんのずれ（x のずれ, y のずれ）
MOVES = [
    (0, 1),         # 下
    (0, -1),        # 上
    (-1, 0),        # 左
    (1, 0),         # 右
]

# ステージの地図
# # 壁  . 床  O ゴール  $ 荷物  @ 主人公
STAGE1 = [
    "########",
    "#......#",
    "#..O.O.#",
    "#..$.$.#",
    "#..@...#",
    "########",
]

STAGE2 = [          # 横にも押せる
    "########",
    "#......#",
    "#.$..O.#",
    "#.@....#",
    "#.$..O.#",
    "#......#",
    "########",
]

STAGE3 = [          # 縦と横を組み合わせる
    "#########",
    "#.O...O.#",
    "#.......#",
    "#..$....#",
    "#....$..#",
    "#..@....#",
    "#.......#",
    "#########",
]

STAGE4 = [          # 壁があるので、押す側へ回り込む
    "##########",
    "#........#",
    "#.O.##.O.#",
    "#...##...#",
    "#..$..$..#",
    "#........#",
    "#...@....#",
    "##########",
]

STAGE5 = [          # 段が仕切られていて、行き来に回り道がいる
    "##########",
    "#........#",
    "#O..$....#",
    "#...##...#",
    "#O..$....#",
    "#...##...#",
    "#O..$....#",
    "#....@...#",
    "##########",
]

STAGE6 = [          # どれから動かすか、順番を考える
    "##########",
    "#........#",
    "#.O.O.O..#",
    "#........#",
    "#.$......#",
    "#..$.....#",
    "#...$....#",
    "#....@...#",
    "##########",
]

STAGE7 = [          # 1 マスの通路。押す向きが決まってしまう
    "#############",
    "#...........#",
    "#OO.........#",
    "#..###.###..#",
    "#.$###.###..#",
    "#..###.###..#",
    "#OO###.###..#",
    "#.$###.###..#",
    "#.@..$....$.#",
    "#...........#",
    "#############",
]

STAGE8 = [          # 荷物が固まって始まる。動かす順番をまちがえられない
    "#############",
    "#@$......OO.#",
    "#.$$$....OO.#",
    "#...........#",
    "#.#########.#",
    "#...........#",
    "#.#########.#",
    "#...........#",
    "#...........#",
    "#...........#",
    "#############",
]

STAGE9 = [          # 中央の大きな壁を、大きく回って運ぶ
    "#############",
    "#...........#",
    "#.OO........#",
    "#...#####...#",
    "#...#####...#",
    "#..$#####...#",
    "#.OO#####...#",
    "#...#####.$.#",
    "#........$$.#",
    "#........@..#",
    "#############",
]

STAGE10 = [         # 仕上げ。遠回りと詰みの両方
    "#############",
    "#...........#",
    "#...$@$.$.$.#",
    "#...........#",
    "#...#.#######",
    "#O###.#O#...#",
    "#...#.#..OO.#",
    "#.#.#.#.$##.#",
    "#.$.....$O#.#",
    "#..#.....O#O#",
    "#############",    
]

STAGES = [STAGE1, STAGE2, STAGE3, STAGE4, STAGE5,
          STAGE6, STAGE7, STAGE8, STAGE9, STAGE10]

def draw_center(text, y, color):
    """文字を、画面の横まんなかに描く"""
    x = (SCREEN_WIDTH - len(text) * 4) // 2
    pyxel.text(x, y, text, color)

def is_blink_on():
    """点滅の「見えている」タイミングなら True を返す"""
    return pyxel.frame_count % BLINK_CYCLE < BLINK_ON

class App:
    def __init__(self):
        """起動時の設定"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Sokoban")
        pyxel.load("sokoban.pyxres")
        self.scene = SCENE_TITLE        # 起動したら、まずタイトル画面
        self.stage_no = 0               # いま何番目のステージか（0 から数える）
        self.all_cleared = False        # 10 個ぜんぶ終わったか
        pyxel.run(self.update, self.draw)

    def start_game(self):
        """いまの stage_no のステージを読み込んで、ゲームを始める"""
        self.load_stage(STAGES[self.stage_no])
        self.scene = SCENE_GAME

    def load_stage(self, rows):
        """文字の地図を読んで、壁・主人公・荷物に分ける"""
        self.tiles = []
        self.boxes = []
        self.player_dir = DIR_DOWN      # はじめは下を向いている
        self.walk_timer = 0             # 0 なら止まっている。1～8は歩いている途中
        self.pushing = False            # いまの一歩で荷物を押しているか
        self.cleared = False            # このステージをクリアしたか

        for y in range(len(rows)):
            line = []
            for x in range(len(rows[y])):
                mark = rows[y][x]
                if mark == "@":
                    self.player_x = x
                    self.player_y = y
                    mark = "."          # 主人公の足元は床
                elif mark == "$":
                    self.boxes.append([x, y])
                    mark = "."          # 荷物の下も床
                line.append(mark)
            self.tiles.append(line)

        self.from_x = self.player_x     # 見た目の出発マス
        self.from_y = self.player_y

        # 盤面を画面の中央に置くための、ずらし幅
        board_w = len(self.tiles[0]) * TILE
        board_h = len(self.tiles) * TILE
        self.ox = (SCREEN_WIDTH - board_w) // 2
        self.oy = HUD_HEIGHT + (SCREEN_HEIGHT - HUD_HEIGHT - board_h) // 2

    def update(self):
        """フレーム毎の更新処理。いまの画面の担当へ渡す"""
        if self.scene == SCENE_TITLE:
            self.update_title()
        else:
            self.update_game()

    def update_title(self):
        """タイトル画面。Enter でゲームを始める"""
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game()

    def update_game(self):
        """あそんでいる間の更新"""
        if self.all_cleared:                    # ぜんぶおわった。Enter で 1 面から
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.stage_no = 0
                self.all_cleared = False
                self.scene = SCENE_TITLE
            return
        
        if pyxel.btnp(pyxel.KEY_R):             # いつでも、最初からやり直せる
            self.load_stage(STAGES[self.stage_no])
            return

        if self.cleared:                        # クリアした。Enter で次のステージへ
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.next_stage()
            return
        
        if self.walk_timer > 0:                 # 歩いている途中
            self.walk_timer += 1
            if self.walk_timer > MOVE_FRAMES:   # 隣のマスに着いた
                self.walk_timer = 0
                self.from_x = self.player_x     # 見た目を、いまいるマスに合わせる
                self.from_y = self.player_y
                self.pushing = False
                if self.is_cleared():           # 着いた、その瞬間に調べる
                    self.cleared = True

        # 止まっていて、まだクリアしていないときだけ、キーを見る    
        if self.walk_timer == 0 and not self.cleared:
            self.handle_key()

    def handle_key(self):
        """矢印キーを見て、押された向きへ 1 歩進もうとする"""
        if pyxel.btn(pyxel.KEY_DOWN):
            self.try_move(DIR_DOWN)
        elif pyxel.btn(pyxel.KEY_UP):
            self.try_move(DIR_UP)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.try_move(DIR_LEFT)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.try_move(DIR_RIGHT)

    def has_box(self, x, y):
        """そのマスに荷物があるかどうかを答える"""
        for box in self.boxes:
            if box[0] == x and box[1] == y:
                return True
        return False

    def move_box(self, x, y, dx, dy):
        """(x, y) にある荷物を、(dx, dy) だけ動かす"""
        for box in self.boxes:
            if box[0] == x and box[1] == y:
                box[0] += dx
                box[1] += dy
                return

    def on_goal(self, box):
        """その荷物が、ゴールのマスに乗っているか"""
        return self.tiles[box[1]][box[0]] == "O"

    def is_cleared(self):
        """すべての荷物がゴールに乗ったか"""
        return all(self.on_goal(box) for box in self.boxes)

    def next_stage(self):
        """次のステージへ進む。最後だったら全クリア"""
        if self.stage_no + 1 < len(STAGES):
            self.stage_no += 1
            self.load_stage(STAGES[self.stage_no])
        else:
            self.all_cleared = True

    def try_move(self, direction):
        """その向きへ動けるか調べて、動けるときだけ 1 マス進む"""
        self.player_dir = direction     # 動けなくても、向きだけは変える

        dx, dy = MOVES[direction]
        next_x = self.player_x + dx
        next_y = self.player_y + dy

        if self.tiles[next_y][next_x] == "#":   # 行き先が壁なら
            return                              # 何もしないで戻る

        if self.has_box(next_x, next_y):        # 行き先に荷物があるなら
            far_x = next_x + dx                 # 荷物の、1 つ先のマス
            far_y = next_y + dy
            if self.tiles[far_y][far_x] == "#": # その先が壁なら押せない
                return
            if self.has_box(far_x, far_y):      # その先に別の荷物があっても押せない
                return
            self.move_box(next_x, next_y, dx, dy)
            self.pushing = True                 # この一歩は、荷物を押している

        self.player_x = next_x
        self.player_y = next_y
        self.walk_timer = 1                     # ここから 8 フレームかけて歩く

    def slide_pos(self, origin, from_cell, to_cell):
        """出発マスから到着マスへ、いまどこまで来たかをドットで返す"""
        moved = (to_cell - from_cell) * TILE * self.walk_timer // MOVE_FRAMES
        return origin + from_cell * TILE + moved

    def draw(self):
        """フレーム毎の描画処理。画面を消してから、担当へ渡す"""
        pyxel.cls(pyxel.COLOR_BLACK)    # 各画面で使うので、ここに 1 回だけ

        if self.scene == SCENE_TITLE:
            self.draw_title()
        else:
            self.draw_game()

    def draw_title(self):
        """タイトル画面を描く"""
        draw_center("SOKOBAN", 30, pyxel.COLOR_YELLOW)
        draw_center("PUSH THE APPLES", 44, pyxel.COLOR_WHITE)

        # ワンコが、リンゴをゴールへ押していく絵
        x = SCREEN_WIDTH // 2 - TILE * 2
        pyxel.blt(x, 66, 0, DIR_RIGHT * TILE, V_PLAYER_A, TILE, TILE, pyxel.COLOR_GRAY)
        pyxel.blt(x + TILE, 66, 0, U_BOX, V_TILE, TILE, TILE, pyxel.COLOR_BLACK)
        pyxel.blt(x + TILE * 3, 66, 0, U_GOAL, V_TILE, TILE, TILE)

        if is_blink_on():               # 1 秒のうち 20 フレームだけ見える
            draw_center("PRESS ENTER", 92, pyxel.COLOR_WHITE)

        draw_center("ARROW: MOVE    R: RETRY", 108, pyxel.COLOR_GRAY)

    def draw_game(self):
        """あそんでいる画面を描く"""

        # 壁を、上の行から 1 マスずつ描く
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                mark = self.tiles[y][x]
                if mark == "#":
                    u = U_WALL
                elif mark == "O":
                    u = U_GOAL
                else:
                    u = U_FLOOR
                pyxel.blt(self.ox + x * TILE, self.oy + y * TILE,
                            0, u, V_TILE, TILE, TILE)

        # 荷物。押している 1 つだけは、主人公といっしょにすべる
        dx, dy = MOVES[self.player_dir]
        push_x = self.player_x + dx             # 押した荷物は主人公の目の前にいる
        push_y = self.player_y + dy
        for box in self.boxes:
            if self.pushing and box[0] == push_x and box[1] == push_y:
                bx = self.slide_pos(self.ox, box[0] - dx, box[0])
                by = self.slide_pos(self.oy, box[1] - dy, box[1])
            else:
                bx = self.ox + box[0] * TILE
                by = self.oy + box[1] * TILE
            u = U_BOX
            if self.on_goal(box):       # ゴールに乗っているあいだは別の絵
                u = U_BOX_ON_GOAL
            pyxel.blt(bx, by, 0, u, V_TILE, TILE, TILE, pyxel.COLOR_BLACK)

        # 主人公
        px = self.slide_pos(self.ox, self.from_x, self.player_x)
        py = self.slide_pos(self.oy, self.from_y, self.player_y)
        v = V_PLAYER_A
        if self.walk_timer >= MOVE_FRAMES // 2:     # 歩きの後半は、足を入れ替える
            v = V_PLAYER_B
        pyxel.blt(px, py, 0, self.player_dir * TILE, v, TILE, TILE, pyxel.COLOR_GRAY)

        # 画面の上の表示
        if self.all_cleared:
            draw_center("ALL CLEAR!  ENTER=TITLE", 3, pyxel.COLOR_YELLOW)
        else:
            pyxel.text(2, 3, f"STAGE {self.stage_no + 1}/{len(STAGES)}",
                       pyxel.COLOR_GRAY)
            if self.cleared:
                draw_center("CLEAR!  ENTER", 3, pyxel.COLOR_YELLOW)
App()
