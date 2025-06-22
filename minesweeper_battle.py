import pygame
import sys
import random
import time

# 初期設定
pygame.init()

# ウィンドウ全体のサイズ
screen_width, screen_height = 1200, 700

# マインスイーパーの描画エリア (左上の座標とサイズ)
game_area = pygame.Rect(50, 100, 400, 400)  # (x, y, width, height)

# ウィンドウを作成
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("マインスイーパー&バトル")

my_HP = 120
my_EP = 0
ene_HP = 100
# time_limit
time_limit = 30

clock = pygame.time.Clock()

# グリッドサイズ
rows, cols = 15, 15  # グリッドの行数と列数
cell_size = game_area.width // cols  # 1セルの幅（正方形）


shield_img = pygame.image.load("image/shield.png")
super_shield_img = pygame.image.load("image/S_shield.png")
sword_img = pygame.image.load("image/sword.png")
TNT_img = pygame.image.load("image/TNT.png")
heal_img = pygame.image.load("image/heal.png")
bomb_rel_dev_img = pygame.image.load("image/bomb_break.png")
ene_img = pygame.image.load("image/ene.png")
back_img = pygame.image.load("image/back.png").convert()
tut_man_img = pygame.image.load("image/tutorial_man.png")

energy_steal_sound = pygame.mixer.Sound("sound/ene_S_attak.mp3")
item_use_sound = pygame.mixer.Sound("sound/item.mp3")
start_sound = pygame.mixer.Sound("sound/start.mp3")
end_sound = pygame.mixer.Sound("sound/end.mp3")
choice_sound = pygame.mixer.Sound("sound/serect.mp3")
decide_sound = pygame.mixer.Sound("sound/decide.mp3")
attck_sound = pygame.mixer.Sound("sound/attak.mp3")
ene_attck_sound = pygame.mixer.Sound("sound/ene_attak.mp3")
my_exp_sound = pygame.mixer.Sound("sound/bomb.mp3")
clear_sound = pygame.mixer.Sound("sound/game_clear.mp3")
lose_sound = pygame.mixer.Sound("sound/game_over.mp3")
bgm = pygame.mixer_music.load("sound/OP_BGM.mp3")


my_items = []

def item_get():
  item_count = len(my_items)
  if item_count <= 7:
    itemadd = random.randint(1, 6)
    if itemadd == 1:
      my_items.append("シールド")
    elif itemadd == 2:
      my_items.append("スーパーシールド")
    elif itemadd == 3:
      my_items.append("ソード")
    elif itemadd == 4:
      my_items.append("TNT")
    elif itemadd == 5:
      my_items.append("救急箱")
    else:
      my_items.append("爆弾解除装置")

# 周囲の爆弾数をカウントする関数
def count_adjacent_bombs(r, c):
  count = 0
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      nr, nc = r + dr, c + dc
      if 0 <= nr < rows and 0 <= nc < cols and bombs[nr][nc]:
        count += 1
  return count


# 0のセルを再帰的に開く関数
def open_empty_cells(r, c):
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      nr, nc = r + dr, c + dc
      if 0 <= nr < rows and 0 <= nc < cols and not opened[nr][nc]:
        opened[nr][nc] = True
        if count_adjacent_bombs(nr, nc) == 0 and not bombs[nr][nc]:
          open_empty_cells(nr, nc)

# 背景色
background_color = (0, 0, 0)
cell_color = (150, 150, 150)
opened_color = (255, 255, 255)
bomb_color = (255, 0, 0)
text_color = (255, 255, 255)
corect_color = (0, 0, 255)
bombcount_color = (0, 0, 0)
serect_color = (255, 255, 0)
# フォント設定
font_battle = pygame.font.SysFont("msgothic", 25)
font_minseeper = pygame.font.SysFont("msgothic", 20)
font_big1text = pygame.font.SysFont("font/Togalite-Bold.otf", 100)
font_bigtext = pygame.font.SysFont("msgothic", 80)
font_titletext = pygame.font.SysFont("font/Togalite-Bold.otf", 130)
font_title2text = pygame.font.SysFont("font/Togalite-Bold.otf", 80)
font_option = pygame.font.SysFont("msgothic", 20)

title_running = True
battle_statu = False

plus_bombs = 0

stutas_start = 0
stutas_middle = 0

option_bool = True

tuta_text_index = 0

tuta_text1_list =[
  font_option.render(f"君が新入りか、まずは実戦の前に訓練を受けて", True, text_color),
  font_option.render(f"よし、それじゃあ左のマス目を見てくれ、ここ", True, text_color),
  font_option.render(f"マインスイーパーはわかるか？マス目を左ク", True, text_color),
  font_option.render(f"この数字を基に爆弾の位置を特定していくのが", True, text_color),
  font_option.render(f"まずはマスを開いて爆弾の位置を特定しろ、爆", True, text_color),
  font_option.render(f"してしまうと爆発して赤色になる。", True, text_color),
  font_option.render(f"本来実戦では時間制限のなかでマインスイー", True, text_color),
  font_option.render(f"マインスイーパーが終われば次は戦闘の訓練だ。", True, text_color),
  font_option.render(f"上下キーで項目を変更し、Wキーで選択した項目", True, text_color),
  font_option.render(f"次に進むには残りエネルギーで", True, text_color),
  font_option.render(f"この画面では使用する道具を選択するんだ。", True, text_color),
  font_option.render(f"使用しないことも可能だ。", True, text_color),
  font_option.render(f"この後は戦闘が自動で行われる。今回は訓練な", True, text_color),
  font_option.render(f"はいけないということだな。", True, text_color),
  font_option.render(f"次は画面上中央を見てくれ、ここでは自分の体", True, text_color),
  font_option.render(f"ちょうどいいだろう。Oキーで表示、非表示を", True, text_color),
  font_option.render(f"訓練はこれで以上だ。", True, text_color),
]

tuta_text2_list =[
  font_option.render(f"もらおう。次のセリフを右キーで表示させてく", True, text_color),
  font_option.render(f"がマインスイーパーを行う場所で、このマス目", True, text_color),
  font_option.render(f"リックで開き、開いたマスの数字を確認するん", True, text_color),
  font_option.render(f"マインスイーパーだ。", True, text_color),
  font_option.render(f"弾の位置が特定できたら、そのマスを右クリッ", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"パーをしてもらう。しかし今回は訓練だ、十分", True, text_color),
  font_option.render(f"まずは画面右下のウィンドウを見てくれ、ここ", True, text_color),
  font_option.render(f"のエネルギーを増やす、またSキーでエネルギ-", True, text_color),
  font_option.render(f"Enterを押すんだ。", True, text_color),
  font_option.render(f"上下キーで道具を選択、Uキーで道具を使用で", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"ので実際には行われないが、自分の攻撃、相手", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"力や解除、爆発した爆弾の数などが見れる。最", True, text_color),
  font_option.render(f"切り替えれる。集中したければ消した方がいい", True, text_color),
  font_option.render(f"これでお前も立派なレンジャーだな。ん？、も", True, text_color),
]

tuta_text3_list =[
  font_option.render(f"れ、前のセリフは左キーで確認できるぞ。", True, text_color),
  font_option.render(f"をクリックして爆弾を探すんだ。", True, text_color),
  font_option.render(f"だ。マス目に書かれている数字はそのマス目の", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"クするんだ。爆弾のマスを右クリックすること", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"練習したと思ったらNキーでマインスイーパー", True, text_color),
  font_option.render(f"では攻撃と防御にエネルギーを割り振る。エネ", True, text_color),
  font_option.render(f"を減らすことができるぞ。", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"きる。UseのUってやつだ、使用した後は道具", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"の攻撃、自爆の順番だ。自爆ダメージは爆発し", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"後に画面左下を見てくれ、ここには簡易的に操", True, text_color),
  font_option.render(f"だろう。", True, text_color),
  font_option.render(f"う実戦に行くのか、それならTABキーを押せ。", True, text_color),
]

tuta_text4_list =[
  font_option.render(f"", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"周囲8マスに爆弾が何個あるかを示している。", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"で爆弾は解除され青色になる。逆に左クリック", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"を終了しろ。", True, text_color),
  font_option.render(f"ルギーは爆弾を1つ解除するごとに1増えるぞ。", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"の効果が表示されるぞ。SPACEキーで道具を", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"た爆弾の数×5だ。なるべく爆弾を爆発させて", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"作方法が示してある。操作を思い出すのに", True, text_color),
  font_option.render(f"", True, text_color),
  font_option.render(f"君の健闘を祈る。", True, text_color),
]

tuta_text1 = tuta_text1_list[tuta_text_index]
tuta_text2 = tuta_text2_list[tuta_text_index]
tuta_text3 = tuta_text3_list[tuta_text_index]
tuta_text4 = tuta_text4_list[tuta_text_index]

mine_start_text = font_bigtext.render(f'爆弾を解除しろ!!!', True, text_color)
tuta_start_text = font_bigtext.render(f"まずは訓練を完了せよ!!!", True, text_color)

bomb_clear_text = font_option.render(f"・爆弾解除:右クリック", True, text_color)
cell_open_text = font_option.render(f"・マスを開ける:左クリック", True, text_color)
decide_next_text = font_option.render(f"・決定,次に進む:Enter", True, text_color)
item_use_text = font_option.render(f"・アイテムの使用:U", True, text_color)
item_no_use_text = font_option.render(f"・アイテムの不使用:SPACE", True, text_color)
energy_select_text = font_option.render(f"・エネルギーの割り振り:W,S", True, text_color)
mode_select_text = font_option.render(f"・項目の選択:↑,↓", True, text_color)
menu_see_text = font_option.render(f"・メニューの表示,不表示:O", True, text_color)

def show_countdown1(screen, font, background_color, clock):
  global stutas_start
  countdown_texts = ["3", "2", "1", "Go!"]
  for text in countdown_texts:
    screen.fill(background_color)
    countdown_surface = font.render(text, True, (255, 255, 255))
    screen.blit(countdown_surface, (590, 300))
    stutas_start += 1
    if stutas_start == 4:
      start_sound.play()
      stutas_start = 0
    pygame.display.flip()
    for _ in range(60):  # 約1秒間表示（60 FPSの場合）
      clock.tick(60)  # フレームレートを維持

def show_countdown(screen, font, background_color, clock):
  countdown_texts = ["3", "2", "1", "Go!"]
  global stutas_middle
  for text in countdown_texts:
    screen.fill(background_color)
    countdown_surface = font.render(text, True, (255, 255, 255))
    screen.blit(countdown_surface, (590, 300))
    stutas_middle += 1
    if stutas_middle == 4:
      start_sound.play()
      stutas_middle = 0
    pygame.display.flip()
    for _ in range(60):  # 約1秒間表示（60 FPSの場合）
      clock.tick(60)  # フレームレートを維持

name_input = True
name = "スペースランナー"
first_OP_setting = True

big_main_running = True

tutorial = True

while big_main_running:
    

    while title_running:
      if name_input:
        if first_OP_setting:
          pygame.mixer.music.play(-1)
          pygame.mixer.music.set_volume(0.2)
          first_OP_setting = False
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False
            pygame.quit()
            sys.exit()
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
              name_input = False


        title1_text = font_titletext.render("mineswee", True, text_color)
        title2_text = font_titletext.render("&", True, text_color)
        title3_text = font_titletext.render("battle", True, text_color)
        title4_text = font_title2text.render("<< press Enter >>", True, text_color)
        title5_text = font_titletext.render("per", True, background_color)
        screen.blit(back_img, (0,0))
        screen.blit(title1_text, (100, 130))
        screen.blit(title2_text, (700, 230))
        screen.blit(title3_text, (800, 130))
        screen.blit(title4_text, (350, 500))
        screen.blit(title5_text, (520,130))
        pygame.display.flip()
      else:
        if tutorial == False:
          pygame.mixer.music.stop()
          screen.fill(background_color)
          screen.blit(mine_start_text, (280, 300))
          pygame.display.flip()
          for _ in range(120):  # 1秒間表示（60 FPS）
            clock.tick(60)
          show_countdown1(screen, font_big1text, background_color, clock)
        else:
          pygame.mixer.music.stop()
          screen.fill(background_color)
          screen.blit(tuta_start_text, (120, 300))
          pygame.display.flip()
          for _ in range(120):  # 1秒間表示（60 FPS）
            clock.tick(60)
        
        
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False
            pygame.quit()
            sys.exit()
        
        bgm = pygame.mixer_music.load("sound/BGM.mp3")
        title_running = False


    mine_end = False

    mine_end_tut = False

    first_setting = True

    first_setting_tut = True

    tutorial_end = False

    battlerunning = False

    battlerunning_tut = False

    def RPG_draw():
      screen.blit(ene_img, (750, 200))
      pygame.draw.rect(screen, background_color, (500, 400, 650, 200), 0)
      pygame.draw.rect(screen, background_color, (500, 50, 250, 200), 0)
      pygame.draw.rect(screen, text_color, (500, 400, 650, 200), 2)
      pygame.draw.rect(screen, text_color, (500, 50, 250, 200), 2)
      my_HP_text = font_battle.render(f"HP {my_HP}", True, text_color)
      my_EP_text = font_battle.render(f"エネルギー {my_EP}", True, text_color)
      my_exp_text = font_battle.render(f"爆発した爆弾 {my_exp}個", True, text_color)
      rel_text = font_battle.render(f"解除した爆弾 {rel_bomb_num}個", True, text_color)
      screen.blit(my_HP_text, (520, 60))
      screen.blit(my_EP_text, (520, 100))
      screen.blit(my_exp_text, (520, 140))
      screen.blit(rel_text, (520, 180))

    def RPG_draw_tuta():
      screen.blit(tut_man_img, (750, 80))
      pygame.draw.rect(screen, background_color, (500, 400, 650, 200), 0)
      pygame.draw.rect(screen, background_color, (500, 50, 250, 200), 0)
      pygame.draw.rect(screen, text_color, (500, 400, 650, 200), 2)
      pygame.draw.rect(screen, text_color, (500, 50, 250, 200), 2)
      my_HP_text = font_battle.render(f"HP {my_HP}", True, text_color)
      my_EP_text = font_battle.render(f"エネルギー {my_EP}", True, text_color)
      my_exp_text = font_battle.render(f"爆発した爆弾 {my_exp}個", True, text_color)
      rel_text = font_battle.render(f"解除した爆弾 {rel_bomb_num}個", True, text_color)
      screen.blit(my_HP_text, (520, 60))
      screen.blit(my_EP_text, (520, 100))
      screen.blit(my_exp_text, (520, 140))
      screen.blit(rel_text, (520, 180))

    num_bombs = 16
    all_bombs = 16

    mainrunning = True
    
    while tutorial:
      screen.blit(back_img, (0,0))
      
      # ゲームループ
      if first_setting_tut == True:
        my_atkP = 0
        my_blkP = 0
        # セルの開閉状態と爆弾配置
        opened = [[False for _ in range(cols)] for _ in range(rows)]
        bombs = [[False for _ in range(cols)] for _ in range(rows)]
        corect = [[False for _ in range(cols)]for _ in range(rows)]
        not_right_click = [[False for _ in range(cols)]for _ in range(rows)]

        add_energy = 0
        rel_bomb_num = 0
        my_exp = 0
        start = time.time()
        prog_time = 0
        item_getflg = True
        first_setting_tut = False
        mine_running_tut = True
        mine_end = False
        mine_end_tut = False

        while num_bombs > 0:

          row = random.randint(0, rows - 1)
          col = random.randint(0, cols - 1)
          if not bombs[row][col]:
            bombs[row][col] = True
            num_bombs -= 1

        right_click_limit_prus = 0
        right_click_limit = int(all_bombs + 3 + right_click_limit_prus)
        all_bombs_char = all_bombs

      while mine_running_tut:  #ここからマインスイーパー
        screen.blit(back_img, (0,0))
        if option_bool:
          pygame.draw.rect(screen, background_color, (7,496,480,175),0)
          pygame.draw.rect(screen, text_color, (7,496,480,175),1)
          screen.blit(item_use_text,(10,500))
          screen.blit(decide_next_text,(10,530))
          screen.blit(bomb_clear_text,(10,560))
          screen.blit(cell_open_text,(10,590))
          screen.blit(item_no_use_text,(10,620))
          screen.blit(energy_select_text,(10,650))
          screen.blit(menu_see_text,(210,500))
          screen.blit(mode_select_text,(245,530)) 

        pygame.draw.rect(screen, background_color, (760,50,440,175),0)
        pygame.draw.rect(screen, text_color, (760,50,440,175),1)
        screen.blit(tuta_text1,(770,70))
        screen.blit(tuta_text2,(770,110))
        screen.blit(tuta_text3,(770,150))
        screen.blit(tuta_text4,(770,190))

        tuta_text1 = tuta_text1_list[tuta_text_index]
        tuta_text2 = tuta_text2_list[tuta_text_index]
        tuta_text3 = tuta_text3_list[tuta_text_index]
        tuta_text4 = tuta_text4_list[tuta_text_index]

        pygame.draw.rect(screen,background_color,(40,60,410,35),0)
        pygame.draw.rect(screen,text_color,(40,60,410,35),2)


        color = (0, 255, 0)

        right_click_limit_text = font_minseeper.render(
            f'爆弾解除装置残り {right_click_limit }個', True, text_color)
        bomb_num_text = font_minseeper.render(f'爆弾の数 {all_bombs_char }個', True, text_color)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False

          elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
              

              # クリックされた座標を取得
              mouse_x, mouse_y = event.pos

        # クリックがゲームエリア内なら処理を実行
              if game_area.collidepoint(mouse_x, mouse_y):
                # ゲームエリア内のセル座標を計算
                col = (mouse_x - game_area.x) // cell_size
                row = (mouse_y - game_area.y) // cell_size

          # 範囲内のセルを開く
                if 0 <= row < rows and 0 <= col < cols:
                  if opened[row][col]:
                    continue
                  opened[row][col] = True
                  if count_adjacent_bombs(row, col) == 0 and not bombs[row][col]:
                    open_empty_cells(row, col)
                  if bombs[row][col]:
                    my_exp += 1
                    bomb_bool = True


            elif event.button == 3 and right_click_limit >= 1:
              right_click_limit = int(right_click_limit - 1)
              print(right_click_limit)
              mouse_x, mouse_y = event.pos

      # クリックがゲームエリア内なら処理を実行
              if game_area.collidepoint(mouse_x, mouse_y):
                # ゲームエリア内のセル座標を計算
                col = (mouse_x - game_area.x) // cell_size
                row = (mouse_y - game_area.y) // cell_size

      # 範囲内のセルを開く
                if 0 <= row < rows and 0 <= col < cols and bombs[row][col]:
                  if opened[row][col]:
                    right_click_limit = int(right_click_limit + 1)
                    continue
                  if opened[row][col] == False:
                    add_energy += 1
                    rel_bomb_num += 1
                  opened[row][col] = True
                  corect[row][col] = True
                  corect[row][col] = corect[row][col]

          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
              option_bool = not option_bool
            elif event.key == pygame.K_n:
              print("nok")
              mine_end_tut = True
              pygame.display.flip()
              pygame.time.wait(100) 
              battlerunning_tut = True
              mine_running_tut = False
            elif event.key == pygame.K_RIGHT:
              if tuta_text_index != 16:
                tuta_text_index += 1
                choice_sound.play()
            elif event.key == pygame.K_TAB:
              tutorial_end = True

            elif event.key == pygame.K_LEFT:
              if tuta_text_index != 0:
                tuta_text_index -= 1
                choice_sound.play()

      # マインスイーパーのグリッドを描画
        for row in range(rows):
          for col in range(cols):
            cell_x = game_area.x + col * cell_size
            cell_y = game_area.y + row * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

            if opened[row][col]:
              # 青色 (正解フラグ)
              if bombs[row][col] and corect[row][col] and not_right_click[row][col] == False:
                pygame.draw.rect(screen, corect_color, cell_rect)
              elif bombs[row][col]:  # 赤色 (爆弾)
                pygame.draw.rect(screen, bomb_color, cell_rect)
                not_right_click[row][col] = True
              else:  # 開いたセル
                pygame.draw.rect(screen, opened_color, cell_rect)
                bomb_count = count_adjacent_bombs(row, col)
                if bomb_count > 0:
                  text = font_minseeper.render(
                      str(bomb_count), True, bombcount_color)
                  screen.blit(text, (cell_x + cell_size //
                                    4, cell_y + cell_size // 8))
            else:
              pygame.draw.rect(screen, cell_color, cell_rect)

            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # セルの枠線


        screen.blit(right_click_limit_text, (50, 70))
        screen.blit(bomb_num_text, (300, 70))
        RPG_draw_tuta()
        wait_text = font_battle.render(f"爆弾を解除してエネルギーを貯めろ!!", True, text_color)
        screen.blit(wait_text, (520, 410))

        pygame.display.flip()

      selected_index = 0
      selected_index1 = 0
      item_choice = False
      item_list = True
      not_use_item = False
      my_exp_blk = 0
      attckmode = False
      ene_attck = False
      my_exp_calc = False
      ene_end = False
      my_end = False
      my_exp_plus = 0
      

      my_EP = int(my_EP + add_energy)
      while battlerunning_tut:
        screen.blit(back_img, (0,0))
        if option_bool:
          pygame.draw.rect(screen, background_color, (7,496,480,175),0)
          pygame.draw.rect(screen, text_color, (7,496,480,175),1)
          screen.blit(item_use_text,(10,500))
          screen.blit(decide_next_text,(10,530))
          screen.blit(bomb_clear_text,(10,560))
          screen.blit(cell_open_text,(10,590))
          screen.blit(item_no_use_text,(10,620))
          screen.blit(energy_select_text,(10,650))
          screen.blit(menu_see_text,(210,500))
          screen.blit(mode_select_text,(245,530)) 

        pygame.draw.rect(screen, background_color, (760,50,440,175),0)
        pygame.draw.rect(screen, text_color, (760,50,440,175),1)
        screen.blit(tuta_text1,(770,70))
        screen.blit(tuta_text2,(770,110))
        screen.blit(tuta_text3,(770,150))          
        screen.blit(tuta_text4,(770,190))

        tuta_text1 = tuta_text1_list[tuta_text_index]
        tuta_text2 = tuta_text2_list[tuta_text_index]
        tuta_text3 = tuta_text3_list[tuta_text_index]
        tuta_text4 = tuta_text4_list[tuta_text_index]

        pygame.draw.rect(screen,background_color,(40,60,410,35),0)
        pygame.draw.rect(screen,text_color,(40,60,410,35),2)

        RPG_draw_tuta()  # RPG描画処理

        if item_getflg == True:
          item_get()
          item_getflg = False

        serect = [f"攻撃に使うエネルギーを決めてください {my_atkP}",
                  f"防御に使うエネルギーを決めてください {my_blkP}",
                  f"残りエネルギー {my_EP}"]

      # マインスイーパーのグリッドを描画
        for row in range(rows):
          for col in range(cols):
            cell_x = game_area.x + col * cell_size
            cell_y = game_area.y + row * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

            if opened[row][col]:
              if bombs[row][col] and corect[row][col] and not_right_click[row][col] == False:
                pygame.draw.rect(screen, corect_color, cell_rect)
              elif bombs[row][col]:
                pygame.draw.rect(screen, bomb_color, cell_rect)
                not_right_click[row][col] = True
              else:
                pygame.draw.rect(screen, opened_color, cell_rect)
                bomb_count = count_adjacent_bombs(row, col)
                if bomb_count > 0:
                  text = font_minseeper.render(
                      str(bomb_count), True, bombcount_color)
                  screen.blit(text, (cell_x + cell_size //
                                    4, cell_y + cell_size // 8))
            else:
              pygame.draw.rect(screen, cell_color, cell_rect)

            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # セルの枠線

        screen.blit(right_click_limit_text, (50, 70))
        screen.blit(bomb_num_text, (300, 70))

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
              option_bool = not option_bool
              print(option_bool)
            elif event.key == pygame.K_RIGHT:
              if tuta_text_index != 16:
                tuta_text_index += 1
                choice_sound.play()

            elif event.key == pygame.K_LEFT:
              if tuta_text_index != 0:
                tuta_text_index -= 1
                choice_sound.play()


            if event.key == pygame.K_UP:
              selected_index = (selected_index - 1) % len(serect)
              choice_sound.play()
            if event.key == pygame.K_DOWN:
              selected_index = (selected_index + 1) % len(serect)
              choice_sound.play()

            if event.key == pygame.K_UP:
              selected_index1 = (selected_index1 - 1) % len(my_items)
              choice_sound.play()
            if event.key == pygame.K_DOWN:
              selected_index1 = (selected_index1 + 1) % len(my_items)
              choice_sound.play()
            if event.key == pygame.K_TAB:
                tutorial_end = True
                print("0")

            if selected_index == 0:
              if event.key == pygame.K_w and my_EP >= 1:
                choice_sound.play()
                my_atkP += 1
                my_EP -= 1
              elif event.key == pygame.K_s:
                choice_sound.play()
                if my_atkP >= 1:
                  my_atkP -= 1
                  my_EP += 1
            elif selected_index == 1:
              if event.key == pygame.K_w and my_EP >= 1:
                choice_sound.play()
                my_blkP += 1
                my_EP -= 1
              elif event.key == pygame.K_s:
                choice_sound.play()
                if my_blkP >= 1:
                  my_blkP -= 1
                  my_EP += 1
            elif selected_index == 2:
              if event.key == pygame.K_RETURN:
                item_choice = True
                selected_index = 0
                selected_index1 = 0
                decide_sound.play()

            if item_choice == True:
              if event.key == pygame.K_u:
                item_list = False
                selected_item = my_items[selected_index1]
                decide_sound.play()
                if selected_item == "シールド":
                  my_exp_blk += 1
                  my_items.remove("シールド")
                  item1_text = font_battle.render(
                      f'シールドを使った！', True, text_color)
                  item2_text = font_battle.render(
                      f'自爆のダメージが-5される!', True, text_color)
                  item_img = shield_img
                elif selected_item == "スーパーシールド":
                  my_exp_blk += 3
                  my_items.remove("スーパーシールド")
                  item1_text = font_battle.render(
                      f'スーパーシールドを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'自爆のダメージが-15される!', True, text_color)
                  item_img = super_shield_img
                elif selected_item == "ソード":
                  my_items.remove("ソード")
                  item1_text = font_battle.render(
                      f'ソードを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'50%の確率の確率で与えるダメージが+10される!', True, text_color)
                  item_img = sword_img
                  if random.random() < 0.5:
                    my_atkP += 10
                elif selected_item == "TNT":
                  my_items.remove("TNT")
                  my_atkP += 25
                  my_exp_plus += 30
                  item1_text = font_battle.render(
                      f'TNTを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'与えるダメージを+25、自爆のダメージを+30する!', True, text_color)
                  item_img = TNT_img
                elif selected_item == "救急箱":
                  my_items.remove("救急箱")
                  my_HP += 20
                  item1_text = font_battle.render(
                      f'救急箱を使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'自分のHPを20回復する!', True, text_color)
                  item_img = heal_img
                elif selected_item == "爆弾解除装置":
                  my_items.remove("爆弾解除装置")
                  right_click_limit_prus = 3
                  item1_text = font_battle.render(
                      f'爆弾解除装置を使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'次の爆弾解除装置の数が+3される!', True, text_color)
                  item_img = bomb_rel_dev_img

              elif event.key == pygame.K_SPACE:
                attckmode = True
                item_choice = False
                choice_sound.play()

              elif event.key == pygame.K_RIGHT:
                if tuta_text_index != 16:
                  tuta_text_index += 1
                  choice_sound.play()

              elif event.key == pygame.K_LEFT:
                if tuta_text_index != 0:
                  tuta_text_index -= 1
                  choice_sound.play()

              elif event.key == pygame.K_TAB:
                tutorial_end = True
                print("ok1")

        if item_choice == True and item_list == True:
          for i, text1 in enumerate(my_items):
            color = serect_color if i == selected_index1 else text_color
            text_surface1 = font_battle.render(text1, True, color)
            if i <= 3:
              text_rect1 = text_surface1.get_rect(center=(620, 430 + i * 35))
            else:
              text_rect1 = text_surface1.get_rect(
                  center=(950, 430 + int(i - 4) * 35))
            screen.blit(text_surface1, text_rect1)

        if item_choice == False and attckmode == False:
          for i, text in enumerate(serect):
            color = serect_color if i == selected_index else text_color
            text_surface = font_battle.render(text, True, color)
            text_rect = text_surface.get_rect(center=(750, 430 + i * 50))
            screen.blit(text_surface, text_rect)


        elif item_choice == True and item_list == False:
          screen.blit(item1_text, (520, 430))
          screen.blit(item2_text, (520, 460))
          screen.blit(item_img, (1000, 500))
          item_use_sound.play()
          pygame.display.flip()
          time.sleep(4)
          attckmode = True
          item_choice = False
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
              if tuta_text_index != 16:
                tuta_text_index += 1
                choice_sound.play()

              elif event.key == pygame.K_LEFT:
                if tuta_text_index != 0:
                  tuta_text_index -= 1
                  choice_sound.play()

              elif event.key == pygame.K_TAB:
                tutorial_end = True
                print("ok2")


        pygame.display.flip()
    
        if tutorial_end == True:
          tutorial = False
          mine_running_tut = False
          battlerunning_tut = False
          my_HP = 120
          my_EP = 0
          ene_HP = 1
          time_limit = 30
          my_items = []
          num_bombs = 16
          all_bombs = 16
          battle_statu = False
          plus_bombs = 0
          item_choice = False
          attckmode = False
          attckmode = True
          screen.fill(background_color)
          screen.blit(mine_start_text, (280, 300))
          pygame.display.flip()
          for _ in range(120):  # 1秒間表示（60 FPS）
            clock.tick(60)
        
          screen.fill(background_color)
          show_countdown1(screen, font_big1text, background_color, clock) #tutorialに渡す

#-------------------------------------------------------------------------------ここまでtutorial
      
    while mainrunning:
      print("ok")
      screen.blit(back_img, (0,0))
      pygame.mixer.music.play(-1)
      pygame.mixer.music.set_volume(0.2)
      # ゲームループ
      if first_setting == True:
        my_atkP = 0
        my_blkP = 0
        # セルの開閉状態と爆弾配置
        opened = [[False for _ in range(cols)] for _ in range(rows)]
        bombs = [[False for _ in range(cols)] for _ in range(rows)]
        corect = [[False for _ in range(cols)]for _ in range(rows)]
        not_right_click = [[False for _ in range(cols)]for _ in range(rows)]

        add_energy = 0
        rel_bomb_num = 0
        my_exp = 0
        start = time.time()
        prog_time = 0
        item_getflg = True
        first_setting = False
        mine_running = True
        mine_end = False

        while num_bombs > 0:

          row = random.randint(0, rows - 1)
          col = random.randint(0, cols - 1)
          if not bombs[row][col]:
            bombs[row][col] = True
            num_bombs -= 1

        right_click_limit_prus = 0
        right_click_limit = int(all_bombs + 3 + right_click_limit_prus)
        all_bombs_char = all_bombs
        if num_bombs < 36:
          num_bombs = 2 + all_bombs
          all_bombs = 2 + all_bombs
        else:
          num_bombs =  num_bombs
          all_bombs =  all_bombs

      while mine_running:
        screen.blit(back_img, (0,0))
        if option_bool:
          pygame.draw.rect(screen, background_color, (7,496,480,175),0)
          pygame.draw.rect(screen, text_color, (7,496,480,175),1)
          screen.blit(item_use_text,(10,500))
          screen.blit(decide_next_text,(10,530))
          screen.blit(bomb_clear_text,(10,560))
          screen.blit(cell_open_text,(10,590))
          screen.blit(item_no_use_text,(10,620))
          screen.blit(energy_select_text,(10,650))
          screen.blit(menu_see_text,(210,500))
          screen.blit(mode_select_text,(245,530)) 

        pygame.draw.rect(screen,background_color,(40,60,410,35),0)
        pygame.draw.rect(screen,text_color,(40,60,410,35),2)

        ene_atkP = random.randint(4, 15)
        ene_blkP = random.randint(4, 8)

        color = (0, 255, 0)

        right_click_limit_text = font_minseeper.render(
            f'爆弾解除装置残り {right_click_limit }個', True, text_color)
        bomb_num_text = font_minseeper.render(f'爆弾の数 {all_bombs_char }個', True, text_color)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False

          elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
              

              # クリックされた座標を取得
              mouse_x, mouse_y = event.pos

        # クリックがゲームエリア内なら処理を実行
              if game_area.collidepoint(mouse_x, mouse_y):
                # ゲームエリア内のセル座標を計算
                col = (mouse_x - game_area.x) // cell_size
                row = (mouse_y - game_area.y) // cell_size

          # 範囲内のセルを開く
                if 0 <= row < rows and 0 <= col < cols:
                  if opened[row][col]:
                    continue
                  opened[row][col] = True
                  if count_adjacent_bombs(row, col) == 0 and not bombs[row][col]:
                    open_empty_cells(row, col)
                  if bombs[row][col]:
                    my_exp += 1
                    bomb_bool = True


            elif event.button == 3 and right_click_limit >= 1:
              right_click_limit = int(right_click_limit - 1)
              print(right_click_limit)
              mouse_x, mouse_y = event.pos

      # クリックがゲームエリア内なら処理を実行
              if game_area.collidepoint(mouse_x, mouse_y):
                # ゲームエリア内のセル座標を計算
                col = (mouse_x - game_area.x) // cell_size
                row = (mouse_y - game_area.y) // cell_size

      # 範囲内のセルを開く
                if 0 <= row < rows and 0 <= col < cols and bombs[row][col]:
                  if opened[row][col]:
                    right_click_limit = int(right_click_limit + 1)
                    continue
                  if opened[row][col] == False:
                    add_energy += 1
                    rel_bomb_num += 1
                  opened[row][col] = True
                  corect[row][col] = True
                  corect[row][col] = corect[row][col]

          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
              option_bool = not option_bool

      # 背景の描画

      # マインスイーパーのグリッドを描画
      # マインスイーパーのグリッドを描画
        for row in range(rows):
          for col in range(cols):
            cell_x = game_area.x + col * cell_size
            cell_y = game_area.y + row * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

            if opened[row][col]:
              # 青色 (正解フラグ)
              if bombs[row][col] and corect[row][col] and not_right_click[row][col] == False:
                pygame.draw.rect(screen, corect_color, cell_rect)
              elif bombs[row][col]:  # 赤色 (爆弾)
                pygame.draw.rect(screen, bomb_color, cell_rect)
                not_right_click[row][col] = True
              else:  # 開いたセル
                pygame.draw.rect(screen, opened_color, cell_rect)
                bomb_count = count_adjacent_bombs(row, col)
                if bomb_count > 0:
                  text = font_minseeper.render(
                      str(bomb_count), True, bombcount_color)
                  screen.blit(text, (cell_x + cell_size //
                                    4, cell_y + cell_size // 8))
            else:
              pygame.draw.rect(screen, cell_color, cell_rect)

            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # セルの枠線

        prog_time = time.time() - start
        if prog_time > time_limit:
          prog_time = time_limit
          time_count = False
          mine_end = True

        bar_width = int((prog_time / time_limit) * 1200)
        red = max(0, min(255, int((prog_time / time_limit) * 255)))
        green = max(0, min(255, 255 - int((prog_time / time_limit) * 255)))
        color = (red, green, 0)
        pygame.draw.rect(screen, color, (0, 0, bar_width, 20))
        screen.blit(right_click_limit_text, (50, 70))
        screen.blit(bomb_num_text, (300, 70))
        RPG_draw()
        wait_text = font_battle.render(f"爆弾を解除してエネルギーを貯めろ!!", True, text_color)
        screen.blit(wait_text, (520, 410))

        if mine_end == True:
          end_sound.play()
          pygame.display.flip()
          for _ in range(210):  
            clock.tick(60)
          battlerunning = True
          mine_running = False
        pygame.display.flip()

      selected_index = 0
      selected_index1 = 0
      item_choice = False
      item_list = True
      not_use_item = False
      my_exp_blk = 0
      attckmode = False
      ene_attck = False
      my_exp_calc = False
      ene_end = False
      my_end = False
      my_exp_plus = 0

      my_EP = int(my_EP + add_energy)
      while battlerunning:
        screen.blit(back_img, (0,0))
        if option_bool:
          pygame.draw.rect(screen, background_color, (7,496,480,175),0)
          pygame.draw.rect(screen, text_color, (7,496,480,175),1)
          screen.blit(item_use_text,(10,500))
          screen.blit(decide_next_text,(10,530))
          screen.blit(bomb_clear_text,(10,560))
          screen.blit(cell_open_text,(10,590))
          screen.blit(item_no_use_text,(10,620))
          screen.blit(energy_select_text,(10,650))
          screen.blit(menu_see_text,(210,500))
          screen.blit(mode_select_text,(245,530)) 

        pygame.draw.rect(screen,background_color,(40,60,410,35),0)
        pygame.draw.rect(screen,text_color,(40,60,410,35),2)

        RPG_draw()  # RPG描画処理

        if item_getflg == True:
          item_get()
          item_getflg = False

        serect = [f"攻撃に使うエネルギーを決めてください {my_atkP}",
                  f"防御に使うエネルギーを決めてください {my_blkP}",
                  f"残りエネルギー {my_EP}"]

      # マインスイーパーのグリッドを描画
        for row in range(rows):
          for col in range(cols):
            cell_x = game_area.x + col * cell_size
            cell_y = game_area.y + row * cell_size
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

            if opened[row][col]:
              if bombs[row][col] and corect[row][col] and not_right_click[row][col] == False:
                pygame.draw.rect(screen, corect_color, cell_rect)
              elif bombs[row][col]:
                pygame.draw.rect(screen, bomb_color, cell_rect)
                not_right_click[row][col] = True
              else:
                pygame.draw.rect(screen, opened_color, cell_rect)
                bomb_count = count_adjacent_bombs(row, col)
                if bomb_count > 0:
                  text = font_minseeper.render(
                      str(bomb_count), True, bombcount_color)
                  screen.blit(text, (cell_x + cell_size //
                                    4, cell_y + cell_size // 8))
            else:
              pygame.draw.rect(screen, cell_color, cell_rect)

            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # セルの枠線

        screen.blit(right_click_limit_text, (50, 70))
        screen.blit(bomb_num_text, (300, 70))

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            mine_running_tut = False
            battlerunning_tut = False
            tutorial = False
            mine_running = False
            battlerunning = False
            mainrunning = False
            big_main_running = False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
              option_bool = not option_bool
              print(option_bool)
            if event.key == pygame.K_UP:
              selected_index = (selected_index - 1) % len(serect)
              choice_sound.play()
            if event.key == pygame.K_DOWN:
              selected_index = (selected_index + 1) % len(serect)
              choice_sound.play()

            if event.key == pygame.K_UP:
              selected_index1 = (selected_index1 - 1) % len(my_items)
              choice_sound.play()
            if event.key == pygame.K_DOWN:
              selected_index1 = (selected_index1 + 1) % len(my_items)
              choice_sound.play()

            if selected_index == 0:
              if event.key == pygame.K_w and my_EP >= 1:
                choice_sound.play()
                my_atkP += 1
                my_EP -= 1
              elif event.key == pygame.K_s:
                choice_sound.play()
                if my_atkP >= 1:
                  my_atkP -= 1
                  my_EP += 1
            elif selected_index == 1:
              if event.key == pygame.K_w and my_EP >= 1:
                choice_sound.play()
                my_blkP += 1
                my_EP -= 1
              elif event.key == pygame.K_s:
                choice_sound.play()
                if my_blkP >= 1:
                  my_blkP -= 1
                  my_EP += 1
            elif selected_index == 2:
              if event.key == pygame.K_RETURN:
                item_choice = True
                selected_index = 0
                selected_index1 = 0
                decide_sound.play()

            if item_choice == True:
              if event.key == pygame.K_u:
                item_list = False
                selected_item = my_items[selected_index1]
                decide_sound.play()
                if selected_item == "シールド":
                  my_exp_blk += 1
                  my_items.remove("シールド")
                  item1_text = font_battle.render(
                      f'シールドを使った！', True, text_color)
                  item2_text = font_battle.render(
                      f'自爆のダメージが-5される!', True, text_color)
                  item_img = shield_img
                elif selected_item == "スーパーシールド":
                  my_exp_blk += 3
                  my_items.remove("スーパーシールド")
                  item1_text = font_battle.render(
                      f'スーパーシールドを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'自爆のダメージが-15される!', True, text_color)
                  item_img = super_shield_img
                elif selected_item == "ソード":
                  my_items.remove("ソード")
                  item1_text = font_battle.render(
                      f'ソードを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'50%の確率の確率で与えるダメージが+10される!', True, text_color)
                  item_img = sword_img
                  if random.random() < 0.5:
                    my_atkP += 10
                elif selected_item == "TNT":
                  my_items.remove("TNT")
                  my_atkP += 25
                  my_exp_plus += 30
                  item1_text = font_battle.render(
                      f'TNTを使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'与えるダメージを+25、自爆のダメージを+30する!', True, text_color)
                  item_img = TNT_img
                elif selected_item == "救急箱":
                  my_items.remove("救急箱")
                  my_HP += 20
                  item1_text = font_battle.render(
                      f'救急箱を使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'自分のHPを20回復する!', True, text_color)
                  item_img = heal_img
                elif selected_item == "爆弾解除装置":
                  my_items.remove("爆弾解除装置")
                  right_click_limit_prus = 3
                  item1_text = font_battle.render(
                      f'爆弾解除装置を使った!', True, text_color)
                  item2_text = font_battle.render(
                      f'次の爆弾解除装置の数が+3される!', True, text_color)
                  item_img = bomb_rel_dev_img

              elif event.key == pygame.K_SPACE:
                attckmode = True
                item_choice = False
                choice_sound.play()

        if item_choice == True and item_list == True:
          for i, text1 in enumerate(my_items):
            color = serect_color if i == selected_index1 else text_color
            text_surface1 = font_battle.render(text1, True, color)
            if i <= 3:
              text_rect1 = text_surface1.get_rect(center=(620, 430 + i * 35))
            else:
              text_rect1 = text_surface1.get_rect(
                  center=(950, 430 + int(i - 4) * 35))
            screen.blit(text_surface1, text_rect1)

        if item_choice == False and attckmode == False:
          for i, text in enumerate(serect):
            color = serect_color if i == selected_index else text_color
            text_surface = font_battle.render(text, True, color)
            text_rect = text_surface.get_rect(center=(750, 430 + i * 50))
            screen.blit(text_surface, text_rect)

        elif ene_end == True:
          ene_end_text = font_battle.render(f"宇宙人を倒した!", True, text_color)
          screen.blit(ene_end_text, (520, 430))
          pygame.mixer.music.stop()
          clear_sound.play()
          pygame.display.flip()
          time.sleep(7)
          battlerunning = False
          mine_running = False
          mainrunning = False
          title_running = True
          my_HP = 120
          my_EP = 0
          ene_HP = 100
          time_limit = 30
          my_items = []
          battle_statu = False
          plus_bombs = 0
          stutas_start = 0
          stutas_middle = 0
          name_input = True
          first_OP_setting = True
          bgm = pygame.mixer_music.load("sound/OP_BGM.mp3")

          
        elif my_end == True:
          my_end_text = font_battle.render(f"{name}は宇宙人に倒されてしまった", True, text_color)
          screen.blit(my_end_text, (520, 430))
          pygame.mixer.music.stop()
          lose_sound.play()
          pygame.display.flip()
          time.sleep(5)
          battlerunning = False
          mine_running = False
          mainrunning = False
          title_running = True
          my_HP = 120
          my_EP = 0
          ene_HP = 100
          time_limit = 30
          my_items = []
          battle_statu = False
          plus_bombs = 0
          stutas_start = 0
          stutas_middle = 0
          name_input = True
          first_OP_setting = True
          bgm = pygame.mixer_music.load("sound/OP_BGM.mp3")


        elif my_exp_calc == True:
          my_exp_dammge = int(int(my_exp - my_exp_blk) * 5)
          if my_exp_dammge < 0:
            my_exp_dammge = 0
          my_HP = my_HP - my_exp_dammge - my_exp_plus
          if my_HP <= 0:
            my_HP = 0

          my_exp_text1 = font_battle.render(f"先ほど解除できなかった爆弾は{my_exp}つ!", True, text_color)
          my_exp_text2 = font_battle.render(
              f"{name}に{my_exp_dammge + my_exp_plus}ポイントのダメージ!", True, text_color)
          my_exp_text3 = font_battle.render(f"爆弾を解除しろ!!", True, text_color)
          screen.blit(my_exp_text1, (520, 430))
          screen.blit(my_exp_text2, (520, 460))
          screen.blit(my_exp_text3, (520, 490))
          my_exp_sound.play()
          pygame.display.flip()
          time.sleep(4)
          if my_HP <= 0:
            my_HP = 0
            my_end = True
          else:
            mine_running = True
            battlerunning = False
            first_setting = True
            show_countdown(screen, font_big1text, background_color, clock)

        elif ene_attck == True:
          if random.random() < 0.5:
            ene_atkP = int(ene_atkP)
            dammge = ene_atkP - my_blkP
            if dammge < 0:
              dammge = 0
            my_HP = my_HP - dammge
            if my_HP <= 0:
              my_HP = 0
            ene_attck_text1 = font_battle.render(f"宇宙人の攻撃!", True, text_color)
            ene_attck_text2 = font_battle.render(
                f"{name}に{dammge}ポイントのダメージ!", True, text_color)
            screen.blit(ene_attck_text1, (520, 430))
            screen.blit(ene_attck_text2, (520, 460))
            ene_attck_sound.play()
            pygame.display.flip()
            time.sleep(3)
            my_exp_calc = True
          else:
            my_EP = my_EP - ene_atkP
            if my_EP < 0:
              my_EP = 0
            ene_attck_text3 = font_battle.render(
                f"宇宙人のエネルギースティール!", True, text_color)
            ene_attck_text4 = font_battle.render(
                f"{name}のエネルギーが{ene_atkP}ポイント減少した!", True, text_color)
            screen.blit(ene_attck_text3, (520, 430))
            screen.blit(ene_attck_text4, (520, 460))
            energy_steal_sound.play()
            pygame.display.flip()
            time.sleep(3)
            my_exp_calc = True
          if my_HP <= 0:
            my_HP = 0
            my_end = True

        elif item_choice == False and attckmode == True:
          ene_HP = ene_HP - my_atkP
          text_attck1 = font_battle.render(f"{name}の攻撃!", True, text_color)
          text_attck2 = font_battle.render(f"宇宙人に{my_atkP}のダメージ", True, text_color)
          screen.blit(text_attck1, (520, 430))
          screen.blit(text_attck2, (520, 460))
          attck_sound.play()
          pygame.display.flip()
          time.sleep(3)
          
          if ene_HP <= 0:
            ene_end = True
          else:
            ene_attck = True

        elif item_choice == True and item_list == False:
          screen.blit(item1_text, (520, 430))
          screen.blit(item2_text, (520, 460))
          screen.blit(item_img, (1000, 500))
          item_use_sound.play()
          pygame.display.flip()
          time.sleep(4)
          attckmode = True
          item_choice = False

        pygame.display.flip()
