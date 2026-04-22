from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QGroupBox,QLineEdit, QInputDialog, QPushButton, QLabel, QVBoxLayout,QHBoxLayout, QRadioButton, QButtonGroup, QListWidget, QTextEdit, QFileDialog
import os
from PIL import Image
from PyQt5.QtGui import QPixmap

from PIL.ImageFilter import SHARPEN

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None 
        self.filname = None
        self.save_dir = "Modified/"
        self.original_image = None

    def LoadImage(self, dir, filname):
        self.dir = dir
        self.filname = filname
        image_path = os.path.join(dir, filname)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w,h = lb_image.width(),lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filname)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filname)
        self.image.save(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filname)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filname)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
       

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filname)
        self.showImage(image_path)

    def do_sbros(self):
        if self.original_image is None:
            return
        self.saveImage()
        image_path = os.path.join(workdir, self.filname)
        self.showImage(image_path)

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle("Easy Editor")


lb_image = QLabel('Картинка')
btn_papka = QPushButton('Папка')
lw_files = QListWidget()


btn_left = QPushButton("Леви")
btn_rigt = QPushButton('Прави')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('ЧБ')
btn_mirror = QPushButton('зерк')
btn_sbros = QPushButton('сброс')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_papka)
col1.addWidget(lw_files)

col2.addWidget(lb_image,95)
row_knopok = QHBoxLayout()
row_knopok.addWidget(btn_left)
row_knopok.addWidget(btn_rigt)
row_knopok.addWidget(btn_sharp)
row_knopok.addWidget(btn_bw)
row_knopok.addWidget(btn_mirror)
row_knopok.addWidget(btn_sbros)
col2.addLayout(row_knopok)

row.addLayout(col1,20)
row.addLayout(col2,80)


win.setLayout(row)

workdir = ""

def fillter(files, extensions):
    result = []
    for filname in files:
        for ext in extensions:
            if filname.endswith(ext):
                result.append(filname)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilnameList():
    extensions = ['jpg','"jpeg','png','gif','.bmp']
    chooseWorkdir()
    filnames = fillter(os.listdir(workdir),extensions)
    lw_files.clear()
    for filname in filnames:
        lw_files.addItem(filname)

btn_papka.clicked.connect(showFilnameList)

workimage=ImageProcessor()


def showChosenImage():
    if lw_files.currentRow() >= 0 :
        filname = lw_files.currentItem().text()
        workimage.LoadImage(workdir, filname)
        image_path = os.path.join(workimage.dir, workimage.filname)
        workimage.showImage(image_path)
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_left.clicked.connect(workimage.do_left)
btn_rigt.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_sbros.clicked.connect(workimage.do_sbros)
win.show()
app.exec()