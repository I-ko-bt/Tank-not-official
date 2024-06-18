import pygame,sys,random,math,cv2,numpy
from pygame.locals import *
pygame.init()
xwindow,ywindow=1000,700
screen = pygame.display.set_mode((xwindow,ywindow))
clock=pygame.time.Clock()
nau_dat=[148,83,5]
xam=[150,150,150]
la_sang=[0,255,0]
vang_gold=[193,140,0]
cam=[236,135,14]
vang=[249,244,0]
do=[255,0,0]
den=[0,0,0]
xanh=[0,0,255]
trang=[255,255,255]
def load_anh(im,i,j,a,b,c):
    la_1=i*j,a*b
    la_ds=[]
    for la_i in range(la_1[0]):
        la_2=la_i//j,la_i%j
        if la_2[1]==0 and i!=1 and j!=1:la_ds.append([])
        im_0=im[la_2[0]*a:(la_2[0]+1)*a,la_2[1]*b:(la_2[1]+1)*b]
        la_surf=pygame.Surface((b,a),SRCALPHA )
        for la_j in range(la_1[1]):
            la_3=la_j%a,la_j//a
            if la_3[0]==0:
                la_5=la_3
                la_6=list(im_0[la_3])
                la_6.reverse()
                continue
            la_4=list(im_0[la_3])
            la_4.reverse()
            if (la_4!=la_6) or(la_3[0]==a-1) or (la_4 in c ):
                if not(la_6 in c):
                    pygame.draw.rect(la_surf,la_6,(la_5[1],la_5[0],1,la_3[0]-la_5[0]))
                    if la_3[0]==a-1:
                        pygame.draw.rect(la_surf,la_4,(la_5[1],a-1,1,1)) 
                la_5,la_6=la_3,la_4
        if (i!=1 and j!=1): la_ds[la_2[0]].append(la_surf)
        else: la_ds.append(la_surf)
    return la_ds
def change(a,b):
    return b,a
def add_or_del_tank(i,j,k):
    if k==1:
        them_dan(i)
        if i>=sl_player or j==0:
            tg_chet[i].append([-1,-1])
            x[i].append(0)
            y[i].append(0)
            h[i].append(0)
            mang_mh[i].append(5*(1+min(level,6)//6))
    elif k==0:
        if i>=sl_player:
            x[i][j]=0
            y[i][j]=0
        tao_tank(i,j)
    else:
        del(tg_chet[i][j])
        del(x[i][j])
        del(y[i][j])
        del(h[i][j])    
        del(kho_dan[i][j])
        del(x_dan[i][j])
        del(y_dan[i][j])
        del(hx_dan[i][j])
        del(hy_dan[i][j])
        del(mang_mh[i][j]) 
        sl_tank_mh[i]-=1
def tao_tank(i,j):
    if i<sl_player:x[i],y[i],h[i]=[xwindow//2-80*(sl_player-2*i)-20],[500],[0]
    else:
        while not tuong_tac_xe_xe(i,j)or x[i][j]==0 or chuong_ngai_vat(i,j,0) or(level<6 and y[i][j]<40):
            x[i][j]=5*random.randint(4,156)
            y[i][j]=20*random.randint(1,5)
            mang_mh[i][j]=mang[type_tank[i]%sl_tank]
        h[i][j]=random.randint(0,3)
def hinh_tank(i,j):
    ht_1=type_tank[i]
    ht_2=tg[1]-tg_chet[i][j][1]
    if ht_2<0:ht_2+=60
    if 0<=ht_2<=1 and tg_chet[i][j][1]!=-1:
        ht_3=(tg[0]+60-tg_chet[i][j][0])%60
        if ht_2>0:ht_4=8
        else: ht_4=4
        if (ht_3%ht_4)<(ht_4//2):ht_5=True
        else: ht_5=False
    else:ht_5=True
    if ((x[i][j]+y[i][j])//5)%8<4:ht_6=0
    else:ht_6=1
    if sl_player-1==i==1:ht_6+=9
    if ht_5 or pause:
        surf_bg.blit(tank[ht_1][h[i][j]%4*2+ht_6],(x[i][j]-20,y[i][j]-20)) 
def tuong_tac_xe_xe(i,j):
    ttxx_1=pygame.Rect(x[i][j],y[i][j],40,40)
    for ttxx_i in range(sl_loai_tank+1):
        for ttxx_j in range(sl_tank_mh[ttxx_i]):
            if ttxx_i!=i or ttxx_j!=j:
                ttxx_2=pygame.Rect(x[ttxx_i][ttxx_j],y[ttxx_i][ttxx_j],40,40)
                ttxx_3=ttxx_1.colliderect(ttxx_2)
                if ttxx_3: 
                    return False       
    return True 
def kt_tank(i,j,k): 
    ktt_ds1,ktt_ds2=y,x
    if (h[i][j]%4)%2:ktt_ds1,ktt_ds2=x,y
    ktt_s=ktt_ds1[i][j]
    if k==0:ktt_e=ktt_ds1[sl_loai_tank][0]
    else:ktt_e=ktt_ds1[k-1][0]
    if 0<h[i][j]%4<3:
        ktt_s+=25
        ktt_st=20
    else:
        ktt_s-=25
        ktt_st=-20   
    for ktt_i in range(sl_player,sl_loai_tank+1):
        if (ktt_i==sl_loai_tank) and (level>5 or k==0):break 
        for ktt_j in range(sl_tank_mh[ktt_i]):
            if ktt_i!=i or ktt_j!=j:
                ktt_1=(ktt_s-ktt_e<0)==(ktt_s-ktt_ds1[ktt_i][ktt_j]<0)
                ktt_2=abs(ktt_ds2[ktt_i][ktt_j]-ktt_ds2[i][j])<25
                ktt_3=abs(ktt_s-ktt_ds1[ktt_i][ktt_j])<abs(ktt_s-ktt_e)
                if ktt_1 and ktt_2 and ktt_3  :return False
    ktt_4=ktt_5=ktt_ds2[i][j]//20;ktt_6=[0,0]
    if ktt_ds2[i][j]%20<5 :
        if h[i][j]%2:ktt_6[0]=-1
        else:ktt_6[1]=-1
    for ktt_i in range(ktt_s,ktt_e,ktt_st): 
        if h[i][j]%2:ktt_5=ktt_i//20
        else:ktt_4=ktt_i//20
        if td_bg[ktt_4][ktt_5]==3:return False
        elif 0<=ktt_4+ktt_6[0]<len(td_bg) and 0<=ktt_5+ktt_6[1]<len(td_bg[0]):
            if td_bg[ktt_4+ktt_6[0]][ktt_5+ktt_6[1]]==3:return False
    return True 
def move_tank(i,j):
    if i<sl_player:mt_1=mt_test
    else:mt_1=str(h[i][j]%4)
    mt_2=("0" in mt_1)!=("2" in mt_1)
    mt_3=("1" in mt_1)!=("3" in mt_1)
    if mt_2:
        if "0" in mt_1:y[i][j]-=5
        else          :y[i][j]+=5
    if mt_3:
        if "1" in mt_1:x[i][j]+=5
        else          :x[i][j]-=5
       
    if tuong_tac_xe_xe(i,j) and not chuong_ngai_vat(i,j,0):
        if h[i][j]>3:h[i][j]-=4 
        return True
    if mt_2:
        if "0" in mt_1:y[i][j]+=5
        else          :y[i][j]-=5
    if mt_3:
        if "1" in mt_1:x[i][j]-=5
        else          :x[i][j]+=5
    if h[i][j]>3:h[i][j]=h[i][j]%4   
    return False

def AI_tank(i,j):
    ait_5=1
    if i<sl_player:move_tank(i,0)
    else:
        ait_1,ait_2=x[0][0]-x[i][j],y[0][0]-y[i][j]
        if sl_player==2:
            ait_3,ait_4=x[1][0]-x[i][j],y[1][0]-y[i][j]
            if min(abs(ait_3),abs(ait_4))<min(abs(ait_1),abs(ait_2)):
                ait_1,ait_2,ait_5=ait_3,ait_4,2
        if level>5:
            ait_3,ait_4=x[sl_loai_tank][0]-x[i][j],y[sl_loai_tank][0]-y[i][j]
            if min(abs(ait_3),abs(ait_4))<min(abs(ait_1),abs(ait_2)):
                ait_1,ait_2,ait_5=ait_3,ait_4,0
        if ait_1<0: chieu_x=-1
        else: chieu_x=1
        if ait_2<0: chieu_y=-1
        else: chieu_y=1
        ait_6=0
        if abs(ait_1)<abs(ait_2):
            ait_6=3

        if min(ait_1,ait_2)>20:
            ait_6=abs(2-ait_6)

        if abs(ait_2)<=20 or abs(ait_1)<=20:
            if   abs(ait_1)<=20:h[i][j]=1+chieu_y
            elif abs(ait_2)<=20:h[i][j]=2-chieu_x
            if (not kho_dan[i][j])and kt_tank(i,j,ait_5):
                tao_dan(i,j)
            elif not kt_tank(i,j,ait_5):move_tank(i,j)

        else:
            if h[i][j]<4:
                ait_6=random.randint(0,3)+4*(random.randint(8,152))
                h[i][j]=ait_6  

        move_tank(i,j)
def toc_do(i,j,k):
    td_1=td_tank[type_tank[i]%sl_tank]
    if i<sl_player:
        if td_1==-1:td_1+=1
        td_1+=1
    if k==0:
        if td_1<0:
            td_2=tg[0]+60*tg[1]+3600*(tg[2]+60*tg[3])
            if td_2%(-td_1)==0:
                AI_tank(i,j)
        else:
            for td_i in range(td_1):AI_tank(i,j)
def them_dan(i):
    x_dan[i].append(0)
    y_dan[i].append(0)
    hx_dan[i].append(0)
    hy_dan[i].append(0)
    kho_dan[i].append(False)        
def kich_hoat_dan(i):
    if (kho_dan[i].count(False)>0):
        tao_dan(i,kho_dan[i].index(False))
def tao_dan(i,j):
    td_1=j
    if i<sl_player:td_1=0
    td_2=x[i][td_1]+15*(2-h[i][td_1]%4)*((h[i][td_1]%4)%2)
    td_3=y[i][td_1]-15*(1-h[i][td_1]%4)*((h[i][td_1]%4+1)%2)
    td_4=5*(2-h[i][td_1]%4)*((h[i][td_1]%4)%2)
    td_5=-5*(1-h[i][td_1]%4)*((h[i][td_1]%4+1)%2)
    td_6=True
    x_dan[i][j],y_dan[i][j],hx_dan[i][j],hy_dan[i][j],kho_dan[i][j]=td_2,td_3,td_4,td_5,td_6
def hinh_dan(i,j):
    hd_1,hd_2,hd_3,hd_4=x_dan[i][j],y_dan[i][j],hx_dan[i][j],hy_dan[i][j]
    hd_5=0
    if hd_3!=0:
        if hd_3<0:hd_5=3
        else:hd_5=1
    elif hd_4>0:hd_5=2    
    surf_bg.blit(bullet[hd_5],(hd_1-5,hd_2-5))    
def va_cham_dan(i,j):
    vcd_1=tuong_tac_xe_dan(i,j)[0]
    vcd_2=tuong_tac_dan_dan(i,j)[0]
    vcd_3=chuong_ngai_vat(i,j,1)
    return vcd_1 or vcd_2 or vcd_3 
def reset_dan(i,j):
    x_dan[i][j]=0
    y_dan[i][j]=0
    hx_dan[i][j]=0
    hy_dan[i][j]=0
    kho_dan[i][j]=False  
def tuong_tac_xe_dan(i,j):
    ttxd_1=pygame.Rect(x_dan[i][j]-5,y_dan[i][j]-5,10,10)
    for ttxd_i in range(sl_loai_tank+1):
        if ttxd_i==i and i<sl_player:continue
        for ttxd_j in range(sl_tank_mh[ttxd_i]):
            if ttxd_i!=i or ttxd_j!=j:
                ttxd_2=pygame.Rect(x[ttxd_i][ttxd_j]-20,y[ttxd_i][ttxd_j]-20,40,40)
                ttxd_3=ttxd_1.colliderect(ttxd_2)
                if ttxd_3:
                    return True,ttxd_i,ttxd_j      
    return False,0,0
def tuong_tac_dan_dan(i,j):
    ttdd_1=pygame.Rect(x_dan[i][j],y_dan[i][j],10,10)
    for ttdd_i in range(sl_loai_tank):
        for ttdd_j in range(sl_tank_mh[ttdd_i]):
            if ttdd_i!=i or ttdd_j!=j:
                ttdd_2=pygame.Rect(x_dan[ttdd_i][ttdd_j],y_dan[ttdd_i][ttdd_j],10,10)
                ttdd_3=ttdd_1.colliderect(ttdd_2)
                if ttdd_3:
                    return True,ttdd_i,ttdd_j      
    return False,0,0
def chuong_ngai_vat(i,j,k):
    if   k==0:cnv_1,cnv_2=(x[i][j],y[i][j]),3
    elif k==1:cnv_1,cnv_2=(x_dan[i][j],y_dan[i][j]),2
    cnv_3=(20/(k+1)**2<=cnv_1[0]<=800-20/(k+1)**2) and(20/(k+1)**2<=cnv_1[1]<=600-20/(k+1)**2)
    if not cnv_3:return True
    for cnv_i in range(cnv_2**2):
        cnv_4=cnv_1[0]//20-1+cnv_i//cnv_2,cnv_1[1]//20-1+cnv_i%cnv_2
        cnv_5=0<=cnv_4[0]<len(td_bg[0]) and 0<=cnv_4[1]<len(td_bg)
        cnv_6=abs(cnv_4[0]*20+10-cnv_1[0])<(30/(k+1)) and abs(cnv_4[1]*20+10-cnv_1[1])<(30/(k+1))
        if cnv_5 and cnv_6:
            if td_bg[cnv_4[1]][cnv_4[0]]>2 or (td_bg[cnv_4[1]][cnv_4[0]]==2 and k==0):
                if k==1:
                    if td_bg[cnv_4[1]][cnv_4[0]]>3:td_bg[cnv_4[1]][cnv_4[0]]+=damage_tank[type_tank[i]%sl_tank]
                    if td_bg[cnv_4[1]][cnv_4[0]]>=8:td_bg[cnv_4[1]][cnv_4[0]]=0
                return True
    return False  
def boom():
    for b_i in range(len(xyt_boom)):
        if b_i>=len(xyt_boom):break
        if xyt_boom[b_i][2]==tg[0]:del(xyt_boom[b_i])
        if b_i>=len(xyt_boom):break
        b_1=xyt_boom[b_i][2]-tg[0]
        if 0<b_1<=10:   
            if b_1%2:b_1+=1
            surf_bg.blit(bapu[1][5-b_1//2],(xyt_boom[b_i][0]-40,xyt_boom[b_i][1]-40))
def tao_vp():
    while kt_vp() or chuong_ngai_vat(ma_vp,0,0):
        x[ma_vp]=[5*random.randint(4,156)]
        y[ma_vp]=[5*random.randint(4,116)]
    vp_random()
def hinh_vp():
    hvp_1=tg_het_vp[1]-tg[1]
    if hvp_1<0:hvp_1+=60
    if 2<=hvp_1<=4:hvp_5=True
    else:
        hvp_2=60-tg_het_vp[0]
        hvp_3=(tg[0]+hvp_2)%60
        if hvp_3<40:hvp_4=8
        else: hvp_4=4
        if hvp_1==5:hvp_4=12-hvp_4
        if (hvp_3%hvp_4)<(hvp_4//2):hvp_5=True
        else: hvp_5=False
    if hvp_5 or pause:
        hvp_6,hvp_7=x[ma_vp][0]-20,y[ma_vp][0]-20
        surf_bg.blit(bapu[3][vp_rd],(hvp_6,hvp_7))    
def kt_vp():
    ktvp_1=check_vp()
    ktvp_2=(abs(x[ma_vp][0]-x[sl_loai_tank][0])<40) and (abs(y[ma_vp][0]-y[sl_loai_tank][0])<40)
    return ktvp_1 or ktvp_2
def check_vp():
    for cvp_i in range(sl_player):
        cvp=abs(x[ma_vp][0]-x[cvp_i][0])<40 and abs(y[ma_vp][0]-y[cvp_i][0])<40
        if cvp: return True
    return False
def vp_random():
    global vp_rd 
    if tt_vp.count(True)>0:
        while tt_vp[vp_rd]==False:
            vp_rd=random.randint(0,sl_vp-1)
        return True
    return False
def hinh_thanh_boss():
    surf_tb.fill(den)
    pygame.draw.polygon(surf_tb,do,thanh_boss)
    if mctm[0]==0:
        mctm[0]=400/sl_mang_boss_mh
        mctm[1]=2*(200-thanh_boss[5][0]+thanh_boss[0][0])/sl_mang_boss_mh  
    else:
        thanh_boss[1][0]=thanh_boss[0][0]+mctm[0]*sl_mang_boss_mh
        thanh_boss[4][0]=thanh_boss[5][0]+mctm[1]*sl_mang_boss_mh
        pygame.draw.polygon(surf_tb,den,thanh_boss[1:5])
    pygame.draw.polygon(surf_tb,xam,thanh_boss,5)
    screen.blit(surf_tb,(xwindow//2-210,650*(min(level,6)//6))) 
def thanh_mt_tank():
    global tmt_7,tmt_8
    surf_mt.fill(den)
    for tmt_i in range(sl_player,sl_loai_tank):
        tmt_co,tmt_1=[xam,do],[pygame.Rect(0,50*(tmt_i-sl_player),90,40),(0,0)]
        if tmt_i>tmt_8>0:tmt_1[0][1]+=120
        tmt_1[1]=tmt_1[0][0],tmt_1[0][1]
        tmt_2=tmt_1[0].collidepoint((xy_m[0]-905,xy_m[1]-50))
        if tmt_2:
            tmt_co[0]=trang  
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:tmt_7=True
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    if event.button==1 and tmt_7:
                        if tmt_8!=tmt_i:tmt_8=tmt_i
                        else:tmt_8=0
                tmt_7=False        
        tmt_1[0]=pygame.Surface((tmt_1[0][2],tmt_1[0][3]))
        tmt_1[0].fill(tmt_co[0])
        pygame.draw.rect(tmt_1[0],nau_dat,(5,5,80,30))
        tmt_1[0].blit(tank_mt[tmt_i],(50,5))
        tmt_txt1=font_mt[0].render(str(sl_tank_mt[tmt_i]),True,tmt_co[0])
        tmt_1[0].blit(tmt_txt1,(45-tmt_txt1.get_width(),5))
        surf_mt.blit(tmt_1[0],tmt_1[1])
    if tmt_8!=0:
        tmt_3=type_tank[tmt_8]%sl_tank
        tmt_4=50*(tmt_8-sl_player+1)
        for tmt_j in range(3):
            tmt_5=bapu[2][tmt_j+1]
            if   tmt_j==0:tmt_6=mang[tmt_3]
            elif tmt_j==1:tmt_6,tmt_co[1]=round(damage_tank[tmt_3],1),[195,195,195]
            else:
                tmt_6,tmt_co[1]=td_tank[tmt_3],[59,59,59]
                if tmt_6 <0:tmt_6=round(-1/tmt_6,1)
            surf_mt.blit(tmt_5,(55,tmt_4+30*tmt_j+10))  
            tmt_txt2=font_mt[1].render(str(tmt_6),True,tmt_co[1])
            surf_mt.blit(tmt_txt2,(50-tmt_txt2.get_width(),tmt_4+30*tmt_j+10))
        pygame.draw.rect(surf_mt,trang,(0,tmt_4,90,110),5)
    screen.blit(surf_mt,(xwindow-95,50))     
def player_infor():
    surf_pl.fill(den)
    for pi_i in range(sl_player):
        if ((x[pi_i][0]+y[pi_i][0])//5)%8<4:pi_1=0
        else:pi_1=1
        pi_2=180*pi_i
        pygame.draw.rect(surf_pl,xam,(0,180*pi_i,90,160))
        pygame.draw.rect(surf_pl,nen_avatar[pi_i],(5,5+pi_2,80,80))
        surf_pl.blit(tank_mt[pi_i][2*h[pi_i][0]+pi_1],(10,10+pi_2))
        for pi_j in range(2):
            pi_3=90+35*pi_j
            if pi_j==0:
                pi_4,pi_5=mang_mh[pi_i][0],do
                if pi_4!=int(pi_4):pi_4+=1
                pi_4=int(pi_4)
            else:pi_4,pi_5=sl_dan_mh[pi_i],cam 
            pygame.draw.rect(surf_pl,den,(5,pi_3+pi_2,80,30))
            surf_pl.blit(bapu[2][1-pi_j],(10,pi_3+pi_2))
            pi_txt1=font_cs.render(str(pi_4),True,pi_5)
            surf_pl.blit(pi_txt1,(80-pi_txt1.get_width(),pi_3+pi_2))
        nen_avatar[pi_i]=nau_dat
    screen.blit(surf_pl,(5,50))    
def end_game():
    global play,kq
    for eg_i in range(sl_player):
        if mang_mh[eg_i][0]<=0 :return True
    eg_1=sl_mang_boss_mh<1
    eg_2=sum(sl_tank_mt)-sl_tank_mt[0]==0
    if eg_1 or eg_2 :#or eg_3:
        if (eg_1 and level<6) or eg_2:
            kq=True
        return True
    return False
def tuong_tac_mh():
    global play,pause,level,ttm_5
    ttm_1=ywindow//2-70
    ttm_2=td_chi_so[3]
    if pause:ttm_txt=txt[0]
    elif kq:ttm_txt=txt[2]
    else:ttm_txt=txt[1]
    surf_bg.blit(ttm_txt,(280,ttm_1-160))  
    for ttm_i in range(3):
        if ttm_i!=1 or kq or (not end_game()): 
            ttm_2=td_chi_so[3]+ttm_i*130
            if (not kq) and end_game():ttm_2-=30*ttm_i-30
            surf_bg.blit(menu[ttm_i],(ttm_2,ttm_1))
            ttm_3=pygame.Rect(ttm_2,ttm_1,100,100)
            ttm_4=ttm_3.collidepoint([xy_m[0]-100,xy_m[1]-50])
            if ttm_4:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1: ttm_5 =True
                else:
                    if event.type==pygame.MOUSEBUTTONUP:
                        if event.button==1 and ttm_5:
                            if   ttm_i==0:play=1
                            elif ttm_i==1:
                                if pause:pause=not pause
                                else:play=2
                            elif ttm_i==2:
                                play=2
                                if kq:level-=1
                    ttm_5=False          
                pygame.draw.rect(surf_bg,trang,ttm_3,5)
                surf_bg.blit(in_txt_menu[ttm_i],(ttm_2,ttm_1+110))
def tuong_tac_mh_level(a,b,w):
    global play,level
    for ttml_i in range(20):
        ttml_1=w+(a+w+10)*(ttml_i%5)
        ttml_2=w+(b+w+10)*(ttml_i//5)
        ttml_3=pygame.Rect(ttml_1,ttml_2,a+10,b+10)
        ttml_4=ttml_3.collidepoint([xy_m[0]-100,xy_m[1]-50])
        pygame.draw.rect(surf_bg,do,ttml_3)
        ttml_5=xam
        if  ttml_4:
            ttml_5=trang
            if event.type==pygame.MOUSEBUTTONDOWN:    
                if event.button==1 and ttml_i<max_level:
                    play,level=2,ttml_i+1
        pygame.draw.rect(surf_bg,ttml_5,ttml_3,5)            
def set_up_map():
    for i in range(0,600,20):
        for j in range(0,800,20):
            if level<6:
                if (340<=j<460) and (i<80):
                    if (not 380<= j<420) or (40<=i<80):td_bg[i//20][j//20]=3
            else:
                if (340<=j<460) and (i>=520):
                    if (not 380<= j<420) or (520<=i<560):td_bg[i//20][j//20]=3
            if   td_bg[i//20][j//20]==3:td_bg[i//20][j//20]=4
            elif td_bg[i//20][j//20]==4:td_bg[i//20][j//20]=3 
    if level>5: 
        y[sl_loai_tank]=[580]
        thanh_boss[0][1]=thanh_boss[1][1]=thanh_boss[2][1]=40
        thanh_boss[3][1]=thanh_boss[4][1]=thanh_boss[5][1]=10
icon=pygame.image.load(r"Image/Tank_icon.ico")
pygame.display.set_caption("Tank")
pygame.display.set_icon(icon)
im_tank=cv2.imread(r"Image/Tank.png")
im_menu=cv2.imread(r"Image/Menu.png")
im_bapu=cv2.imread(r"Image/Block_and_powerup.png")
im_txt=cv2.imread(r"Image/Text.png")
tank=load_anh(im_tank,6,18,40,40,[nau_dat]).copy()
menu=load_anh(im_menu,1,3,100,100,[]).copy()
bapu=load_anh(im_bapu,4,6,40,40,[trang,nau_dat]).copy()
txt=load_anh(im_txt,3,1,140,240,[trang]).copy()
bullet=[pygame.image.load(r"Image/bullet.png")]
for i in range(3):bullet.append(pygame.transform.rotate(bullet[i],-90))
for i in range(5):
    bapu[1][i]=pygame.transform.scale2x(bapu[1][i])
    if i==4:break
    bapu[0][i]=pygame.transform.scale(bapu[0][i],(20,20))   
ds_phim=[[pygame.K_w ,pygame.K_d    ,pygame.K_s   ,pygame.K_a   ,pygame.K_RETURN],
         [pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT,pygame.K_SPACE ]]
font_cs=pygame.font.Font(None,50)
font_mt=[pygame.font.Font(None,50),
         pygame.font.Font(None,40)]
font_eg=pygame.font.Font(None,100)
font_mh=pygame.font.Font(None,50)
in_txt_eg=[font_eg.render("Pause",True,xam),
           font_eg.render("Lose",True,xam),
           font_eg.render("Win",True,xam)]
in_txt_menu=[font_mh.render("Menu",True,xam),
             font_mh.render("Continue",True,xam),
             font_mh.render("Return",True,xam)]
surf_bg=pygame.Surface((800,600))
surf_tb=pygame.Surface((420,50))
surf_pl=pygame.Surface((90,340))
surf_mt=pygame.Surface((90,510))
sl_tank=len(tank)//2
running=True
play=0
max_level=7
type_tank=[0]
sl_player=1
while running:
    xy_m=pygame.mouse.get_pos()
    move=pygame.key.get_pressed()
    if play!=2:
        screen.fill(nau_dat)
        surf_bg.fill(nau_dat)
        if play==1 or play==3:
            pygame.draw.rect(screen,den,(0,0,xwindow,ywindow),50)
            pygame.draw.rect(screen,den,(xwindow-100,0,50,ywindow))
            pygame.draw.rect(screen,den,(50,0,50,ywindow))
    if   play==0:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:running=False
                if event.key==pygame.K_a:type_tank[0]=0
                if event.key==pygame.K_b:type_tank[0]=1
                if event.key==pygame.K_c:type_tank[0]=2
                if sl_player==2:
                    if event.key==pygame.K_d:type_tank[1]=0
                    if event.key==pygame.K_e:type_tank[1]=1
                    if event.key==pygame.K_f:type_tank[1]=2    
                if event.key==pygame.K_1 and sl_player==2:
                    sl_player=1
                    del(type_tank[1])
                if event.key==pygame.K_2 and sl_player==1:
                    sl_player=2
                    if len(type_tank)<2:type_tank.append(0)
                    type_tank[1]=0
                if event.key==pygame.K_p:play=1
    elif play==1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:running=False
                if event.key==pygame.K_r:play=0    
        tuong_tac_mh_level(120,70,20)        
    elif play==2:
        mctm=[0,0]
        type_tank=[i for i in type_tank[0:sl_player]]
        nen_avatar=[nau_dat for i in range(sl_player)]
        kieu_choi=1
        f_map=open(r"Text\map.txt","r")
        td_bg=[]
        fline=f_map.readline()
        while fline!=str(level)+"\n":
            fline=f_map.readline()
        fline=f_map.readline()  
        while fline!="\n" and fline!="":
            td_bg.append(list(map(int,fline.split())))
            fline=f_map.readline()
        f_map.close()
        f_infor=open(r"Text\Information_tank.txt","r")
        f_infor.readline()
        f_infor.readline()
        td_tank=[]
        damage_tank=[]
        mang=[]
        xyt_boom=[]
        for i in range(3):
            f_line=list(map(int,f_infor.readline().split("|")))
            mang.append(f_line[1])
            damage_tank.append(f_line[2])
            td_tank.append(f_line[3])
            if damage_tank[i]<0:damage_tank[i]=-1/damage_tank[i]
        f_infor.close()
        sl_tank_mh,sl_tank_mt,tank_mt=[],[],[]
        for i in range(sl_player):
            sl_tank_mh.append(1)
            sl_tank_mt.append(5)
            tank_mt.append([])
            for j in tank[type_tank[i]][i*9:i*9+8]:
                tank_mt[i].append(pygame.transform.scale(j,(70,70)))
        f_infor=open(r"Text\Information_level.txt","r")
        f_infor.readline()
        f_infor.readline()
        fline=list(map(int,f_infor.readline().split("|")))
        
        while fline[0]!=level:
            fline=list(map(int,f_infor.readline().split("|")))
            
        sl_mang_boss=sl_mang_boss_mh=fline[1]
        sl_vp=fline[2]
        M_sl_tank=[]
        for i in range(sl_tank):
            if fline[3*i+5]!=0:
                sl_tank_mh.append(fline[3*i+3])
                M_sl_tank.append(fline[3*i+4])
                sl_tank_mt.append(fline[3*i+5])
                type_tank.append(i+3)
                tank_mt.append(pygame.transform.scale(tank[i+3][8],(30,30)))       
        f_infor.close()
        for i in range(2):sl_tank_mh.append(1)
        sl_loai_tank=len(type_tank)
        x,y,x_d,y_d,h,kho_dan,x_dan,y_dan,hx_dan,hy_dan,tg_chet,mang_mh=[],[],[],[],[],[],[],[],[],[],[],[]
        sl_dan=sum(M_sl_tank)
        ma_huy_bot=0
        tt_vp=[True for i in range(sl_vp)]
        vp_mh=False
        for i in range(sl_loai_tank+2):
            x.append([])
            y.append([])
            h.append([]) 
            if i<sl_loai_tank:
                x_dan.append([])
                y_dan.append([])
                hx_dan.append([])
                hy_dan.append([])
                kho_dan.append([])
                tg_chet.append([])
                mang_mh.append([])
                if i<sl_player:end_j=sl_dan
                else:end_j=sl_tank_mh[i]
                for j in range(end_j):
                    add_or_del_tank(i,j,1)
        td_chi_so=[167+(30*5)//2,
                   167+(15*sl_dan)//2,
                   845,
                   xwindow//2-280]
        thanh_boss=[[10,10],[0,10],[410,10],[392,40],[0,40],[28,40]]
        ma_vp=sl_loai_tank+1
        x[sl_loai_tank],y[sl_loai_tank]=[xwindow//2-100],[20]
        set_up_map()   
        for i in range(sl_loai_tank):
            for j in range(sl_tank_mh[i]):
                tao_tank(i,j) 
        x[ma_vp],y[ma_vp]=x[0],y[0]
        vp_rd=random.randint(0,sl_vp-1)
        tao_vp()     
        tg_vp=[0,5]
        tg_het_vp=[0,10]
        tg_vp2=[-1,-1] 
        pause=True
        kq=False
        tg=[0,0,0,0]
        play=3
        tmt_8=0
    elif play==3:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_t:surf_bg.blit(tank_mt[1][0],(0,0))
                if event.key==pygame.K_p:
                    if not end_game():pause=not pause
                    if kq:play=2
                if pause or end_game():
                    if event.key==pygame.K_q:running=False
                    if event.key==pygame.K_m:play=1
                    if event.key==pygame.K_r:
                        play=2
                        if kq:level-=1
                    if event.key==pygame.K_c:kieu_choi=1-kieu_choi
                else:
                    for i in range(sl_player):
                        if sl_player==1:j=kieu_choi
                        else:j=1-i
                        if event.key==ds_phim[j][4]:
                            kich_hoat_dan(i)
        if not pause :
            if tg[0]!=-1:tg[0]+=1
            for i in range(3):
                if tg[i]==60:
                    tg[i]=0
                    tg[i+1]+=1
                    if tg[1]%5==i==0:
                        for j in range(sl_player,sl_loai_tank):
                            if sl_tank_mh[j]<M_sl_tank[j-sl_player]<sl_tank_mt[j]:
                                add_or_del_tank(j,0,1)
                                tao_tank(j,sl_tank_mh[j])
                                tg_chet[j][sl_tank_mh[j]]=tg[:2]
                                sl_tank_mh[j]+=1
            if  tg_vp[0]==tg[0]and tg_vp[1]==tg[1]:
                if tt_vp.count(True)>0:
                    x[ma_vp]=[5*random.randint(4,180)]
                    y[ma_vp]=[5*random.randint(4,108)]
                    vp_rd=random.randint(0,sl_vp-1)
                    tao_vp()
                    vp_mh=True
                tg_vp=[tg[0],(tg[1]+10)%60]
                tg_het_vp=[tg[0],(tg[1]+5)%60]
            if tg_het_vp[0]==tg[0]and tg_het_vp[1]==tg[1]:
                vp_mh=False
            if sl_vp>2: 
                if tg_vp2[0]==tg[0] and tg_vp2[1]==tg[1]:
                    tt_vp[2]=True
            for i in range(sl_loai_tank):
                for j in range(sl_tank_mh[i]):
                    if (tg_chet[i][j][1]+1)%60==tg[1] and (tg_chet[i][j][0]==tg[0])and tg_chet[i][j][0]!=-1:
                        tg_chet[i][j]=[-1,-1]
            for i in range(sl_loai_tank):
                for j in range(sl_tank_mh[i]):
                    if i<sl_player and (not kq):
                        kt=False
                        mt_test=""
                        if sl_player==1:k=kieu_choi
                        else:k=i
                        if move[ds_phim[k][0]]:
                            kt,h[i][0]=True,0
                            mt_test+=str(0)
                        if move[ds_phim[k][1]]:
                            kt,h[i][0]=True,1
                            mt_test+=str(1)
                        if move[ds_phim[k][2]]:
                            kt,h[i][0]=True,2
                            mt_test+=str(2)
                        if move[ds_phim[k][3]]:
                            kt,h[i][0]=True,3
                            mt_test+=str(3)
                        if kt:toc_do(i,0,0)
                    elif tg_chet[i][j][0]==-1 and not(end_game()) :
                        if sl_vp>2:
                            if not tt_vp[2]:break
                        toc_do(i,j,0)
            for i in range(sl_loai_tank):
                for j in range(len(kho_dan[i])):
                    if i>=sl_player:
                        if j>sl_tank_mh[i]-1:break
                    for k in range(2):
                        if kho_dan[i][j]:
                            x_dan[i][j]+=hx_dan[i][j]
                            y_dan[i][j]+=hy_dan[i][j]
                            if va_cham_dan(i,j):
                                trung_dan,loai_dan,stt_dan=tuong_tac_dan_dan(i,j)
                                trung_tank,loai_tank,stt_tank=tuong_tac_xe_dan(i,j)
                                t=chuong_ngai_vat(i,j,1) 
                                if trung_dan:
                                    reset_dan(loai_dan,stt_dan)
                                    t=True
                                if trung_tank:
                                    if loai_tank<sl_loai_tank:
                                        mang_mh[loai_tank][stt_tank]-=damage_tank[type_tank[i]%sl_tank]
                                        if (tg_chet[loai_tank][stt_tank][0]==-1 and loai_tank<sl_player) or mang_mh[loai_tank][stt_tank]<=0:
                                            kt,tg_chet[loai_tank][stt_tank]=True,tg[:2]
                                        else:kt=False    
                                        if loai_tank<sl_player:
                                            nen_avatar[loai_tank]=do
                                            if kt:
                                                t=True
                                                x_d.append(x[loai_tank][0])
                                                y_d.append(y[loai_tank][0])
                                                x[loai_tank],y[loai_tank]=[xwindow//2-80*(sl_player-2*loai_tank)-20],[500]
                                            else:mang_mh[loai_tank][0]+=damage_tank[type_tank[i]%sl_tank]    
                                        else:        
                                            if mang_mh[loai_tank][stt_tank]<=0:
                                                t=True
                                                x_d.append(x[loai_tank][stt_tank])
                                                y_d.append(y[loai_tank][stt_tank])
                                                sl_tank_mt[loai_tank]-=1
                                                if sl_tank_mh[loai_tank]>sl_tank_mt[loai_tank]:
                                                    add_or_del_tank(loai_tank,stt_tank,-1)
                                                else:    
                                                    add_or_del_tank(loai_tank,stt_tank,0)
                                    else:
                                        if (i<sl_player)!=(level>5):
                                            sl_mang_boss_mh-=damage_tank[type_tank[i]%sl_tank]
                                if t:xyt_boom.append([x_dan[i][j],y_dan[i][j],(tg[0]+10)%60])            
                                if i<sl_player or j<sl_tank_mh[i]:
                                    reset_dan(i,j)
                                break
            if vp_mh and vp_random() and not end_game():
                if check_vp() and tt_vp[vp_rd]:
                    i=0
                    if sl_player==2:
                        if abs(x[ma_vp][0]-x[1][0])<40:i=1
                    vp_mh=False
                    if vp_rd==0:  mang_mh[i][0]+=1
                    elif vp_rd==1:them_dan(i)
                    elif vp_rd==2:
                        tt_vp[2]=False
                        tg_vp2=[tg[0],(tg[1]+15)%60]    
                    vp_rd=random.randint(0,sl_vp-1)
                    tao_vp()
                    tg_vp=[tg[0],(tg[1]+10)%60]                    
        boom()
        if vp_mh:hinh_vp() 
        for i in range(0,len(td_bg)):
            for j in range(0,len(td_bg[0])):
                if td_bg[i][j]==2:surf_bg.blit(bapu[0][1],(j*20,i*20))
        for i in range(sl_loai_tank):
            for j in range(len(kho_dan[i])):
                if kho_dan[i][j]:hinh_dan(i,j)
                if i>=sl_player or j==0:
                    if end_game():
                        if (i<sl_player) != kq :continue
                    hinh_tank(i,j)
                    
        
        for i in range(0,len(td_bg)):
            for j in range(0,len(td_bg[0])):
                if   td_bg[i][j]==1:surf_bg.blit(bapu[0][0],(j*20,i*20))
                elif td_bg[i][j]==3:surf_bg.blit(bapu[0][3],(j*20,i*20))
                elif td_bg[i][j] >3:surf_bg.blit(bapu[0][2],(j*20,i*20))       
        thanh_mt_tank()
        if not end_game() or (sl_mang_boss_mh>0):
            hinh_thanh_boss()
            surf_bg.blit(bapu[0][4+min(level,6)//6],(x[sl_loai_tank][0]-20,y[sl_loai_tank][0]-20))
        sl_dan_mh=[kho_dan[i].count(False) for i in range(sl_player)]
        player_infor()
        if pause or end_game():tuong_tac_mh()
        if kq and tg[0]!=-1:
            if level==max_level:max_level+=1
            level+=1
            tg[0]=-1
    if play!=2:screen.blit(surf_bg,(100,50))    
    pygame.display.update()
    clock.tick(60)    
pygame.quit()
