import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import Counter 




#Tải model nhận diện cảm xúc qua tin nhắn đã train
import pickle
from pyvi import ViTokenizer


with open("emotion_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

#Mapping cảm xúc
emotion_map = {
    "Enjoyment": "Vui vẻ",
    "Sadness": "Buồn bã",
    "Anger": "Giận dữ",
    "Fear": "Sợ hãi",
    "Surprise": "Ngạc nhiên",
    "Disgust": "Chán ghét",
    "Other": "Không rõ cảm xúc"
}


def du_doan_cam_xuc_viet(text):
    text_tok = ViTokenizer.tokenize(text)
    vec = vectorizer.transform([text_tok])
    emotion_en = model.predict(vec)[0]
    return emotion_map.get(emotion_en, "Không rõ")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.resize(1208, 955)

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.main_boy = QtWidgets.QLabel(self.centralwidget)
        self.main_boy.setGeometry(QtCore.QRect(10, 50, 581, 821))
        self.main_boy.setStyleSheet("background-color: rgb(121, 123, 255); border-radius:20px;")

        self.line_boy = QtWidgets.QLineEdit(self.centralwidget)
        self.line_boy.setGeometry(QtCore.QRect(20, 780, 421, 61))
        self.line_boy.setStyleSheet("border-radius:20px;")

        self.send_boy = QtWidgets.QPushButton(self.centralwidget)
        self.send_boy.setGeometry(QtCore.QRect(470, 780, 93, 61))
        self.send_boy.setStyleSheet(self._button_stylesheet())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/ADMIN1/cv2_PYTHON/cv2_start.py/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_boy.setIcon(icon)
        self.send_boy.setIconSize(QtCore.QSize(60, 60))
        self.send_boy.clicked.connect(self.send_boy_message)

        self.main_girl = QtWidgets.QLabel(self.centralwidget)
        self.main_girl.setGeometry(QtCore.QRect(610, 50, 581, 821))
        self.main_girl.setStyleSheet("background-color: rgb(255, 102, 253); border-radius:20px;")

        self.line_girl = QtWidgets.QLineEdit(self.centralwidget)
        self.line_girl.setGeometry(QtCore.QRect(620, 780, 421, 61))
        self.line_girl.setStyleSheet("border-radius:20px;")

        self.send_girl = QtWidgets.QPushButton(self.centralwidget)
        self.send_girl.setGeometry(QtCore.QRect(1070, 780, 93, 61))
        self.send_girl.setStyleSheet(self._button_stylesheet())
        self.send_girl.setIcon(icon)
        self.send_girl.setIconSize(QtCore.QSize(60, 60))
        self.send_girl.clicked.connect(self.send_girl_message)

        self.but_tong_hop_boy = QtWidgets.QPushButton("TỔNG HỢP", self.centralwidget)
        self.but_tong_hop_boy.setGeometry(QtCore.QRect(230, 80, 121, 61))
        self.but_tong_hop_boy.setFont(QtGui.QFont("", 12))
        self.but_tong_hop_boy.setStyleSheet("border-radius:20px; background-color: rgb(157, 234, 255);")
        self.but_tong_hop_boy.clicked.connect(self.show_used_emotions)

        self.but_tong_hop_girl = QtWidgets.QPushButton("TỔNG HỢP", self.centralwidget)
        self.but_tong_hop_girl.setGeometry(QtCore.QRect(870, 90, 121, 61))
        self.but_tong_hop_girl.setFont(QtGui.QFont("", 12))
        self.but_tong_hop_girl.setStyleSheet("border-radius:20px; background-color: rgb(157, 234, 255);")
        self.but_tong_hop_girl.clicked.connect(self.show_used_emotions)

        self.statusbar = self.statusBar()

        self.boy_layout=QtWidgets.QVBoxLayout(self.main_boy)
        self.boy_layout.setAlignment(QtCore.Qt.AlignTop)
        self.girl_layout=QtWidgets.QVBoxLayout(self.main_girl)
        self.girl_layout.setAlignment(QtCore.Qt.AlignTop)

        #cuộn lên 
        self.boy_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.boy_scroll.setGeometry(QtCore.QRect(10, 130, 581, 600))
        self.boy_scroll.setStyleSheet("background-color: rgb(121, 123, 255); border-radius:20px;")
        self.boy_scroll.setWidgetResizable(True)

        self.boy_inner = QtWidgets.QWidget()
        self.boy_scroll.setWidget(self.boy_inner)

        self.boy_layout = QtWidgets.QVBoxLayout(self.boy_inner)
        self.boy_layout.setAlignment(QtCore.Qt.AlignTop)



        self.girl_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.girl_scroll.setGeometry(QtCore.QRect(610, 130, 581, 600))
        self.girl_scroll.setStyleSheet("background-color: rgb(255, 102, 253); border-radius:20px;")
        self.girl_scroll.setWidgetResizable(True)

        self.girl_inner = QtWidgets.QWidget()
        self.girl_scroll.setWidget(self.girl_inner)

        self.girl_layout = QtWidgets.QVBoxLayout(self.girl_inner)
        self.girl_layout.setAlignment(QtCore.Qt.AlignTop)


        self.used_emotions_boy = Counter()
        self.used_emotions_girl=Counter()

    def _button_stylesheet(self):
        return """
        QPushButton {
            font: 12pt "MS Shell Dlg 2";
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4B0082, stop:1 #00CED1);
            color: white;
            border-radius: 8px;
            padding: 5px 15px;
            border: none;
            box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2);
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00CED1, stop:1 #4B0082);
            box-shadow: 0px 3px 5px rgba(0, 0, 0, 0.3);
            transform: scale(1.05);
        }  
        QPushButton:pressed {
            background-color: #388E3C;
            transform: scale(0.95);
        }
        """
    def add_message(self, layout, text, align, is_sender, scroll_area,sender):
        container = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(container)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(2)
        tat_ca_tu_dong_nghia_tien = [
                        "tiền", "tiền bạc", "tiền tệ", "ngân lượng", "kim tiền", "tiền nong", "tiền mặt", "tiền vốn",
                        "vốn liếng", "đồng", "lúa", "thóc", "xèng", "xiền", "đạn", "gạo","vay","quỹ","lãi",
                        "thu nhập", "chi phí", "lợi nhuận", "tài sản", "vốn", "quỹ", "khoản vay", "ngân quỹ", "ngân sách"
                        ]


        # === Đính kèm cảm xúc ===
        emotion = du_doan_cam_xuc_viet(text)
        if any(tu in text for tu in tat_ca_tu_dong_nghia_tien):
                emotion = "Tiền"
        if sender == "boy":
                self.used_emotions_boy[emotion] += 1
        elif sender == "girl":
                self.used_emotions_girl[emotion] += 1


        # Biểu tượng cảm xúc
        emoji_map = {
            "Tiền":"🤑",
            "Vui vẻ": "😄",
            "Buồn bã": "😢",
            "Giận dữ": "😡",
            "Sợ hãi": "😨",
            "Ngạc nhiên": "😲",
            "Chán ghét": "🤢",
            "Không rõ cảm xúc": "❓"
        }
        emoji = emoji_map.get(emotion, "❓")

        label_emotion = QtWidgets.QLabel(f"{emoji} {emotion}")
        label_emotion.setStyleSheet("color: white; font-weight: bold; padding-left: 6px; font-size: 12px;")
        label_emotion.setAlignment(align)
        v_layout.addWidget(label_emotion)

        # === Bong bóng tin nhắn ===
        bubble_container = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(bubble_container)
        h_layout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        label.setMaximumWidth(300)
        label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)

        if is_sender:
            label.setStyleSheet("""
                background-color: #00c853;
                color: white;
                border-radius: 15px;
                padding: 12px 16px;
                font-size: 13px;
            """)
            h_layout.addStretch()
            h_layout.addWidget(label)
        else:
            label.setStyleSheet("""
                background-color: #2c2c2e;
                color: white;
                border-radius: 15px;
                padding: 12px 16px;
                font-size: 13px;
            """)
            h_layout.addWidget(label)
            h_layout.addStretch()

        v_layout.addWidget(bubble_container)

        layout.addWidget(container)
        QtCore.QTimer.singleShot(50, lambda: scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum()))


         
    def send_girl_message(self):
         message=self.line_girl.text()
         print(du_doan_cam_xuc_viet(message))
         if message:
              self.add_message(self.boy_layout,message,QtCore.Qt.AlignLeft,False,self.boy_scroll,"girl")
              self.add_message(self.girl_layout,message,QtCore.Qt.AlignRight,True,self.girl_scroll,"girl")
              self.line_girl.clear()
    def send_boy_message(self):
        message = self.line_boy.text()
        print(du_doan_cam_xuc_viet(message))
        if message:
            self.add_message(self.boy_layout,message,QtCore.Qt.AlignRight,True,self.boy_scroll,"boy")
            self.add_message(self.girl_layout,message,QtCore.Qt.AlignLeft,False,self.girl_scroll,"boy")
            self.line_boy.clear()
    def show_used_emotions(self):
        if not self.used_emotions_boy and not self.used_emotions_girl:
                message = "Chưa có cảm xúc nào được sử dụng."
        else:
                message = "Cảm xúc từ Boy:\n"
                if self.used_emotions_boy:
                        for emo, count in self.used_emotions_boy.items():
                                message += f"  - {emo}: {int(count/2)} lần\n"
                else:
                        message += "  (Không có)\n"

                message += "\n Cảm xúc từ Girl:\n"
                if self.used_emotions_girl:
                        for emo, count in self.used_emotions_girl.items():
                                message += f"  - {emo}: {int(count/2)} lần\n"
                else:
                        message += "  (Không có)\n"

        QtWidgets.QMessageBox.information(self, "Tổng hợp cảm xúc", message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
