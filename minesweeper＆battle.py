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
pygame.display.set_caption("マインスイーパー")

my_HP = 150
my_EP = 0
ene_HP = 150
# 制限時間
制限時間 = 30

clock = pygame.time.Clock()

# グリッドサイズ
rows, cols = 15, 15  # グリッドの行数と列数
cell_size = game_area.width // cols  # 1セルの幅（正方形）


シールドimg = pygame.image.load("image/shield.png")
スーパーシールドimg = pygame.image.load("image/S_shield.png")
ソードimg = pygame.image.load("image/sword.png")
TNTimg = pygame.image.load("image/TNT.png")
救急箱img = pygame.image.load("image/heal.png")
爆弾処理装置img = pygame.image.load("image/bomb_break.png")
ene_img = pygame.image.load("image/ene.png")

エネスティsound = pygame.mixer.Sound("sound/ene_S_attak.mp3")
道具使用sound = pygame.mixer.Sound("sound/item.mp3")
開始sound = pygame.mixer.Sound("sound/start.mp3")
終了sound = pygame.mixer.Sound("sound/end.mp3")
選択sound = pygame.mixer.Sound("sound/serect.mp3")
決定sound = pygame.mixer.Sound("sound/decide.mp3")
攻撃sound = pygame.mixer.Sound("sound/attak.mp3")
敵攻撃sound = pygame.mixer.Sound("sound/ene_attak.mp3")
自爆sound = pygame.mixer.Sound("sound/bomb.mp3")
クリアsound = pygame.mixer.Sound("sound/game_clear.mp3")
負けsound = pygame.mixer.Sound("sound/game_over.mp3")

my_items = []

def item_get():
  道具数 = len(my_items)
  if 道具数 <= 7:
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
font_bigtext = pygame.font.SysFont("msgothic", 80)

タイトルrunning = True
battle_statu = False

plus_bombs = 0

開始状態 = 0
中間状態 = 0

マインスイーパー開始_text = font_bigtext.render(f'爆弾を解除しろ!!!', True, text_color)
マインスイーパー終了_text = font_bigtext.render(f'終了!!!', True, text_color)

def show_countdown1(screen, font, background_color, clock):
  global 開始状態
  countdown_texts = ["3", "2", "1", "Go!"]
  for text in countdown_texts:
    screen.fill(background_color)
    countdown_surface = font.render(text, True, (255, 255, 255))
    screen.blit(countdown_surface, (590, 300))
    開始状態 += 1
    if 開始状態 == 4:
      開始sound.play()
      開始状態 = 0
    pygame.display.flip()
    for _ in range(60):  # 約1秒間表示（60 FPSの場合）
      clock.tick(60)  # フレームレートを維持

def show_countdown(screen, font, background_color, clock):
  countdown_texts = ["3", "2", "1", "Go!"]
  global 中間状態
  for text in countdown_texts:
    screen.fill(background_color)
    countdown_surface = font.render(text, True, (255, 255, 255))
    screen.blit(countdown_surface, (590, 300))
    中間状態 += 1
    if 中間状態 == 4:
      開始sound.play()
      中間状態 = 0
    pygame.display.flip()
    for _ in range(60):  # 約1秒間表示（60 FPSの場合）
      clock.tick(60)  # フレームレートを維持

名前入力 = True
名前 = ""


while タイトルrunning:
  if 名前入力:
    screen.fill(background_color)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        タイトルrunning = False
        mainrunning = False
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          名前入力 = False
        elif event.key == pygame.K_BACKSPACE:
          名前 = 名前[:-1]
        else:
          名前 += event.unicode

    名前_text = font_bigtext.render("名前を入力してください", True, text_color)
    名前入力_text = font_bigtext.render(名前, True, text_color)
    screen.blit(名前_text, (150, 250))
    screen.blit(名前入力_text, (150, 350))
    pygame.display.flip()
  else:
    screen.fill(background_color)
    screen.blit(マインスイーパー開始_text, (280, 300))
    pygame.display.flip()
    for _ in range(120):  # 1秒間表示（60 FPS）
      clock.tick(60)

    screen.fill(background_color)
    show_countdown1(screen, font_bigtext, background_color, clock)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        タイトルrunning = False
        mainrunning = False
        pygame.quit()
        sys.exit()

    タイトルrunning = False


マインスイーパー終了 = False

初期設定 = True

battlerunning = False

def RPG_draw():
  screen.blit(ene_img, (750, 200))
  pygame.draw.rect(screen, text_color, (500, 400, 650, 200), 2)
  pygame.draw.rect(screen, text_color, (500, 50, 250, 200), 2)
  my_HP_text = font_battle.render(f"HP {my_HP}", True, text_color)
  my_EP_text = font_battle.render(f"エネルギー {my_EP}", True, text_color)
  自爆_text = font_battle.render(f"爆発した爆弾 {自爆}個", True, text_color)
  解除_text = font_battle.render(f"解除した爆弾 {解除爆弾数}", True, text_color)
  screen.blit(my_HP_text, (520, 60))
  screen.blit(my_EP_text, (520, 100))
  screen.blit(自爆_text, (520, 140))
  screen.blit(解除_text, (520, 180))

num_bombs = 18
all_bombs = 18

mainrunning = True
while mainrunning:
  # ゲームループ
  if 初期設定 == True:
    my_atkP = 0
    my_blkP = 0
    # セルの開閉状態と爆弾配置
    opened = [[False for _ in range(cols)] for _ in range(rows)]
    bombs = [[False for _ in range(cols)] for _ in range(rows)]
    corect = [[False for _ in range(cols)]for _ in range(rows)]
    not右クリック = [[False for _ in range(cols)]for _ in range(rows)]

    増加エネルギー量 = 0
    解除爆弾数 = 0
    自爆 = 0
    start = time.time()
    経過時間 = 0
    item_getflg = True
    初期設定 = False
    マインスイーパーrunning = True
    マインスイーパー終了 = False

    while num_bombs > 0:

      row = random.randint(0, rows - 1)
      col = random.randint(0, cols - 1)
      if not bombs[row][col]:
        bombs[row][col] = True
        num_bombs -= 1

    num_bombs = 18
    all_bombs = 18
    plus_bombs += 2
    num_bombs = plus_bombs + num_bombs
    all_bombs = plus_bombs + all_bombs
    右クリック制限prus = 0
    右クリック制限 = int(all_bombs + 3 + 右クリック制限prus)

  while マインスイーパーrunning:

    ene_atkP = random.randint(4, 15)
    ene_blkP = random.randint(4, 8)

    color = (0, 255, 0)

    右クリック制限_text = font_minseeper.render(
        f'爆弾処理装置残り {右クリック制限}個', True, text_color)
    爆弾の数_text = font_minseeper.render(f'爆弾の数 {all_bombs}個', True, text_color)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        マインスイーパーrunning = False
        battlerunning = False
        mainrunning = False

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
              opened[row][col] = True
              if count_adjacent_bombs(row, col) == 0 and not bombs[row][col]:
                open_empty_cells(row, col)
              if bombs[row][col]:
                自爆 += 1

        elif event.button == 3 and 右クリック制限 >= 1:
          右クリック制限 = int(右クリック制限 - 1)
          print(右クリック制限)
          mouse_x, mouse_y = event.pos

  # クリックがゲームエリア内なら処理を実行
          if game_area.collidepoint(mouse_x, mouse_y):
            # ゲームエリア内のセル座標を計算
            col = (mouse_x - game_area.x) // cell_size
            row = (mouse_y - game_area.y) // cell_size

  # 範囲内のセルを開く
            if 0 <= row < rows and 0 <= col < cols and bombs[row][col]:
              if opened[row][col] == False:
                増加エネルギー量 += 1
                解除爆弾数 += 1
              opened[row][col] = True
              corect[row][col] = True
              corect[row][col] = corect[row][col]

  # 背景の描画
    screen.fill(background_color)

  # マインスイーパーのグリッドを描画
  # マインスイーパーのグリッドを描画
    for row in range(rows):
      for col in range(cols):
        cell_x = game_area.x + col * cell_size
        cell_y = game_area.y + row * cell_size
        cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

        if opened[row][col]:
          # 青色 (正解フラグ)
          if bombs[row][col] and corect[row][col] and not右クリック[row][col] == False:
            pygame.draw.rect(screen, corect_color, cell_rect)
          elif bombs[row][col]:  # 赤色 (爆弾)
            pygame.draw.rect(screen, bomb_color, cell_rect)
            not右クリック[row][col] = True
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

    経過時間 = time.time() - start
    if 経過時間 > 制限時間:
      経過時間 = 制限時間
      time計測 = False
      マインスイーパー終了 = True

    bar_width = int((経過時間 / 制限時間) * 1200)
    red = max(0, min(255, int((経過時間 / 制限時間) * 255)))
    green = max(0, min(255, 255 - int((経過時間 / 制限時間) * 255)))
    color = (red, green, 0)
    pygame.draw.rect(screen, color, (0, 0, bar_width, 20))
    screen.blit(右クリック制限_text, (50, 70))
    screen.blit(爆弾の数_text, (300, 70))
    RPG_draw()
    待機_text = font_battle.render(f"爆弾を解除してエネルギーを貯めろ!!", True, text_color)
    screen.blit(待機_text, (520, 410))

    if マインスイーパー終了 == True:
      screen.blit(マインスイーパー終了_text, (440, 300))
      終了sound.play()
      pygame.display.flip()
      for _ in range(210):  # 1秒間表示（60 FPS）
        clock.tick(60)
      screen.fill(background_color)
      battlerunning = True
      マインスイーパーrunning = False
    pygame.display.flip()

  selected_index = 0
  selected_index1 = 0
  道具選択 = False
  道具一覧 = True
  not_use_item = False
  自爆blk = 0
  attckmode = False
  ene_attck = False
  自爆計算 = False
  ene_end = False
  my_end = False
  自爆plus = 0

  my_EP = int(my_EP + 増加エネルギー量)
  while battlerunning:
    screen.fill(background_color)  # 画面全体を背景色で塗りつぶす

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
          if bombs[row][col] and corect[row][col] and not右クリック[row][col] == False:
            pygame.draw.rect(screen, corect_color, cell_rect)
          elif bombs[row][col]:
            pygame.draw.rect(screen, bomb_color, cell_rect)
            not右クリック[row][col] = True
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

    screen.blit(右クリック制限_text, (50, 70))
    screen.blit(爆弾の数_text, (300, 70))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        battlerunning = False
        マインスイーパーrunning = False
        mainrunning = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          selected_index = (selected_index - 1) % len(serect)
          選択sound.play()
        if event.key == pygame.K_DOWN:
          selected_index = (selected_index + 1) % len(serect)
          選択sound.play()

        if event.key == pygame.K_UP:
          selected_index1 = (selected_index1 - 1) % len(my_items)
          選択sound.play()
        if event.key == pygame.K_DOWN:
          selected_index1 = (selected_index1 + 1) % len(my_items)
          選択sound.play()

        if selected_index == 0:
          if event.key == pygame.K_w and my_EP >= 1:
            選択sound.play()
            my_atkP += 1
            my_EP -= 1
          elif event.key == pygame.K_s:
            選択sound.play()
            if my_atkP >= 1:
              my_atkP -= 1
              my_EP += 1
        elif selected_index == 1:
          if event.key == pygame.K_w and my_EP >= 1:
            選択sound.play()
            my_blkP += 1
            my_EP -= 1
          elif event.key == pygame.K_s:
            選択sound.play()
            if my_blkP >= 1:
              my_blkP -= 1
              my_EP += 1
        elif selected_index == 2:
          if event.key == pygame.K_RETURN:
            道具選択 = True
            selected_index = 0
            selected_index1 = 0
            決定sound.play()

        if 道具選択 == True:
          if event.key == pygame.K_u:
            道具一覧 = False
            選択された道具 = my_items[selected_index1]
            決定sound.play()
            if 選択された道具 == "シールド":
              自爆blk += 1
              my_items.remove("シールド")
              道具1_text = font_battle.render(
                  f'シールドを使った！', True, text_color)
              道具2_text = font_battle.render(
                  f'自爆のダメージが-5される!', True, text_color)
              道具img = シールドimg
            elif 選択された道具 == "スーパーシールド":
              自爆blk += 3
              my_items.remove("スーパーシールド")
              道具1_text = font_battle.render(
                  f'スーパーシールドを使った!', True, text_color)
              道具2_text = font_battle.render(
                  f'自爆のダメージが-15される!', True, text_color)
              道具img = スーパーシールドimg
            elif 選択された道具 == "ソード":
              my_items.remove("ソード")
              道具1_text = font_battle.render(
                  f'ソードを使った!', True, text_color)
              道具2_text = font_battle.render(
                  f'50%の確率の確率で与えるダメージが+10される!', True, text_color)
              道具img = ソードimg
              if random.random() < 0.5:
                my_atkP += 10
            elif 選択された道具 == "TNT":
              my_items.remove("TNT")
              my_atkP += 25
              自爆plus += 30
              道具1_text = font_battle.render(
                  f'TNTを使った!', True, text_color)
              道具2_text = font_battle.render(
                  f'与えるダメージを+25、自爆のダメージを+30する!', True, text_color)
              道具img = TNTimg
            elif 選択された道具 == "救急箱":
              my_items.remove("救急箱")
              my_HP += 20
              道具1_text = font_battle.render(
                  f'救急箱を使った!', True, text_color)
              道具2_text = font_battle.render(
                  f'自分のHPを20回復する!', True, text_color)
              道具img = 救急箱img
            elif 選択された道具 == "爆弾解除装置":
              my_items.remove("爆弾解除装置")
              右クリック制限prus = 3
              道具1_text = font_battle.render(
                  f'爆弾解除装置を使った!', True, text_color)
              道具2_text = font_battle.render(
                  f'次の爆弾解除装置の数が+3される!', True, text_color)
              道具img = 爆弾処理装置img

          elif event.key == pygame.K_SPACE:
            attckmode = True
            道具選択 = False
            選択sound.play()

    if 道具選択 == True and 道具一覧 == True:
      for i, text1 in enumerate(my_items):
        color = serect_color if i == selected_index1 else text_color
        text_surface1 = font_battle.render(text1, True, color)
        if i <= 3:
          text_rect1 = text_surface1.get_rect(center=(620, 430 + i * 35))
        else:
          text_rect1 = text_surface1.get_rect(
              center=(950, 430 + int(i - 4) * 35))
        screen.blit(text_surface1, text_rect1)

    if 道具選択 == False and attckmode == False:
      for i, text in enumerate(serect):
        color = serect_color if i == selected_index else text_color
        text_surface = font_battle.render(text, True, color)
        text_rect = text_surface.get_rect(center=(750, 430 + i * 50))
        screen.blit(text_surface, text_rect)

    elif ene_end == True:
      ene_end_text = font_battle.render(f"宇宙人を倒した!", True, text_color)
      screen.blit(ene_end_text, (520, 430))
      クリアsound.play()
      pygame.display.flip()
      time.sleep(3)
      battlerunning = False
      マインスイーパーrunning = False
      mainrunning = False
    elif my_end == True:
      my_end_text = font_battle.render(f"{名前}は宇宙人に倒されてしまった", True, text_color)
      screen.blit(my_end_text, (520, 430))
      負けsound.play()
      pygame.display.flip()
      time.sleep(3)
      battlerunning = False
      マインスイーパーrunning = False
      mainrunning = False

    elif 自爆計算 == True:
      自爆dammge = int(int(自爆 - 自爆blk) * 5)
      if 自爆dammge < 0:
        自爆dammge = 0
      my_HP = my_HP - 自爆dammge - 自爆plus
      if my_HP <= 0:
        my_HP = 0

      自爆_text1 = font_battle.render(f"先ほど解除できなかった爆弾は{自爆}つ!", True, text_color)
      自爆_text2 = font_battle.render(
          f"{名前}に{自爆dammge + 自爆plus}ポイントのダメージ!", True, text_color)
      自爆_text3 = font_battle.render(f"爆弾を解除しろ!!", True, text_color)
      screen.blit(自爆_text1, (520, 430))
      screen.blit(自爆_text2, (520, 460))
      screen.blit(自爆_text3, (520, 490))
      自爆sound.play()
      pygame.display.flip()
      time.sleep(4)
      if my_HP <= 0:
        my_HP = 0
        my_end = True
      else:
        マインスイーパーrunning = True
        battlerunning = False
        初期設定 = True
        show_countdown(screen, font_bigtext, background_color, clock)

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
            f"{名前}に{dammge}ポイントのダメージ!", True, text_color)
        screen.blit(ene_attck_text1, (520, 430))
        screen.blit(ene_attck_text2, (520, 460))
        敵攻撃sound.play()
        pygame.display.flip()
        time.sleep(3)
        自爆計算 = True
      else:
        my_EP = my_EP - ene_atkP
        if my_EP < 0:
          my_EP = 0
        ene_attck_text3 = font_battle.render(
            f"宇宙人のエネルギースティール!", True, text_color)
        ene_attck_text4 = font_battle.render(
            f"{名前}のエネルギーが{ene_atkP}ポイント減少した!", True, text_color)
        screen.blit(ene_attck_text3, (520, 430))
        screen.blit(ene_attck_text4, (520, 460))
        エネスティsound.play()
        pygame.display.flip()
        time.sleep(3)
        自爆計算 = True
      if my_HP <= 0:
        my_HP = 0
        my_end = True

    elif 道具選択 == False and attckmode == True:
      ene_HP = ene_HP - my_atkP
      text_attck1 = font_battle.render(f"{名前}の攻撃!", True, text_color)
      text_attck2 = font_battle.render(f"宇宙人に{my_atkP}のダメージ", True, text_color)
      screen.blit(text_attck1, (520, 430))
      screen.blit(text_attck2, (520, 460))
      攻撃sound.play()
      pygame.display.flip()
      time.sleep(3)
      if ene_HP <= 0:
        ene_end = True
      else:
        ene_attck = True

    elif 道具選択 == True and 道具一覧 == False:
      screen.blit(道具1_text, (520, 430))
      screen.blit(道具2_text, (520, 460))
      screen.blit(道具img, (1000, 500))
      道具使用sound.play()
      pygame.display.flip()
      time.sleep(4)
      attckmode = True
      道具選択 = False

    pygame.display.flip()
