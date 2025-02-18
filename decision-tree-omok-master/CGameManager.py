# -*- coding:cp949 -*-
import pygame
from pygame.locals import *
import CSoundManager
import CMenuManager
import CMultiPlayManager
import _thread as thread
import string
import AIServer
import SitRepTurn,SitRepGame
from random import randint
import time
import MakeOrder

lock = thread.allocate_lock()

class CGameManager(object):
    def __init__(self, Screen):    
        try:
            self.m_Screen = Screen
            self.map_size = 10
            self.whatmock = 4
            self.m_bWinner = False
            self.m_UserTurn = False
            # self.m_GameStatus = 0
            self.m_GameStatus = 1
            self.m_UserSton = 1
            self.m_MultiPlayManager = CMultiPlayManager.CMultiPlayManager()
            self.idGame= 0
            self.idTurn=0
            self.mo = MakeOrder.MakeOrder()
            print ("Initialize Variables - Success...")
        except:
            print ("Initialize Variables - Failed...")
            exit()
            
        # try:
        #     self.m_Map = []
        #     self.m_CrossPoint = []
        #     for y in range(19):  # type: int
        #         self.m_Map.append(range(19))
        #         self.m_CrossPoint.append(range(19))
        #         for x in range(19):
        #             self.m_Map[y][x] = 0
        #             self.m_CrossPoint[y][x] = [(x*30)+30, (y*30)+30]
        #     print ("Initialize MapList - Success...")
        # except:
        #     print ("Initialize MapList - Failed...")
        #     exit()
        self.m_Map = []
        self.m_CrossPoint = []
        for y in range(self.map_size):  # type: int
            self.m_Map.append(list(range(self.map_size)))
            self.m_CrossPoint.append(list(range(self.map_size)))
            for x in range(self.map_size):
                self.m_Map[y][x] = 0
                self.m_CrossPoint[y][x] = [(x * 30) + 30, (y * 30) + 30]
        print("Initialize MapList - Success...")
        
        try:            
            self.m_StonSound = CSoundManager.CSound("sound/OmokSound.ogg")
            self.m_ButtonSound = CSoundManager.CSound("sound/Enter.ogg")
            self.m_QuitSound = CSoundManager.CSound("sound/Quit.ogg")
            print ("Initialize sound effects - Success...")
        except:
            print ("Initialize sound effects - Failed...")
            exit()
            
        try:
            self.m_MenuOn_Color = (142, 14, 13)
            self.m_MenuOff_Color = (191, 253, 248)

            self.m_SoloPlay_Pos = (230, 270)
            self.m_MultiPlay_Pos = (230, 335)
            #self.m_Option_Pos = (230, 400)
            self.m_QuitGame_Pos = (230, 460)
            self.m_MainMenu = CMenuManager.CMenuManager(Screen)
            self.m_MainMenu.AppendMenu("font/��������Bold.ttf", 34, 'play alone'.encode('utf-8'), self.m_SoloPlay_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_MainMenu.AppendMenu("font/��������Bold.ttf", 34, '�����ϱ�'.encode('cp949'), self.m_MultiPlay_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            #self.m_MainMenu.AppendMenu("font/��������Bold.ttf", 34, unicode('ȯ�漳��','cp949'), self.m_Option_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_MainMenu.AppendMenu("font/��������Bold.ttf", 34, '��������'.encode('cp949'), self.m_QuitGame_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)

            self.m_BlackSton_Pos = (260, 210)
            self.m_WhiteSton_Pos = (260, 285)
            self.m_ChoiceSton_Back_Pos = (512, 8)
            self.m_ChoiceStonMenu = CMenuManager.CMenuManager(Screen)
            self.m_ChoiceStonMenu.AppendMenu("font/��������Bold.ttf", 34, 'black'.encode('cp949'), self.m_BlackSton_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_ChoiceStonMenu.AppendMenu("font/��������Bold.ttf", 34, 'white(not supported)'.encode('cp949'), self.m_WhiteSton_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_ChoiceStonMenu.AppendMenu("font/��������Bold.ttf", 34, 'back'.encode('cp949'), self.m_ChoiceSton_Back_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)

            self.m_Onemore_Pos = (233, 240)
            self.m_StopGame_Pos = (233, 302)
            self.m_ResultMenu = CMenuManager.CMenuManager(Screen)
            self.m_ResultMenu.AppendMenu("font/��������Bold.ttf", 34, 'one more'.encode('cp949'), self.m_Onemore_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_ResultMenu.AppendMenu("font/��������Bold.ttf", 34, 'stop playing'.encode('cp949'), self.m_StopGame_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)

            self.m_Host_Pos = (230, 210)
            self.m_Connect_Pos = (230, 285)
            self.m_Multi_Back_Pos = (512, 8)
            self.m_MultiMenu = CMenuManager.CMenuManager(Screen)
            self.m_MultiMenu.AppendMenu("font/��������Bold.ttf", 34, '�游���'.encode('cp949'), self.m_Host_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_MultiMenu.AppendMenu("font/��������Bold.ttf", 34, '�����ϱ�'.encode('cp949'), self.m_Connect_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)
            self.m_MultiMenu.AppendMenu("font/��������Bold.ttf", 34, '�ڷ�'.encode('cp949'), self.m_Multi_Back_Pos, self.m_MenuOn_Color, self.m_MenuOff_Color)

            self.m_WaitClient_Back = (512, 8)
            self.m_WaitClientMenu = CMenuManager.CMenuManager(Screen)
            self.m_WaitClientMenu.AppendMenu("font/��������Bold.ttf", 34, 'Back'.encode('cp949'), self.m_WaitClient_Back, self.m_MenuOn_Color, self.m_MenuOff_Color)

            self.m_Connect_Back = (512, 8)
            self.m_ConnectMenu = CMenuManager.CMenuManager(Screen)
            self.m_ConnectMenu.AppendMenu("font/��������Bold.ttf", 34, 'Back'.encode('cp949'), self.m_Connect_Back, self.m_MenuOn_Color, self.m_MenuOff_Color)
            print ("Initialize Menu - Success...")
        except:
            print ("Initialize Menu - Failed...")
            exit()

            
        try:
            self.m_MainMenuImg = pygame.image.load('img/Menu.jpg').convert()
            self.m_SelectStonImg = pygame.image.load('img/SelectSton.jpg').convert()
            self.m_WinImg = pygame.image.load('img/Win.jpg').convert()
            self.m_LoseImg = pygame.image.load('img/Lose.jpg').convert()
            self.m_DrawImg = pygame.image.load('img/Draw.jpg').convert()
            self.m_MultiMainMenu = pygame.image.load('img/MultiMainMenu.jpg').convert()
            self.m_WaitClientImg = pygame.image.load('img/WaitClient.jpg')
            self.m_ConnectImg = pygame.image.load('img/Connect.jpg')
            self.m_ConnectingImg = pygame.image.load('img/Connecting.jpg')
            
            print ("Initialize Images - Success...")
        except:
            print ("Initialize Images - Failed...")
            exit()

        try:
            self.aiserver = AIServer.AIServer()
            self.aiserver.completenessCheck()
            print("Server connection - Success ...")
        except:
            print("Server connection - Failed ...")
            exit()


    def GetGameStatus(self):
        return self.m_GameStatus
    
    def SetGameStatus(self, value):
        lock.acquire()
        self.m_GameStatus = value
        lock.release()
    
    def ClearScreen(self, Color=(255, 255, 255)):
        self.m_Screen.fill(Color)
        
    def ClearMap(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.m_Map[y][x] = 0
                
    def DrawBaseMap(self, Color=(0, 0, 0)):
        self.m_Screen.fill((255, 204, 33))
        for i in range(self.map_size):
            pygame.draw.line(self.m_Screen,
                             Color,
                             (self.m_CrossPoint[i][0][0], self.m_CrossPoint[i][0][1]),
                             (self.m_CrossPoint[i][self.map_size-1][0], self.m_CrossPoint[i][self.map_size-1][1]))
            pygame.draw.line(self.m_Screen,
                             Color,
                             (self.m_CrossPoint[0][i][0], self.m_CrossPoint[0][i][1]),
                             (self.m_CrossPoint[self.map_size-1][i][0], self.m_CrossPoint[self.map_size-1][i][1]))
            
        # pygame.draw.circle(self.m_Screen, Color, self.m_CrossPoint[3][3], 3)
        # pygame.draw.circle(self.m_Screen, Color, self.m_CrossPoint[15][3], 3)
        # pygame.draw.circle(self.m_Screen, Color, self.m_CrossPoint[3][15], 3)
        # pygame.draw.circle(self.m_Screen, Color, self.m_CrossPoint[15][15], 3)
        # pygame.draw.circle(self.m_Screen, Color, self.m_CrossPoint[9][9], 3)
        
    def DrawSton(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                if self.m_Map[y][x] == 1:
                    pygame.draw.circle(self.m_Screen, (0, 0, 0), self.m_CrossPoint[y][x], 14)
                elif self.m_Map[y][x] == 2:
                    pygame.draw.circle(self.m_Screen, (255, 255, 255), self.m_CrossPoint[y][x], 14)
    def DrawAIStatus(self):
        myfont=pygame.font.SysFont('arial',30)
        textsurface=myfont.render(str(self.idGame),False,(0,0,0))
        self.m_Screen.blit(textsurface,(0,0))

    def DrawMap(self):
        self.DrawBaseMap()
        self.DrawSton()
        self.DrawAIStatus()

    def SetSton(self, CursorX, CursorY, Type):
        for y in range(self.map_size):
            for x in range(self.map_size):
                CrossX = self.m_CrossPoint[y][x][0]
                CrossY = self.m_CrossPoint[y][x][1]
                if ((CursorX-14) < CrossX) and ((CursorX+14) > CrossX) and ((CursorY-14) < CrossY) and ((CursorY+14) > CrossY):
                    if self.m_Map[y][x] == 0:
                        self.m_Map[y][x] = Type
                        # print ("(X =", x,", Y =", y, ") - Ston =", Type )
                        return [x, y]
                    else:
                        return False
        return False
                
    def GetFavorableValue(self, nX, nY, Type):
        x = nX
        y = nY
        count = 0
        hazard = 0
        
        Map = self.m_Map[:]
        for i in range(self.map_size):
            Map[i] = self.m_Map[i][:]
            
        Map[nY][nX] = Type

        while (x > 0) and (Map[y][x-1] == Type):
            x-=1
        while (x <=self.map_size-1) and (Map[y][x] == Type):
            count+=1
            x+=1
        if (count > 5):
            count = 2
        hazard += pow(10, count)
        
        x = nX
        y = nY
        count = 0

        while (y > 0) and (Map[y-1][x] == Type):
            y-=1
        while (y <= self.map_size-1) and (Map[y][x] == Type):
            count+=1
            y+=1
        if (count > 5):
            count = 2
        hazard += pow(10, count)
        
        x = nX
        y = nY
        count = 0
        
        while (x > 0) and (y > 0) and (Map[y-1][x-1] == Type):
            x-=1
            y-=1
        while (x <= self.map_size-1) and (y <= self.map_size-1) and (Map[y][x] == Type):
            count+=1
            x+=1
            y+=1
        if (count > 5):
            count = 2
        hazard += pow(10, count)
        
        x = nX
        y = nY
        count = 0
        
        while (x < self.map_size-1) and (y > 0) and (Map[y-1][x+1] == Type):
            x+=1
            y-=1
        while (x >= 0) and (y <= self.map_size-1) and (Map[y][x] == Type):
            count+=1
            x-=1
            y+=1
        if (count > 5):
            count = 2
        hazard += pow(10, count)
        
        return hazard

    def GetFavorablePos(self, Type):
        FavorableList = []
        max_many_mode = True
        random_range = 5
        for y in range(self.map_size):
            FavorableList.append(list(range(self.map_size)))
            for x in range(self.map_size):
                if self.m_Map[y][x] == 0:
                    FavorableList[y][x] = self.GetFavorableValue(x, y, Type)
                else:
                    FavorableList[y][x] = 0
        max = 0
        FavorX, FavorY = -1, -1
        max_many= []
        max_many_loc=[]
        # ���⸦ �����Ѵ����� ������ ����, �ټ��� ����, ���߿� �ϳ��������� �������� �ɷ� �ٲ���.
        if max_many_mode:
            for y in range(self.map_size):
                for x in range(self.map_size):
                    inserted = False
                    for i in range(len(max_many)):
                        if (FavorableList[y][x] > max_many[i]) and not inserted:
                            max_many.insert(i,FavorableList[y][x])
                            max_many_loc.insert(i,{'x':x,'y':y})
                            inserted = True
                    if not inserted:
                        max_many.append(FavorableList[y][x])
                    max_many_loc.append({'x':x,'y':y})
        # �� ���� �ѹ��� ũ�� �ʾ����� ���� �����־��ִ°� �ؾ���.
            r= randint(0, random_range-1)
            # print(max_many, max_many_loc)
            return [max_many_loc[r]['x'],max_many_loc[r]['y'],max_many[r]]


        else:
            for y in range(self.map_size):
                for x in range(self.map_size):
                    if (FavorableList[y][x] > max):
                        max = FavorableList[y][x];
                        FavorX = x
                        FavorY = y
            return [FavorX, FavorY, max]


    def SendSitRepTurn(self, sitRepTurn):
        # store sitRep in DB by passing it to server.
        self.aiserver.storeSitRep(sitRepTurn)

    def SendSitRepGame(self,sitRepGame):
        print("sendSitRepGame")
        self.aiserver.storeSitRepGame(sitRepGame)

    def WinnerCheck(self, nX, nY, Type):
        x = nX
        y = nY
        count = 0
        
        while (x > 0) and (self.m_Map[y][x-1] == Type):
            x-=1
        while (x <= self.map_size-1) and (self.m_Map[y][x] == Type):
            count+=1
            x+=1
        if (count == self.whatmock):
            return True
        
        x = nX
        y = nY
        count = 0
        
        while (y > 0) and (self.m_Map[y-1][x] == Type):
            y-=1
        while (y <= self.map_size-1) and (self.m_Map[y][x] == Type):
            count+=1
            y+=1
        if (count == self.whatmock):
            return True
        
        x = nX
        y = nY
        count = 0
        
        while (x > 0) and (y > 0) and (self.m_Map[y-1][x-1] == Type):
            x-=1
            y-=1
        while (x <= self.map_size-1) and (y <= self.map_size-1) and (self.m_Map[y][x] == Type):
            count+=1
            x+=1
            y+=1
        if (count == self.whatmock):
            return True
        
        x = nX
        y = nY
        count = 0
        
        while (x < self.map_size-1) and (y > 0) and (self.m_Map[y-1][x+1] == Type):
            x+=1
            y-=1
        while (x >= 0) and (y <= self.map_size-1) and (self.m_Map[y][x] == Type):
            count+=1
            x-=1
            y+=1
        if (count == self.whatmock):
            return True
        
        return False

    def CountZeroCheck(self):
        countZero=0
        for row in self.m_Map:
            for item in row:
                if item ==0:
                    countZero+=1
        return countZero

    def AI(self, Type):
        if self.CountZeroCheck() == 0:
            self.Draw()
            print("Draw")
            return False
        Cpu = self.GetFavorablePos(Type)
        if (Type == 1):
            User = self.GetFavorablePos(2)
        else:
            User = self.GetFavorablePos(1)


        if (Cpu[2] >= User[2]):
            self.SetSton(self.m_CrossPoint[Cpu[1]][Cpu[0]][0], self.m_CrossPoint[Cpu[1]][Cpu[0]][1], Type)
            self.idTurn += 1
            sitRepTurn = SitRepTurn.SitRepTurn(self.idGame, self.idTurn, self.m_Map, Type)
            self.SendSitRepTurn(sitRepTurn)
            if self.WinnerCheck(Cpu[0], Cpu[1], Type):
                self.Lose()
        else:
            self.SetSton(self.m_CrossPoint[User[1]][User[0]][0], self.m_CrossPoint[User[1]][User[0]][1], Type)
            self.idTurn += 1
            sitRepTurn = SitRepTurn.SitRepTurn(self.idGame, self.idTurn, self.m_Map, Type)
            self.SendSitRepTurn(sitRepTurn)
            if self.WinnerCheck(User[0], User[1], Type):
                self.Lose()
        self.m_UserTurn = True

    def TempUserAI(self, Type):
        if self.CountZeroCheck()==0:
            self.Draw()
            print("Draw")
            return False

        User = self.GetFavorablePos(Type)
        if (Type == 1):
            Cpu = self.GetFavorablePos(2)
        else:
            print("nope")
            Cpu = self.GetFavorablePos(1)

        if Cpu[2] <= User[2]:
            self.SetSton(self.m_CrossPoint[User[1]][User[0]][0], self.m_CrossPoint[User[1]][User[0]][1], Type)
            if self.WinnerCheck(User[0], User[1], Type):
                self.Win()
                return True
        else:
            self.SetSton(self.m_CrossPoint[Cpu[1]][Cpu[0]][0], self.m_CrossPoint[Cpu[1]][Cpu[0]][1], Type)
            if self.WinnerCheck(Cpu[0], Cpu[1], Type):
                self.Win()
                return True

        self.m_UserTurn = False
        # return Cpu[0],Cpu[1]

    def TotalRandom(self,Type):

        x, y = randint(0, self.map_size-1), randint(0, self.map_size-1)
        while self.m_Map[x][y] != 0:
            x, y = randint(0,self.map_size-1),randint(0,self.map_size-1)
        pos = self.SetSton(self.m_CrossPoint[y][x][0],self.m_CrossPoint[y][x][1],Type)

        return pos

    def SetUserSton(self, PosX, PosY, Type):
        if self.m_UserTurn == True:
            pos = self.SetSton(PosX, PosY, Type)
            if pos != False:
                self.idTurn += 1
                sitRepTurn = SitRepTurn.SitRepTurn(self.idGame, self.idTurn, self.m_Map,Type)
                self.SendSitRepTurn(sitRepTurn)
                self.m_UserTurn = False

                if self.WinnerCheck(pos[0], pos[1], Type) == True:
                    self.Win()
                if Type == 1:
                    self.AI(2)
                else:
                    self.AI(1)
                self.m_StonSound.Play()
                return True
        return False

    def SimulateUserStone(self,Type):
        if self.m_UserTurn==True:
            is_random= False
            is_ML_mode =True
            total = 0
            for row in self.m_Map:
                total += sum(row)
            # ù �� ����
            if total== 0:
                print("map empty!")
                pos = self.SetSton(self.m_CrossPoint[5][5][0],self.m_CrossPoint[5][5][1],Type)

            else:
                if is_random: # ��ü ������� ����������
                    pos = self.TotalRandom(Type)
                else:
                    if is_ML_mode: # Decision Tree ������� ���� �� ����
                        current_sit_rep = SitRepTurn.SitRepTurn(self.idGame,self.idTurn,self.m_Map,Type)
                        # �̹� �� �������� aiserver�� ������ ���� �� order�� �޾ƿ´�.
                        next_order = self.aiserver.giveNextMove(current_sit_rep)
                        if next_order is False: # aiserver���� �̷� ���� ó�� ����
                            pos = self.TempUserAI(Type) # ���� �ְ����� �ڸ��� �α� �˰����� �۵�.
                        else:
                            x, y = next_order[0]['x'],next_order[0]['y']
                            print(next_order)
                            pos = self.SetSton(self.m_CrossPoint[y][x][0],self.m_CrossPoint[y][x][1],Type)
                            if self.WinnerCheck(x, y, Type):
                                self.Win()
                                return True
                    else:
                        pos = self.TempUserAI(Type)
                    if pos:
                        return True
            if pos!= False:
                self.idTurn+=1
                sitRepTurn = SitRepTurn.SitRepTurn(self.idGame, self.idTurn, self.m_Map,Type)
                # print("sitrepTurn", sitRepTurn)
                self.SendSitRepTurn(sitRepTurn)

                self.m_UserTurn = False
                # if self.WinnerCheck(pos[0], pos[1], Type) == True:
                #     self.Win()
                #     return True
                if Type == 1:
                    self.AI(2)
                else:
                    self.AI(1)
                self.m_StonSound.Play()
                return True
            return False

    def Win(self):
        sitRepGame=SitRepGame.SitRepGame(self.idGame,'win')
        self.SendSitRepGame(sitRepGame)

        self.ClearMap()
        self.m_bWinner = 2
        self.SetGameStatus(3)
        
    def Lose(self):
        sitRepGame = SitRepGame.SitRepGame(self.idGame,'lose')
        self.SendSitRepGame(sitRepGame)

        self.ClearMap()
        self.m_bWinner = 0
        self.SetGameStatus(3)

    def Draw(self):
        sitRepGame=SitRepGame.SitRepGame(self.idGame,'draw')
        self.SendSitRepGame(sitRepGame)

        self.ClearMap()
        self.m_bWinner = 1
        self.SetGameStatus(3)
        
    def DrawMainMenu(self):  
        self.m_Screen.blit(self.m_MainMenuImg, (0, 0))      
        self.m_MainMenu.DrawMenuList(pygame.mouse.get_pos())
        return None

    def DrawChoiceStonMenu(self): 
        self.m_Screen.blit(self.m_SelectStonImg, (0, 0))
        self.m_ChoiceStonMenu.DrawMenuList(pygame.mouse.get_pos())
        return None
    
    def DrawResultMenu(self):
        if (self.m_bWinner==2):
            self.m_Screen.blit(self.m_WinImg, (0, 0))
        elif self.m_bWinner ==0:
            self.m_Screen.blit(self.m_LoseImg, (0, 0))
        else:
            self.m_Screen.blit(self.m_DrawImg, (0, 0))
        self.m_ResultMenu.DrawMenuList(pygame.mouse.get_pos())

        return None
    
    def DrawMultiMainMenu(self):
        self.m_Screen.blit(self.m_MultiMainMenu, (0, 0))
        self.m_MultiMenu.DrawMenuList(pygame.mouse.get_pos())
        return None
    
    def DrawWaitClient(self):
        self.m_Screen.blit(self.m_WaitClientImg, (0, 0))
        self.m_WaitClientMenu.DrawMenuList(pygame.mouse.get_pos())
        return None
    
    def DrawConnecting(self):
        self.m_Screen.blit(self.m_ConnectingImg, (0, 0))
        return None

    def UpdateScreen(self):
        self.ClearScreen()
        
        if (self.m_GameStatus == 0):
            self.DrawMainMenu()
        elif (self.m_GameStatus == 1):
            self.DrawChoiceStonMenu()
        elif (self.m_GameStatus == 2):
            self.DrawMap()
        elif (self.m_GameStatus == 3):
            self.DrawResultMenu()
        elif (self.m_GameStatus == 4):
            self.DrawMultiMainMenu()
        elif (self.m_GameStatus == 5):
            self.DrawWaitClient()
        elif (self.m_GameStatus == 7):
            self.DrawMap()
        elif (self.m_GameStatus == 8):
            self.DrawConnecting()
            
        pygame.display.flip()
    
    def StartSoloPlay(self, Type):
        self.ClearMap()

        if (Type == 2):
            self.SetSton(300, 300, 1)
        self.SetGameStatus(2)
        self.m_UserTurn = True

    def GetKey(self):
        while 1:
            event = pygame.event.poll()
            if (self.m_GameStatus != 6):
                return None
            elif (event.type == pygame.KEYDOWN):
                return event.key
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                self.MouseDownEvent(event)
            elif (event.type == pygame.QUIT):
                exit()
            else:
                pass
            self.m_ConnectMenu.DrawMenuList(pygame.mouse.get_pos())
            pygame.display.update((self.m_ConnectMenu.GetRect(0)))
            
    def Display_EditBox(self, hScreen, szMsg, Rect):   
        self.m_Screen.blit(self.m_ConnectImg, (0, 0))
        self.m_ConnectMenu.DrawMenuList(pygame.mouse.get_pos())
        Font = pygame.font.Font(None, 50)
        pygame.draw.rect(hScreen, (0, 0, 0), Rect, 0)
        if len(szMsg) != 0:
            hScreen.blit(Font.render(szMsg, 1, (255,255,255)), (Rect[0], Rect[1]))
        pygame.display.flip()
        return None
    
    def InputIPToEdit(self, Question, Rect):
        pygame.font.init()
        Text = []
        self.Display_EditBox(self.m_Screen, Question + ": " + string.join(Text, ""), Rect)
        while 1:
            key = self.GetKey()
            if (self.m_GameStatus != 6):
                return None
            elif key == pygame.K_BACKSPACE:
                Text = Text[0:-1]
            elif key == pygame.K_RETURN:
                break
            elif key <= 127:
                Text.append(chr(key))
            self.Display_EditBox(self.m_Screen, Question + ": " + string.join(Text, ""), Rect)
        return string.join(Text, "")
    
    def MultiPlayProcess(self):
        while (True):
            pData = self.m_MultiPlayManager.Receive(32)
            if (pData == False):
                self.m_QuitSound.Play()
                self.SetGameStatus(4)
                self.m_MultiPlayManager.Close()
                self.m_MultiPlayManager.StopServer()
                self.ClearMap()
                print ("The other party has Disconnected...")
                break;
            Values = pData.split(",")
            if ( Values[0] == '0' ):
                self.ClearMap()
                self.SetGameStatus(7)
            if ( Values[0] == '2' ):
                self.m_QuitSound.Play()
                self.SetGameStatus(4)
                self.m_MultiPlayManager.Close()
                self.m_MultiPlayManager.StopServer()
                self.ClearMap()
                print ("The other party has Disconnected...")
            elif( Values[0] == '1' ):
                CursorX = int(Values[1])
                CursorY = int(Values[2])
                Type = int(Values[3])
                Pos = self.SetSton(CursorX, CursorY, Type)
                if (Pos != False):
                    self.m_StonSound.Play()
                    self.m_UserTurn = not self.m_UserTurn     
                    if ( self.WinnerCheck(Pos[0], Pos[1], Type) ):
                        self.ClearMap()
                        if (self.m_UserSton == Type):
                            self.m_UserTurn = False
                            self.m_UserSton = 2
                        else:
                            self.m_UserTurn = True
                            self.m_UserSton = 1

    def StartMultiPlayProcess(self):
        thread.start_new_thread(self.MultiPlayProcess, ())
        return None
    
    def MouseDownEvent(self, e):
        if (e.button == 1):
            #########################################################
            if (self.m_GameStatus == 0):
                if (self.m_MainMenu.GetActivationMenu(e.pos) == 0):
                    self.SetGameStatus(1)
                    self.m_ButtonSound.Play()
                elif (self.m_MainMenu.GetActivationMenu(e.pos) == 1):
                    self.SetGameStatus(4)
                    self.m_ButtonSound.Play()
                elif (self.m_MainMenu.GetActivationMenu(e.pos) == 2):
                    self.m_QuitSound.Play()
                    exit(0)
            #########################################################
            elif (self.m_GameStatus == 1):
                if (self.m_ChoiceStonMenu.GetActivationMenu(e.pos) == 0):
                    self.m_UserSton = 1
                    self.m_ButtonSound.Play()
                    self.idGame=self.aiserver.getLatestGame()+1
                    self.idTurn=0
                    self.StartSoloPlay(self.m_UserSton) # ���� ������ 1�� ���ϰ� ���ӽ���, gamestatus =2 ��
                elif (self.m_ChoiceStonMenu.GetActivationMenu(e.pos) == 1):
                    self.m_UserSton = 2
                    self.m_ButtonSound.Play()
                    self.StartSoloPlay(self.m_UserSton)
                elif (self.m_ChoiceStonMenu.GetActivationMenu(e.pos) == 2):
                    self.SetGameStatus(0)
                    self.m_QuitSound.Play()
            ######################################################### 
            elif (self.m_GameStatus == 2):
                self.SetUserSton(e.pos[0], e.pos[1], self.m_UserSton)
            #########################################################
            elif (self.m_GameStatus == 3):
                if (self.m_ResultMenu.GetActivationMenu(e.pos) == 0):
                    self.m_ButtonSound.Play()
                    self.SetGameStatus(1)
                elif (self.m_ResultMenu.GetActivationMenu(e.pos) == 1):
                    self.m_QuitSound.Play()
                    self.SetGameStatus(0)
            #########################################################
            elif (self.m_GameStatus == 4):
                if (self.m_MultiMenu.GetActivationMenu(e.pos) == 0):
                    self.m_ButtonSound.Play()
                    self.SetGameStatus(5)
                    if ( self.m_MultiPlayManager.InitServer(5000) == False ):
                        return None
                    self.m_MultiPlayManager.StartSelectLoop()
                    if( self.m_MultiPlayManager.ConnectToServer('127.0.0.1', 5000) == False ):
                        return None
                    self.StartMultiPlayProcess()
                    self.m_UserTurn = True
                    self.m_UserSton = 1
                    
                elif (self.m_MultiMenu.GetActivationMenu(e.pos) == 1):
                    self.m_ButtonSound.Play()
                    self.SetGameStatus(6)
                    szIp = self.InputIPToEdit("IP", (150, 250, 330, 30))
                    if(szIp == ""):
                        return None
                    self.SetGameStatus(8)
                    self.UpdateScreen()
                    if (self.m_MultiPlayManager.ConnectToServer(szIp, 5000) == False):
                        self.SetGameStatus(4)
                        return None
                    self.StartMultiPlayProcess()
                    self.m_MultiPlayManager.Send("0")
                    self.m_UserTurn = False
                    self.m_UserSton = 2
                    
                elif (self.m_MultiMenu.GetActivationMenu(e.pos) == 2):
                    self.m_QuitSound.Play()
                    self.SetGameStatus(0)
            #########################################################
            elif (self.m_GameStatus == 5):
                if (self.m_WaitClientMenu.GetActivationMenu(e.pos) == 0):
                    self.m_QuitSound.Play()
                    self.m_MultiPlayManager.Close()
                    self.m_MultiPlayManager.StopServer()
                    self.SetGameStatus(4)
            #########################################################
            elif (self.m_GameStatus == 6):
                if (self.m_ConnectMenu.GetActivationMenu(e.pos) == 0):
                    self.m_QuitSound.Play()
                    self.SetGameStatus(4)
            ######################################################### 
            elif (self.m_GameStatus == 7):
                if (self.m_UserTurn):
                    self.m_MultiPlayManager.SendStonPos(e.pos[0], e.pos[1], self.m_UserSton)

    def SimulationEvent(self):
            #########################################################
        # if (self.m_GameStatus == 0):
        #     if (self.m_MainMenu.GetActivationMenu(e.pos) == 0):
        #         self.SetGameStatus(1)
        #         self.m_ButtonSound.Play()
        #     elif (self.m_MainMenu.GetActivationMenu(e.pos) == 1):
        #         self.SetGameStatus(4)
        #         self.m_ButtonSound.Play()
        #     elif (self.m_MainMenu.GetActivationMenu(e.pos) == 2):
        #         self.m_QuitSound.Play()
        #         exit(0)
        #########################################################
        if (self.m_GameStatus == 1):
            self.m_UserSton = 1
            self.idTurn=0
            self.m_ButtonSound.Play()
            self.idGame=self.aiserver.getLatestGame()
            self.StartSoloPlay(self.m_UserSton) # ���� ������ 1�� ���ϰ� ���ӽ���, gamestatus =2 ��
            ## no need for now
            # elif (self.m_ChoiceStonMenu.GetActivationMenu(e.pos) == 1):
            #     self.m_UserSton = 2
            #     self.m_ButtonSound.Play()
            #     self.StartSoloPlay(self.m_UserSton)
            # elif (self.m_ChoiceStonMenu.GetActivationMenu(e.pos) == 2):
            #     self.SetGameStatus(0)
            #     self.m_QuitSound.Play()
        #########################################################
        elif (self.m_GameStatus == 2):
            self.SimulateUserStone(self.m_UserSton)

        elif (self.m_GameStatus == 3):
            time.sleep(0.1)
            self.m_ButtonSound.Play()
            self.SetGameStatus(1)
