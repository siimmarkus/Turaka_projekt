
import pygame
import math
import time
from random import choice, shuffle, seed


#-------------------------------------------------SEADED--------------------------------------------------------------------------------

laius = 1440
kõrgus = int(laius/1.6)
skaala = laius*(0.22/1440)
teksti1_x,teksti1_y = int(laius-kõrgus/1.9), int(kõrgus/1.9)
teksti2_x,teksti2_y = int(laius-kõrgus/1.9), int(kõrgus/1.7)
teksti_suurus = int(laius * 63/1440)
teksti_font = 'Bauhaus 93'
teksti_font = 'Arial'
seed(1)

#Juhuks kui tahan kaartide pilte vahetata, peab uued dimensioonid kirja panema (pikslites)
pildi_laius,pildi_kõrgus = 691, 1056

#-------------------------------------------MUUTUJAD ARVUTILE----------------------------------------------------------------------------

p = pygame
mastid = {'H':'Ärtu','S':'Poti','D':'Ruutu','C':'Risti'}
numbrid = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
väärtused = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
trump = choice(['H','S','D','C'])

clock = pygame.time.Clock()
#clock.tick(60)
#Pildid
skaleeritud_laius = int(round(pildi_laius*skaala)) 
skaleeritud_kõrgus = int(round(pildi_kõrgus*skaala))

taust = pygame.image.load('laua_taust.png')
taust = pygame.transform.scale(taust, (laius, kõrgus+100))

kaardi_tagakülg = pygame.image.load('PNG/gray_back.png')
kaardi_tagakülg = pygame.transform.scale(kaardi_tagakülg, (skaleeritud_laius, skaleeritud_kõrgus))
kaardi_tagakülg_külili = pygame.transform.rotate(kaardi_tagakülg, 90)

infokast = pygame.image.load('infokast2.png')
infokast_laius,infokast_kõrgus = int(laius*500/1440),int(laius*500/1440)
infokast = pygame.transform.scale(infokast, (infokast_laius,infokast_kõrgus))

trumpi_pilt = pygame.image.load('PNG/{}.png'.format(trump))
trumpi_pilt_laius = trumpi_pilt_kõrgus = int(laius*(60/1700))
trumpi_pilt = pygame.transform.scale(trumpi_pilt, (trumpi_pilt_laius,trumpi_pilt_kõrgus))

kaardipakk = []
käsi1 = []
käsi2 = []
kaardid_laual = []
tapvad_kaardid = []
näita_kaarte = 1
käigu_seis = 0
käigu_seisud = {0:'Mäng algab', 1:'Mina käin', 2:'Vastane tapab', 3:'Vastane käib', 4:'Mina tapan'}
trump_kaart = 0
sõnumi_timer = 0


#-------------------------------------------KLASSID--------------------------------------------------------------------------------

class Kaart(object):
    def __init__(self,mast,number):
        self.nimi = '{} {}'.format(mastid[mast], number)
        self.mast = mast
        self.number = number
        self.faili_nimi = 'PNG/' + number + mast +'.png'
        if mast == trump:
            self.väärtus = väärtused[number]+20
        else:
            self.väärtus = väärtused[number]
        self.pilt = pygame.image.load(self.faili_nimi)
        self.pilt = pygame.transform.scale(self.pilt, (skaleeritud_laius, skaleeritud_kõrgus))
        self.nurga_x = 0
        self.nurga_y = 0
        self.tapetud = False

#-------------------------------------------FUNKTSIOONID--------------------------------------------------------------------------------


# loob ja segab kaardipaki
def loo_kaardipakk():
    global kaardipakk
    for i in mastid:
        for j in numbrid:
            kaardipakk.append(Kaart(i,j))
    shuffle(kaardipakk)
    for i in range(len(kaardipakk)):
        if kaardipakk[i].mast == trump:
            kaardipakk.insert(0,kaardipakk.pop(i))
            break
    return kaardipakk

# Käsi1 ja käsi2 korjavad kaarte, kuni neil on käes vähemalt kuus
def võta_kaarte(esimesena='arvuti'):
    global käsi1, käsi2, kaardipakk, trump_kaart
    if esimesena == 'mängija':
        while len(käsi1)<6 and len(kaardipakk)>0:
                käsi1.append(kaardipakk.pop())
        while len(käsi2)<6 and len(kaardipakk)>0:
                käsi2.append(kaardipakk.pop())
    else:
        while len(käsi2)<6 and len(kaardipakk)>0:
                käsi2.append(kaardipakk.pop())
        while len(käsi1)<6 and len(kaardipakk)>0:
                käsi1.append(kaardipakk.pop())

    käsi1 = trumbid_lõppu(käsi1)
    käsi2 = trumbid_lõppu(käsi2)
    määra_nurk(käsi1,'käsi')
    määra_nurk(käsi2,'vastase käsi')
    

# Annab kaardi objektile ülemise vasaku nurga koordinaadid
def määra_nurk(kaardid, tüüp):
    global kaardi_vasak_nurk_x
    if tüüp == 'käsi':
        if len(kaardid)<=6:
            kaardi_vasak_nurk_x = skaleeritud_laius
        else:
            kaardi_vasak_nurk_x = (6*skaleeritud_laius - skaleeritud_laius)/len(kaardid)
        for i in range(len(kaardid)):
            kaardid[i].nurga_x = i*kaardi_vasak_nurk_x
            kaardid[i].nurga_y = kõrgus-skaleeritud_kõrgus
    
    elif tüüp == 'laual':
        for i in range(len(kaardid)):
            kaardid[i].nurga_x = i*skaleeritud_laius
            kaardid[i].nurga_y = skaleeritud_kõrgus*1.1
    
    elif tüüp == 'tapvad':
        for i in range(len(kaardid)):
            kaardid[i].nurga_x = i*skaleeritud_laius
            kaardid[i].nurga_y = skaleeritud_kõrgus*1.1 + kõrgus*0.1
    
    elif tüüp == 'vastase käsi':
        if len(kaardid)<=6:
            kaardi_vasak_nurk_x = skaleeritud_laius
        else:
            kaardi_vasak_nurk_x = (6*skaleeritud_laius - skaleeritud_laius)/len(kaardid)
        for i in range(len(kaardid)):
            kaardid[i].nurga_x = i*kaardi_vasak_nurk_x
            kaardid[i].nurga_y = 0
    
    return kaardid


# Returnib duple ((xmin, x-max),(y-min, y-max))
def kaardi_mõõtmed(kaart):
    ülemine_vasak = (kaart.nurga_x,kaart.nurga_y)
    alumine_parem = (kaart.nurga_x+skaleeritud_laius,kaart.nurga_y+skaleeritud_kõrgus)
    return((ülemine_vasak[0],alumine_parem[0]),(ülemine_vasak[1],alumine_parem[1]))

# Joonistab kaardid lauale
def joonista():
    for i in range(len(käsi2)):
        if näita_kaarte % 2 == 0:
            ekraani_pind.blit(käsi2[i].pilt, (käsi2[i].nurga_x, käsi2[i].nurga_y))
        else:
            ekraani_pind.blit(kaardi_tagakülg, (käsi2[i].nurga_x, käsi2[i].nurga_y))    
    for i in range(len(kaardid_laual)):
        ekraani_pind.blit(kaardid_laual[i].pilt, (kaardid_laual[i].nurga_x, kaardid_laual[i].nurga_y))
    #Joonistab tapvad kaardid
    for i in range(len(tapvad_kaardid)):
        ekraani_pind.blit(tapvad_kaardid[i].pilt, (tapvad_kaardid[i].nurga_x, tapvad_kaardid[i].nurga_y))
    #Joonistab kaardid lauale, juhul kui mõni kaart on 'valitud', jätab selle joonistamata
    for i in range(len(käsi1)):
        ekraani_pind.blit(käsi1[i].pilt, (käsi1[i].nurga_x, käsi1[i].nurga_y))
    
    #Trump
    if len(kaardipakk)>0:
        ekraani_pind.blit(kaardipakk[0].pilt, (laius-skaleeritud_laius-(skaleeritud_kõrgus-skaleeritud_laius)/2, 0))
    
    #Kaardipakk
    for i in range(math.ceil(len(kaardipakk)/5)):
        ekraani_pind.blit(kaardi_tagakülg_külili, (laius-skaleeritud_kõrgus, i*1))
    
    #Infokast
    ekraani_pind.blit(infokast, (laius-(infokast_laius), kõrgus-(infokast_kõrgus)))
    
    #Tekst
    ekraani_pind.blit(tekstipind1,(teksti1_x,teksti1_y))
    ekraani_pind.blit(tekstipind2,(teksti2_x,teksti2_y))

    #Trumbi pilt
    ekraani_pind.blit(trumpi_pilt, (laius*0.954, kõrgus*0.465))

def trumbid_lõppu(käsi):
    käsi.sort(key=lambda x: x.väärtus, reverse=False)
    käsi.sort(key=lambda x: x.mast, reverse=False)
    tavalised = []
    trumbid = []
    for i in käsi:
        if i.mast == trump:
            trumbid.append(i)
        else:
            tavalised.append(i)
    käsi = tavalised + trumbid
    return käsi

def võta_trump_kaart():
    global kaardipakk, trump_kaart
    trump_kaart = kaardipakk[0]



#-------------------------------------------ALGAB MÄNGU KOOD--------------------------------------------------------------------------
loo_kaardipakk()
võta_trump_kaart()
võta_kaarte()
p.init()
infoObject = pygame.display.Info()
#kõrgus = infoObject.current_h
#laius = infoObject.current_w
ekraani_pind = pygame.display.set_mode((laius, kõrgus))
p.display.set_caption('TURAKAS')
pygame.font.init()
myfont = pygame.font.SysFont(teksti_font, teksti_suurus)
valitud = -1
sõnum = ''


# Mängu loop

mäng_käib = True
while mäng_käib:
    
    mx,my = p.mouse.get_pos()
    mxr,myr = p.mouse.get_rel()
    ekraani_pind.blit(taust,(0,0))
    event = p.event.poll()


    
    # Mängu lõpetamine klahvidega ESC või Q
    if event.type == pygame.QUIT:
        break
    elif event.type == p.KEYDOWN and event.key == pygame.K_ESCAPE:
        break
    elif event.type == p.KEYDOWN and event.key == p.K_q:
        break    
    if len(kaardipakk) == 0 and ( len(käsi1)==0 or len(käsi2)==0 ):
        if  len(käsi1)==0 and len(käsi2)==0:
            tekstipind1 = myfont.render('Jäite viiki!', False, (0,0,0))
        elif  len(käsi1)==0 and len(käsi2)!=0:
            tekstipind1 = myfont.render('Sina võtsid!', False, (0,0,0))
        elif  len(käsi1)!=0 and len(käsi2)==0:
            tekstipind1 = myfont.render('Vastane võitis!', False, (0,0,0))
        sõnum = ''
        näita_kaarte = 0
    else:
        tekstipind1 = myfont.render(käigu_seisud[käigu_seis], False, (0,0,0))
        tekstipind2 = myfont.render(sõnum, False, (0,0,0))

    if sõnumi_timer < time.time():
        sõnum = ''

#---------------------------------------------CHEATS--------------------------------------------------------------------------
    if event.type == p.KEYDOWN and event.key == p.K_n:
        näita_kaarte += 1
    elif event.type == p.KEYDOWN and event.key == p.K_w:
        käsi1 = []
        kaardipakk = []
        trump_kaart = 0
        continue

#-------------------------------------------MÄNG ALGAB--------------------------------------------------------------------------

    if käigu_seis == 0:
        võta_kaarte('mängija')
        käigu_seis = 1

#-------------------------------------------MINU KÄIMINE--------------------------------------------------------------------------

    # Mina pean kaardi käima
    if käigu_seis == 1:
        if pygame.mouse.get_pressed()[0]:
            while True:
                mx,my = p.mouse.get_pos()
                mxr,myr = p.mouse.get_rel()
                ekraani_pind.blit(taust,(0,0))
                # Valib hiirevajutusel käest õige kaardi, kontrollides, kas kursor on mõne käesoleva kaardi hitboxis
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(käsi1)):
                        vahemik = kaardi_mõõtmed(käsi1[i])
                        if vahemik[0][0] <= mx <= vahemik[0][1] and vahemik[1][0] <= my <= vahemik[1][1]:
                            valitud = i
                            #Salvestab valitud kaardi algse asukoha, juhuks kui sellega ei ole võimalik käia
                            algne_nurga_x = käsi1[valitud].nurga_x
                            algne_nurga_y = käsi1[valitud].nurga_y

                # Kaardi 'lahti laskmisel' kontrollib, kas on võimalik tappa
                elif  valitud != -1 and event.type == pygame.MOUSEBUTTONUP:
                    #Tingimused tapmiseks #1-Kursor mõne kaardi kohal ja see kaart on tapmata; #2-Sama mast või trump; #3-Suurem väärtus
                    tingimus_1 = vahemik[0][0] <= mx <= vahemik[0][1] and vahemik[1][0] <= my <= vahemik[1][1]
                    

                    #Tingimused juurde käimiseks (Kaardi väärtuse kontrollimine)
                    tingimus_3 = len(kaardid_laual) > 0 and (kaardid_laual[0].väärtus == käsi1[valitud].väärtus  or kaardid_laual[0].väärtus - 20 == käsi1[valitud].väärtus or kaardid_laual[0].väärtus + 20 == käsi1[valitud].väärtus)

                    tingimus_4 = my < 2*kõrgus/3
                    
                    # Kaardi lauale asetamine
                    if tingimus_4 and len(kaardid_laual) == 0:
                        kaardid_laual.append(käsi1.pop(käsi1.index(käsi1[valitud])))
                        määra_nurk(kaardid_laual,'laual')
                        valitud = -1
                    
                    # Juurde käimine
                    elif len(kaardid_laual) > 0 and tingimus_3 and tingimus_4:
                        kaardid_laual.append(käsi1.pop(käsi1.index(käsi1[valitud])))
                        valitud = -1
                        määra_nurk(kaardid_laual,'laual')

                    # Kaart läheb kätte oma kohale tagasi
                    elif valitud != -1:
                        käsi1[valitud].nurga_x  = algne_nurga_x
                        käsi1[valitud].nurga_y  = algne_nurga_y
                        valitud = -1
                    break

                #Muudab valitud kaardi x- ja y-koordinaate
                if valitud != -1 and pygame.mouse.get_pressed()[0]:
                    käsi1[valitud].nurga_x += mxr
                    käsi1[valitud].nurga_y += myr
                joonista()
                p.display.flip()
                event = p.event.poll()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(kaardid_laual) > 0:
            käigu_seis = 2
            event = p.event.poll()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(kaardid_laual) == 0:
            sõnum = 'Vali kaart!'
            sõnumi_timer = time.time()+3


#-------------------------------------------VASTASE TAPMINE--------------------------------------------------------------------------


    if käigu_seis == 2:
        for i in range(len(kaardid_laual)):
            tapmis_valik = 0
            #Arvuti vaatab mängulaual olavad kaardid üle ja tapab, kui self.tapetud = false
            if not kaardid_laual[i].tapetud:
                for j in range(len(käsi2)):
                    if (käsi2[j].mast == kaardid_laual[i].mast or käsi2[j].mast == trump) and käsi2[j].väärtus > kaardid_laual[i].väärtus:
                        if tapmis_valik == 0:
                            tapmis_valik = käsi2[j]
                        elif käsi2[j].väärtus < tapmis_valik.väärtus:
                            tapmis_valik = käsi2[j]
                if tapmis_valik != 0:
                    käsi2[käsi2.index(tapmis_valik)].nurga_x = kaardid_laual[i].nurga_x
                    käsi2[käsi2.index(tapmis_valik)].nurga_y = kõrgus*0.1
                    tapvad_kaardid.append(käsi2.pop(käsi2.index(tapmis_valik)))
                    kaardid_laual[i].tapetud = True
                    määra_nurk(tapvad_kaardid,'tapvad')
                else:
                    time.sleep(0.5)
                    käsi2 = käsi2 + kaardid_laual + tapvad_kaardid
                    määra_nurk(käsi2,'vastase käsi')
                    kaardid_laual = []
                    tapvad_kaardid = []
                    sõnum = 'Vastane korjas'
                    sõnumi_timer = time.time()+3
                    käigu_seis = 0

                
        
        if pygame.mouse.get_pressed()[0]:
            while True:
                mx,my = p.mouse.get_pos()
                mxr,myr = p.mouse.get_rel()
                ekraani_pind.blit(taust,(0,0))
                # Valib hiirevajutusel käest õige kaardi, kontrollides, kas kursor on mõne käesoleva kaardi hitboxis
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(käsi1)):
                        vahemik = kaardi_mõõtmed(käsi1[i])
                        if vahemik[0][0] <= mx <= vahemik[0][1] and vahemik[1][0] <= my <= vahemik[1][1]:
                            valitud = i
                            #Salvestab valitud kaardi algse asukoha, juhuks kui sellega ei ole võimalik käia
                            algne_nurga_x = käsi1[valitud].nurga_x
                            algne_nurga_y = käsi1[valitud].nurga_y

                # Kaardi 'lahti laskmisel' kontrollib, kas on võimalik tappa
                elif  valitud != -1 and event.type == pygame.MOUSEBUTTONUP:

                    sobivad_väärtused = []
                    for i in kaardid_laual:
                        if i.väärtus not in sobivad_väärtused:
                            if i.mast == trump:
                                sobivad_väärtused.append(i.väärtus)
                                sobivad_väärtused.append(i.väärtus-20)
                            elif i.mast != trump:
                                sobivad_väärtused.append(i.väärtus)
                                sobivad_väärtused.append(i.väärtus+20)

                    for i in tapvad_kaardid:
                        if i.väärtus not in sobivad_väärtused:
                            if i.mast == trump:
                                sobivad_väärtused.append(i.väärtus)
                                sobivad_väärtused.append(i.väärtus-20)
                            elif i.mast != trump:
                                sobivad_väärtused.append(i.väärtus)
                                sobivad_väärtused.append(i.väärtus+20)

                    #Sobiv väärtus
                    tingimus_2 = käsi1[valitud].väärtus in sobivad_väärtused
                    #Hiir ekraani üleval osas
                    tingimus_4 = my < 2*kõrgus/3
                    #Vastasel on kaarte, laual < 6kaarti
                    tingimus_5 = len(käsi2)>0 and len(kaardid_laual)<6
                   
                    
                    # Juurde käimine
                    if tingimus_2 and tingimus_4 and tingimus_5 and valitud != -1:
                        kaardid_laual.append(käsi1.pop(käsi1.index(käsi1[valitud])))
                        valitud = -1
                        määra_nurk(kaardid_laual,'laual')
                    
                    # Kaart läheb kätte oma kohale tagasi
                    elif valitud != -1:
                        käsi1[valitud].nurga_x  = algne_nurga_x
                        käsi1[valitud].nurga_y  = algne_nurga_y
                        valitud = -1
                        sõnum = 'See kaart ei sobi'
                        sõnumi_timer = time.time()+3
                    break

                #Muudab valitud kaardi x- ja y-koordinaate
                if valitud != -1 and pygame.mouse.get_pressed()[0]:
                    käsi1[valitud].nurga_x += mxr
                    käsi1[valitud].nurga_y += myr
                joonista()
                p.display.flip()
                event = p.event.poll()

#-----------------------------LAUA TÜHJENDAMINE JA KAARTIDE JUURDE VÕTMINE--------------------------------------------------------------------------

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            käigu_seis = 3
            võta_kaarte()
            määra_nurk(käsi1, 'käsi')
            kaardid_laual = []
            tapvad_kaardid = []
            joonista()
            p.display.flip()
            event = p.event.poll()

#-------------------------------------------VASTASE KÄIMINE--------------------------------------------------------------------------


    if käigu_seis == 3:
        käidav = []
        for i in range(len(käsi2)):
            if len(käidav) == 0:
                käidav.append(i)
            elif käsi2[i].väärtus == käsi2[käidav[0]].väärtus:
                käidav.append(i)
            elif käsi2[i].väärtus < käsi2[käidav[0]].väärtus:
                käidav = [i]
                for j in range(len(käsi2)):
                    if j != i and käsi2[j].väärtus == käsi2[käidav[0]].väärtus:
                        käidav.append(j)
        
        for i in käidav[::-1]:
            kaardid_laual.append(käsi2.pop(i))
        määra_nurk(kaardid_laual,'laual')

        käigu_seis = 4

#-------------------------------------------MINU TAPMINE--------------------------------------------------------------------------
    if käigu_seis == 4:
        if pygame.mouse.get_pressed()[0]:
            while True:
                mx,my = p.mouse.get_pos()
                mxr,myr = p.mouse.get_rel()
                ekraani_pind.blit(taust,(0,0))
                # Valib hiirevajutusel käest õige kaardi, kontrollides, kas kursor on mõne käesoleva kaardi hitboxis
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(käsi1)):
                        vahemik = kaardi_mõõtmed(käsi1[i])
                        if vahemik[0][0] <= mx <= vahemik[0][1] and vahemik[1][0] <= my <= vahemik[1][1]:
                            valitud = i
                            #Salvestab valitud kaardi algse asukoha, juhuks kui sellega ei ole võimalik käia
                            algne_nurga_x = käsi1[valitud].nurga_x
                            algne_nurga_y = käsi1[valitud].nurga_y

                # Kaardi 'lahti laskmisel' kontrollib, kas on võimalik tappa
                elif  valitud != -1 and event.type == pygame.MOUSEBUTTONUP:
                    for i in range(len(kaardid_laual)):
                        

                        vahemik = kaardi_mõõtmed(kaardid_laual[i])
                        #Tingimused tapmiseks #1-Kursor mõne kaardi kohal ja see kaart on tapmata; #2-Sama mast või trump; #3-Suurem väärtus
                        tingimus_1 = vahemik[0][0] <= mx <= vahemik[0][1] and vahemik[1][0] <= my <= vahemik[1][1] and not kaardid_laual[i].tapetud
                        tingimus_2 = kaardid_laual[i].mast == käsi1[valitud].mast or käsi1[valitud].mast == trump
                        tingimus_3 = kaardid_laual[i].väärtus < käsi1[valitud].väärtus

                        #Tingimused juurde käimiseks
                        tingimus_4 = my < 2*kõrgus/3
                        tingimus_5 = kaardid_laual[i].väärtus == käsi1[valitud].väärtus  or kaardid_laual[i].väärtus - 20 == käsi1[valitud].väärtus or kaardid_laual[i].väärtus + 20 == käsi1[valitud].väärtus
                        tingimus_6 = (len(tapvad_kaardid) == 0)
                        tingimus_7 = len(käsi2)>len(kaardid_laual)

                        # Tapmine
                        if tingimus_1 and tingimus_2 and tingimus_3:
                            käsi1[valitud].nurga_x = skaleeritud_laius*i
                            käsi1[valitud].nurga_y = skaleeritud_laius*0.4
                            kaardid_laual[i].tapetud = True
                            tapvad_kaardid.append(käsi1.pop(käsi1.index(käsi1[valitud])))
                            määra_nurk(tapvad_kaardid,'tapvad')
                            valitud = -1
                        # Juurde käimine
                        elif not tingimus_1 and tingimus_4 and tingimus_5 and tingimus_6 and tingimus_7:
                            kaardid_laual.append(käsi1.pop(käsi1.index(käsi1[valitud])))
                            valitud = -1
                            määra_nurk(kaardid_laual,'laual')
                            käigu_seis = 2

                        # Kaart läheb kätte oma kohale tagasi
                        elif valitud != -1:
                            käsi1[valitud].nurga_x  = algne_nurga_x
                            käsi1[valitud].nurga_y  = algne_nurga_y
                            valitud = -1
                    break

                #Muudab valitud kaardi x- ja y-koordinaate
                if valitud != -1 and pygame.mouse.get_pressed()[0]:
                    käsi1[valitud].nurga_x += mxr
                    käsi1[valitud].nurga_y += myr
                joonista()
                p.display.flip()
                event = p.event.poll()
        
        #Tapmise lõpetamine/korjamine
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            #Kontrollib, kas mängija on kõik kaardid ära tapnud
            if len(tapvad_kaardid) == len(kaardid_laual):
                käigu_seis = 0
                kaardid_laual = []
                tapvad_kaardid = []
                event = p.event.poll()
                valitud = -1
            else:
                sõnum = 'Korjamiseks "K"'
                sõnumi_timer = time.time()+3        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
            käsi1 = käsi1 + kaardid_laual + tapvad_kaardid
            kaardid_laual = []
            tapvad_kaardid = []
            sõnum = 'Mina korjasin'
            sõnumi_timer = time.time()+3
            võta_kaarte()
            käigu_seis = 3
    
    joonista()
    p.display.flip()
     
p.quit()