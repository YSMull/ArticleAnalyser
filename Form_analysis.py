#coding=utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import re
import en
class analysis_Form(QDialog):

    def __init__(self, time_used, files_paths_list, words_to_be_learned_llist, words2sentence_list, parent = None):
        super(analysis_Form,self).__init__(parent)

        self.files_paths_list = files_paths_list

        self.words_to_be_learned_llist = words_to_be_learned_llist
        self.words2sentence_list = words2sentence_list

        self.files_table = QTableWidget()
        self.refresh_files_table()

        self.words_list_Table = QTableWidget()
        self.refresh_words_table()

        self.add_to_known_words_Btuuon = QPushButton(u"已掌握")
        self.quit_Button = QPushButton(u"取消")
        #搞一个进度条

        self.sentence_TextEdit_Label = QLabel(u"原文再现:")
        self.sentence_TextEdit = QTextBrowser()
        self.explanation_TextEdit_Label = QLabel(u"单词趣解:")
        self.explanation_TextEdit = QTextBrowser()
        self.explanation_TextEdit.acceptRichText()
        self.TextEdit_layout = QVBoxLayout()
        self.TextEdit_layout.addWidget(self.sentence_TextEdit_Label)
        self.TextEdit_layout.addWidget(self.sentence_TextEdit)
        self.TextEdit_layout.addWidget(self.explanation_TextEdit_Label)
        self.TextEdit_layout.addWidget(self.explanation_TextEdit)


        self.blocks_layout = QHBoxLayout()
        self.blocks_layout.addWidget(self.files_table)
        self.blocks_layout.addWidget(self.words_list_Table)
        self.blocks_layout.addLayout(self.TextEdit_layout)
        

        self.four_widget_layout = QHBoxLayout()
        # self.four_widget_layout.addStretch()
        self.four_widget_layout.addStretch()
        self.four_widget_layout.addWidget(self.add_to_known_words_Btuuon)
        
        self.four_widget_layout.addWidget(self.quit_Button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.blocks_layout)
        self.layout.addLayout(self.four_widget_layout)

        self.setLayout(self.layout)
        self.setWindowTitle(u"分析结果")

        self.connect(self.quit_Button, SIGNAL("clicked()"), self, SLOT("reject()"))#这里不能单纯的退出，可能还要清理一下表
        self.connect(self.files_table, SIGNAL("itemSelectionChanged()"), self.refresh_words_table)
        self.connect(self.words_list_Table, SIGNAL("itemSelectionChanged()"), self.refresh_TextEdit)
        QMessageBox.information(self, u"分析完毕", u"耗时{0}秒".format(time_used))

    def refresh_files_table(self):
    	print("refresh_files_table_in_analysis_Form")
        self.files_table.clear()

        self.Y_MAX = len(self.files_paths_list)
        self.X_MAX = 1
        self.files_table.setColumnCount(self.X_MAX)
        self.files_table.setRowCount(self.Y_MAX)
        self.files_table.setHorizontalHeaderLabels([u'文章'])#tips:这一句必须在setHeaderLabels之后出现
        for y in range(self.Y_MAX):
            text = re.split("[^a-zA-Z0-9\_\.\(\)]",#这里用正则表达式，因为windows和linux下的斜杠不同
            									   #不行，这样的话中文就无法识别了
                            self.files_paths_list[y])[-1]
            item = QTableWidgetItem(u"{0}".format(text))
            self.files_table.setItem(y, 0, item)

    def refresh_words_table(self):
    	print("refresh_words_table")

    	self.words_list_Table.clear()
    	self.Y_MAX = len(self.words_to_be_learned_llist[self.files_table.currentRow()])#文件列表的第几个文件
        self.X_MAX = 1
        self.words_list_Table.setColumnCount(self.X_MAX)
        self.words_list_Table.setRowCount(self.Y_MAX)
        self.words_list_Table.setHorizontalHeaderLabels([u'单词'])#tips:这一句必须在setHeaderLabels之后出现
        for y in range(self.Y_MAX):
            text = self.words_to_be_learned_llist[self.files_table.currentRow()][y]
            item = QTableWidgetItem(u"{0}".format(text))
            self.words_list_Table.setItem(y, 0, item)

    def refresh_TextEdit(self):
        self.sentence_TextEdit.clear()
        self.explanation_TextEdit.clear()

        tword = u"{0}".format(self.words_list_Table.currentItem().text())#记得要把QString变成普通字符串
        try:
            tsentence = self.words2sentence_list[self.files_table.currentRow()][tword]
        except:
            tsentence = "None"

        self.sentence_TextEdit.append("{0}".format(tsentence))


        #noun
        counter = 0
        noun_exp_list = []
        while True:
            noun_exp = en.noun.gloss(tword, counter)
            if noun_exp == "":
                break;
            counter = counter + 1
            noun_exp_list.append(noun_exp)
        len_noun_exp_list = len(noun_exp_list)
        if len_noun_exp_list != 0:
            self.explanation_TextEdit.append("<font color=red><b>noun.</b></font>")
            for i in range(len_noun_exp_list):
                self.explanation_TextEdit.append("<font color=red><b>{0}</b></font> . {1}".format(i+1, noun_exp_list[i]))

        #verb
        counter = 0
        verb_exp_list = []
        while True:
            verb_exp = en.verb.gloss(tword, counter)
            if verb_exp == "":
                break;
            counter = counter + 1
            verb_exp_list.append(verb_exp)
        len_verb_exp_list = len(verb_exp_list)
        if len_verb_exp_list != 0:
            self.explanation_TextEdit.append("<font color=blue><b>verb.</b></font>")
            for i in range(len_verb_exp_list):
                self.explanation_TextEdit.append("<font color=blue><b>{0}</b></font> . {1}".format(i+1, verb_exp_list[i]))

        #adverb
        counter = 0
        adverb_exp_list = []
        while True:
            adverb_exp = en.adverb.gloss(tword, counter)
            if adverb_exp == "":
                break;
            counter = counter + 1
            adverb_exp_list.append(adverb_exp)
        len_adverb_exp_list = len(adverb_exp_list)
        if len_adverb_exp_list != 0:
            self.explanation_TextEdit.append("<font color=green><b>adverb.</b></font>")
            for i in range(len_adverb_exp_list):
                self.explanation_TextEdit.append("<font color=green><b>{0}</b></font> . {1}".format(i+1, adverb_exp_list[i]))

        #adjective
        counter = 0
        adjective_exp_list = []
        while True:
            adjective_exp = en.adjective.gloss(tword, counter)
            if adjective_exp == "":
                break;
            counter = counter + 1
            adjective_exp_list.append(adjective_exp)
        len_adjective_exp_list = len(adjective_exp_list)
        if len_adjective_exp_list != 0:
            self.explanation_TextEdit.append("<font color=brown><b>adjective.</b></font>")
            for i in range(len_adjective_exp_list):
                self.explanation_TextEdit.append("<font color=brown><b>{0}</b></font> . {1}".format(i+1, adjective_exp_list[i]))
