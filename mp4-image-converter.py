# pip install PyQt5 opencv-python
import sys
import os
import cv2
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class VideoToPngConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ドラッグ＆ドロップを有効化
        self.setAcceptDrops(True)
        self.setWindowTitle('MP4 to PNG Converter')
        self.resize(400, 200)

        # UIレイアウト
        layout = QVBoxLayout()
        self.label = QLabel("ここにMP4動画をドロップしてね！", self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # ちょっとスタイリッシュに
        self.setStyleSheet("""
            QWidget { background-color: #1a1a1a; color: #00ffff; font-size: 14px; font-weight: bold; }
            QLabel { border: 2px dashed #00ffff; border-radius: 10px; }
        """)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.mp4'):
                self.process_video(file_path)
            else:
                self.label.setText("MP4ファイルじゃないみたい！やり直し！")

    def process_video(self, video_path):
        self.label.setText("変換中...")
        QApplication.processEvents()

        # スクリプトがある場所に「日付＋時刻」のフォルダを作成
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_dir = os.path.join(script_dir, f"image-{timestamp}")

        try:
            os.makedirs(output_dir, exist_ok=True)
            cap = cv2.VideoCapture(video_path)
            frame_count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # 6桁の連番でPNG保存
                output_file = os.path.join(output_dir, f"{frame_count:06d}.png")
                cv2.imwrite(output_file, frame)
                frame_count += 1

            cap.release()
            self.label.setText(f"完了！\n{frame_count}枚の画像を保存したよ！\n保存先: {output_dir}")
            
        except Exception as e:
            self.label.setText(f"エラーが発生したよ:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoToPngConverter()
    ex.show()
    sys.exit(app.exec_())