import serial
import cv2
import numpy as np
import time
from PIL import ImageGrab
import os
#import win32gui
#import win32con

ser = serial.Serial('COM5', 9600)
ser.reset_input_buffer()

# accs = ['images/nick_1.jpg',
#         'images/nick_2.jpg',
#         'images/nick_3.jpg',
#         'images/nick_4.jpg',
#         'images/nick_5.jpg',
#         'images/nick_6.jpg']
spot_id = 0
spot_map_cord = [[531, 314, 595, 365], [1000, 580, 1070, 644], [974, 604, 1037, 672]]# [564, 387, 644, 464]]
spot_mark_cord = [[26, 21], [33, 41], [32, 34]]#[46, 41]] #31, 41, [31, 23]
map_close_cord = [1470, 203, 1555, 263]

#error_net = 760, 370, 960, 430, 'images/error_net.jpg'
error_net = 1120, 560, 1220, 620, 'images/no.jpg'
error_enter = 890, 550, 1023, 630, 'images/error_enter.jpg'
aa_b_play2 = 1180, 110, 1380, 175, 'images/aa_b_play2.jpg'
aa_b_play3 = 1180, 110, 1380, 175, 'images/aa_b_play3.jpg'
check_enter_ok = 755, 635, 933, 690, 'images/check_enter_ok.jpg'
connect = 820, 685, 1100, 744, 'images/connect.jpg'
disconnect = 820, 685, 1100, 744, 'images/disconnect.jpg'
aa_b_accept = 55, 635, 933, 690, 'images/aa_b_accept.jpg'
aa_b1 = 850, 650, 1080, 740, 'images/aa_b1.jpg'
aa_b2 = 1600, 970, 1900, 1060, 'images/aa_b2.jpg'
check_enter_ = 1111, 180, 1500, 300, 'images/check_enter.jpg'
vpn_0 = 893, 453, 929, 481, 'images/vpn_0.jpg'
vpn_e0 = 888, 431, 950, 494, 'images/vpn_e0.jpg'
cancel = 820, 685, 1100, 744, 'images/cancel.jpg'
vpn_crash = 920, 252, 1035, 337, 'images/vpn_crash.jpg'
g1_exp = 894, 464, 1280, 530, 'images/g1_exp.jpg'
g1_honor = 894, 464, 1280, 530, 'images/g1_honor.jpg'
g2_or = 845, 623, 1214, 696, 'images/g2_or.jpg'
g2_sk = 845, 623, 1214, 696, 'images/g2_sk.jpg'
aa_b_enter = 1672, 1026, 1720, 1071, 'images/aa_b_enter.jpg'
aa_b_icon4 = 336, 1029, 383, 1079, 'images/aa_b_icon4.jpg'
vm_start = 486, 300, 554, 374, 'images/vm_start.jpg'
vm_autoriz = 1560, 1024, 1666, 1055, 'images/vm_autoriz.jpg'
vm_autoriz_check = 1037, 443, 1295, 646, 'images/vm_autoriz_check.jpg'
vm_autoriz_check2 = 860, 490, 1007, 634, 'images/vm_autoriz_check2.jpg'
vm_win = 972, 979, 1026, 1038, 'images/vm_win.jpg'
vm_play = 1358, 350, 1590, 451, 'images/vm_play.jpg'
vm_ok = 893, 722, 1137, 818, 'images/vm_ok.jpg'
vm_serv = 1016, 727, 1278, 860, 'images/vm_serv.jpg'
vm_char = 1291, 927, 1674, 1007, 'images/vm_char.jpg'
vm_char2 = 1291, 927, 1674, 1007, 'images/vm_char2.jpg'
chat = 28, 625, 365, 924, 'images/chat.jpg'
#browser = 0, 25, 40, 70, 'images/browser.jpg'


class aa:

    #l = []
    #last_acc_id = 1

    def find_img(self, search, delay):
        while True:
            time.sleep(delay)
            img = ImageGrab.grab(bbox=(search[0], search[1], search[2], search[3]))
            img.save('images/grabIm.png')
            img = cv2.imread('images/grabIm.png')
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.Canny(img_rgb, 1, 240)

            template = cv2.imread(search[4])
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 101, 101)
            w, h = template.shape[:2]

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            total = 0
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
                total = +1
            if total:
                break

    def find_img_mouse_active(self, search, delay):
        while True:
            time.sleep(delay)
            ser.write(b'Q ')
            img = ImageGrab.grab(bbox=(search[0], search[1], search[2], search[3]))
            img.save('images/grabIm.png')
            img = cv2.imread('images/grabIm.png')
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.Canny(img_rgb, 1, 240)

            template = cv2.imread(search[4])
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 101, 101)
            w, h = template.shape[:2]

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            total = 0
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
                total = +1
            if total:
                break

    def find_img_return(self, search, delay):
        while True:
            time.sleep(delay)
            img = ImageGrab.grab(bbox=(search[0], search[1], search[2], search[3]))
            img.save('images/grabIm.png')
            img = cv2.imread('images/grabIm.png')
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.Canny(img_rgb, 1, 240)

            template = cv2.imread(search[4])
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 101, 101)
            w, h = template.shape[:2]

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            total = 0
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
                total = +1
            if total:
                return 1
            else:
                return 0

    def check_mob(self):
        time.sleep(1)
        img = ImageGrab.grab(bbox=(680, 230, 1260, 850))
        img.save('images/grabIm.png')
        img = cv2.imread('images/grabIm.png')
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.Canny(img_rgb, 1, 240)

        template = cv2.imread('images/aa_b_mob.jpg')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 101, 101)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        total = 0
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            total = +1
        if total:
            ser.write(b'4 ')

    def check_net_connet(self):
        if self.find_img_return(error_net, 1) == 1:
            print("net")
            time.sleep(1)
            ser.write(b'S ')
            time.sleep(10)
            ser.write(b'2 ')
            time.sleep(2)

    def while_img(self, x1, y1, x2, y2, search_b, delay):
        while True:
            time.sleep(delay)
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img.save('images/grabIm.png')
            img = cv2.imread('images/grabIm.png')
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.Canny(img_rgb, 1, 240)

            template = cv2.imread(search_b)
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 101, 101)
            w, h = template.shape[:2]

            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            total = 0
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
                total = 1
            if total == 0:
                break

    # def pick_last_acc(self):
    #     if self.last_acc_id == 1:
    #         time.sleep(2)
    #     elif self.last_acc_id == 2:  # round_count
    #         ser.write(b'C ')  # 1
    #     elif self.last_acc_id == 3:
    #         ser.write(b'D ')
    #     elif self.last_acc_id == 4:
    #         ser.write(b'E ')
    #     elif self.last_acc_id == 5:
    #         ser.write(b'F ')
    #     elif self.last_acc_id == 6:
    #         ser.write(b'G ')
    #     elif self.last_acc_id == 7:
    #         ser.write(b'H ')  # оставть только выбор последнего акка

    # def check_acc(self):
    #     time.sleep(5)
    #     self.check_net_connet()
    #     time.sleep(2)
    #     for acc_id in range(len(accs)):
    #         current_acc = -1
    #         if self.find_img_return(1444, 122, 1555, 160, accs[acc_id], 7):
    #             print("acc_id ", acc_id)
    #             current_acc = acc_id
    #             break
    #         else:
    #             print("ошибка id")
    #     if current_acc == -1:  # ошибка авторизации
    #         #ser.write(b'C ')  # последний акк
    #         self.pick_last_acc()
    #         time.sleep(15)
    #         print("некст")
    #     else:  # выбран акк
    #         newAcc = 1
    #         for l_id in self.l:
    #             if current_acc == l_id:
    #                 print("уже есть")
    #                 newAcc = 0
    #                 break
    #             else:
    #                 print("пока норм")
    #         if newAcc:
    #             print("ок")
    #             self.l.append(current_acc)
    #             print(self.l)
    #             return 1
    #         else:
    #             print("не ок")
    #             #ser.write(b'C ')  # последний акк
    #             self.pick_last_acc()
    #             time.sleep(15)
    #             return 0

    def daily_check(self):
        self.check_mob()
        time.sleep(1)
        img = ImageGrab.grab(bbox=(930, 600, 1380, 680))
        img.save('images/grabIm.png')
        img = cv2.imread('images/grabIm.png')
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.Canny(img_rgb, 1, 240)

        template = cv2.imread('images/aa_b_done.jpg')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 101, 101)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            return 2

        template = cv2.imread('images/aa_b_open.jpg')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 101, 101)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        total = 0
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            total = 1

        template = cv2.imread('images/aa_b_50000.jpg')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 101, 101)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            total = 1
        if total:
            return 0
        ser.write(b'6 ')
        return 1

    def enterGame(self):
        #self.find_img_return(aa_b_enter, 10) == 0
        cr = 1
        while cr:
            tr = 0
            while self.find_img_return(aa_b_play2, 4) == 0: # and self.find_img_return(aa_b_play3, 4) == 0:
                time.sleep(3)
                tr += 1
                if tr == 5:
                    ser.write(b'7 ')
                    tr = 0
                    time.sleep(10)
                print('поиск play')
            #self.find_img(1180, 110, 1380, 175, 'images/aa_b_play2.jpg', 4)  # играть
            time.sleep(3)
            ser.write(b'2 ')
            time.sleep(15)
            self.check_net_connet()
            #time.sleep(5)
            # if self.find_img_return(check_enter_ok, 4) == 1:
            #     ser.write(b'l ')
            #     time.sleep(15)
            #     #ser.write(b'k ')
            #     #time.sleep(5)
            #     if self.find_img_return(connect, 2) == 1:
            #         ser.write(b'n ')
            #         time.sleep(15)
            #         self.find_img(disconnect, 7)  # впн
            #         time.sleep(10)
            #     ser.write(b'2 ')
            #time.sleep(5)
            self.find_img(aa_b_accept, 4)  # accept
            time.sleep(3)
            ser.write(b'3 ')
            time.sleep(15)
            cont = 1
            while True:
                ser.write(b'b ') #mouse active
                time.sleep(4)
                if self.find_img_return(aa_b1, 3) == 1:  # вход на серв
                    time.sleep(15)
                    ser.write(b'0 ')
                    cont = 1
                    break
                if self.find_img_return(error_enter, 3) == 1:
                    ser.write(b'S ') #e
                    cont = 0
                    print("Enter error")
                    break
                if self.find_img_return(aa_b_play2, 4) == 1 or self.find_img_return(aa_b_play3, 4) == 1:
                    cont = 0
                    print("Enter error")
                    break
            if cont == 1:
                while True:
                    ser.write(b'b ') #mouse active
                    time.sleep(4)
                    if self.find_img_return(aa_b2, 3) == 1:  # вход в игру
                        time.sleep(5)
                        ser.write(b'1 ')
                        cr = 0
                        break
                    if self.find_img_return(error_enter, 3) == 1:
                        ser.write(b'S ') #e
                        time.sleep(5)
                        print("Enter error")
                        break
                    if self.find_img_return(aa_b_play2, 4) == 1 or self.find_img_return(aa_b_play3, 4) == 1:
                        print("Enter error")
                        break
            # if cont == 1:
            #     self.find_img_mouse_active(aa_b2, 7)  # вход в игру
            #     time.sleep(5)
            #     ser.write(b'1 ')
            #     cr = 0

    def check_enter(self):
        if self.find_img_return(aa_b_play2, 2) == 0:
            self.find_img(check_enter_, 2)  # проверить
            ser.write(b'R ')
            self.find_img(check_enter_ok, 4)  # ок
            ser.write(b'S ')

    def check_vpn(self):
        while self.find_img_return(vpn_0, 3) == 1 or self.find_img_return(vpn_e0, 3) == 1 or self.find_img_return(connect, 2) == 1:
            print('vpn_error')
            time.sleep(2)
            #self.check_vpn_crash()
            time.sleep(2)
            # if self.find_img_return(disconnect, 2) == 1:
            #     print('disc')
            #     time.sleep(5)
            #     ser.write(b'n ')  # впн вкл/выкл
            #     time.sleep(15)
            if self.find_img_return(cancel, 2) == 1:  # впн
                print('cncl')
                time.sleep(5)
                ser.write(b'n ')  # впн вкл/выкл
                time.sleep(10)
                if self.find_img_return(cancel, 2) == 1:  # впн
                    print('cncl')
                    time.sleep(5)
                    ser.write(b'n ')  # впн вкл/выкл
                    time.sleep(15)
                time.sleep(5)
            print('auto')
            ser.write(b'm ')  # авто
            # time.sleep(15)
            # ser.write(b'n ')
            time.sleep(25)
        print('vpn_ok')

    def check_vpn_crash(self):
        if self.find_img_return(vpn_crash, 2) == 1:
            print('vpn crash')
            os.system("taskkill /f /im app.exe")
            time.sleep(20)
            ser.write(b'g ')
            time.sleep(5)
            v_check = 0
            if self.find_img_return(aa_b_accept, 4) == 0:  # accept
                time.sleep(5)
                v_check += 1
                if v_check == 6:
                    ser.write(b'g ')
                    time.sleep(15)
            ser.write(b'f ')
            time.sleep(20)
            self.find_img(connect, 4)  # впн
            #time.sleep(5)
            #ser.write(b'm ')  # авто режим впн

    def Gu_quests(self):
        change_gq = 0
        gq_ok = 0
        while change_gq < 4 and gq_ok < 2:
            if self.find_img_return(g1_exp, 2) != 1 and self.find_img_return(g1_honor, 2) != 1:
                change_gq += 1
                print('1 ne ok')
                ser.write(b'j ')
                time.sleep(13)
            else:
                gq_ok += 1
            if self.find_img_return(g2_or, 2) != 1 and self.find_img_return(g2_sk, 2) != 1:
                change_gq += 1
                print('2 ne ok')
                ser.write(b'i ')
                time.sleep(13)
            else:
                gq_ok += 1

    def round(self, round_count, isEnter): #, current_acc_id):
        #self.last_acc_id = round_count
        #if current_acc_id != 1:
        time.sleep(5)
        if self.find_img_return(connect, 4) == 1:
            time.sleep(5)
            ser.write(b'n ')
            time.sleep(15)
        #авто режим уже включен
            # self.find_img(connect, 2) # впн
            # time.sleep(2)
            # ser.write(b'n ') #впн вкл/выкл
            # time.sleep(25)
            # #self.find_img(820, 685, 1100, 744, 'images/disconnect.jpg', 7)  # впн
            # self.check_vpn()
            # time.sleep(10)
        #1 акк
        print("0 Acc")
        time.sleep(5)
        os.startfile(r'D:\GC\GameCenter1\GameCenter.exe')
        time.sleep(10)
        #if isEnter == 0:
        #time.sleep(1)
        #self.check_acc()
        time.sleep(1)
        #self.check_enter()
        self.enterGame()

        change_daily = 0
        self.find_img_mouse_active(aa_b_enter, 10)  # в игре
        time.sleep(10)
        self.check_mob()
        time.sleep(5)
        ser.write(b'h ')  # активация ги квестов
        time.sleep(20)
        self.Gu_quests()
        time.sleep(10)
        ser.write(b'5 ')  # делики

        time.sleep(83)
        for i in range(12):  # 8 - 1, 12 - 2
            change_flag = 1
            self.check_mob()
            time.sleep(5)
            ser.write(b'9 ')
            time.sleep(5)
            while change_daily < 6 and change_flag:
                change_flag = self.daily_check()  # минимум 7 сек
                if change_flag:
                    change_daily += 1
                elif change_flag == 2:
                    change_daily = 6
                time.sleep(15)  # daily_check()
            ser.write(b'8 ')
            time.sleep(45)
        time.sleep(10)
        ser.write(b'P ')  # инвентарь
        time.sleep(5)
        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        img.save(r'D:\aa\info\Acc_0.png')
        self.check_mob()
        time.sleep(5)
        ser.write(b'A ')  # выход
        time.sleep(23)
        while self.find_img_return(aa_b_icon4, 10) == 0:  # лаунчер
            ser.write(b'A ')  # выход
            time.sleep(23)
        time.sleep(10)
        os.system("taskkill /f /im GameCenter.exe")
        time.sleep(10)
                # if self.find_img_return(connect, 4) == 1:
                #     ser.write(b'n ')
                #     time.sleep(15)
                #     ser.write(b'm ')
                #     time.sleep(25)
                # if self.find_img_return(disconnect, 4) == 1:  # впн
                #     time.sleep(3)
                #     ser.write(b'n ')
                #     time.sleep(10)
                #     self.find_img(connect, 4)  # впн
                #     time.sleep(5)
                #     ser.write(b'm ')  # авто режим впн
                #     time.sleep(15)
                # self.check_vpn_crash()
                # time.sleep(5)
        #ser.write(b'7 ')

        #остальные акки
        for acc in range(round_count):
            #if current_acc_id != (acc + 2):
                #авто режим уже включен
                    # time.sleep(2)
                    # self.find_img(connect, 2)  # впн
                    # time.sleep(2)
                    # ser.write(b'n ')
                    # time.sleep(25)
                    # #self.find_img(820, 685, 1100, 744, 'images/disconnect.jpg', 7)  # впн
                    # self.check_vpn()
            time.sleep(10)

            print(acc+1, "Acc")
            time.sleep(5)
            os.startfile(r'D:\GC\GameCenter' + str(acc + 2) + '\GameCenter.exe')
            time.sleep(10)
            #self.find_img(1180, 110, 1380, 175, 'images/aa_b_play2.jpg', 4) #ожидание лаунчера

            time.sleep(3)
            #self.pick_last_acc()
            time.sleep(10)
            #self.while_img(670, 420, 1230, 640, 'images/aa_b_autoriz.jpg', 3)  #ожидание авторизации
            #time.sleep(10)
            #проверка на новый акк
            # n = 0
            # while n != 1:
            #     n = self.check_acc() # поменять в конце на ser.write(b'H ')
            #     print(n)

            change_daily = 0

            self.enterGame()
            self.find_img_mouse_active(aa_b_enter, 10) #в игре
            time.sleep(10)
            self.check_mob()
            time.sleep(5)
            ser.write(b'h ')  # активация ги квестов
            time.sleep(20)
            self.Gu_quests()
            time.sleep(10)
            ser.write(b'5 ') #делики
            time.sleep(83)
            for i in range(12): #8 - 1, 12 - 2
                change_flag = 1
                self.check_mob()
                time.sleep(5)
                ser.write(b'9 ')
                time.sleep(5)
                while change_daily < 6 and change_flag:
                    change_flag = self.daily_check() # минимум 7 сек
                    if change_flag:
                        change_daily+=1
                    elif change_flag == 2:
                        change_daily = 6
                    time.sleep(15) #daily_check()
                ser.write(b'8 ')
                time.sleep(45)
            time.sleep(10)
            ser.write(b'P ')  # инвентарь
            time.sleep(5)
            img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
            img.save(r'D:\aa\info\Acc_'+str(acc+1)+'.png')
            self.check_mob()
            ser.write(b'A ') #выход
            time.sleep(23)
            while self.find_img_return(aa_b_icon4, 10) == 0: #лаунчер
                ser.write(b'A ')  # выход
                time.sleep(23)
            time.sleep(10)
            os.system("taskkill /f /im GameCenter.exe")
            time.sleep(10)
                    # if self.find_img_return(connect, 4) == 1:
                    #     ser.write(b'n ')
                    #     time.sleep(15)
                    #     ser.write(b'm ')
                    #     time.sleep(25)
                    # if self.find_img_return(disconnect, 4) == 1:  # впн
                    #     time.sleep(3)
                    #     ser.write(b'n ')
                    #     time.sleep(10)
                    #     self.find_img(connect, 4)  # впн
                    #     time.sleep(5)
                    #     ser.write(b'm ')  # авто режим впн
                    #     time.sleep(15)
                    # self.check_vpn_crash()
                    # time.sleep(5)
            #ser.write(b'7 ')

    def coord(self):
        time.sleep(3)
        img = ImageGrab.grab(bbox=(map_close_cord))
        img.save('images/grabIm.png')
        img = cv2.imread('images/grabIm.png')
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.Canny(img_rgb, 1, 240)

        template = cv2.imread('images/map.JPG')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 101, 101)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        total = 0
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            total = +1
        if total == 0:
            return 0


        time.sleep(3)
        img = ImageGrab.grab(bbox=(spot_map_cord[spot_id][0], spot_map_cord[spot_id][1], spot_map_cord[spot_id][2], spot_map_cord[spot_id][3]))
        img.save('images/grabIm.png')
        img = cv2.imread('images/grabIm.png')
        up = np.array([0, 0, 0])
        low = np.array([80, 55, 55])  # 100 50 50 / 60, 36, 42
        mask = cv2.inRange(img, up, low)

        template = cv2.imread('images/newMark5.png')
        template = cv2.inRange(template, up, low)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(mask, template, cv2.TM_CCORR)
        threshold = 0.99
        loc = np.where(res >= threshold)
        total = 0
        totalX = 0
        totalY = 0
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            cv2.rectangle(img, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
            total = total + 1
            x = pt[0] + h
            y = pt[1] + w
            totalX += x
            totalY += y

        if total > 0 and total < 22:
            #print("Есть ", total)
            x = int(totalX / total)
            y = int(totalY / total)
            #print(x, y)
            #print(int(totalX / total), int(totalY / total))
            # cv2.imshow('result', img)
            # cv2.waitKey(0)
            return x, y
        else:
            print("Нету/много", total)
            return 0
        #cv2.imshow('tt', img)
        #cv2.waitKey(0)

    def fix_dir(self):
        dir = [[5,4,3,2,1,0,7,6],
               [6,5,4,3,2,1,0,7],
               [7,6,5,4,3,2,1,0],
               [0,7,6,5,4,3,2,1],
               [1,0,7,6,5,4,3,2],
               [2,1,0,7,6,5,4,3],
               [3,2,1,0,7,6,5,4],
               [4,3,2,1,0,7,6,5]]
        ser_bt = ser.readline()
        dec_bt = ser_bt[0:len(ser_bt) - 2].decode("utf-8")

        if dec_bt == '2':
            c1 = self.coord()
            if c1 == 0:
                print('error c1')
                return 0
            #print('c1 ', c1)
            ser.write(b'y ')
            time.sleep(2)#6
            c2 = self.coord()
            #time.sleep(1)
            if c2 == 0:
                print('error c2')
                return 0

            cx = c2[0] - c1[0] #проверка на некорректные корды
            cy = c2[1] - c1[1]

            dx = c2[0] - spot_mark_cord[spot_id][0] #176 #60 #176
            dy = c2[1] - spot_mark_cord[spot_id][1] #85 #69 #87

            #print('c2 ', c2)
            #print("Cx Cy",cx, cy)
            #print("Dx Dy", dx, dy)

            if cx < 0 and cy < 0:
                d = 0
            elif cx == 0 and cy < 0:
                d = 1
            elif cx > 0 and cy < 0:
                d = 2
            elif cx > 0 and cy == 0:
                d = 3
            elif cx > 0 and cy > 0:
                d = 4
            elif cx == 0 and cy > 0:
                d = 5
            elif cx < 0 and cy > 0:
                d = 6
            elif cx < 0 and cy == 0:
                d = 7
            else:
                return 0

            #print("Направление", d)

            if dx < 0 and dy < 0:
                p = 0
            elif dx == 0 and dy < 0:
                p = 1
            elif dx > 0 and dy < 0:
                p = 2
            elif dx > 0 and dy == 0:
                p = 3
            elif dx > 0 and dy > 0:
                p = 4
            elif dx == 0 and dy > 0:
                p = 5
            elif dx < 0 and dy > 0:
                p = 6
            elif dx < 0 and dy == 0:
                p = 7
            else:
                return 0

            #print("Сторона", p)
            #print("Домой", dir[p][d])

            if dir[p][d] == 0:
                ser.write(b'w ')
            elif dir[p][d] == 1:
                ser.write(b'v ')
            elif dir[p][d] == 2:
                ser.write(b'u ')
            elif dir[p][d] == 3:
                ser.write(b't ')
            elif dir[p][d] == 4:
                ser.write(b's ')
            elif dir[p][d] == 5:
                ser.write(b'r ')
            elif dir[p][d] == 6:
                ser.write(b'q ')
            elif dir[p][d] == 7:
                ser.write(b'p ')
            else:
                return 0

    def crl_farm(self, hr, m, daily_cl): #, current_id):
        over_time = False
        while True:
            for i in range(2):
                time.sleep(45)
                for p in range(2):
                    if over_time:
                        break
                    time.sleep(3)
                    player_check = self.find_img_return(chat, 1) # 1 is ok

                    if player_check == 0:
                        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
                        img.save(r'D:\aa\info\Warning.png')
                        time.sleep(1)
                        #проверка на win
                        img = cv2.imread(r'D:\aa\info\Warning.png')
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        img_rgb = cv2.Canny(img_rgb, 1, 240)

                        template = cv2.imread('images/aa_b_icon4.jpg')
                        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                        template = cv2.Canny(template, 101, 101)
                        w, h = template.shape[:2]

                        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                        threshold = 0.7
                        loc = np.where(res >= threshold)
                        t1 = 0
                        for pt in zip(*loc[::-1]):  # Switch collumns and rows
                            t1 = 1
                        if t1 == 1:
                            player_check = 1
                            break


                time_hs = time.localtime(time.time())
                hour = time.strftime('%H', time_hs)
                minutes = time.strftime('%M', time_hs)
                if (int(hour) == hr and int(minutes) >= m) or player_check == 0 or over_time:
                    over_time = True
                    print("выход")
                    time.sleep(2)
                    ser.write(b'A ')  # выход
                    time.sleep(40)
                    while self.find_img_return(aa_b_icon4, 10) == 0:  # лаунчер
                        print("выход 2")
                        ser.write(b'A ')  # выход
                        time.sleep(16)
                    time.sleep(35)
                    os.system("taskkill /f /im GameCenter.exe")
                    time.sleep(15)
                    #if self.find_img_return(browser, 3) == 1:
                    os.system("taskkill /f /im msedge.exe")
                    time.sleep(15)
                    ser.write(b'K ') #выход из VM
                    time.sleep(25)
                    os.system("taskkill /f /im VirtualBoxVM.exe")
                    time.sleep(25)
                    os.system("taskkill /f /im VirtualBox.exe")
                    if self.find_img_return(connect, 4) == 1:
                        time.sleep(5)
                        ser.write(b'n ')
                        time.sleep(15)
                    if daily_cl == 1 and player_check == 1:
                        # os.startfile(r'C:\Users\USER\AppData\Local\GameCenter\GameCenter.exe')
                        # time.sleep(10)
                        # self.find_img(connect, 4)
                        # #self.check_vpn_crash()
                        # time.sleep(15)
                        # ser.write(b'm ')
                        # time.sleep(25)

                        #self.check_vpn()
                        #while self.find_img_return(disconnect, 4) != 1:  # впн
                            # self.check_vpn_crash()
                            #time.sleep(10)
                            # self.check_vpn()
                            # ser.write(b'n ')
                            # time.sleep(10)
                            # self.find_img(connect, 4)  # впн
                            # time.sleep(5)
                            # ser.write(b'm ') #авто режим впн
                            # time.sleep(15)
                        time.sleep(5)
                        self.round(4, 0) # -1 #, current_id) #убрать acc_check, перед заходом, запускать .exe
                        time.sleep(20)
                    time.sleep(10)
                    ser.write(b'n ')
                    time.sleep(15)
                    os.system("taskkill /f /im VBoxSDS.exe")
                    time.sleep(3)
                    os.system("taskkill /f /im VBoxSVC.exe")
                    time.sleep(5)
                    ser.write(b'o ')  # off
                    time.sleep(2)
                    exit(0)
                    return 0

            # hwnd = win32gui.FindWindow(None, "User2 - Виртуальная клавиатура")
            # win32gui.ShowWindow(hwnd, 5)
            # win32gui.SetForegroundWindow(hwnd)
            # ser.write(b'd ')
            # time.sleep(2)

            c = self.coord()
            print(c)
            if c:
                ser.write(b'O ')
                self.fix_dir()
            else:
                print('uncorrect c in crl_farm')

    def dalyWithoutExit(self):
        #self.enterGame()
        change_daily = 0
        self.find_img_mouse_active(aa_b_enter, 10)  # в игре
        time.sleep(10)
        self.check_mob()
        time.sleep(5)
        ser.write(b'h ')  # активация ги квестов
        time.sleep(20)
        self.Gu_quests()
        time.sleep(10)
        ser.write(b'5 ')  # делики
        time.sleep(83)
        for i in range(12):  # 8 - 1, 12 - 2
            change_flag = 1
            self.check_mob()
            time.sleep(5)
            ser.write(b'9 ')
            time.sleep(5)
            while change_daily < 6 and change_flag:
                change_flag = self.daily_check()  # минимум 7 сек
                if change_flag:
                    change_daily += 1
                elif change_flag == 2:
                    change_daily = 6
                time.sleep(15)  # daily_check()
            ser.write(b'8 ')
            time.sleep(35)
        time.sleep(10)
        ser.write(b'P ')  # инвентарь
        time.sleep(5)
        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
        img.save(r'D:\aa\info\Acc_F.png')

    def enter2window(self, acc_num):
        time.sleep(2)
        os.startfile(r'C:\Program Files\Oracle\VirtualBox\VirtualBox.exe')
        self.find_img(vm_start, 5)
        ser.write(b'B ')
        time.sleep(20)
        while self.find_img_return(vm_autoriz_check, 5) == 1:  # or self.find_img_return(vm_autoriz_check2, 5) == 1:
            time.sleep(5)
            print("win wait")
        self.find_img(vm_autoriz, 5)
        ser.write(b'C ')
        self.find_img(vm_win, 5)
        ser.write(b'D ')
        time.sleep(5)
        for i in range(acc_num - 1):
            ser.write(b'E ')
            time.sleep(3)
        ser.write(b'F ')
        self.find_img(vm_play, 5)
        ser.write(b'G ')
        self.find_img(vm_ok, 5)
        ser.write(b'H ')
        self.find_img(vm_serv, 5)
        ser.write(b'I ')
        while self.find_img_return(vm_char, 2) == 0 and self.find_img_return(vm_char2, 2) == 0:
            time.sleep(5)
        ser.write(b'J ')

#if __name__ == '__main__':
aa1 = aa()
#time.sleep(5)
while True:
    print("farm ------------------- 1\n"
          "enter game x2 ---------- 2\n"
          "daily cycle (out game) - 3\n"
          "enter game ------------- 4\n"
          "daily w/o exit --------- 5\n"
          "farm w/o daily --------- 6\n"
          "start 2 window --------- 7\n"
          "close the program ------ 8")
    input_num = input()
    if int(input_num) == 1:
        print("Spot id (0-1): ")
        spot_id = input()
        spot_id = int(spot_id)
        #print("current acc id: ")
        #c_id = input()
        print("end of farm: \n-1 for unlimited \nHour: ")
        h = int(input())
        print("Minutes")
        m = int(input())
        aa1.crl_farm(h, m, 1)
    elif int(input_num) == 2:
        print("Acc num:")
        acc_num = input()
        # time.sleep(5)
        # ser.write(b'g ')  # start vpn
        #   os.startfile(r'E:\hmn\app.exe')
        # aa1.find_img(aa_b_accept, 4)  # accept
        # ser.write(b'3 ')
        # aa1.find_img(connect, 4)
        # ser.write(b'c ')  # auto vpn
        # aa1.find_img(connect, 5)
        # ser.write(b'n ')  # on
        # aa1.find_img(disconnect, 4)
        aa1.enter2window(int(acc_num))
        time.sleep(10)
        os.startfile(r'D:\GC\GameCenter_bow\GameCenter.exe')
        time.sleep(4)
        aa1.enterGame()
        # print("number of acc: ")
        # n = input()
        # print("current acc id: ")
        # c_id = input()
        # aa1.round(int(n), 1, int(c_id)) #( кол-во акков, в игре (1) или нет(0) )
        # time.sleep(10)
        # ser.write(b'o ')
    elif int(input_num) == 3:
        print("number of acc: ")
        n = input()
        #print("current acc id: ")
        #c_id = input()
        aa1.round(int(n), 0) #, int(c_id))
        time.sleep(10)
        ser.write(b'o ')
    elif int(input_num) == 4:
        #aa1.check_enter()
        time.sleep(2)
        aa1.enterGame()
    elif int(input_num) == 5:
        aa1.dalyWithoutExit()
        #print('test')
    elif int(input_num) == 6:
        #time.sleep(2)
        #ser.write(b'm ')
        #os.system("taskkill /f /im VirtualBoxVM.exe")
        #print(aa1.find_img_return(disconnect, 4))
        #ser.write(b'c ')  # auto vpn
        # aa1.dalyWithoutExit()
        print("Spot id (0-1): ")
        spot_id = input()
        spot_id = int(spot_id)
        print("end of farm: \n-1 for unlimited \nHour: ")
        h = input()
        print("Minutes")
        m = input()
        aa1.crl_farm(int(h), int(m), 0)
    elif int(input_num) == 7:
        print("Acc num:")
        acc_num = input()
        time.sleep(3)
        aa1.enter2window(int(acc_num))
    elif int(input_num) == 9:
        time.sleep(3)
        img = ImageGrab.grab(bbox=(953, 426, 954, 427))
        img.save('images/newMark6.png')
    elif int(input_num) == 8:
        # time.sleep(2)
        # if aa1.find_img_return(error_net, 1) == 1:
        #     ser.write(b'S ')
        # player_check = aa1.find_img_return(chat, 1)
        #
        # img = cv2.imread(r'D:\aa\info\Warning.png')
        # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img_rgb = cv2.Canny(img_rgb, 1, 240)
        #
        # template = cv2.imread('images/aa_b_icon4.jpg')
        # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # template = cv2.Canny(template, 101, 101)
        # w, h = template.shape[:2]
        #
        # res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        # threshold = 0.7
        # loc = np.where(res >= threshold)
        # t1 = 0
        # for pt in zip(*loc[::-1]):  # Switch collumns and rows
        #     t1 = +1
        #
        # print(t1)
        # img = ImageGrab.grab(bbox=(930, 600, 1380, 680))
        # img.save('images/grabIm.png')
        # img = cv2.imread('images/grabIm.png')
        # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img_rgb = cv2.Canny(img_rgb, 1, 240)
        #
        #
        #
        # template = cv2.imread('images/aa_b_open.jpg')
        # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # template = cv2.Canny(template, 101, 101)
        # w, h = template.shape[:2]
        #
        # res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        # threshold = 0.7
        # loc = np.where(res >= threshold)
        # total = 0
        # for pt in zip(*loc[::-1]):  # Switch collumns and rows
        #     total = 1
        # print(total)
        #os.system("taskkill /f /im VBoxSDC.exe")
        # ser.write(b'A ')  # выход
        # time.sleep(40)
        # while aa1.find_img_return(aa_b_icon4, 10) == 0:  # лаунчер
        #     print("выход 2")
        #     ser.write(b'A ')  # выход
        #     time.sleep(16)
        # time.sleep(35)
        # os.system("taskkill /f /im GameCenter.exe")
        # time.sleep(15)
        # # if self.find_img_return(browser, 3) == 1:
        # os.system("taskkill /f /im msedge.exe")
        # time.sleep(15)
        # ser.write(b'K ')
        # time.sleep(35)
        # os.system("taskkill /f /im VirtualBox.exe")
        # if aa1.find_img_return(disconnect, 4) == 1:
        #     time.sleep(5)
        #     ser.write(b'n ')
        #     time.sleep(15)


        # hwnd = win32gui.FindWindowEx(0, 0, 0, "User2 - Виртуальная клавиатура")
        # print(hwnd)
        # win32gui.ShowWindow(hwnd, 1)
        #print(aa1.find_img_return(aa_b_icon4,2))
        # hwnd = win32gui.FindWindow(None, "User2 - Виртуальная клавиатура")
        # win32gui.ShowWindow(hwnd, 5)
        # win32gui.SetForegroundWindow(hwnd)

        # hWnd = win32gui.FindWindow(None, "User2 - Виртуальная клавиатура")  # Получает хендл окна
        # win32gui.ShowWindow(hWnd, 5)
        # win32gui.SetForegroundWindow(hWnd)
        # win32gui.SetFocus(hWnd)

        # def callback(hwnd, hwnds):
        #     if win32gui.IsWindowVisible(hwnd):
        #         if not win32gui.GetWindow(hwnd, 4):
        #             print(win32gui.GetWindowText(hwnd))
        #
        #
        # win32gui.EnumWindows(callback, 0)

        #print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))

        #aa1.check_vpn() 36 36/ 35 36, 36 35, 35 36,
        # time.sleep(3)
        # img = ImageGrab.grab(bbox=(604, 406, 605, 407))
        # img.save('images/newMark6.png')


        time.sleep(3)
        img = ImageGrab.grab(bbox=(
        spot_map_cord[0][0], spot_map_cord[0][1], spot_map_cord[0][2], spot_map_cord[0][3]))
        img.save('images/grabIm.png')
        img = cv2.imread('images/grabIm.png')
        up = np.array([0, 0, 0])
        low = np.array([80, 55, 55])  # 100 50 50 / 60, 36, 42 / 80, 45, 55
        mask = cv2.inRange(img, up, low)

        template = cv2.imread('images/newMark5.png')
        template = cv2.inRange(template, up, low)
        w, h = template.shape[:2]

        res = cv2.matchTemplate(mask, template, cv2.TM_CCORR)
        threshold = 0.99
        loc = np.where(res >= threshold)
        total = 0
        totalX = 0
        totalY = 0
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            cv2.rectangle(img, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
            total = total + 1
            x = pt[0] + h
            y = pt[1] + w
            totalX += x
            totalY += y

        if total > 0 and total < 22:
            # print("Есть ", total)
            x = int(totalX / total)
            y = int(totalY / total)
            # print(x, y)
            # print(int(totalX / total), int(totalY / total))
            # cv2.imshow('result', img)
            # cv2.waitKey(0)
            print(x, y)
        else:
            print("Нету/много", total)

        cv2.imshow('tt', img)
        cv2.waitKey(0)

        #ser.write(b'2 ')
        #aa1.check_vpn()
        #aa1.check_vpn_crash()
        #os.system('taskkill /f /im app.exe')
        #os.system("\"D:\hmn\hidemy.name VPN 2.0\\app.exe\"")
        #os.system('start app.exe')
        #os.spawnl(os.P_NOWAIT, 'D:/hmn/hidemy.name VPN 2.0/app.exe', 'app.exe')
        # os.system("\"D:\hmn\hidemy.name VPN 2.0\\app.exe\"")
        # print('123')
        #time.sleep(4) #933, 213, 1012, 264

            #os.startfile(r'D:\hmn\hidemy.name VPN 2.0\app.exe')

        #print(aa1.find_img_return(894, 464, 1280, 530, 'images/g1_honor.jpg', 2))

        #time.sleep(10)
        #ser.write(b'5 ')  # делики
        #os.system("taskkill /f /im GameCenter.exe")
        #os.startfile(r'C:\Users\USER\AppData\Local\GameCenter\GameCenter.exe')
        #exit(0)
        #ser.write(b'7 ')
        # os.system("taskkill /f /im GameCenter.exe")
        # time.sleep(5)
        # os.startfile(r'D:\GC\GameCenter1\GameCenter.exe')
        # time.sleep(10)
        # os.system("taskkill /f /im GameCenter.exe")
        # time.sleep(10)
        # os.startfile(r'D:\GC\GameCenter2\GameCenter.exe')
        # time.sleep(10)
        # os.system("taskkill /f /im GameCenter.exe")
        # time.sleep(2)
        # aa1.last_acc_id = 2
        # n = 0
        # while n != 1:
        #     n = aa1.check_acc()
        #     print(n)


    #определить id ника
    #записать id в массив пройденных акков
    #на след. шаге цикла, после смены акка, проверить новый ли это акк
    #иначе выбирать последний(нижний) акк

    # elif int(input_num) == 7:
    #     n = 0
    #     while n != 2:
    #         n += aa1.check_acc()
    #         print(n)
    print("\n")

#ser.write(b'2 ')
# #aa1.find_img(825,700,1080,800, 'images/aa_b1.jpg')
# time.sleep(3)
# ser.write(b' E')