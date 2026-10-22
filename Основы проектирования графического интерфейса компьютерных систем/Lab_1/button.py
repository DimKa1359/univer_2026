import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class ImageChangerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №1")
        self.resize(550, 480)

        # Безрамочное окно с поддержкой прозрачности
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # Режимы отображения
        self.is_custom_shape = False
        self.drag_position = QtCore.QPoint()

        # Верхняя панель с кнопкой закрытия (так как окно без рамки)
        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addStretch()
        self.btn_close = QtWidgets.QPushButton("✕")
        self.btn_close.setFixedSize(28, 28)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background: #e0e0e0; 
                border-radius: 14px; 
                font-weight: bold;
            }
            QPushButton:hover { background: #ff5c5c; color: white; }
        """)
        self.btn_close.clicked.connect(self.close)
        top_bar.addWidget(self.btn_close)

        # Текстовая надпись
        self.label = QtWidgets.QLabel("Здесь появится изображение")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        font = self.label.font()
        font.setPointSize(12)
        self.label.setFont(font)

        # Кнопка 1: По нажатию надпись меняется на изображение
        self.btn1 = QtWidgets.QPushButton("Кнопка 1 (Показать изображение)")
        self.btn1.setFixedHeight(35)
        self.btn1.clicked.connect(self.on_button1_clicked)

        # Кнопка 2: Окно меняет форму / загрузка полупрозрачного PNG
        self.btn2 = QtWidgets.QPushButton("Кнопка 2 (Полупрозрачная форма PNG)")
        self.btn2.setFixedHeight(35)
        self.btn2.clicked.connect(self.on_button2_clicked)

        # Компоновка
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.label, stretch=1)
        main_layout.addLayout(btn_layout)
        main_layout.setContentsMargins(25, 20, 25, 25)

        self.setLayout(main_layout)

    # Кнопка 1: смена надписи на масштабированное изображение
    def on_button1_clicked(self):
        pixmap = QtGui.QPixmap("image.png")
        if pixmap.isNull():
            self.label.setText("Ошибка: файл image.png не найден")
            return

        scaled = pixmap.scaled(
            440, 
            300, 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled)

    # Кнопка 2: переключение полупрозрачной формы окна
    def on_button2_clicked(self):
        self.is_custom_shape = not self.is_custom_shape
        if self.is_custom_shape:
            self.btn2.setText("Вернуть стандартную форму")
        else:
            self.btn2.setText("Кнопка 2 (Полупрозрачная форма PNG)")
        self.update()

    # Отрисовка формы окна и фона
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if not self.is_custom_shape:
            # Обычный вид: белое аккуратное окно со скруглением
            painter.setBrush(QtGui.QColor(255, 255, 255, 250))
            painter.setPen(QtGui.QColor(180, 180, 180))
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 16, 16)
        else:
            # Полупрозрачный режим по PNG-макету
            # Рисуем полупрозрачную подложку и фигурный контур
            pixmap = QtGui.QPixmap("image.png")
            if not pixmap.isNull():
                # Рисуем изображение с полупрозрачностью (alpha 140/255)
                painter.setOpacity(0.55)
                scaled_bg = pixmap.scaled(
                    self.size(), 
                    QtCore.Qt.KeepAspectRatioByExpanding, 
                    QtCore.Qt.SmoothTransformation
                )
                # Фигурная маска в виде эллипса/скругленного бейджа
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(self.rect().adjusted(4, 4, -4, -4)), 40, 40)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, scaled_bg)

                # Затемнение поверх для читаемости кнопок и текста
                painter.fillPath(path, QtGui.QColor(255, 255, 255, 120))
                painter.setOpacity(1.0)
                painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 120, 200), 3))
                painter.drawPath(path)
            else:
                # Фолбэк, если файл не найден
                painter.setBrush(QtGui.QColor(240, 240, 255, 150))
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(self.rect(), 30, 30)

    # Возможность перетаскивать окно мышью за любое свободное место
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and not self.drag_position.isNull():
            self.move(event.globalPos() - self.drag_position)
            event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImageChangerApp()
    window.show()
    sys.exit(app.exec_())