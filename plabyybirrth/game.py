import pygame, sys ,random

#pygame.mixer.pre_init(frequency = 44100, size = 16 , channels=1,buffer =512)

pygame.init()

screen = pygame.display.set_mode((576,1024)) #kich thuoc man hinh

clock = pygame.time.Clock()#set thoi gian

game_font = pygame.font.Font(pygame.font.get_default_font(),40) # font chu1

def tao_cot():
	random_cot = random.randint(400,800)
	cot_duoi = cot_surface.get_rect(midtop = (700,random_cot)) # vi tri cot
	cot_tren = cot_surface.get_rect(midbottom = (700,random_cot - 300))
	mid = (random_cot + (random_cot - 300))/2
	return cot_duoi,cot_tren

def di_chuyen_cot(cot_list):
	x = []
	y = []
	for cot in cot_list:
		cot.centerx -= 5
		x.append(cot.centerx)
		y.append(cot.centery)
	return cot_list,x,y

def ve_cot(cot_list):
	for cot in cot_list:
		if cot.bottom >= 1024:
			screen.blit(cot_surface,cot)
		else:
			flip_pipe = pygame.transform.flip(cot_surface,False,True)
			screen.blit(flip_pipe ,cot)

def check(cot_list):
	for cot in cot_list:
		if chim_vitri.colliderect(cot):
			am_thanh_chet.play()
			return False
	if chim_vitri.top <= -100 or chim_vitri.bottom >= 900:
		am_thanh_chet.play()
		return False
	return True 

def rotate_chim(chim_surface):
	new = pygame.transform.rotozoom(chim_surface,-chim_roi*3,1)
	return new

def hinh_chim():
	new = chim_hinh[chim_index]
	new_vitri = new.get_rect(center = (100,chim_vitri.centery))
	return new,new_vitri

def diem(game_state):
	if game_state == 'main_game':
		diem_surface = game_font.render('Score: '+ str(int(dim)),True,(255,0,255))
		diem_vitri = diem_surface.get_rect(center = (288,100))
		screen.blit(diem_surface,diem_vitri)
	if game_state == 'game_over':
		diem_surface = game_font.render('Score: '+ str(int(dim)),True,(255,0,255))
		diem_vitri = diem_surface.get_rect(center = (288,100))
		screen.blit(diem_surface,diem_vitri)

		diem_cao = game_font.render('Score: '+ str(int(dim_cao)),True,(255,0,255))
		diem_cao_vitri = diem_surface.get_rect(center = (288,850 ))
		screen.blit(diem_cao,diem_cao_vitri)

def update_diem(dim,dim_cao):
	if dim > dim_cao:
		dim_cao = dim
	return dim_cao



def f(x,a,b,c):
	return ((x**2)*a) +( x*b) + c 

def fc(x1,y1,x2,y2):
	a = y1/( (((-2) * (x1**2))+ x1 + y2 - (((-2) * (x2**2)) + x2) ))
	c = y2 - (((-2) * (x2**2)) + x2)*a 
	b = (-2)*x1*a 
	return a,b,c 

# bien doi
gravity = 0.25
chim_roi = 0
game_active = True
dim = 0
dim_cao = 0

nen_surface = pygame.image.load('sprites/background-day.png').convert() #load hình nền
nen_surface = pygame.transform.scale2x(nen_surface) # x2 kích thước ảnh

dat_surface = pygame.image.load('sprites/base.png').convert() # nền đất
dat_surface = pygame.transform.scale2x(dat_surface)
dat_x = 0

#chim_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha() # chim xanh
#chim_surface = pygame.transform.scale2x(chim_surface)
#chim_vitri = chim_surface.get_rect(center = (100,512))

canh_xuong = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png')).convert_alpha()
canh_giua = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png')).convert_alpha()
canh_len = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png')).convert_alpha()
chim_index = 0
chim_hinh = [canh_xuong,canh_giua,canh_len]
chim_surface = chim_hinh[chim_index]
chim_vitri = chim_surface.get_rect(center = (100,512))
bird = pygame.USEREVENT + 1
pygame.time.set_timer(bird,200)

cot_list = []
cot_surface = pygame.image.load('sprites/pipe-green.png').convert() # chim xanh
cot_surface = pygame.transform.scale2x(cot_surface)
 # danh sách cột 
spawnpipe = pygame.USEREVENT # sự kiện tạo cột
pygame.time.set_timer(spawnpipe,1200) # mỗi 1200 mili giây sẽ tạo ra 1 cột mới

game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
game_over_vi_tri = game_over_surface.get_rect(center = (288,512))

am_thanh_nhay = pygame.mixer.Sound('audio/wing.wav')
am_thanh_chet = pygame.mixer.Sound('audio/hit.wav')
am_thanh_diem = pygame.mixer.Sound('audio/point.wav')
kem_theo_diem = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # nut thoat
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				chim_roi = 0
				chim_roi -= 10 
				am_thanh_nhay.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				cot_list.clear()
				chim_vitri.center = (100,512)
				chim_roi = 0
				dim = 0 
				kem_theo_diem = 100
		diem_surface = game_font.render('Score: '+ str(int(dim)),True,(255,0,255))
		diem_vitri = diem_surface.get_rect(center = (288,100))
		screen.blit(diem_surface,diem_vitri)
		if event.type == spawnpipe:
			cot_list.extend(tao_cot())
			#print(cot_list)
			if len(cot_list) > 5:    
				del cot_list[1]
				del cot_list[0]
		if event.type == bird:
			if chim_index <2:
				chim_index+=1
			else:
				chim_index = 0

			chim_surface,chim_vitri = hinh_chim()

	# hinh nền - blit(hinh,tọa độ hình , )
	screen.blit(nen_surface,(0,0))
	if game_active:			
		# vex chim
		chim_roi += gravity
		rotated_chim = rotate_chim(chim_surface)
		chim_vitri.centery += chim_roi
		screen.blit(rotated_chim,chim_vitri)
		print(chim_vitri)

		#game_active = check(cot_list)

		# ve cot
		cot_list,vitri_cot_x,vitri_cot_y = di_chuyen_cot(cot_list)
		ve_cot(cot_list)
		print(vitri_cot_y)

		dim += 0.01
		diem('main_game')
		kem_theo_diem -= 1
		if kem_theo_diem <=0 :
			am_thanh_diem.play()
			kem_theo_diem = 100
	else:
		screen.blit(game_over_surface,game_over_vi_tri)
		dim_cao = update_diem(dim,dim_cao)
		diem('game_over')



	# vẽ nền 
	dat_x -= 1
	screen.blit(dat_surface,(dat_x,900)) # nền di chuyển
	screen.blit(dat_surface,(dat_x + 576,900)) # nền chống lag 
	if dat_x <= -576: # kích thước chiều ngang màn hình
		dat_x = 0


	pygame.display.update()
	clock.tick(120)