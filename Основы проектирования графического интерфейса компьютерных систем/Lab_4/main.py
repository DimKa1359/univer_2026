import sys
import os
from datetime import datetime
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    # Сигнал для передачи имени файла во фронтенд.
    saveRequested = pyqtSignal(str, arguments=['filename'])

    def __init__(self):
        super().__init__()
        
        # Настройка таймера автоматического сохранения.
        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self.trigger_autosave)
        self.save_timer.start(10000)  # 10 000 мс = 10 секунд.

    def trigger_autosave(self):
        # Формирование уникального имени файла на основе текущего времени.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_autosave_{timestamp}.png"
        
        # Запуск процесса сохранения на стороне qml.
        self.saveRequested.emit(filename)
        print(f"Автосохранение: {filename}")


if __name__ == '__main__':
    # Создаем экземпляр приложения.
    app = QApplication(sys.argv)

    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)

    # Загружаем QML.
    engine.load("mainWindow.qml")

    # Проверка успешной загрузки QML.
    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    sys.exit(app.exec())