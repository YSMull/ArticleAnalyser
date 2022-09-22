#coding=utf8
import sys
import time
import re
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import Article_analysis_v2 as A_a

import Form_analysis as F_a

class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.words_to_be_learned_llist = []
        self.words2sentence_list = []

        self.files_table = QTableWidget()
        self.files_paths_list = []
        self.refresh_files_table()

        self.files_Button = QPushButton(u"添加文章")

        self.zhong_kao_CheckBox = QCheckBox(u"中考词汇")
        self.gao_kao_CheckBox = QCheckBox(u"高考词汇")
        self.analysis_Button = QPushButton(u"分析")

        self.files_layout =  QHBoxLayout()
        self.files_layout.addWidget(self.files_table)
        self.files_layout.addWidget(self.files_Button)

        self.a_g_layout = QHBoxLayout()
        self.a_g_layout.addWidget(self.zhong_kao_CheckBox)
        self.a_g_layout.addWidget(self.gao_kao_CheckBox)
        self.a_g_layout.addWidget(self.analysis_Button)
        # self.a_g_layout.addWidget(self.generate_Button)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.files_layout)
        self.layout.addLayout(self.a_g_layout)

        self.setLayout(self.layout)
        self.setWindowTitle(u"外文阅读工具")
        
        self.files_Button.clicked.connect(self.addFiles)
        self.analysis_Button.clicked.connect(self.analysis)

    def addFiles(self):
        print("addFiles")
        locations = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.DocumentsLocation)
        if not locations:
            return
        files, _ = QFileDialog.getOpenFileNames(self, "Select Music Files", locations[0])
        if not files:
            return
        self.files_paths_list = files
        print("len_list = {0}".format(len(self.files_paths_list)))
        self.refresh_files_table()

    def refresh_files_table(self):
        print("refresh_files_table")
        self.files_table.clear()

        self.Y_MAX = len(self.files_paths_list)
        self.X_MAX = 1
        self.files_table.setColumnCount(self.X_MAX)
        self.files_table.setRowCount(self.Y_MAX)
        self.files_table.setHorizontalHeaderLabels([u'文章列表'])#tips:这一句必须在setHeaderLabels之后出现
        for y in range(self.Y_MAX):
            text = re.split("[^a-zA-Z0-9\_\.\(\)]",#这里用正则表达式，因为windows和linux下的斜杠不同
                            self.files_paths_list[y])[-1]
            item = QTableWidgetItem(u"{0}".format(text))
            self.files_table.setItem(y, 0, item)

    def analysis(self):
        print("in analysis")
        time1 = time.time()
        try:#每次读取known时建立一个.bak备份吧
            known_words = A_a.load_known_words()
            print("known_words", len(known_words))
        except:
            QMessageBox.warning(self, u"Error", u"known.txt not found!")
            return

        if len(self.files_paths_list) == 0:
            QMessageBox.warning(self, u"Error", u"文章列表不能为空！")
            return

        self.words_to_be_learned_llist = []#!!复原这个llist,别掉了self了
        self.words2sentence_list = []
        for _file in self.files_paths_list:
            words_to_be_learned, words_sentence = A_a.analysis_article(_file, known_words)
            self.words_to_be_learned_llist.append(words_to_be_learned)
            self.words2sentence_list.append(words_sentence)

        time_used = time.time() - time1
        Form_analysis = F_a.analysis_Form(time_used ,self.files_paths_list,
                                    self.words_to_be_learned_llist, self.words2sentence_list)
        if Form_analysis.exec_():
            pass



def main():
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    app.exec()


if __name__ == '__main__':
    main()
