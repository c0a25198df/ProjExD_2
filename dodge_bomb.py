import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650

DELTA = {pg.K_UP:(0, -5),
         pg.K_DOWN:(0, +5),
         pg.K_LEFT:(-5, 0),
         pg.K_RIGHT:(+5, 0),}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内科画面外貨を判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向,縦方向の判定結果
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    go_img = pg.Surface((1100, 650))
    go_img.fill((0, 0, 0))
    go_img.set_alpha(100)
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect()
    text_rct.center = WIDTH // 2, HEIGHT // 2
    cry_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_rct1 = cry_img1.get_rect()
    cry_rct2 = cry_img2.get_rect()
    cry_rct1.center = WIDTH // 2 -200 , HEIGHT // 2
    cry_rct2.center = WIDTH // 2 +200 , HEIGHT // 2
    screen.blit(go_img, (0, 0))
    screen.blit(cry_img1, cry_rct1)
    screen.blit(cry_img2, cry_rct2)
    screen.blit(text, text_rct)
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (250, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_img.set_colorkey((0, 0, 0))
    bb_accs = [a for a in range(1,11)]
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")     
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200


    bb_img = pg.Surface((20, 20))#爆弾用の空のサーフェイス
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)#爆弾の円を描く
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #爆弾の初期座標ランダム
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5
    bb_imgs, bb_accs = init_bb_imgs()
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            print("ゲームオーバー")
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#こうかとんを逃がさない
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        idx = min(tmr // 500, 9)

        bb_img = bb_imgs[idx]
        center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = center
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)

        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct) #爆弾表示させる
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
