import pygame
from pygame import mixer
from random import randint, uniform
import sys
from PIL import Image
import time

# Khởi tạo game
pygame.init()


#Khung game
Screen_Width = 800
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Width, Screen_Height))

#Background, nhạc nền, âm thanh hiệu ứng, font
background = pygame.image.load('background.png').convert_alpha()
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
Gameover = pygame.mixer.Sound("Gameover.wav")
explosionSound = pygame.mixer.Sound("explosion.wav")
Lasersound = pygame.mixer.Sound("laser.wav")
Effectsound = pygame.mixer.Sound("Effect.wav")
Effectsound = pygame.mixer.Sound("Effect.wav")
Sbulletsound = pygame.mixer.Sound("3bullet.wav")


# Tiêu đề và biểu tượng game
pygame.display.set_caption("Green space")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Bộ đếm
clock = pygame.time.Clock()
score = 0

#Tạo biến
game_over = False
running = True



#Tạo hình ảnh nhân vật
P1 = pygame.image.load("D1.png").convert_alpha()
P1_surf = P1.get_rect(topleft =(Screen_Width // 3 -145 , Screen_Height // 2 +25))
P2 = pygame.image.load("D2.png").convert_alpha()
P2_surf = P2.get_rect(topleft =(Screen_Width // 3 , Screen_Height // 2 +30))
P3 = pygame.image.load("D3.png").convert_alpha()
P3_surf = P3.get_rect(topleft =(Screen_Width // 3 + 150 , Screen_Height // 2 +25))
P4 = pygame.image.load('spaceship.png').convert_alpha()
P4_surf = P4.get_rect(topleft =(Screen_Width // 3 + 310 , Screen_Height // 2 +25))

#Đạn
P1_Bullet =pygame.image.load("luado.jpg").convert_alpha()
P2_Bullet =pygame.image.load("luaxanh.jpg").convert_alpha()
P3_Bullet =pygame.image.load("sarin.jpg").convert_alpha()
bullet_image = pygame.image.load("bullet.png").convert_alpha()

#Font select
Select = pygame.font.Font('04B_30__.TTF', 40)
Select_surf = Select.render('CHOOSE YOUR PLAYER', True, (0, 0, 0))
font = pygame.font.Font("04B_30__.TTF", 25)

# Game over text
over_font = pygame.font.Font('04B_30__.TTF', 64)
over = over_font.render('GAME OVER', True, (255, 255, 255))

# Chơi lại text
replay = pygame.font.Font('04B_30__.TTF', 20)
lai = replay.render('If you want to play again press space bar', True, (255, 255, 255))

# game name text
Prepare = pygame.font.Font('04B_30__.TTF', 64)
Prepare_surf = Prepare.render('GREEN SPACE', True, (255, 255, 255))

# bắt đầu text
letsplay = pygame.font.Font('04B_30__.TTF', 20)
letsplay_surf = letsplay.render('If you want to play again press space bar', True, (255, 255, 255))


#Lớp tàu
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, gif_path, groups, pos=(400, 300), speed=200):
        super().__init__(groups)

        # Tải các frame từ GIF
        self.frames = self.load_gif(gif_path)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]  # Frame hiện tại để hiển thị
       # Vị trí và tốc độ di chuyển
        self.Ship_direct = pygame.math.Vector2(0, 0)
        self.rect = self.image.get_rect(center=pos)
        self.spd = 500
        #Thời gian hồi đạn và giới hạn hiệu ứng
        self.bullet_shoot_time = 0
        self.Sbullet_shoot_time = 0
        self.cooldown_duration = 1000
        self.limit_duration = 3000
        self.limit3 = 0
        self.can_shoot = True
        self.threecan_shoot = False
        self.SS_canshoot = False
        # Điều khiển animation
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100  # Thời gian giữa các frame (ms)

    def load_gif(self, gif_path):
        """Tải GIF và phân tách từng frame."""
        pil_gif = Image.open(gif_path)  # Tải ảnh dạng PIL
        frames = []

        try:
            while True:
                frame = pil_gif.copy().convert("RGBA")  # Convert frame
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame_image)
                pil_gif.seek(pil_gif.tell() + 1)
        except EOFError:
            pass  # Hết frame

        return frames

    def bullet_timer(self):
        if not self.can_shoot:  #Nếu đang bắn
            current_time = pygame.time.get_ticks() #Lấy thời gian hiện tại - thời gian lúc bắn 
            if current_time - self.bullet_shoot_time >= self.cooldown_duration:  # Cooldown đã hết
                self.can_shoot = True  # Cho phép bắn lại

    def Speed_timer(self):
        if self.SS_canshoot:  # Nếu đang bắn
            current_time = pygame.time.get_ticks()
            if current_time - self.Sbullet_shoot_time <= self.limit_duration:  #điều kiện để bắn trong 1 khoảng thời gian
                self.cooldown_duration = 1  # Cho phép bắn liên túc
            else: 
                self.SS_canshoot = False #Nếu hết thời gian trả về tốc độ bắn bình thường
                self.cooldown_duration = 1000
    def giuvitri(self):
        # Giữ cho phi thuyền di chuyển trong một khoảng không bị out ra khung hình
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= 536:
            self.rect.bottom = 536

    def update(self, dt):
        global Chọn
        """Cập nhật vị trí và animation."""
        # Animation: chuyển frame
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:  # Kiểm tra thời gian tr
            self.last_update = now #đủ thời gian trễ thì lấy thời gian lúc đó
            self.current_frame = (self.current_frame + 1) % len(self.frames) #Lấy chỉ số khung hình lúc đó
            self.image = self.frames[self.current_frame] #Hiển thị khung hình lúc đó

        #Chuyển động của spaceship
        keys = pygame.key.get_pressed()
        self.Ship_direct.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) # để đi chéo
        self.Ship_direct.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.Ship_direct = self.Ship_direct.normalize() if self.Ship_direct else self.Ship_direct # xác định xem đường đi có phải đường chéo không
        self.rect.center += self.Ship_direct * self.spd * dt #vị trí ở tại 1 khung hình
        if keys[pygame.K_SPACE] and self.can_shoot: # Ấn space để bắn
            if Chọn == 1:
                Bullet(P1_Bullet, self.rect.midtop, (all_sprites, Bullet_sprites))
            elif Chọn == 2:
                Bullet(P2_Bullet, self.rect.midtop, (all_sprites, Bullet_sprites))
            elif Chọn == 3:
                Bullet(P3_Bullet, self.rect.midtop, (all_sprites, Bullet_sprites))
            elif Chọn == 4:
                Bullet(bullet_image, self.rect.midtop, (all_sprites, Bullet_sprites))
            self.can_shoot = False  # Tạm thời vô hiệu hóa bắn
            self.bullet_shoot_time = pygame.time.get_ticks()
            Lasersound.play()

        #Nếu trúng effect three bullet thì Có thể bắn 1 viên three bullet
        if pygame.sprite.spritecollide(spaceship, Three_bullet_sprites, True):
            Effectsound.play()
            self.threecan_shoot = True
        if keys[pygame.K_SPACE] and self.threecan_shoot:  # Three-bullet spread after
            if Chọn == 1:
                Bullet(P1_SBullet, self.rect.midtop, (all_sprites, Three_bullet_sprites))
            elif Chọn == 2:
                Bullet(P2_SBullet, self.rect.midtop, (all_sprites, Three_bullet_sprites))
            elif Chọn == 3:
                Bullet(P3_SBullet, self.rect.midtop, (all_sprites, Three_bullet_sprites))
            elif Chọn == 4:
                Bullet(Tbu, self.rect.midtop, (all_sprites, Three_bullet_sprites))
            self.threecan_shoot = False #Vô hiệu hóa bắn
            Sbulletsound.play()
        
        #Nếu trúng speed bullet -> Được bắn liên tục trong 4 giây
        if pygame.sprite.spritecollide(spaceship, SBBullet_sprites, True):
            Effectsound.play()
            self.SS_canshoot = True #mở khóa tính năng
            self.Sbullet_shoot_time = pygame.time.get_ticks()
        
        self.bullet_timer()
        self.Speed_timer()
        self.giuvitri()

#lớp đạn 
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.spd = 400     

    def update(self, dt):
        self.rect.y -= self.spd * dt  # Di chuyển đạn lên trên
        if self.rect.bottom < 0:  # Xóa đạn khi ra khỏi màn hình
            self.kill()

#Lớp hiệu ứng three_bullet
class Three_bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.originall_surf = surf
        self.image = self.originall_surf
        self.rect = self.image.get_rect(center=pos)
        self.spd = 300 + score // 5 #Cứ 5 điểm sẽ tăng tốc độ rơi
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000 #Thời gian tồn tại
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation = 0
    def update(self, dt):
        self.rect.center += self.direction * self.spd * dt #Số pixel di chuyển trong dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill() #Xóa khi hết tg tồn tại
        self.rotation += 40 * dt #Độ xoay
        self.image = pygame.transform.rotozoom(self.originall_surf, self.rotation, 1.5)# Hàm phóng to và xoay
        self.rect = self.image.get_rect(center=self.rect.center) 

#Lớp Speed Bullet (Giống Three_bullet
class SS_bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.originall_surf = surf
        self.image = self.originall_surf
        self.rect = self.image.get_rect(center=pos)
        self.spd = 300 + score // 5
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.spd * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += 40 * dt
        self.image = pygame.transform.rotozoom(self.originall_surf, self.rotation, 1.2)
        self.rect = self.image.get_rect(center=self.rect.center)

#Tải ảnh 
three_bullet = pygame.image.load("3_bullet.png").convert_alpha()
Sbullet = pygame.image.load("SSBullet.png").convert_alpha()
Tbu = pygame.image.load("SBullet.png").convert_alpha()
P1_SBullet = pygame.image.load("sLUA.png").convert_alpha()      
P2_SBullet = pygame.image.load("rONG.png").convert_alpha()
P3_SBullet = pygame.image.load("susano.jpg").convert_alpha()

#Lớp rác cũng giống 2 lớp trên
class Trash(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.originall_surf = surf
        self.image = self.originall_surf
        self.rect = self.image.get_rect(center=pos)
        self.spd = 300 + score // 5
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.spd * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += 40 * dt
        self.image = pygame.transform.rotozoom(self.originall_surf, self.rotation, 1.5)
        self.rect = self.image.get_rect(center=self.rect.center)

#Biến trash
rac = pygame.image.load('rac.png').convert_alpha()
apple = pygame.image.load('apple.png').convert_alpha()
fishbone = pygame.image.load('fishbone.png').convert_alpha()

#Lớp hiệu ứng nổ
class Hieu_ung_no(pygame.sprite.Sprite):
    def __init__(self, frame, pos, groups):
        super().__init__(groups)
        self.frame = frame #Gán hình ảnh ở bên ngoài
        self.current_frame = 0 #Chỉ số khung hình
        self.image = self.frame[self.current_frame] #Gán hình ảnh bằng khung hình ban đầu
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.current_frame += 20 * dt #Thay đổi chỉ khung hình
        if self.current_frame < len(self.frame): #Chỉ thực hiện khi chỉ số khung hình nhỏ hơn số lượng khung hình No_frames
            self.image = self.frame[int(self.current_frame)] #Gán hình bằng khung hình lúc đó
        else:
            self.kill() #Xóa hiệu ứng 


#HIệu ứng nổ
No_frame = [pygame.image.load(f"{i}.png").convert_alpha() for i in range(21)] #Tại tất cả khung hình

def vacham():
    global game_over, score
    # Va chạm giữa spaceship và trash
    Tainan = pygame.sprite.groupcollide(Spaceshipp, Trash_sprites, False, True)
    if Tainan:  # Nếu va chạm, kết thúc trò chơi
            game_over = True
            Gameover.play(  )

 #kiểm tra từng viên đạn   
    for bullet in Bullet_sprites:      
        # Va chạm đạn với trash
        if pygame.sprite.spritecollide(bullet, Trash_sprites, True):
            bullet.kill() #Xóa đạn
            explosionSound.play() #Âm thanh nổ
            Hieu_ung_no(No_frame, bullet.rect.midtop, all_sprites) #Tạo hiệu ứng nổ 
            score += 1

    collisions = pygame.sprite.groupcollide(Three_bullet_sprites, Trash_sprites, False, True) #Lưu trữ Three Bullet khi nó va chạm
    for bullet, trash_list in collisions.items(): 
        for trash in trash_list: #đặt hiệu ứng cho tất cả phần tử thuộc Group Trash_sprites
            Hieu_ung_no(No_frame, trash.rect.center, all_sprites) #Tạo hiệu ứng nổ
            score += 1  # **THÊM ĐIỂM** giống như đạn thường
            explosionSound.play() #Âm thanh

#Tạo điểm
def Score():
    Text_sur = font.render(f"SCORE: {score}", True, "White")
    Text_s = Text_sur.get_rect(topleft=(10, 10))
    screen.blit(Text_sur, Text_s)

#Hàm reset game
def reset_game():
    global score, game_over, Chọn
    #Đặt Lại tất cả nhóm sprites trong game
    all_sprites.empty()
    Trash_sprites.empty()
    Bullet_sprites.empty()
    Three_bullet_sprites.empty()
    SBBullet_sprites.empty()
    Spaceshipp.empty()
    Chọn = None
    #Đặt lại điểm
    score = 0

#tạo group chứa tất cả sprite trong code
all_sprites = pygame.sprite.Group()
#Group chứa tàu
Spaceshipp = pygame.sprite.Group()
#Group chứa rác
Trash_sprites = pygame.sprite.Group()
#Group chứa đạn
Bullet_sprites = pygame.sprite.Group()
#Group chứa hiệu ứng đặc biệt
Three_bullet_sprites = pygame.sprite.Group()
SBBullet_sprites = pygame.sprite.Group()


# Custom events - set delay xuất hiện vật thể
Trash_event = pygame.event.custom_type()
pygame.time.set_timer(Trash_event, 2000)
Trash_type = [rac, apple, fishbone]


# đặt một số biện cần thiết
Chọn = None
can_select = True

#Hàm vẽ menu chọn nhân vật
def draw_menu_selecchar():
    global can_select, Chọn
    if can_select:
        pygame.draw.rect(screen, "white", (20, 20, 760, 560), 0, 10)
        screen.blit(Select_surf, (Screen_Width // 2 - Prepare_surf.get_width() // 2, Screen_Height // 3))

        #Vẽ Khung chọn nhân vật 1,2,3,4
        screen.blit(P1, (Screen_Width // 3 -150 , Screen_Height // 2 +30))
        pygame.draw.rect(screen, "Black", (Screen_Width // 3 -145 , Screen_Height // 2 +25, 100,120), 3, 10)
    
        pygame.draw.rect(screen, "Black", (Screen_Width // 3 , Screen_Height // 2 +25, 100,120), 3, 10)
        screen.blit(P2, (Screen_Width // 3 -10 , Screen_Height // 2 +10))

        screen.blit(P3, (Screen_Width // 3 + 130 , Screen_Height // 2 +10))
        pygame.draw.rect(screen, "Black", (Screen_Width // 3 + 150 , Screen_Height // 2 +25, 100,120), 3, 10)
        
        screen.blit(P4, (Screen_Width // 3 +330 , Screen_Height // 2 +50))
        pygame.draw.rect(screen, "Black", (Screen_Width // 3 + 310 , Screen_Height // 2 +25, 100,120), 3, 10)

        # Gọi hàm kiểm tra chọn tàu
        check_ship_selection()
        
        pygame.display.update()

#Hàm kiểm tra tàu
def check_ship_selection():
    global spaceship, Chọn, can_select, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột khi click

            # Kiểm tra chọn nhân vật nào thì gán nhân vật cho lớp Spaceship, Gán giá trị cho biến chọn
            if P1_surf.collidepoint(mouse_pos):
                spaceship = Spaceship("Rồng.gif", (all_sprites, Spaceshipp))
                Chọn = 1

            elif P2_surf.collidepoint(mouse_pos):
                spaceship = Spaceship("ghost.gif", (all_sprites, Spaceshipp))
                Chọn = 2

            elif P3_surf.collidepoint(mouse_pos):
                spaceship = Spaceship("demon.gif", (all_sprites, Spaceshipp))
                Chọn = 3

            elif P4_surf.collidepoint(mouse_pos):
                spaceship = Spaceship("spaceship.gif", (all_sprites, Spaceshipp))
                Chọn = 4

            #Nếu chưa chọn 
            if Chọn is not None:
                can_select = False #Nếu đã chọn thì bắt đầu game
                game_over = False
                print("Chọn xong nhân vật!")
                break

def gameplay():
    global running, game_over, can_select
    while running:
        screen.blit(background, (0, 0))
        dt = clock.tick(60) / 1000  # Use delta time for consistent motion
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Handle object generation and collisions during gameplay
            if event.type == Trash_event and not game_over:
                num_trash = max(3, score // 5)
                three_bullet_shown = False  # No duplicate Three_bullet items
                ss_bullet_shown = False  # No duplicate SS_bullet items

                for _ in range(num_trash):
                    trash = Trash_type[randint(0, len(Trash_type) - 1)]
                    x, y = randint(50, Screen_Width - 50), randint(-200, -100)
                    z, t = randint(50, Screen_Width - 50), randint(-200, -100)
                    Trash(trash, (x, y), (all_sprites, Trash_sprites))

                # Handle Three_bullet and SS_bullet generation logic
                if score % 4 == 0 and score >= 4 and not three_bullet_shown:
                    Three_bullet(three_bullet, (z, t), (all_sprites, Three_bullet_sprites))
                    three_bullet_shown = True
                if score % 6 == 0 and score >= 6 and not ss_bullet_shown:
                    SS_bullet(Sbullet, (z, t), (all_sprites, SBBullet_sprites))
                    ss_bullet_shown = True

        
        #Bắt đầu game
        if not game_over:
            all_sprites.update(dt)
            vacham()
            Score()

        # Nếu thua thì hiện chữ
        if game_over:
                 reset_game()
                 can_select =True
                 draw_menu_selecchar()

        all_sprites.draw(screen)
        pygame.display.update()

#Chạy chương trình 
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        #Nếu có thể chọn thì hiện menu chọn nhân vật để chọn
        if can_select:
            draw_menu_selecchar()
        
        elif not can_select: #Nếu Không thể chọn thì bắt đầu game
            gameplay()

