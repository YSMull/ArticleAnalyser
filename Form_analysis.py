#coding=utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import re
class analysis_Form(QDialog):

    def __init__(self, files_paths_list, words_to_be_learned_llist, words2sentence_list, parent = None):
        super(analysis_Form,self).__init__(parent)

        self.files_paths_list = files_paths_list
        
        self.words_to_be_learned_llist = words_to_be_learned_llist
        self.words2sentence_list = words2sentence_list

        self.files_table = QTableWidget()
        self.refresh_files_table()

        self.words_list_Table = QTableWidget()
        self.refresh_words_table()

        self.quit_Button = QPushButton(u"取消")
        #搞一个进度条
        self.sentence_TextEdit = QTextEdit()

        self.two_blocks_layout = QHBoxLayout()
        self.two_blocks_layout.addWidget(self.files_table)
        self.two_blocks_layout.addWidget(self.words_list_Table)
        self.two_blocks_layout.addWidget(self.sentence_TextEdit)

        self.four_widget_layout = QHBoxLayout()
        # self.four_widget_layout.addStretch()
        
        self.four_widget_layout.addStretch()
        self.four_widget_layout.addWidget(self.quit_Button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.two_blocks_layout)
        self.layout.addLayout(self.four_widget_layout)

        self.setLayout(self.layout)
        self.setWindowTitle(u"分析结果")

        self.connect(self.quit_Button, SIGNAL("clicked()"), self, SLOT("reject()"))#这里不能单纯的退出，可能还要清理一下表
        self.connect(self.files_table, SIGNAL("itemSelectionChanged()"), self.refresh_words_table)
        self.connect(self.words_list_Table, SIGNAL("itemSelectionChanged()"), self.refresh_TextEdit)

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
        tword = u"{0}".format(self.words_list_Table.currentItem().text())#记得要把QString变成普通字符串
        tsentence = self.words2sentence_list[self.files_table.currentRow()][tword]
        
        self.sentence_TextEdit.setPlainText("{0}".format(tsentence))


