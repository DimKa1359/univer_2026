import sys
import json
import urllib.request
from PyQt5 import QtWidgets

# Главное окно конвертера валют.
class CurrencyConverter(QtWidgets.QWidget):
    
    # Инициализация интерфейса.
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.resize(450, 200)

        # Установка базового шрифта.
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        # Базовые курсы.
        self.usd_rate = 95.0
        self.eur_rate = 105.0

        # Загрузка актуальных курсов.
        self.fetch_rates()

        # Элементы ввода для вещественных чисел.
        self.rub_spin = QtWidgets.QDoubleSpinBox()
        self.usd_spin = QtWidgets.QDoubleSpinBox()
        self.eur_spin = QtWidgets.QDoubleSpinBox()

        # Настройка полей ввода.
        for spin in (self.rub_spin, self.usd_spin, self.eur_spin):
            spin.setRange(0, 1000000)
            spin.setDecimals(2)
        
        self.rub_spin.setSuffix(" ₽")
        self.usd_spin.setSuffix(" $")
        self.eur_spin.setSuffix(" €")

        # Контейнер формы.
        layout = QtWidgets.QFormLayout()
        layout.addRow("Рубли:", self.rub_spin)
        layout.addRow("Доллары:", self.usd_spin)
        layout.addRow("Евро:", self.eur_spin)
        self.setLayout(layout)

        # Подключение сигналов.
        self.rub_spin.valueChanged.connect(self.update_from_rub)
        self.usd_spin.valueChanged.connect(self.update_from_usd)
        self.eur_spin.valueChanged.connect(self.update_from_eur)

    # Получение курсов валют через api.
    def fetch_rates(self):
        try:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            req = urllib.request.Request(url)
            # Выполнение сетевого запроса с ограничением по времени.
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.usd_rate = data['Valute']['USD']['Value']
                self.eur_rate = data['Valute']['EUR']['Value']
                print(f"Курсы обновлены: 1$ = {self.usd_rate}₽, 1€ = {self.eur_rate}₽")
        except Exception as e:
            # Обработка сетевой ошибки.
            print(f"Ошибка загрузки курсов: {e}. Используются значения по умолчанию.")

    # Расчет долларов и евро при вводе рублей.
    def update_from_rub(self, value):
        self.usd_spin.blockSignals(True)
        self.eur_spin.blockSignals(True)
        self.usd_spin.setValue(value / self.usd_rate)
        self.eur_spin.setValue(value / self.eur_rate)
        self.usd_spin.blockSignals(False)
        self.eur_spin.blockSignals(False)

    # Расчет рублей и евро при вводе долларов.
    def update_from_usd(self, value):
        self.rub_spin.blockSignals(True)
        self.eur_spin.blockSignals(True)
        self.rub_spin.setValue(value * self.usd_rate)
        self.eur_spin.setValue((value * self.usd_rate) / self.eur_rate)
        self.rub_spin.blockSignals(False)
        self.eur_spin.blockSignals(False)

    # Расчет рублей и долларов при вводе евро.
    def update_from_eur(self, value):
        self.rub_spin.blockSignals(True)
        self.usd_spin.blockSignals(True)
        self.rub_spin.setValue(value * self.eur_rate)
        self.usd_spin.setValue((value * self.eur_rate) / self.usd_rate)
        self.rub_spin.blockSignals(False)
        self.usd_spin.blockSignals(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec_())