# coding=utf-8
from datetime import datetime
import os.path
from sys import argv, exit

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, QEvent, QPoint, Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsOpacityEffect, QListWidgetItem, QFileDialog, QPushButton, QHBoxLayout, \
    QWidget, QSpacerItem, QSizePolicy, QLabel, QVBoxLayout
from pytz import timezone

from Code.Log import print_, Log_Clear, Log_Return
from UI.MainWindow.MainWindow import Ui_MainWindow
from Code.Code import JsonRead, JsonFile, System, JsonWrite, File, Json_Cheak


class RunUi(QMainWindow, Ui_MainWindow):

    SinOut_moveEvent = pyqtSignal(int,int)

    def __init__(self):
        super(RunUi, self).__init__()

        import UI.MainWindow.img_rc
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowType.MacWindowToolBarButtonHint)
        self.show()
        self.L_XY = {'X':self.x(),
                     'Y':self.y()
        }
        self.SinOut_moveEvent.connect(self.L_XY_)

        print_('Info', "程序启动(UI显示): 已成功显示窗体")
        self.__init__setAll()
        self.__init__setToolTipDuration()
        self.__init__setShadow()
        self.X_Y_ = self.frameGeometry().topLeft()

        global Win_XY
        Win_XY = self.geometry()

        self.MEM_Clear_QTime = QTimer()
        self.MEM_Clear_QTime.start(60000)  # 60s一次
        self.MEM_Clear_QTime.timeout.connect(self.MEM_Clear_)


    def MEM_Clear_(self):
        print_('Info','[有可能导致错误]开始进行强制内存清理')
        import gc
        gc.collect()
        print_('Info', '[有可能导致错误]强制内存清理完成')

    # 左边栏"按钮"被点击后（槽）
    def Back_Clicked(self):
        # self.Sidebar_Clicked(Want='Back')
        try:
            print_('Info', '返回系统: 开始返回上一个')
            print(self.H_B)
            if self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
                if len(self.H_B) > 2:
                    B = self.H_B[-1]
                    if 'Left' in B and 'Left_L' in B:
                        if B['Left'] != False:
                            B_1 = B['Left_L']
                            if B_1 == 0:
                                self.Sidebar_Clicked(Want='User', H=False)
                            elif B_1 == 1:
                                self.Sidebar_Clicked(Want='Home', H=False)
                            elif B_1 == 2:
                                self.Sidebar_Clicked(Want='Online', H=False)
                            elif B_1 == 3:
                                self.Sidebar_Clicked(Want='Download', H=False)
                            elif B_1 == 4:
                                self.Sidebar_Clicked(Want='Settings', H=False)
                    if B['Name'] != False:
                        B_1 = B['Index_L']
                        if B_1 == 0:
                            self.Sidebar_Clicked(Want='User', H=False)
                        elif B_1 == 1:
                            self.Sidebar_Clicked(Want='Home', H=False)
                        elif B_1 == 2:
                            self.Sidebar_Clicked(Want='Online', H=False)
                        elif B_1 == 3:
                            self.Sidebar_Clicked(Want='Download', H=False)
                        elif B_1 == 4:
                            self.Sidebar_Clicked(Want='Settings', H=False)
                        B['Name'].setCurrentIndex(B['Index_L'])
                    # B['Name'].setCurrentIndex(B['Index_L'])

                    if B['And_'] != None:
                        for a in B['And_']:
                            a_1 = a[0]
                            a_1.setCurrentIndex(a[1])
                        self.Sidebar_Clicked(Want='Home', H=False)


                    if B['And__'] != None:
                        a = B['And__']
                        a()

                    print_('Info', '返回系统: 返回完成 本次执行配置值: ' + str(self.H_B[-1]))
                    self.H_B.remove(self.H_B[-1])

                elif len(self.H_B) == 2:
                    B = self.H_B[-1]
                    B_1 = B['Index_L']
                    if B['Name'] != False:
                        B['Name'].setCurrentIndex(B['Index_L'])
                    self.Sidebar_Clicked(Want='Home', H=False)

                    if B['And_'] != None:
                        for a in B['And_']:
                            a_1 = a[0]
                            a_1.setCurrentIndex(a[1])
                        self.Sidebar_Clicked(Want='Home', H=False)

                    if B['And__'] != None:
                        a = B['And__']
                        a()


                    print_('Info', '返回系统: 返回完成 本次执行配置值: ' + str(self.H_B[-1]))
                    self.H_B.remove(self.H_B[-1])


                if len(self.H_B)+1 == 1:
                    self.label_Sidebar_Back.setEnabled(False)
                    print_('Info', '返回系统: 返回失败, 无需返回 已将按钮改为禁用')

        except IndexError:
            pass

    def User_Clicked(self):
        self.Sidebar_Clicked(Want='User')

    def Home_Clicked(self):
        self.Sidebar_Clicked(Want='Home')

    def Online_Clicked(self):
        self.Sidebar_Clicked(Want='Online')

    def Download_Clicked(self):
        if self.stackedWidget_page_download.currentIndex() == 0:
            self.stackedWidget_page_download_1.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.Sidebar_Clicked(Want='Download')

    def DownloadPage_Cheak(self):
        """下载页面,在合适的时候对部分控件进行翻页"""
        if self.stackedWidget_page_download.currentIndex() == 0:
            self.stackedWidget_2.setCurrentIndex(0)

    def Settings_Clicked(self):
        self.Sidebar_Clicked(Want='Settings')

    def StackedWidget_Main(self):
        """在切换stackedWidget_main_2后"""
        i = self.stackedWidget_main_2.currentIndex()
        if i == 3:
            # 如果切换到了下载页后
            if self.listWidget_page_1_download.count() == 0:
                self.DownloadPage_stackedWidget_GetGameList_()

    def UserPage_Up_AddUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_addUser.setIcon(icon2)

    def UserPage_Up_AddUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_addUser.setIcon(icon2)

        # 显示窗口
        from Code.AddUserWindow import Dialog_AddUserWindows_
        self.Dialog_AddUserWindows_ = Dialog_AddUserWindows_(self.JsonFile)
        #self.Dialog_AddUserWindows_.sinOut_Win_XY.connect(self.Window_XY)
        self.Dialog_AddUserWindows_.sinOut_OK.connect(self.AddUserWindow_OK)
        self.Dialog_AddUserWindows_.setWindowFlags(
            Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
            Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
            Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
            Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
            Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
            Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
        )
        self.Dialog_AddUserWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground,True)
        self.Dialog_AddUserWindows_.setWindowModality(
            Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
        )

        self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
        self.Dialog_AddUserWindows_.move(
            round(self.MainWindow_xy_size.x() + (self.size().width()/2 - self.Dialog_AddUserWindows_.size().width()/2)),
            round(self.MainWindow_xy_size.y() + (self.size().height()/3)
        ))  # 子界面移动到 居中
        self.UserPage_Up_AddUser()  # 窗口弹出后，主页面不再刷新，所以在窗口弹出前改变
        self.SinOut_moveEvent.connect(self.Dialog_AddUserWindows_.MoveXY)

        self.Dialog_AddUserWindows_.show()

    def UserPage_Up_RefreshUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_refreshUser.setIcon(icon2)

    def UserPage_Up_RefreshUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_refreshUser.setIcon(icon2)

    def UserPage_Up_DeleteUser(self):
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_deleteUser.setIcon(icon2)

    def UserPage_Up_DeleteUser_Pressed(self):
        """再按下按钮时 切换图片"""
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete-pressed.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.pushButton_page_users_up_deleteUser.setIcon(icon2)

    def UserPage_Up_SetChoiceUser(self):
        """账户页 -> 账户列表设置 -> 单/多选"""
        if self.UserPage_setChoice == 'Choice':
            print_('Info', '用户点击: 账户页 -> 账户列表设置 -> 单/多选:设置为多选状态')
            self.UserPage_Up_SetChoiceUser_Set('Choices')
        else:
            print_('Info', '用户点击: 账户页 -> 账户列表设置 -> 单/多选:设置为单选状态')
            self.UserPage_Up_SetChoiceUser_Set('Choice')

    def UserPage_Up_SetChoiceUser_Set(self, a):
        """
            设置"账户"页面的 多选和单选
            a --> 设置为单选还是多选 传入值:'Choice' or' Choices'
        """
        if a == 'Choice':
            # 如果是要设置为单选
            self.UserPage_setChoice = 'Choice'
            self.label_page_users_up_setChoice.setText(
                '<html><head/><body><p><span style=" font-size:16pt;">单选</span>/<span style=" font-size:12pt;">多选</span></p></body></html>')
            self.label_page_users_up_setChoice_icon.setPixmap(
                QtGui.QPixmap(":/widget_Sidebar/images/User_Page_setChoice_Choice.png"))
            self.pushButton_page_users_up_refreshUser.setText('刷新全部')
            self.pushButton_page_users_up_deleteUser.setText('删除全部')
            self.listWidget_users_down.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.Json_MOS['UserPage_setChoice'] = 'Choice'
            JsonWrite(self.Json_MOS, self.JsonFile)

        else:
            # 如果是要设置为多选
            self.UserPage_setChoice = 'Choices'
            self.label_page_users_up_setChoice.setText(
                '<html><head/><body><p><span style=" font-size:16pt;">多选</span>/<span style=" font-size:12pt;">单选</span></p></body></html>')
            self.label_page_users_up_setChoice_icon.setPixmap(
                QtGui.QPixmap(":/widget_Sidebar/images/User_Page_setChoice_Choices.png"))
            self.pushButton_page_users_up_refreshUser.setText('刷新所选')
            self.pushButton_page_users_up_deleteUser.setText('删除所选')
            self.listWidget_users_down.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
            self.Json_MOS['UserPage_setChoice'] = 'Choices'
            JsonWrite(self.Json_MOS, self.JsonFile)

        self.Users_List_Refresh()

    def UserPage_Down_ListWidget_Clicked(self):
        """账户页 -> 账户列表:选择项目"""
        print_('Info', '用户点击: 账户页 -> 账户列表:选择项目')
        if self.UserPage_setChoice == 'Choices':
            item = self.listWidget_users_down.currentItem()
            print(item.text())
            if str(item.checkState()) == 'CheckState.Checked':
                # 如果已经选中
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)
            self.listWidget_users_down.editItem(item)

    def MainPage_GameList(self):
        """主页 -> 游戏列表"""
        self.SetCurrentIndex(self.stackedWidget_page_home, 1, 1, True)
        print_('Info', '用户点击: 主页 -> 游戏列表')

    def MainPage_GameList_List_GameFileAdd(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹"""
        self.SetCurrentIndex(self.stackedWidget_page_home, 2, 1, True)
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹')
        self.MainPage_GameList_List_GameFileAdd_Add()

    def MainPage_GameList_List_Refresh(self):
        """
            主页 -> 游戏列表 -> 刷新
        """
        self.listWidget_page_home_game_left.clear()
        self.listWidget_page_home_game_right_gamefile_game.clear()
        self.GameFiles_Read_Thread_Start()

    def MainPage_GameList_List_GameFileAdd_Add(self):
        """
            主页 -> 游戏列表 -> 添加游戏文件夹\n
            主页 -> 游戏列表 -> 添加游戏文件夹 -> 重新选择\n

            弹出选择窗口
        """
        dir = QFileDialog()
        dir.setFileMode(QFileDialog.FileMode.Directory)
        dir.setDirectory(self.File_Parent)
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择窗口:弹出')
        icon = QIcon()
        if dir.exec():
            F = dir.selectedFiles()  # 选择的路径
            print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择目录: ' + str(F[0]))
            self.label_home_game_file_add_file_2.setText(str(F[0]))
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Main_Page_GameFile_AddAgain.png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        else:
            print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 选择窗口:弹出 -> 取消')
            self.pushButton_game_file_add_again.setText('选择文件夹')
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Add.png"),
                            QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_game_file_add_again.setIcon(icon)

    def MainPage_GameList_List_GameFileAdd_TextChanged(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 名称:填写"""
        if self.lineEdit_game_file_add.styleSheet() == "border:2px solid rgb(255, 47, 146);":
            self.lineEdit_game_file_add.setStyleSheet("")

    def MainPage_GameList_List_GameFileAdd_OK(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 确定(保存)"""
        print_('Info', '用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 确定(保存)')
        n = self.lineEdit_game_file_add.text()
        if n  == '':
            self.lineEdit_game_file_add.setStyleSheet("border:2px solid rgb(255, 47, 146);")
        else:
            from Code.MC_Code.GameFile import GameFile
            f = self.label_home_game_file_add_file_2.text()
            a = GameFile(self.JsonFile,self.Json_MOS)
            a.GameFile_Add(n,f)
            print_('Info', '游戏文件夹(添加): 添加文件夹 完成')
            self.stackedWidget_page_home.setCurrentIndex(1)
            self.MainPage_GameList_List_Refresh()  # 刷新
            self.label_home_game_file_add_file_2.setText('请先选择目录')
            self.lineEdit_game_file_add.setText('')



    def MainPage_GameList_List_GameFileAdd_Cancel(self):
        """主页 -> 游戏列表 -> 添加游戏文件夹 -> 取消"""
        self.stackedWidget_page_home.setCurrentIndex(1)
        print_('Info','用户点击: 主页 -> 游戏列表 -> 添加游戏文件夹 -> 取消')

    def MainPage_GameList_List(self):
        """主页 -> 游戏列表 -> 选中一项"""
        item = self.listWidget_page_home_game_left.currentItem()
        N = item.text()
        # 改变配置文件中的当前选中
        print(self.listWidget_page_home_game_left.currentRow())
        self.Json_MOS['GameFile_List_Clicked'] = int(self.listWidget_page_home_game_left.currentRow())
        JsonWrite(self.Json_MOS,self.JsonFile)

        F = self.Json_MOS['GameFile'][N]['File']
        self.listWidget_page_home_game_right_gamefile_game.clear()
        self.GameFiles_ReturnGameList_Thread_Start(F)

    def DownloadPage_Game_Clicked(self):
        """下载页 -> 游戏本体"""
        self.stackedWidget_2.setCurrentIndex(0)
        if self.stackedWidget_page_download.currentIndex() == 0:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 0, 3, True, And__=self.DownloadPage_Cheak)
        self.stackedWidget_page_download_1.setCurrentIndex(0)
        self.stackedWidget_page_download_1_main.setCurrentIndex(0)

    def DownloadPage_Game_Refresh_Clicked(self):
        """下载页 -> 刷新"""
        self.pushButton_page_download_mc_refresh.setEnabled(False)
        self.DownloadPage_stackedWidget_GetGameList_()

    def DownloadPage_Word_Clicked(self):
        """下载页 -> 世界存档"""
        self.stackedWidget_2.setCurrentIndex(1)
        if self.stackedWidget_page_download.currentIndex() == 1:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 1, 3, True, And__=self.DownloadPage_Cheak)

    def DownloadPage_Mode_Clicked(self):
        """下载页 -> mod"""
        self.stackedWidget_2.setCurrentIndex(1)
        if self.stackedWidget_page_download.currentIndex() == 2:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 2, 3, True, And__=self.DownloadPage_Cheak)

    def DownloadPage_Conformity_Clicked(self):
        """下载页 -> 整合包"""
        self.stackedWidget_2.setCurrentIndex(1)
        if self.stackedWidget_page_download.currentIndex() == 3:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 3, 3, True, And__=self.DownloadPage_Cheak)

    def DownloadPage_Resource_Clicked(self):
        """下载页 -> 资源包"""
        self.stackedWidget_2.setCurrentIndex(1)
        if self.stackedWidget_page_download.currentIndex() == 4:
            pass
        else:
            self.SetCurrentIndex(self.stackedWidget_page_download, 4, 3, True, And__=self.DownloadPage_Cheak)

    def DownloadPage_stackedWidget_setButtonStyleSheet(self,I):
        """
            在下载页面的stackedWidget改变时, 设置 下载页 -> 左上方的按钮控件样式
            :param I : 将下载页面的stackedWidget设置为了第……页
        """
        S = 'border-bottom: 2px solid rgb(0, 119, 225);'
        if I == 0:
            if self.label_page_download_2_game.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet(S)
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')
                if self.listWidget_page_1_download.count() == 0:
                    self.DownloadPage_stackedWidget_GetGameList_()
        elif I == 1:
            if self.label_page_download_2_word.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet(S)
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 2:
            if self.label_page_download_2_mode.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet(S)
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 3:
            if self.label_page_download_2_conformity.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet(S)
                self.label_page_download_2_resource.setStyleSheet('')

        elif I == 4:
            if self.label_page_download_2_resource.styleSheet() != S:
                self.label_page_download_2_game.setStyleSheet('')
                self.label_page_download_2_word.setStyleSheet('')
                self.label_page_download_2_mode.setStyleSheet('')
                self.label_page_download_2_conformity.setStyleSheet('')
                self.label_page_download_2_resource.setStyleSheet(S)


    def DownloadPage_stackedWidget_GetGameList_(self):
        """启动多线程请求版本列表"""
        # release: 原版 / Snapshot: 快照版/ old_alpha: 远古版本

        self.pushButton_page_download_mc_refresh.setEnabled(False)

        self.label_page_download_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
        self.label_page_download_loading.setMovie(self.label_page_download_loading_)
        self.label_page_download_loading_.start()
        self.stackedWidget_page_download.setCurrentIndex(5)

        try:
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.quit()
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.exit()
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.wait()
        except:
            pass
        self.listWidget_page_1_download.clear()
        if self.checkBox_page_download_mc_official.isChecked() == True:
            self.Download_MC_Kind = 'release'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_Grass.png'
        elif self.checkBox_page_download_mc_test.isChecked() == True:
            self.Download_MC_Kind = 'snapshot'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_CommandBlock.png'
        elif self.checkBox_page_download_mc_previously.isChecked() == True:
            self.Download_MC_Kind = 'old_alpha'
            self.Download_MC_Kind_IconFile = ':/widget_Sidebar/images/MC_CraftingTable.png'
        # print(self.File)
        self.listWidget_page_1_download.clear()
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_ = DownloadPage_stackedWidget_GetGameList_Thread(
            'MCBBS', self.File, self.Download_MC_Kind)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.SinOut.connect(
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.SinOut_OK.connect(
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_OK)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.SinOut_Error.connect(
            self.DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_Error)
        self.DownloadPage_stackedWidget_GetGameList_Thread_Start_.start()


    def DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut(self,name,time):
        """
            得到"多线程请求版本列表"线程输出 并在列表中添加控件
            :param name: 版本名字
            :param time: 发布时间
        """
        item = QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.Download_MC_Kind_IconFile), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        item.setText(name)
        widget = QWidget()
        QVBoxLayout_ = QVBoxLayout()

        l_l = QLabel()
        l_l.setText(name)
        font = QFont()
        font.setPixelSize(17)
        l_l.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(l_l.sizePolicy().hasHeightForWidth())
        l_l.setSizePolicy(sizePolicy)


        l_l2 = QLabel()
        l_l2.setText(time)
        font = QFont()
        font.setPixelSize(11)
        l_l2.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(l_l2.sizePolicy().hasHeightForWidth())
        l_l2.setSizePolicy(sizePolicy)

        QVBoxLayout_.addWidget(l_l)
        QVBoxLayout_.addWidget(l_l2)
        QVBoxLayout_.setContentsMargins(0, 0, 0, 0)
        QVBoxLayout_.setSpacing(3)

        widget.setLayout(QVBoxLayout_)
        widget.setContentsMargins(0, 0, 0, 0)

        self.listWidget_page_1_download.addItem(item)
        self.listWidget_page_1_download.setItemWidget(item, widget)
    
    def DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_OK(self):
        """
            得到"多线程请求版本列表"线程完成信号
        """
        self.stackedWidget_page_download.setCurrentIndex(0)
        self.stackedWidget_page_download_1_main.setCurrentIndex(0)
        self.label_page_download_loading_.stop()
        self.pushButton_page_download_mc_refresh.setEnabled(True)

    def DownloadPage_stackedWidget_GetGameList_Thread_Start_SinOut_Error(self):
        """
            得到"多线程请求版本列表"线程错误信号
        """
        self.stackedWidget_page_download.setCurrentIndex(0)
        self.stackedWidget_page_download_1_main.setCurrentIndex(1)
        self.label_page_download_loading_.stop()

    def DownloadPage_stackedWidget_GameList_Clicked(self):
        """下载页面 -> 原版下载列表: 点击项目"""
        self.stackedWidget_2.setCurrentIndex(1)
        item = self.listWidget_page_1_download.currentItem()
        self.DownloadPage_V = item.text()
        self.label_page_download_1_install_bottom.setText(str(self.DownloadPage_V) + '安装')
        self.label_page_download_1_install_forge_up_state.setText('正在获取')
        self.label_page_download_1_install_forge_up_state_2.setText('')
        self.label_page_download_1_install_fabric_up_state.setText('正在获取')
        self.label_page_download_1_install_fabric_up_state_2.setText('')
        self.label_page_download_1_install_optifine_up_state.setText('正在获取')
        self.label_page_download_1_install_optifine_up_state_2.setText('')
        self.label_page_download_1_install_forge_up_state.setStyleSheet('')
        self.label_page_download_1_install_fabric_up_state.setStyleSheet('')
        self.label_page_download_1_install_optifine_up_state.setStyleSheet('')
        self.pushButton_page_download_1_install_forge_up_close.setEnabled(False)
        self.pushButton_page_download_1_install_fabric_up_close.setEnabled(False)
        self.pushButton_page_download_1_install_optifine_up_close.setEnabled(False)
        self.pushButton_page_download_1_install_bottom_ok.setEnabled(False)
        self.lineEdit_page_download_1_install_bottom_GameName.setPlaceholderText(str(self.DownloadPage_V))
        self.lineEdit_page_download_1_install_bottom_GameName.setText(str(self.DownloadPage_V))
        self.SetCurrentIndex(self.stackedWidget_page_download_1, 1, 3, True, [[self.stackedWidget_2,0]])
        self.listWidget_page_download_1_install_forge.clear()
        self.listWidget_page_download_1_install_fabric.clear()
        self.listWidget_page_download_1_install_optifine.clear()
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start(str(self.DownloadPage_V))

    def DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start(self,MCName):
        """启动 根据版本获取Forge,Fabric,Optifine列表"""
        self.widget_page_download_1_install_forge.setEnabled(True)
        self.widget_page_download_1_install_fabric.setEnabled(True)
        self.widget_page_download_1_install_optifine.setEnabled(True)

        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge = DownloadPage_stackedWidget_GameList_Clicked_Get_Thread('Forge',MCName)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge.SinOut.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge.SinOut_OK.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_OK)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge.SinOut_Error.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_Error)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge.start()

        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric = DownloadPage_stackedWidget_GameList_Clicked_Get_Thread('Fabric', MCName)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric.SinOut.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric.SinOut_OK.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_OK)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric.SinOut_Error.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_Error)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric.start()

        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine = DownloadPage_stackedWidget_GameList_Clicked_Get_Thread('Optifine', MCName)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine.SinOut.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine.SinOut_OK.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_OK)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine.SinOut_Error.connect(self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_Error)
        self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine.start()

    def DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut(self, Kind, Name, Time, State):
        """
            根据版本获取Forge,Fabric,Optifine列表线程的SinOut
            :param Kind: 种类(Forge,Fabric,Optifine)
            :param Name: 名字
            :param Time: 时间
            :param State: 状态(Stable,Bata)
        """
        # print(Kind + '|' + Name + '|' + Time + '|' + State)
        if Kind == 'Forge':
            U = self.listWidget_page_download_1_install_forge
            IconFile = ':/widget_Sidebar/images/MC_Forge.png'
            Layout_ = QVBoxLayout()
        elif Kind == 'Fabric':
            U = self.listWidget_page_download_1_install_fabric
            IconFile = ':/widget_Sidebar/images/MC_Fabric.png'
            Layout_ = QHBoxLayout()
        elif Kind == 'Optifine':
            U = self.listWidget_page_download_1_install_optifine
            IconFile = ':/widget_Sidebar/images/MC_Optifine.png'
            Layout_ = QHBoxLayout()

        item = QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(IconFile), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        widget = QWidget()


        # l_1
        l_1 = QLabel()
        l_1.setText(Name)
        font = QFont()
        font.setPixelSize(17)
        l_1.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(l_1.sizePolicy().hasHeightForWidth())
        l_1.setSizePolicy(sizePolicy)

        if Time != '':
            # l_2
            l_2 = QLabel()
            l_2.setText(Time)
            font = QFont()
            font.setPixelSize(11)
            l_2.setFont(font)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(l_2.sizePolicy().hasHeightForWidth())
            l_2.setSizePolicy(sizePolicy)

        if State != '':
            if State == 'Bata':
                T = ' 测试版 '
                S = "background-color: rgb(255, 147, 0);color: rgb(255, 255, 255);border-radius: 4px;"
            else:
                T = ' 稳定版 '
                S = "background-color: rgb(94, 99, 204);color: rgb(255, 255, 255);border-radius: 4px;"
            item.setText(Name + '|' + T)
            l_3 = QLabel()
            l_3.setText(T)
            font = QFont()
            font.setPixelSize(13)
            l_3.setFont(font)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(l_3.sizePolicy().hasHeightForWidth())
            l_3.setSizePolicy(sizePolicy)
            l_3.setStyleSheet(S)
            l_3.setMinimumSize(0,20)

            l_4 = QLabel()
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(l_3.sizePolicy().hasHeightForWidth())
            l_4.setSizePolicy(sizePolicy)

        else:
            item.setText(Name)


        # add in Widget
        Layout_.addWidget(l_1)
        if Time != '':
            Layout_.addWidget(l_2)
        if State != '':
            Layout_.addWidget(l_3)
            Layout_.addWidget(l_4)
        Layout_.setContentsMargins(0, 0, 0, 0)
        Layout_.setSpacing(3)
        widget.setLayout(Layout_)
        widget.setContentsMargins(0, 0, 0, 0)

        # add in listWidget item
        U.addItem(item)
        U.setItemWidget(item, widget)

    def DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_OK(self,Kind,Z=True):
        """
            根据版本获取Forge,Fabric,Optifine列表线程的SinOut_OK
            :param Kind: 种类(Forge,Fabric,Optifine)
            :param Z: 有没项目(True:有)
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/MCDownloadPage_Close.png"),
                       QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        if Z:
            if Kind == 'Forge':
                self.label_page_download_1_install_forge_up_state.setText('')
                self.pushButton_page_download_1_install_forge_up_close.setIcon(icon)
                self.pushButton_page_download_1_install_forge_up_close.setEnabled(True)
            elif Kind == 'Fabric':
                self.label_page_download_1_install_fabric_up_state.setText('')
                self.pushButton_page_download_1_install_fabric_up_close.setIcon(icon)
                self.pushButton_page_download_1_install_fabric_up_close.setEnabled(True)
            elif Kind == 'Optifine':
                self.label_page_download_1_install_optifine_up_state.setText('')
                self.pushButton_page_download_1_install_optifine_up_close.setIcon(icon)
                self.pushButton_page_download_1_install_optifine_up_close.setEnabled(True)
        else:
            print('=========')
            print(Kind)
            if Kind == 'Forge':
                self.label_page_download_1_install_forge_up_state.setText('无')
                self.pushButton_page_download_1_install_forge_up_close.setEnabled(False)
                self.widget_page_download_1_install_forge.setEnabled(False)
                self.pushButton_page_download_1_install_forge_up_close.setIcon(icon)
            elif Kind == 'Fabric':
                self.label_page_download_1_install_fabric_up_state.setText('无')
                self.pushButton_page_download_1_install_fabric_up_close.setEnabled(False)
                self.widget_page_download_1_install_fabric.setEnabled(False)
                self.pushButton_page_download_1_install_fabric_up_close.setIcon(icon)
            elif Kind == 'Optifine':
                self.label_page_download_1_install_optifine_up_state.setText('无')
                self.pushButton_page_download_1_install_optifine_up_close.setEnabled(False)
                self.widget_page_download_1_install_optifine.setEnabled(False)
                self.pushButton_page_download_1_install_optifine_up_close.setIcon(icon)

    def DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_SinOut_Error(self,Kind):
        if Kind == 'Forge':
            self.label_page_download_1_install_forge_up_state.setText('获取出错,点击右侧按钮重试')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh-pressed.png"),
                             QtGui.QIcon.Mode.Normal,
                             QtGui.QIcon.State.Off)
            self.pushButton_page_download_1_install_forge_up_close.setIcon(icon)
            self.pushButton_page_download_1_install_forge_up_close.setEnabled(True)
            del icon
        elif Kind == 'Fabric':
            self.label_page_download_1_install_fabric_up_state.setText('获取出错,点击右侧按钮重试')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh-pressed.png"),
                           QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.pushButton_page_download_1_install_fabric_up_close.setIcon(icon)
            self.pushButton_page_download_1_install_fabric_up_close.setEnabled(True)
            del icon
        elif Kind == 'Optifine':
            self.label_page_download_1_install_optifine_up_state.setText('获取出错,点击右侧按钮重试')
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Refresh-pressed.png"),
                           QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            self.pushButton_page_download_1_install_optifine_up_close.setIcon(icon)
            self.pushButton_page_download_1_install_optifine_up_close.setEnabled(True)
            del icon


    def DownloadPage_stackedWidget_install_fabric(self):
        """下载页面 -> 选择安装 -> Fabric"""
        self.SetCurrentIndex(self.stackedWidget_page_download_1, 3, 3, True)

    def DownloadPage_stackedWidget_install_forge(self):
        """下载页面 -> 选择安装 -> Forge"""
        self.SetCurrentIndex(self.stackedWidget_page_download_1, 2, 3, True)
    def DownloadPage_stackedWidget_install_optifine(self):
        """下载页面 -> 选择安装 -> Optifine"""
        self.SetCurrentIndex(self.stackedWidget_page_download_1, 4, 3, True)
    def DownloadPage_stackedWidget_install_forge_itemPressed(self):
        """下载页面 -> 选择安装 -> Forge -> 点击项目"""
        item = self.listWidget_page_download_1_install_forge.currentItem()
        self.label_page_download_1_install_forge_up_state.setText(item.text())
        self.Back_Clicked()

    def DownloadPage_stackedWidget_install_fabric_itemPressed(self):
        """下载页面 -> 选择安装 -> Fabric -> 点击项目"""
        item = self.listWidget_page_download_1_install_fabric.currentItem()
        t = item.text().split('|')
        t_n = t[0]
        t_s = t[1]
        self.label_page_download_1_install_fabric_up_state_2.setText(t_n)
        if t_s == ' 测试版 ':
            s = "background-color: rgb(255, 147, 0);color: rgb(255, 255, 255);border-radius: 4px;"
        else:
            s = "background-color: rgb(94, 99, 204);color: rgb(255, 255, 255);border-radius: 4px;"
        self.label_page_download_1_install_fabric_up_state.setText(t_s)
        self.label_page_download_1_install_fabric_up_state.setStyleSheet(s)
        self.Back_Clicked()

    def DownloadPage_stackedWidget_install_optifine_itemPressed(self):
        """下载页面 -> 选择安装 -> Optifine -> 点击项目"""
        item = self.listWidget_page_download_1_install_optifine.currentItem()
        t = item.text().split('|')
        t_n = t[0]
        t_s = t[1]
        self.label_page_download_1_install_optifine_up_state_2.setText(t_n)
        if t_s == ' 测试版 ':
            s = "background-color: rgb(255, 147, 0);color: rgb(255, 255, 255);border-radius: 4px;"
        else:
            s = "background-color: rgb(94, 99, 204);color: rgb(255, 255, 255);border-radius: 4px;"
        self.label_page_download_1_install_optifine_up_state.setText(t_s)
        self.label_page_download_1_install_optifine_up_state.setStyleSheet(s)
        self.Back_Clicked()

    def DownloadPage_stackedWidget_install_forge_close(self):
        """下载页面 -> 选择安装 -> Forge -> 取消"""
        if self.label_page_download_1_install_forge_up_state.text() != '获取出错,点击右侧按钮重试':
            self.label_page_download_1_install_forge_up_state.setText('')
            self.label_page_download_1_install_forge_up_state_2.setText('')
        else:
            self.pushButton_page_download_1_install_forge_up_close.setEnabled(False)
            self.label_page_download_1_install_forge_up_state.setText('正在重试')
            self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Forge.start()

    def DownloadPage_stackedWidget_install_fabric_close(self):
        """下载页面 -> 选择安装 -> Fabric -> 取消"""
        if self.label_page_download_1_install_fabric_up_state.text() != '获取出错,点击右侧按钮重试':
            self.label_page_download_1_install_fabric_up_state.setText('')
            self.label_page_download_1_install_fabric_up_state_2.setText('')
        else:
            self.pushButton_page_download_1_install_fabric_up_close.setEnabled(False)
            self.label_page_download_1_install_fabric_up_state.setText('正在重试')
            self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Fabric.start()

    def DownloadPage_stackedWidget_install_optifine_close(self):
        """下载页面 -> 选择安装 -> Optifine -> 取消"""
        if self.label_page_download_1_install_optifine_up_state.text() != '获取出错,点击右侧按钮重试':
            self.label_page_download_1_install_optifine_up_state.setText('')
            self.label_page_download_1_install_optifine_up_state_2.setText('')
        else:
            self.pushButton_page_download_1_install_optifine_up_close.setEnabled(False)
            self.label_page_download_1_install_optifine_up_state.setText('正在重试')
            self.DownloadPage_stackedWidget_GameList_Clicked_Get_Thread_Start_Optifine.start()

    def DownloadPage_stackedWidget_install_ok(self):
        """下载页面 -> 选择安装 -> 安装"""
        if self.lineEdit_page_download_1_install_bottom_GameName.text() == '':
            self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet("border: 2px solid rgb(255, 38, 0);")
        else:
            # 显示窗口
            self.pushButton_page_download_1_install_bottom_ok.setEnabled(False)
            from Code.GameInstallWindow import Dialog_GameInstallWindows_
            GameFile_M = self.Json_MOS['GameFile_List'][self.Json_MOS['GameFile_List_Clicked']]
            GameFile_M = self.Json_MOS['GameFile'][GameFile_M]['File']
            Name = self.lineEdit_page_download_1_install_bottom_GameName.text()
            GameFile_V  = os.path.join(GameFile_M,'versions',Name)
            V_JsonFile = os.path.join(self.File,'Versions','Versions.json')
            V_Forge = self.label_page_download_1_install_forge_up_state_2.text()
            V_Fabric = self.label_page_download_1_install_fabric_up_state_2.text()
            V_Optifine = self.label_page_download_1_install_optifine_up_state_2.text()
            if V_Forge == '':
                V_Forge = None
            if V_Fabric == '':
                V_Fabric = None
            if V_Optifine == '':
                V_Optifine = None
            AssetsFileDownloadMethod = 'A'
            Sha1Cleck = True
            MaxConcurrence = 100
            # ProgressGetModule = self.GameInstallWindow_Progress
            self.Dialog_GameInstallWindows_ = Dialog_GameInstallWindows_(GameFile_M, GameFile_V, self.File, self.Json_MOS['Download_Source'], V_JsonFile,
                                                                        self.DownloadPage_V, Name, V_Forge,V_Fabric,V_Optifine,
                                                                        self.Json_MOS['System'],self.Json_MOS['System_V'],self.Json_MOS['System_Places'],
                                                                        AssetsFileDownloadMethod,Sha1Cleck,MaxConcurrence,self.GameInstallError)
            #self.Dialog_GameInstallWindows_.sinOut_Win_XY.connect(self.Window_XY)
            self.Dialog_GameInstallWindows_.sinOut_OK.connect(self.GameInstallWindow_OK)
            self.Dialog_GameInstallWindows_.sinOut_Error.connect(self.GameInstallWindow_Error)
            self.Dialog_GameInstallWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.Dialog_GameInstallWindows_.setWindowFlags(
                Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
                Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
                Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
                Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
                Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
                Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
            )

            self.Dialog_GameInstallWindows_.setWindowModality(
                Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
            )

            self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
            self.Dialog_GameInstallWindows_.move(
                round(self.MainWindow_xy_size.x() + (
                            self.size().width() / 2 - self.Dialog_GameInstallWindows_.size().width() / 2)),
                round(self.MainWindow_xy_size.y() + (self.size().height() / 3)
                      ))  # 子界面移动到 居中
            self.SinOut_moveEvent.connect(self.Dialog_GameInstallWindows_.MoveXY)

            self.pushButton_page_download_1_install_bottom_ok.setEnabled(True)
            self.Dialog_GameInstallWindows_.show()

            self.Dialog_GameInstallWindows_.Run()

    def GameInstallError(self, GameName, Game_V, ErrorKind, ErrorCause, ErrorInfo):
        """当游戏安装出现错误时, 调用错误弹框显示函数"""
        self.GameInstallErrorWindow(GameName, Game_V, ErrorKind, ErrorCause, ErrorInfo)

    def GameInstallErrorWindow(self, GameName, Game_V, ErrorKind, ErrorCause, ErrorInfo):
        """显示游戏安装错误页面"""
        from Code.GameInstallErrorWindow import Dialog_GameInstellErrorWindows_
        self.Dialog_GameInstellErrorWindows_ = Dialog_GameInstellErrorWindows_(GameName, Game_V, ErrorKind, ErrorCause, ErrorInfo)
        # self.Dialog_DelateGameWindows_.sinOut_Win_XY.connect(self.Window_XY)
        self.Dialog_GameInstellErrorWindows_.sinOut_OK.connect(self.GameInstallErrorWindow_SinOut_OK)
        self.Dialog_GameInstellErrorWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.Dialog_GameInstellErrorWindows_.setWindowFlags(
            Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
            Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
            Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
            Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
            Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
            Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
        )

        self.Dialog_GameInstellErrorWindows_.setWindowModality(
            Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
        )

        self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
        self.Dialog_GameInstellErrorWindows_.move(
            round(self.MainWindow_xy_size.x() + (
                        self.size().width() / 2 - self.Dialog_GameInstellErrorWindows_.size().width() / 2)),
            round(self.MainWindow_xy_size.y() + (self.size().height() / 3)
                  ))  # 子界面移动到 居中
        self.SinOut_moveEvent.connect(self.Dialog_GameInstellErrorWindows_.MoveXY)

        self.Dialog_GameInstellErrorWindows_.show()

    def GameInstallErrorWindow_SinOut_OK(self):
        self.SinOut_moveEvent.disconnect(self.Dialog_GameInstellErrorWindows_.MoveXY)
        self.pushButton_page_download_1_install_bottom_ok.setEnabled(True)

    def GameInstallWindow_Error(self):
        """安装时出现错误"""
        self.listWidget_page_download_1_install_forge.clear()
        self.listWidget_page_download_1_install_fabric.clear()
        self.listWidget_page_download_1_install_optifine.clear()

        self.SinOut_moveEvent.disconnect(self.Dialog_GameInstallWindows_.MoveXY)
        self.stackedWidget_page_download_1.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.pushButton_page_download_1_install_bottom_ok.setEnabled(True)

    def GameInstallWindow_OK(self):
        """安装完成"""
        # 显示完成的窗口
        # 切换页面
        self.listWidget_page_download_1_install_forge.clear()
        self.listWidget_page_download_1_install_fabric.clear()
        self.listWidget_page_download_1_install_optifine.clear()

        self.SinOut_moveEvent.disconnect(self.Dialog_GameInstallWindows_.MoveXY)
        self.stackedWidget_page_download_1.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)

    def DownloadPage_stackedWidget_install_lineEdit(self):
        """下载页面 -> 选择安装 -> 输入游戏名"""
        T = self.lineEdit_page_download_1_install_bottom_GameName.text()
        i = self.Json_MOS['GameFile_List_Clicked']
        text = self.Json_MOS['GameFile_List'][i]
        F = self.Json_MOS['GameFile'][text]['File']
        F = os.path.join(F,'versions',T)
        if T != '':
            if os.path.isdir(F):
                self.label_page_download_1_install_bottom_GameName.setText('游戏名(版本名重复,请换一个名字)')
                self.label_page_download_1_install_bottom_GameName.setStyleSheet("color: 2px solid rgb(255, 38, 0);")
                self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet("border: 2px solid rgb(255, 38, 0);")
            else:
                if len(T.split('/')) == 1 and len(T.split('\\')) == 1 and len(T.split('\\')) == 1:
                    if len(T.split(' 缺少Jar文件, 并且Json文件可能已损坏')) == 1 and len(T.split(' 缺少Jar文件')) == 1 and len(T.split(' 缺少Json文件')) == 1 and len(T.split(' Json文件可能已损坏')) == 1:
                        self.label_page_download_1_install_bottom_GameName.setText('游戏名')
                        self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet(
                            "border: 2px solid rgb(56, 56, 56);")
                        self.pushButton_page_download_1_install_bottom_ok.setEnabled(True)
                    else:
                        self.label_page_download_1_install_bottom_GameName.setText('游戏名(你隔着卡Bug呢?)')
                        self.label_page_download_1_install_bottom_GameName.setStyleSheet(
                            "color: 2px solid rgb(255, 38, 0);")
                        self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet(
                            "border: 2px solid rgb(255, 38, 0);")
                        self.pushButton_page_download_1_install_bottom_ok.setEnabled(False)

                else:
                    self.label_page_download_1_install_bottom_GameName.setText('游戏名(含有特殊字符)')
                    self.label_page_download_1_install_bottom_GameName.setStyleSheet(
                        "color: 2px solid rgb(255, 38, 0);")
                    self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet(
                        "border: 2px solid rgb(255, 38, 0);")
                    self.pushButton_page_download_1_install_bottom_ok.setEnabled(False)

        else:
            self.label_page_download_1_install_bottom_GameName.setText('游戏名')
            self.lineEdit_page_download_1_install_bottom_GameName.setStyleSheet("border: 2px solid rgb(56, 56, 56);")
            self.pushButton_page_download_1_install_bottom_ok.setEnabled(False)


    def DownloadPage_MC_Official(self):
        self.checkBox_page_download_mc_official.setEnabled(False)
        self.checkBox_page_download_mc_test.setEnabled(True)
        self.checkBox_page_download_mc_previously.setEnabled(True)

        self.checkBox_page_download_mc_test.setChecked(False)
        self.checkBox_page_download_mc_previously.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()
    def DownloadPage_MC_Text(self):
        self.checkBox_page_download_mc_official.setEnabled(True)
        self.checkBox_page_download_mc_test.setEnabled(False)
        self.checkBox_page_download_mc_previously.setEnabled(True)

        self.checkBox_page_download_mc_official.setChecked(False)
        self.checkBox_page_download_mc_previously.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()

    def DownloadPage_MC_Previously(self):
        self.checkBox_page_download_mc_official.setEnabled(True)
        self.checkBox_page_download_mc_test.setEnabled(True)
        self.checkBox_page_download_mc_previously.setEnabled(False)

        self.checkBox_page_download_mc_official.setEnabled(True)
        self.checkBox_page_download_mc_official.setChecked(False)
        self.checkBox_page_download_mc_test.setChecked(False)
        self.DownloadPage_stackedWidget_GetGameList_()


    def DownloadPage_stackedWidget_CurrentIndex(self):
        """当下载页面的stackedWidget传来页数改变的信号时 调用DownloadPage_stackedWidget_setButtonStyleSheet"""
        I = self.stackedWidget_page_download.currentIndex()
        print(I)
        if I == 5:
            pass
        else:
            self.DownloadPage_stackedWidget_setButtonStyleSheet(I)

    def SettingsPage_Page_Settings_Game_Settings(self):
        """设置页面 -> 游戏全局设置"""
        if self.stackedWidget_page_settings.currentIndex() == 0:
            pass
        else:
            self.label_page_settings_game_settings.setStyleSheet("border-bottom: 2px solid rgb(0, 119, 225);")
            self.label_page_settings_appearance.setStyleSheet('')
            self.label_page_settings_download.setStyleSheet('')
            self.label_page_settings_else.setStyleSheet('')
            self.label_page_settings_about.setStyleSheet('')
            self.SetCurrentIndex(self.stackedWidget_page_settings, 0, 4, True)

    def SettingsPage_Page_Settings_Game_Appearance(self):
        """设置页面 -> 外观"""
        if self.stackedWidget_page_settings.currentIndex() == 1:
            pass
        else:
            self.label_page_settings_game_settings.setStyleSheet('')
            self.label_page_settings_appearance.setStyleSheet("border-bottom: 2px solid rgb(0, 119, 225);")
            self.label_page_settings_download.setStyleSheet('')
            self.label_page_settings_else.setStyleSheet('')
            self.label_page_settings_about.setStyleSheet('')
            self.SetCurrentIndex(self.stackedWidget_page_settings, 1, 4, True)

    def SettingsPage_Page_Settings_Game_Download(self):
        """设置页面 -> 下载"""
        if self.stackedWidget_page_settings.currentIndex() == 2:
            pass
        else:
            self.label_page_settings_game_settings.setStyleSheet('')
            self.label_page_settings_appearance.setStyleSheet('')
            self.label_page_settings_download.setStyleSheet("border-bottom: 2px solid rgb(0, 119, 225);")
            self.label_page_settings_else.setStyleSheet('')
            self.label_page_settings_about.setStyleSheet('')
            self.SetCurrentIndex(self.stackedWidget_page_settings, 2, 4, True)

    def SettingsPage_Page_Settings_Game_Else(self):
        """设置页面 -> 其他"""
        if self.stackedWidget_page_settings.currentIndex() == 3:
            pass
        else:
            self.label_page_settings_game_settings.setStyleSheet('')
            self.label_page_settings_appearance.setStyleSheet('')
            self.label_page_settings_download.setStyleSheet('')
            self.label_page_settings_else.setStyleSheet("border-bottom: 2px solid rgb(0, 119, 225);")
            self.label_page_settings_about.setStyleSheet('')
            self.SetCurrentIndex(self.stackedWidget_page_settings, 3, 4, True)

    def SettingsPage_Page_Settings_Game_About(self):
        """设置页面 -> 关于"""
        if self.stackedWidget_page_settings.currentIndex() == 4:
            pass
        else:
            self.label_page_settings_game_settings.setStyleSheet('')
            self.label_page_settings_appearance.setStyleSheet('')
            self.label_page_settings_download.setStyleSheet('')
            self.label_page_settings_else.setStyleSheet('')
            self.label_page_settings_about.setStyleSheet("border-bottom: 2px solid rgb(0, 119, 225);")
            self.SetCurrentIndex(self.stackedWidget_page_settings, 4, 4, True)

    def SettingsPage_Background_None_Clicked(self):
        """设置页面 -> 背景设置:选择：无"""
        self.MainWinowMainBackground(None)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：无')

    def SettingsPage_Background_1_Clicked(self):
        """设置页面 -> 背景设置:选择：1(清爽橙黄)"""
        self.MainWinowMainBackground(1)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：1(清爽橙黄)')

    def SettingsPage_Background_2_Clicked(self):
        """设置页面 -> 背景设置:选择：2(梦幻浅蓝)"""
        self.MainWinowMainBackground(2)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：2(梦幻浅蓝)')

    def SettingsPage_Background_3_Clicked(self):
        """设置页面 -> 背景设置:选择：3(梦幻浅红)"""
        self.MainWinowMainBackground(3)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：3(梦幻浅红)')

    def SettingsPage_Background_4_Clicked(self):
        """设置页面 -> 背景设置:选择：4(三彩斑斓)"""
        self.MainWinowMainBackground(4)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：4(三彩斑斓)')

    def SettingsPage_Background_5_Clicked(self):
        """设置页面 -> 背景设置:选择：5(蓝白相照)"""
        self.MainWinowMainBackground(5)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：5(蓝白相照)')

    def SettingsPage_Background_6_Clicked(self):
        """设置页面 -> 背景设置:选择：6(深蓝天空)"""
        self.MainWinowMainBackground(6)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：6(深蓝天空)')

    def SettingsPage_Background_7_Clicked(self):
        """设置页面 -> 背景设置:选择：7(粉色迷雾)"""
        self.MainWinowMainBackground(7)
        print_('Info', '用户点击: 设置页面 -> 背景设置:选择：7(粉色迷雾)')

    def SettingsPage_Sidebar_horizontalSlider(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动"""
        i = self.horizontalSlider_page_settings_sidebar.value()
        i_2 = i * 30
        self.spinBox_page_settings_sidebar.setValue(i)
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2 / 1000) + 's)完成')

    def SettingsPage_Sidebar_horizontalSlider_sliderReleased(self):
        """设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动抬起后"""
        v = self.horizontalSlider_page_settings_sidebar.value()
        self.Json_MOS['Sidebar_Sidebar_Time'] = v
        print_('Info', '用户点击: 设置页面 -> 左边栏动画设置 -> 滑动控件: 拖动抬起/旋转数字输入框    左边栏动画设置值为: ' + str(v))
        JsonWrite(self.Json_MOS, self.JsonFile)

    def SettingsPage_Sidebar_spinBox(self):
        """设置页面 -> 左边栏动画设置 -> 旋转数字输入框"""
        i = self.spinBox_page_settings_sidebar.value()
        self.horizontalSlider_page_settings_sidebar.setValue(i)
        i_2 = i * 30
        self.label_page_settings_background_h3_2.setText('预计 ' + str(i_2) + 'mm' + ' (' + str(i_2 / 1000) + 's)完成')
        self.SettingsPage_Sidebar_horizontalSlider_sliderReleased()

    def AddUserWindow_OK(self):
        self.SinOut_moveEvent.disconnect(self.Dialog_AddUserWindows_.MoveXY)
        self.Users_List_Refresh()

    def Users_List_Refresh(self):
        """读取账户列表并反馈在控件上"""
        print_('Info', '账户: 刷新账户列表')
        self.Json_MOS = JsonRead(self.JsonFile)  # 重新读取
        U = self.Json_MOS['Users']
        I = -1
        self.listWidget_users_down.clear()
        if U != {}:
            self.stackedWidget_page_users_down.setCurrentIndex(1)

            self.label_users_down_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
            self.label_users_down_loading.setMovie(self.label_users_down_loading_)
            self.label_users_down_loading_.start()

            for U_1 in U:
                I += 1
                User_Name = self.Json_MOS['Users'][U_1]['User_Name']
                F = self.Json_MOS['Users'][U_1]['Manner']
                if F == 'OffLine':
                    # 如果账户是离线账户
                    T = '[离线]' + User_Name
                item = QListWidgetItem(self.listWidget_users_down)
                item.setText(T)
                if self.Json_MOS['UserPage_setChoice'] == 'Choices':
                    # 如果多选开启
                    item.setCheckState(Qt.CheckState.Unchecked)
                self.listWidget_users_down.addItem(item)

            self.label_users_down_loading_.stop()
            self.stackedWidget_page_users_down.setCurrentIndex(0)
        else:
            self.stackedWidget_page_users_down.setCurrentIndex(2)
        print_('Info', '账户: 刷新账户列表完成')

    def MainWinowMainBackground(self, Want, _init_=False):
        """主窗口背景"""
        if Want == None:
            self.centralwidget.setStyleSheet('')
            self.page_main.setStyleSheet(
                '/*模拟阴影*/\n#widget_Middle > #stackedWidget_main_2{border-image: url(:/Scrub/images/Scrub_B2_FFFFFF-50_Main-M-B.png);}')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = False
                JsonWrite(self.Json_MOS, self.JsonFile)
        else:
            self.centralwidget.setStyleSheet(
                '#stackedWidget_main > #page_main{border-image: url(:/BackGround/images/BackGround/' + str(
                    Want) + '.png);}')
            self.page_main.setStyleSheet('')
            if _init_ == False:
                # 如果不是初始化 就改变json配置
                self.Json_MOS['BackGround'] = Want
                JsonWrite(self.Json_MOS, self.JsonFile)

    def SettingsPage_Page_Download_Settings_Download(self):
        """设置页面 -> 下载 -> 下载源选择"""
        i = self.comboBox_page_settings_download.currentIndex()
        if i == 0:
            self.Json_MOS['Download_Source'] = 'MCBBS'
            JsonWrite(self.Json_MOS, self.JsonFile)
        elif i == 1:
            self.Json_MOS['Download_Source'] = 'BMCLAPI'
            JsonWrite(self.Json_MOS, self.JsonFile)
        elif i == 2:
            self.Json_MOS['Download_Source'] = 'MC'
            JsonWrite(self.Json_MOS, self.JsonFile)

    def SettingsPage_Page_Download_Settings_DownloadExceptionHandling(self,cb):
        """设置页面 -> 下载 -> 节点文件出现问题时，自动尝试其他节点"""
        if self.checkBox_page_settings_download_exceptionHandling.checkState() == 2:
            self.Json_MOS['Download_Source_ExceptionHandling'] = True
        else:
            self.Json_MOS['Download_Source_ExceptionHandling'] = False
        JsonWrite(self.Json_MOS, self.JsonFile)


    def Sidebar_Clicked(self, Want=None, H=True):
        """
            用户点击左边栏按钮后…\n
            Want: 被点击的"按钮" \n
            H: 是否记录历史(True, False)
        """

        def Go():
            """动画开始运行后 初始化"""
            # 线条动画属性

            self.label_Sidebar_QTime_Go_B = -1  # 步长
            self.label_Sidebar_QTime_Go_Start = 30  # 最小(起始数值)
            self.label_Sidebar_QTime_Go_Stop = 0  # 最大(终止数值)

            # ========= #

            self.label_Sidebar_QTime_Back_B = 1  # 步长
            self.label_Sidebar_QTime_Back_Start = 0  # 最小(起始数值)
            self.label_Sidebar_QTime_Back_Stop = 30  # 最大(终止数值)

            # ========== #
            # 背景动画属性

            self.label_Sidebar_B_QTime_Go_Start = 0  # 起始数值
            self.label_Sidebar_B_QTime_Go_Stop = 10  # 终止数值
            self.label_Sidebar_B_QTime_Go_B = 1  # 步长

            # ========== #

            self.label_Sidebar_B_QTime_Back_Start = 10  # 起始数值
            self.label_Sidebar_B_QTime_Back_Stop = 0  # 终止数值
            self.label_Sidebar_B_QTime_Back_B = -1  # 步长

            if self.Sidebar_Click_Ok:
                # 如果上次全运行完了
                self.label_Sidebar_QTime_Ok = False  # 线条动画是否完成
                self.label_Sidebar_B_QTime_Ok = False  # 背景动画是否完成
                self.label_Sidebar_QTime_Go_N = int(self.label_Sidebar_QTime_Go_Start)  # 记录第几(线-去)
                self.label_Sidebar_QTime_Back_N = int(self.label_Sidebar_QTime_Back_Start)  # 记录第几(线-回)
                self.label_Sidebar_B_QTime_Go_N = int(self.label_Sidebar_B_QTime_Go_Start)  # 记录第几(背景-去)
                self.label_Sidebar_B_QTime_Back_N = int(self.label_Sidebar_B_QTime_Back_Start)  # 记录第几(背景-回)

                self.Sidebar_Click_I = str(self.Sidebar_Click_C)  # 正在变回去的(上次点击的)
            else:
                self.Sidebar_Click_I = str(self.Sidebar_Click_)  # 正在变回去的(上次点击的)
                if self.label_Sidebar_QTime_Ok == False:
                    # 如果上次的线条动画没有运行完成
                    pass
                elif self.label_Sidebar_B_QTime_Ok == False:
                    # 如果上次的背景动画没有运行完成
                    pass

        def label_Sidebar_Go_QTime_():
            self.label_Sidebar_QTime_Go_N += self.label_Sidebar_QTime_Go_B
            if self.label_Sidebar_QTime_Go_N > self.label_Sidebar_QTime_Go_Stop:
                # 如果没小于终止数值 就运行
                if Want == 'Home':
                    self.label_Sidebar_Home.setPixmap(
                        QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Download':
                    self.label_Sidebar_Download.setPixmap(
                        QtGui.QPixmap(
                            ":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))
                elif Want == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(
                        QtGui.QPixmap(
                            ":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Go_N) + ".png"))

                label_Sidebar_Back_QTime_()

            elif self.label_Sidebar_QTime_Go_N == self.label_Sidebar_QTime_Go_Stop:
                label_Sidebar_Back_QTime_()

            else:
                self.label_Sidebar_QTime_Ok = True
                IfOk()
                self.label_Sidebar_QTime.stop()
                if len(self.H_B) > 1:
                    self.label_Sidebar_Back.setEnabled(True)
                else:
                    self.label_Sidebar_Back.setEnabled(False)

        def label_Sidebar_Back_QTime_():
            if self.label_Sidebar_QTime_Back_N <= self.label_Sidebar_QTime_Back_Stop:
                # 如果小于等于终止数值 就运行
                self.label_Sidebar_QTime_Back_N += self.label_Sidebar_QTime_Back_B
                if self.Sidebar_Click_I == 'Home':
                    self.label_Sidebar_Home.setPixmap(
                        QtGui.QPixmap(":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_Home/images/Home/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setPixmap(
                        QtGui.QPixmap(":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_User/images/User/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setPixmap(
                        QtGui.QPixmap(":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                    # print_('Info',":/Gif_Online/images/Online/" + str(self.label_Sidebar_QTime_Back_N) + ".png")
                elif self.Sidebar_Click_I == 'Download':
                    self.label_Sidebar_Download.setPixmap(QtGui.QPixmap(
                        ":/Gif_Download/images/Download/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))
                elif self.Sidebar_Click_I == 'Settings':
                    self.label_Sidebar_Settings.setPixmap(QtGui.QPixmap(
                        ":/Gif_Settings/images/Settings/" + str(self.label_Sidebar_QTime_Back_N) + ".png"))

            else:
                pass

        def label_Sidebar_B_Go_QTime_():
            self.label_Sidebar_B_QTime_Go_N += self.label_Sidebar_B_QTime_Go_B
            if self.label_Sidebar_B_QTime_Go_N <= self.label_Sidebar_B_QTime_Go_Stop:
                # 如果没小于终止数值 就运行
                if Want == 'Home':
                    self.label_Sidebar_Home.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Online':
                    self.label_Sidebar_OnLine.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Download':
                    self.label_Sidebar_Download.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")
                elif Want == 'Settings':
                    self.label_Sidebar_Settings.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Go_N) + "%);")

                label_Sidebar_B_Back_QTime_()

            else:
                IfOk()
                self.label_Sidebar_B_QTime_Ok = True
                self.label_Sidebar_B_QTime.stop()

        def label_Sidebar_B_Back_QTime_():
            self.label_Sidebar_B_QTime_Back_N += self.label_Sidebar_B_QTime_Back_B
            if self.label_Sidebar_B_QTime_Back_N >= self.label_Sidebar_B_QTime_Back_Stop:
                # 如果没小于终止数值 就运行
                if self.Sidebar_Click_I == 'Home':
                    self.label_Sidebar_Home.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'User':
                    self.label_Sidebar_User.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                    # print_('Info',"background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Online':
                    self.label_Sidebar_OnLine.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Download':
                    self.label_Sidebar_Download.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")
                elif self.Sidebar_Click_I == 'Settings':
                    self.label_Sidebar_Settings.setStyleSheet(
                        "background-color: rgba(128, 128, 128, " + str(self.label_Sidebar_B_QTime_Back_N) + "%);")

        def IfOk():
            """检查动画是否完全完成"""
            if self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
                # 如果都完成了
                self.Sidebar_Click_Ok = True
                self.Sidebar_Click_I = False  # 正在变回去的
                self.Sidebar_Click_C = str(Want)  # 彻底完成后……

        print_('Info', '用户点击: 左边栏按钮 -> ' + str(Want))

        if self.Sidebar_Click_Ok:
            self.label_Sidebar_Back.setEnabled(False)
            Go()
            self.Sidebar_Click_Ok = False
            self.Sidebar_Click_ = str(Want)

            if Want == self.Sidebar_Click_C:
                # 如果用户又点了一次同样的按钮
                self.Sidebar_Click_ = ''
                self.Sidebar_Click_I = ''

            Time_ = self.Json_MOS['Sidebar_Sidebar_Time']
            self.label_Sidebar_QTime = QTimer()
            self.label_Sidebar_QTime.start(Time_)
            self.label_Sidebar_QTime.timeout.connect(label_Sidebar_Go_QTime_)

            self.label_Sidebar_B_QTime = QTimer()
            self.label_Sidebar_B_QTime.start(Time_)
            self.label_Sidebar_B_QTime.timeout.connect(label_Sidebar_B_Go_QTime_)

            if Want == 'Home':
                self.SetCurrentIndex(False, 1, 1, H)
            elif Want == 'User':
                self.SetCurrentIndex(False, 0, 0, H)
            elif Want == 'Online':
                self.SetCurrentIndex(False, 2, 2, H)
            elif Want == 'Download':
                self.SetCurrentIndex(False, 3, 3, H)
            elif Want == 'Settings':
                self.SetCurrentIndex(False, 4, 4, H)

    def RunInitialize(self, First=True):
        """在启动器启动后初始化启动器(读取设置+设置启动器)"""

        def Settings_():
            """设置启动器"""
            # 导入
            # 读取阶段(读取配置等)
            self.System = System()
            print_('Info', '系统检测: 系统：' + self.System)
            self.Json_MOS = JsonRead(self.JsonFile)
            print_('Info', '程序启动(初始化设置): Json读取完成')
            C = Json_Cheak(self.JsonFile)
            if C:
                # 如果返回为True(已补全文件)
                self.Json_MOS = JsonRead(self.JsonFile)
                print_('Info', '程序启动(初始化设置:Json检查): Json不完整, 以补全')
            else:
                print_('Info', '程序启动(初始化设置:Json检查): Json完整')
            print_('Info', '程序启动(初始化设置:Json检查): Json验证完成')
            self.label_loading_text_2.setText('正在设置启动器(4/7)')
            # 设置阶段
            if self.System != 'Mac':
                self.radioButton_settings_subject_automatic.setEnabled(False)
                self.radioButton_settings_subject_automatic.setToolTip('跟随系统(只限于Mac系统)-当前不可用')
            if self.System == 'Mac':
                # 如果是Mac
                M = 'sw_vers'
                import subprocess
                M_ = subprocess.Popen(M,shell=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                M_T = M_.communicate()
                M_T = str(M_T[0]).split('\n')[1]
                System_V = M_T.split('\t')[1]
                self.Json_MOS['System_V'] = System_V
                self.Json_MOS['System_Places'] = 64
            elif self.System == 'Win':
                import platform
                M_T = platform.platform()
                System_V = str(M_T).split('-')[1]
                Places = int(str(platform.architecture()[0]).split('bit')[0])
                self.Json_MOS['System_Places'] = Places
                self.Json_MOS['System_V'] = System_V
            else:
                import platform
                System_V = platform.release()
                self.Json_MOS['System_Places'] = 64
                self.Json_MOS['System_V'] = System_V

            self.Json_MOS['System'] = self.System

            if self.Json_MOS['Subject'] == 'Light':
                self.radioButton_settings_subject_light.setChecked(True)
            elif self.Json_MOS['Subject'] == 'Dark':
                self.radioButton_settings_subject_dark.setChecked(True)
            elif self.Json_MOS['Subject'] == 'Automatic':
                self.radioButton_settings_subject_automatic.setChecked(True)
            self.horizontalSlider_page_settings_sidebar.setValue(self.Json_MOS['Sidebar_Sidebar_Time'])
            self.spinBox_page_settings_sidebar.setValue(self.Json_MOS['Sidebar_Sidebar_Time'])

            self.UserPage_setChoice = self.Json_MOS['UserPage_setChoice']
            if self.UserPage_setChoice == 'Choice':
                # 如果是单选 就设置为单选
                self.UserPage_Up_SetChoiceUser_Set('Choice')
                self.pushButton_page_users_up_refreshUser.setText('刷新全部')
                self.pushButton_page_users_up_deleteUser.setText('删除全部')

            print_('Info', '程序启动(初始化设置): 设置背景……')
            self.label_loading_text_2.setText('正在设置启动器(5/7)')

            if self.Json_MOS['BackGround'] == False:
                self.MainWinowMainBackground(None)
                self.radioButton_settings_background_none.setChecked(True)
            else:
                self.MainWinowMainBackground(self.Json_MOS['BackGround'], _init_=True)
                if self.Json_MOS['BackGround'] == 1:
                    self.radioButton_settings_background_1.setChecked(True)
                elif self.Json_MOS['BackGround'] == 2:
                    self.radioButton_settings_background_2.setChecked(True)
                elif self.Json_MOS['BackGround'] == 3:
                    self.radioButton_settings_background_3.setChecked(True)
                elif self.Json_MOS['BackGround'] == 4:
                    self.radioButton_settings_background_4.setChecked(True)
                elif self.Json_MOS['BackGround'] == 5:
                    self.radioButton_settings_background_5.setChecked(True)
                elif self.Json_MOS['BackGround'] == 6:
                    self.radioButton_settings_background_6.setChecked(True)
                elif self.Json_MOS['BackGround'] == 7:
                    self.radioButton_settings_background_7.setChecked(True)

            if self.Json_MOS['Download_Source'] == 'MCBBS':
                pass
            elif self.Json_MOS['Download_Source'] == 'BMCLAPI':
                self.comboBox_page_settings_download.setCurrentIndex(1)
            elif self.Json_MOS['Download_Source'] == 'MC':
                self.comboBox_page_settings_download.setCurrentIndex(2)

            if self.Json_MOS['Download_Source_ExceptionHandling'] == False:
                self.checkBox_page_settings_download_exceptionHandling.setChecked(False)

        if First == True:
            self.RunInitialize_.stop()

        # 引用阶段
        print_('Info', '程序启动(初始化设置): 引入库')
        self.label_loading_text_2.setText('正在设置启动器(2/7)')
        import UI.Gif_rc
        import pytz

        # 开始播放动图
        self.Page_Loading = QtGui.QMovie(":/widget_Sidebar/images/MOS_Logo_gif.gif")
        self.label_loading_gif.setMovie(self.Page_Loading)
        self.Page_Loading.start()

        self.JsonFile_Q = os.path.join('')
        self.JsonFile = JsonFile()  # 读取Json路径

        self.File = File()  # 获取缓存目录
        self.File_Parent = os.path.dirname(self.File)  # 缓存目录上一级

        self.H_B = []

        if os.path.isfile(self.JsonFile) == False:
            """如果没有Json这个目录 就转到欢迎(初始化)页面"""
            self.stackedWidget_main.setCurrentIndex(2)
        else:
            # 如果有 就进行下一步
            self.label_loading_text_2.setText('正在设置启动器(3/7)')
            Settings_()
            JsonWrite(self.Json_MOS, self.JsonFile)

            print_('Info', '程序启动(初始化设置): 读取用户账户')
            self.label_loading_text_2.setText('正在设置启动器(6/7)')
            self.Users_List_Refresh()

            print_('Info', '程序启动(初始化设置): 读取游戏目录列表')
            self.label_loading_text_2.setText('正在设置启动器(7/7)')
            self.GameFiles_Read_Thread_Start()

            print_('Info', '程序启动(初始化设置): 设置完成')
            self.label_loading_text_2.setText('设置完成')
            self.Animation_ToMainWindow()
            self.Page_Loading.stop()  # 暂停动图

            # 设置完成后就运行日志记录程序
            self.Log_QTime = QTimer()
            self.Log_QTime.setInterval(4000)  # 4秒
            self.Log_QTime.timeout.connect(self.Log_QTime_)
            self.Log_QTime.start()

    def FirstStartInitialize(self):
        """在第一次启动时 初始化(缓存)"""
        from Code.Code import InitializeFirst
        InitializeFirst()
        self.Animation_ToMainWindow(HelloToMainLoading=True)

    def FirstStartInitializeOk(self):
        """在第一次启动时 初始化(缓存) 的页面切换动画完成后"""
        self.RunInitialize(First=False)  # 重新读取配置

    def Animation_ToMainWindow(self, HelloToMainLoading=False):
        """
            动画函数-……(默认 加载)页面->主页面

            HelloToMainLoading: 从欢迎页面到加载页面
        """

        # 切换为第……页
        if HelloToMainLoading == False:
            self.Animation_ToMainWindow_Int_Page = 0
        elif HelloToMainLoading:
            # 欢迎页切换为加载页
            self.Animation_ToMainWindow_Int_Page = 1

        # 设置透明度
        self.Opacity = QGraphicsOpacityEffect()  # 透明度对象
        # self.Opacity.setOpacity(1)  # 初始化设置透明度为，即不透明
        # self.label.setGraphicsEffect(self.Opacity)  # 把标签的透明度设置为为self.opacity

        self.Animation_ToMainWindow_Int_Original = 1  # 原来多少
        self.Animation_ToMainWindow_Int = 0.05  # 每次淡出/入多少

        def Animation():
            """淡出"""
            self.Animation_ToMainWindow_Int_Original -= self.Animation_ToMainWindow_Int
            if self.Animation_ToMainWindow_Int_Original < 0:
                self.Animation_ToMainWindow_Run.stop()
                self.stackedWidget_main.setCurrentIndex(self.Animation_ToMainWindow_Int_Page)

                # 初始化淡出
                self.Animation_ToMainWindow_Int_Original = 0  # 原来多少
                self.Opacity.setOpacity(0)  # 为了防止出现负数 所以重新设置

                # 触发切换动画(淡入)
                self.Animation_ToMainWindow_Run_In = QTimer()
                self.Animation_ToMainWindow_Run_In.start(2)
                self.Animation_ToMainWindow_Run_In.timeout.connect(AnimationIn)

            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        def AnimationIn():
            """淡入"""
            self.Animation_ToMainWindow_Int_Original += self.Animation_ToMainWindow_Int
            if self.Animation_ToMainWindow_Int_Original > 1:
                self.Animation_ToMainWindow_Run_In.stop()
                if HelloToMainLoading == True:
                    # 如果是从欢迎页面渐变的 就重新加载json
                    self.FirstStartInitializeOk()
                else:
                    # 不是就播放左边栏动画
                    self.Sidebar_Clicked(Want='Home')
            else:
                self.Opacity.setOpacity(self.Animation_ToMainWindow_Int_Original)
                self.stackedWidget_main.setGraphicsEffect(self.Opacity)

        # 触发切换动画(淡出)
        self.Animation_ToMainWindow_Run = QTimer()
        self.Animation_ToMainWindow_Run.start(1)
        self.Animation_ToMainWindow_Run.timeout.connect(Animation)

    def __init__setAll(self):
        """设置控件信号"""
        self.RunInitialize_ = QTimer()
        self.RunInitialize_.setInterval(20)
        self.RunInitialize_.timeout.connect(self.RunInitialize)
        self.RunInitialize_.start()
        self.pushButton_hello_start.clicked.connect(self.FirstStartInitialize)

        # 左边栏
        self.Sidebar_Click_ = ''  # 当前点击的控件
        self.Sidebar_Click_Ok = True  # 记录动画是否完成
        self.Sidebar_Click_C = 'Home'  # 彻底完成后……
        self.label_Sidebar_Back.clicked.connect(self.Back_Clicked)
        self.label_Sidebar_User.clicked.connect(self.User_Clicked)
        self.label_Sidebar_Home.clicked.connect(self.Home_Clicked)
        self.label_Sidebar_OnLine.clicked.connect(self.Online_Clicked)
        self.label_Sidebar_Download.clicked.connect(self.Download_Clicked)
        self.label_Sidebar_Settings.clicked.connect(self.Settings_Clicked)

        self.stackedWidget_main_2.currentChanged.connect(self.StackedWidget_Main)

        # 账户页面
        self.pushButton_page_users_up_addUser.clicked.connect(self.UserPage_Up_AddUser)
        self.pushButton_page_users_up_addUser.pressed.connect(self.UserPage_Up_AddUser_Pressed)
        self.pushButton_page_users_up_refreshUser.clicked.connect(self.UserPage_Up_RefreshUser)
        self.pushButton_page_users_up_refreshUser.pressed.connect(self.UserPage_Up_RefreshUser_Pressed)
        self.pushButton_page_users_up_deleteUser.clicked.connect(self.UserPage_Up_DeleteUser)
        self.pushButton_page_users_up_deleteUser.pressed.connect(self.UserPage_Up_DeleteUser_Pressed)
        self.widget_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice_icon.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.label_page_users_up_setChoice.clicked.connect(self.UserPage_Up_SetChoiceUser)
        self.listWidget_users_down.itemPressed.connect(self.UserPage_Down_ListWidget_Clicked)

        # 主页
        self.pushButton_page_home_main_game_list.clicked.connect(self.MainPage_GameList)
        # ---> 游戏列表
        self.pushButton_page_home_file_add.clicked.connect(self.MainPage_GameList_List_GameFileAdd)
        self.pushButton_page_home_file_leftrefresh.clicked.connect(self.MainPage_GameList_List_Refresh)
        self.pushButton_game_file_add_again.clicked.connect(self.MainPage_GameList_List_GameFileAdd_Add)
        self.lineEdit_game_file_add.textChanged.connect(self.MainPage_GameList_List_GameFileAdd_TextChanged)
        self.pushButton_game_file_add_ok.clicked.connect(self.MainPage_GameList_List_GameFileAdd_OK)
        self.pushButton_game_file_add_cancel.clicked.connect(self.MainPage_GameList_List_GameFileAdd_Cancel)
        self.listWidget_page_home_game_left.clicked.connect(self.MainPage_GameList_List)

        # 下载页面
        self.label_page_download_2_game.clicked.connect(self.DownloadPage_Game_Clicked)
        self.pushButton_page_download_mc_refresh.clicked.connect(self.DownloadPage_Game_Refresh_Clicked)
        self.label_page_download_2_word.clicked.connect(self.DownloadPage_Word_Clicked)
        self.label_page_download_2_mode.clicked.connect(self.DownloadPage_Mode_Clicked)
        self.label_page_download_2_conformity.clicked.connect(self.DownloadPage_Conformity_Clicked)
        self.label_page_download_2_resource.clicked.connect(self.DownloadPage_Resource_Clicked)
        self.stackedWidget_page_download.currentChanged.connect(self.DownloadPage_stackedWidget_CurrentIndex)
        self.checkBox_page_download_mc_official.clicked.connect(self.DownloadPage_MC_Official)
        self.checkBox_page_download_mc_test.clicked.connect(self.DownloadPage_MC_Text)
        self.checkBox_page_download_mc_previously.clicked.connect(self.DownloadPage_MC_Previously)
        self.listWidget_page_1_download.itemPressed.connect(self.DownloadPage_stackedWidget_GameList_Clicked)
        self.widget_page_download_1_install_fabric_up.clicked.connect(self.DownloadPage_stackedWidget_install_fabric)
        self.widget_page_download_1_install_forge_up.clicked.connect(self.DownloadPage_stackedWidget_install_forge)
        self.widget_page_download_1_install_optifine_up.clicked.connect(self.DownloadPage_stackedWidget_install_optifine)
        self.listWidget_page_download_1_install_forge.itemPressed.connect(self.DownloadPage_stackedWidget_install_forge_itemPressed)
        self.listWidget_page_download_1_install_fabric.itemPressed.connect(self.DownloadPage_stackedWidget_install_fabric_itemPressed)
        self.listWidget_page_download_1_install_optifine.itemPressed.connect(self.DownloadPage_stackedWidget_install_optifine_itemPressed)
        self.pushButton_page_download_1_install_forge_up_close.clicked.connect(self.DownloadPage_stackedWidget_install_forge_close)
        self.pushButton_page_download_1_install_fabric_up_close.clicked.connect(self.DownloadPage_stackedWidget_install_fabric_close)
        self.pushButton_page_download_1_install_optifine_up_close.clicked.connect(self.DownloadPage_stackedWidget_install_optifine_close)
        self.pushButton_page_download_1_install_bottom_ok.clicked.connect(self.DownloadPage_stackedWidget_install_ok)
        self.lineEdit_page_download_1_install_bottom_GameName.textChanged.connect(self.DownloadPage_stackedWidget_install_lineEdit)
        self.listWidget_page_1_download_errorText.clicked.connect(self.DownloadPage_Game_Refresh_Clicked)

        # 设置页面
        self.radioButton_settings_background_none.clicked.connect(self.SettingsPage_Background_None_Clicked)
        self.radioButton_settings_background_1.clicked.connect(self.SettingsPage_Background_1_Clicked)
        self.radioButton_settings_background_2.clicked.connect(self.SettingsPage_Background_2_Clicked)
        self.radioButton_settings_background_3.clicked.connect(self.SettingsPage_Background_3_Clicked)
        self.radioButton_settings_background_4.clicked.connect(self.SettingsPage_Background_4_Clicked)
        self.radioButton_settings_background_5.clicked.connect(self.SettingsPage_Background_5_Clicked)
        self.radioButton_settings_background_6.clicked.connect(self.SettingsPage_Background_6_Clicked)
        self.radioButton_settings_background_7.clicked.connect(self.SettingsPage_Background_7_Clicked)
        self.label_page_settings_game_settings.clicked.connect(self.SettingsPage_Page_Settings_Game_Settings)
        self.label_page_settings_appearance.clicked.connect(self.SettingsPage_Page_Settings_Game_Appearance)
        self.label_page_settings_download.clicked.connect(self.SettingsPage_Page_Settings_Game_Download)
        self.label_page_settings_else.clicked.connect(self.SettingsPage_Page_Settings_Game_Else)
        self.label_page_settings_about.clicked.connect(self.SettingsPage_Page_Settings_Game_About)
        self.comboBox_page_settings_download.currentIndexChanged.connect(self.SettingsPage_Page_Download_Settings_Download)
        self.checkBox_page_settings_download_exceptionHandling.stateChanged.connect(self.SettingsPage_Page_Download_Settings_DownloadExceptionHandling)

        self.horizontalSlider_page_settings_sidebar.sliderMoved.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.horizontalSlider_page_settings_sidebar.sliderPressed.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.horizontalSlider_page_settings_sidebar.sliderReleased.connect(
            self.SettingsPage_Sidebar_horizontalSlider_sliderReleased)
        self.horizontalSlider_page_settings_sidebar.valueChanged.connect(self.SettingsPage_Sidebar_horizontalSlider)
        self.spinBox_page_settings_sidebar.valueChanged.connect(self.SettingsPage_Sidebar_spinBox)

    def __init__setShadow(self):
        """设置控件阴影"""
        # 添加阴影
        """
        self.effect_shadow = QGraphicsDropShadowEffect(self.widget_page_users_up)
        self.effect_shadow.setOffset(0, 0)  # 偏移 (向右,向下)
        self.effect_shadow.setColor(QColor(225, 225, 225, 200))  # 阴影颜色
        self.effect_shadow.setBlurRadius(16) # 阴影圆角
        self.widget_page_users_up.setGraphicsEffect(self.effect_shadow)  # 将设置套用
        """

    def __init__setToolTipDuration(self):
        """初始化设置: 设置提示框"""
        # 悬浮提示窗
        from UI.Custom_UI.QToolTip import ToolTip
        self._toolTip = ToolTip(parent=self)
        self.label_Sidebar_Back.setToolTipDuration(1000)
        self.label_Sidebar_User.setToolTipDuration(1000)
        self.label_Sidebar_Home.setToolTipDuration(1000)
        self.label_Sidebar_OnLine.setToolTipDuration(1000)
        self.label_Sidebar_Download.setToolTipDuration(1000)
        self.label_Sidebar_Settings.setToolTipDuration(1000)
        self.radioButton_settings_subject_light.setToolTipDuration(1000)
        self.radioButton_settings_subject_dark.setToolTipDuration(1000)
        self.radioButton_settings_subject_automatic.setToolTipDuration(1000)

        self.label_Sidebar_Back.installEventFilter(self)
        self.label_Sidebar_User.installEventFilter(self)
        self.label_Sidebar_Home.installEventFilter(self)
        self.label_Sidebar_OnLine.installEventFilter(self)
        self.label_Sidebar_Download.installEventFilter(self)
        self.label_Sidebar_Settings.installEventFilter(self)
        self.radioButton_settings_subject_light.installEventFilter(self)
        self.radioButton_settings_subject_dark.installEventFilter(self)
        self.radioButton_settings_subject_automatic.installEventFilter(self)

        self._toolTip.hide()

    def Log_QTime_(self):
        """定时将日志写入文件"""
        logs = Log_Return()
        time_2 = datetime.now(timezone('Etc/GMT-8')).strftime('%Y%m%d')
        time = time_2 + '.log'
        file = os.path.join(self.File, 'Logs', time)

        if os.path.exists(file):
            with open(file, 'a', encoding='utf-8') as f:
                for log_ in logs:
                    f.write(log_)
        else:
            with open(file, 'w', encoding='utf-8') as f:
                for log_ in logs:
                    f.write(log_)
        Log_Clear()

    def SetCurrentIndex(self, U, I, L=False, H=True, And_=None, And__=None):
        """
            更改控件的页数，并记录历史
            参数:
                U: 要更改的控件(如果为左边栏请传入False) \n
                I: 要将控件更改为第……页 \n
                L: 是否需要更改左边边栏显示(False, 如果更改->int) \n
                H: 是否记录(True False)
                And_: 如果记录,在返回的时候同时执行的其他翻页[[执行控件,页码],[执行控件,页码],[执行控件,页码]]
                And__: 如果记录,在返回后执行的函数
        """


        if U != False:
            if U.currentIndex() == I:
                H = False
        else:
            if L != False:
                if L == 0 and U == False:
                    if L == self.stackedWidget_main_2.currentIndex():
                        H=False
                elif L == 1 and U == False and len(self.H_B)!=0:
                    if L == self.stackedWidget_main_2.currentIndex():
                        H=False
                elif L == 2 and U == False:
                    if L == self.stackedWidget_main_2.currentIndex():
                        H=False
                elif L == 3 and U == False:
                    if L == self.stackedWidget_main_2.currentIndex():
                        H=False
                elif L == 4 and U == False:
                    if L == self.stackedWidget_main_2.currentIndex():
                        H=False


        if H == True and U == False:
            a = {
                "Name": U,  # 控件名
                "Index_L": int(self.stackedWidget_main_2.currentIndex()),  # 原来页码
                "Left": L,  # 是否更改左边 如果改 值为改为多少 如果不改 值为False
                "Left_L": int(self.stackedWidget_main_2.currentIndex()),  # 原来左边页码
                "And_": And_,
                "And__": And__
            }
            self.H_B.append(a)
            self.stackedWidget_main_2.setCurrentIndex(I)
        elif H == True and U != False:
            a = {
                "Name": U,  # 控件名
                "Index": I,  # 页码
                "Index_L": int(U.currentIndex()),  # 原来页码
                "Left": L,  # 是否更改左边 如果改 值为改为多少 如果不改 值为False
                "Left_L": int(self.stackedWidget_main_2.currentIndex()),  # 原来左边页码
                "And_" : And_,
                "And__": And__
            }
            self.H_B.append(a)
            self.stackedWidget_main_2.setCurrentIndex(L)
            U.setCurrentIndex(I)
        elif H == False:
            self.stackedWidget_main_2.setCurrentIndex(L)
        if len(self.H_B) > 1 and self.label_Sidebar_QTime_Ok and self.label_Sidebar_B_QTime_Ok:
            self.label_Sidebar_Back.setEnabled(True)
        else:
            self.label_Sidebar_Back.setEnabled(False)
        print(self.H_B)

    def GameFiles_Read_Thread_Start(self):
        """启动游戏目录返回线程 同时启动动画"""
        # 在启动前就检测是不是一个都没有
        if self.Json_MOS['GameFile'] == {}:
            self.stackedWidget_page_home_game_left.setCurrentIndex(1)
        else:
            self.label_page_home_game_left_none_loading_ = QtGui.QMovie(":/Gif/images/Gif/Loaging.gif")
            self.label_page_home_game_left_none_loading.setMovie(self.label_page_home_game_left_none_loading_)
            self.label_page_home_game_left_none_loading_.start()
            
            self.listWidget_page_home_game_left.clear()
            
            self.GameFiles_Read_Thread_Start_ = GameFiles_Read_Thread(self.Json_MOS)
            self.GameFiles_Read_Thread_Start_.SinOut.connect(self.GameFiles_Read_Thread_SinOut)
            self.GameFiles_Read_Thread_Start_.SinOutOK.connect(self.GameFiles_Read_Thread_SinOutOK)
            self.GameFiles_Read_Thread_Start_.start()

    def GameFiles_Read_Thread_SinOut(self,N):
        """
            游戏目录返回线程 信号槽
            :param N: 游戏目录名称
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Game_File.png"), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        item = QListWidgetItem(icon, N)
        self.listWidget_page_home_game_left.addItem(item)

    def GameFiles_Read_Thread_SinOutOK(self):
        """
            游戏目录返回线程 完成信号
        """
        self.stackedWidget_page_home_game_left.setCurrentIndex(0)
        self.label_page_home_game_left_none_loading_.stop()
        # 设置当前选中
        if self.listWidget_page_home_game_left.count() == 0:
            pass
        else:
            index = self.Json_MOS['GameFile_List_Clicked']
            self.listWidget_page_home_game_left.setCurrentRow(index)
            text_ = self.listWidget_page_home_game_left.item(index)
            text = text_.text()
            GameFile = self.Json_MOS['GameFile'][text]['File']
            self.GameFiles_ReturnGameList_Thread_Start(GameFile)

    def GameFiles_ReturnGameList_Thread_Start(self,GameFile):
        """启动"检测游戏目录下的游戏线程" 同时启动动画"""
        self.GameFiles_ReturnGameList_Thread_Start_ = GameFiles_ReturnGameList_Thread(GameFile)
        self.GameFiles_ReturnGameList_Thread_Start_.SinOut.connect(self.GameFiles_ReturnGameList_Thread_SinOut)
        #self.GameFiles_ReturnGameList_Thread_Start_.SinOutOK.connect(self.GameFiles_Read_Thread_SinOutOK)
        self.GameFiles_ReturnGameList_Thread_Start_.start()

    def GameFiles_ReturnGameList_Thread_SinOut(self,Name):
        """检测游戏目录下的游戏线程 输出处理"""
        item = QListWidgetItem()
        item.setText(Name)
        font = QFont()
        font.setPixelSize(13)
        item.setFont(font)
        print(Name)
        widget = QWidget()
        hLayout = QHBoxLayout()


        btn_s = QPushButton()  # 设置
        icon_s = QtGui.QIcon()
        icon_s.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/Settings_Game.png"), QtGui.QIcon.Mode.Normal,
                         QtGui.QIcon.State.Off)
        btn_s.setIcon(icon_s)
        btn_s.setIconSize(QSize(20, 20))
        btn_s.setMinimumWidth(20)
        btn_s.setMinimumSize(QSize(35, 35))
        btn_s.setMaximumSize(QSize(35, 35))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_s.sizePolicy().hasHeightForWidth())
        btn_s.setSizePolicy(sizePolicy)

        btn_d = QPushButton()  # 删除
        icon_d = QtGui.QIcon()
        icon_d.addPixmap(QtGui.QPixmap(":/widget_Sidebar/images/User_Page_Delete-pressed.png"), QtGui.QIcon.Mode.Normal,
                         QtGui.QIcon.State.Off)
        btn_d.setIcon(icon_d)
        btn_d.setIconSize(QSize(23, 23))
        btn_d.setMinimumWidth(20)
        btn_d.setMinimumSize(QSize(35,35))
        btn_d.setMaximumSize(QSize(35,35))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_d.sizePolicy().hasHeightForWidth())
        btn_d.setSizePolicy(sizePolicy)

        hl = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)  # 水平

        hLayout.addItem(hl)
        hLayout.addWidget(btn_s)
        hLayout.addWidget(btn_d)

        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(5)
        widget.setLayout(hLayout)
        widget.setContentsMargins(0, 0, 0, 0)

        btn_s.clicked.connect(lambda: self.GameFiles_ReturnGameList_Thread_SinOut_PushButton_settings())
        btn_d.clicked.connect(lambda: self.GameFiles_ReturnGameList_Thread_SinOut_PushButton_delate())

        self.listWidget_page_home_game_right_gamefile_game.addItem(item)
        self.listWidget_page_home_game_right_gamefile_game.setItemWidget(item, widget) # 为item设置widget

    def GameFiles_ReturnGameList_Thread_SinOut_PushButton_settings(self):
        """游戏列表设置按钮信号处理"""
        # 获取button
        btn = self.sender()
        # 获取按钮相对于listwwdget的坐标
        # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
        buttonpos = btn.mapToGlobal(QPoint(0, 0)) - self.widget_page_home_game_right.mapToGlobal(QPoint(0, 0))
        # 获取到对象
        item = self.listWidget_page_home_game_right_gamefile_game.indexAt(buttonpos)
        # 获取位置
        index = item.row()
        item_ = self.listWidget_page_home_game_right_gamefile_game.item(index)
        print(item_.text())

    def GameFiles_ReturnGameList_Thread_SinOut_PushButton_delate(self):
        """游戏列表设置按钮信号处理"""
        # 获取button
        btn = self.sender()
        # 获取按钮相对于listwidget的坐标
        # listwidget 相对于窗体的坐标 减去 button 相对于窗体的坐标
        buttonpos = btn.mapToGlobal(QPoint(0, 0)) - self.widget_page_home_game_right.mapToGlobal(QPoint(0, 0))
        # 获取到对象
        item = self.listWidget_page_home_game_right_gamefile_game.indexAt(buttonpos)
        # 获取位置
        index = item.row()
        item_ = self.listWidget_page_home_game_right_gamefile_game.item(index)
        N = item_.text()
        from Code.DelateGameWindow import Dialog_DelateGameWindows_
        gamefile_name = self.listWidget_page_home_game_left.item(self.Json_MOS['GameFile_List_Clicked']).text()
        self.Dialog_DelateGameWindows_ = Dialog_DelateGameWindows_(
            os.path.join(self.Json_MOS['GameFile'][gamefile_name]['File'],'versions'),
            N,
            gamefile_name
        )
        #self.Dialog_DelateGameWindows_.sinOut_Win_XY.connect(self.Window_XY)
        self.Dialog_DelateGameWindows_.sinOut_OK.connect(self.AddUserWindow_OK)
        self.Dialog_DelateGameWindows_.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.Dialog_DelateGameWindows_.setWindowFlags(
            Qt.WindowType.Popup |  # 表示该窗口小部件是一个弹出式顶层窗口，即它是模态的，但有一个适合弹出式菜单的窗口系统框架。
            Qt.WindowType.Tool |  # 表示小部件是一个工具窗口,如果有父级，则工具窗口将始终保留在其顶部,在 macOS 上，工具窗口对应于窗口的NSPanel类。这意味着窗口位于普通窗口之上，因此无法在其顶部放置普通窗口。默认情况下，当应用程序处于非活动状态时，工具窗口将消失。这可以通过WA_MacAlwaysShowToolWindow属性来控制。
            Qt.WindowType.FramelessWindowHint |  # 生成无边框窗口
            Qt.WindowType.MSWindowsFixedSizeDialogHint |  # 在 Windows 上为窗口提供一个细对话框边框。这种风格传统上用于固定大小的对话框。
            Qt.WindowType.Dialog |  # 指示该小部件是一个应装饰为对话框的窗口（即，通常在标题栏中没有最大化或最小化按钮）。这是 的默认类型QDialog。如果要将其用作模式对话框，则应从另一个窗口启动它，或者具有父级并与该windowModality属性一起使用。如果将其设为模态，对话框将阻止应用程序中的其他顶级窗口获得任何输入。我们将具有父级的顶级窗口称为辅助窗口。
            Qt.WindowType.NoDropShadowWindowHint  # 禁用支持平台上的窗口投影。
        )

        self.Dialog_DelateGameWindows_.setWindowModality(
            Qt.WindowModality.ApplicationModal  # 该窗口对应用程序是模态的，并阻止对所有窗口的输入。
        )

        self.MainWindow_xy_size = self.geometry()  # 获取主界面 初始坐标
        self.Dialog_DelateGameWindows_.move(
            round(self.MainWindow_xy_size.x() + (self.size().width()/2 - self.Dialog_DelateGameWindows_.size().width()/2)),
            round(self.MainWindow_xy_size.y() + (self.size().height()/3)
        ))  # 子界面移动到 居中
        self.SinOut_moveEvent.connect(self.Dialog_DelateGameWindows_.MoveXY)

        self.Dialog_DelateGameWindows_.show()


    def setUIFondSize(self,UI,followSystem=False):
        """
            设置制定Ui的字体大小
            :param UI: 控件
            :param followSystem:是否跟随系统,如果是Mac就使用
        """
        pass


    def Window_XY(self, X, Y):
        """改变窗口的XY坐标"""
        self.move(round(X), round(Y))

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        global Win_XY
        Win_XY = self.geometry()
        self.Is_Drag_ = True
        self.Mouse_Start_Point_ = a0.globalPosition()  # 获得鼠标的初始位置
        self.Window_Start_Point_ = self.frameGeometry().topLeft()  # 获得窗口的初始位置

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        # 判断是否在拖拽移动
        try:
            if self.Is_Drag_:
                # 获得鼠标移动的距离
                self.Move_Distance = a0.globalPosition() - self.Mouse_Start_Point_
                # 改变窗口的位置
                self.move(
                    round(self.Window_Start_Point_.x() + self.Move_Distance.x()),
                    round(self.Window_Start_Point_.y() + self.Move_Distance.y())
                )
        except AttributeError:
            pass

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # 放下左键即停止移动
        if a0.button() == Qt.MouseButton.LeftButton:
            self.Is_Drag_ = False

    def eventFilter(self, obj, e: QEvent):
        """重写 悬浮提示 方法"""
        if obj is self:
            return super().eventFilter(obj, e)

        tip = self._toolTip
        if e.type() == QEvent.Type.Enter:
            tip.setText(obj.toolTip())
            tip.setDuration(obj.toolTipDuration())
            tip.adjustPos(obj.mapToGlobal(QPoint()), obj.size())
            tip.show()
        elif e.type() == QEvent.Type.Leave:
            tip.hide()
        elif e.type() == QEvent.Type.ToolTip:
            return True

        return super().eventFilter(obj, e)


    def L_XY_(self,x,y):
        """刷新XY坐标缓存"""
        self.L_XY = {
            'X': self.x(),
            'Y': self.y()
        }
    def moveEvent(self, a0: QtGui.QMoveEvent):
        """重写坐标变化信号"""
        # 获取XY的变化
        try:
            x = self.x() - self.L_XY['X']
            y = self.y() - self.L_XY['Y']
            self.SinOut_moveEvent.emit(x,y)
            #print([x,y])
        except AttributeError:
            pass

class GameFiles_Read_Thread(QThread):
    SinOut = pyqtSignal(str)
    SinOutOK = pyqtSignal()
    def __init__(self,Json_MOS):
        """
            多线程进行游戏目录读取
            :param Json_MOS: Json内容
        """
        super(GameFiles_Read_Thread, self).__init__()
        self.Json_MOS = Json_MOS
    def run(self):
        # self.Json_MOS = JsonRead(self.JsonFile)
        key_ = self.Json_MOS['GameFile_List']
        for J in key_:
            N = self.Json_MOS['GameFile'][J]['Name']
            F = self.Json_MOS['GameFile'][J]['File']
            self.SinOut.emit(N)

        self.SinOutOK.emit()
        import gc
        del key_,J,N,F
        gc.collect()

class GameFiles_ReturnGameList_Thread(QThread):
    SinOut = pyqtSignal(str)
    def __init__(self,GameFile):
        """
            多线程读取游戏目录下的游戏
            :param GameFile: 游戏目录
        """
        super(GameFiles_ReturnGameList_Thread, self).__init__()
        self.GameFile = GameFile
    def run(self):
        from Code.MC_Code.GameFile_Game import GameFile_Game
        a = GameFile_Game()
        out = a.GameFile_Game_ReturnGames(self.GameFile)
        print(out)
        for game in out:
            if out[game]['Jar_Exist'] == False and out[game]['Json_Check'] == False:
                Z = '缺少Jar文件, 并且Json文件可能已损坏'
            elif out[game]['Jar_Exist'] == False:
                Z = '缺少Jar文件'
            elif out[game]['Json_Exist'] == False:
                Z = '缺少Json文件'
            elif out[game]['Json_Check'] == False:
                Z = 'Json文件可能已损坏'
            else:
                Z = ''
            if Z == '':
                N = out[game]['Name']
            else:
                N = out[game]['Name'] + ' ' + Z
            self.SinOut.emit(N)
        import gc
        del out,a
        gc.collect()

class DownloadPage_stackedWidget_GetGameList_Thread(QThread):
    SinOut = pyqtSignal(str,str)
    SinOut_Error = pyqtSignal()
    SinOut_OK = pyqtSignal()
    def __init__(self,Source,File,Kind):
        """多线程获取版本列表"""
        super(DownloadPage_stackedWidget_GetGameList_Thread, self).__init__()
        self.Source = Source
        self.File = File
        self.Kind = Kind
    def run(self):
        from Code.MC_Code.GamePublishListReturn import GamePublishListReturn
        a = GamePublishListReturn(self.Source,self.File)
        b = a.ListReturn(self.Kind)
        # print(b)
        if b != 'Error':
            l = []
            for b_1 in b:
                N = b_1['id']
                T = b_1['time']
                self.SinOut.emit(N, T)
            self.SinOut_OK.emit()
            del a, b, l, N, T
        else:
            self.SinOut_Error.emit()
            del a, b
        import gc
        gc.collect()

class DownloadPage_stackedWidget_GameList_Clicked_Get_Thread(QThread):
    SinOut = pyqtSignal(str,str,str,str)
    SinOut_Error = pyqtSignal(str)
    SinOut_OK = pyqtSignal(str,bool)
    def __init__(self, Kind, V):
        """
            多线程 根据版本获取Forge,Fabric,Optifine列表
            :param Kind: 种类(Forge,Fabric,Optifine)
            :param V: 版本号
        """
        super(DownloadPage_stackedWidget_GameList_Clicked_Get_Thread, self).__init__()
        self.Kind = Kind
        self.V = V
    def run(self):
        try:
            print('start')
            if self.Kind == 'Forge':
                self.URL = 'https://bmclapi2.bangbang93.com/forge/minecraft/' + str(self.V)
            elif self.Kind == 'Fabric':
                self.URL = 'https://bmclapi2.bangbang93.com/fabric-meta/v2/versions/loader/' + str(self.V)
            elif self.Kind == 'Optifine':
                self.URL = 'https://bmclapi2.bangbang93.com/optifine/' + str(self.V)
            import requests, gc
            print(self.URL)
            r = requests.get(self.URL)

            if r.text != '[]':
                try:
                    j = r.json()
                    print(self.URL)
                    for a in j:
                        if self.Kind == 'Forge':
                            n = a['version']
                            t = a['modified']
                            k = None
                        elif self.Kind == 'Fabric':
                            n = a['loader']['version']
                            t = None
                            if a['loader']['stable'] == True:
                                k = 'Stable'
                            else:
                                k = 'Bata'
                        elif self.Kind == 'Optifine':
                            n = a['type']
                            t = None
                            if 'forge' in a:
                                k = 'Stable'
                            else:
                                k = 'Bata'
                                n = n + '_' + a['patch']
                        self.SinOut.emit(self.Kind, n, t, k)
                    self.SinOut_OK.emit(self.Kind, True)
                except requests.exceptions.JSONDecodeError:
                    self.SinOut_OK.emit(self.Kind, False)
            else:
                self.SinOut_OK.emit(self.Kind, False)
        except:
            self.SinOut_Error.emit(self.Kind)

        gc.collect()




def Return_Window_XY():
    """返回窗口的坐标"""
    global Win_XY
    return Win_XY


def Run():
    print_('Info', "程序启动(UI显示): 程序已开始运行！")
    app = QtWidgets.QApplication(argv)
    print_('Info', "程序启动(UI显示): 创建窗口对象成功！")
    ui = RunUi()
    print_('Info', "程序启动(UI显示): 创建PyQt窗口对象成功！")
    exit(app.exec())
