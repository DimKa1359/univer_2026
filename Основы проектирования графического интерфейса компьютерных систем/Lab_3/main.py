import sys
from PyQt5 import QtWidgets, QtSql, QtCore

class DatabaseApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер базы данных SQLite")
        self.resize(800, 600)

        # Хранилище ссылок на модели таблиц для защиты от сборщика мусора.
        self.models = {}

        self.setup_ui()
        self.setup_database()

    def setup_ui(self):
        # Создает основные элементы пользовательского интерфейса.
        
        # Настройка главного меню.
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Меню")
        
        self.action_connect = QtWidgets.QAction("Set connection", self)
        self.action_close = QtWidgets.QAction("Close connection", self)
        
        file_menu.addAction(self.action_connect)
        file_menu.addAction(self.action_close)
        
        self.action_connect.triggered.connect(self.open_connection)
        self.action_close.triggered.connect(self.close_connection)

        # Настройка центрального виджета и сетки.
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        # Панель управления с кнопками.
        control_layout = QtWidgets.QHBoxLayout()
        
        self.btn_1 = QtWidgets.QPushButton("bt1 'SELECT name'")
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(["type", "name", "tbl_name", "rootpage", "sql"])
        self.btn_2 = QtWidgets.QPushButton("bt2 'Query 2'")
        self.btn_3 = QtWidgets.QPushButton("bt3 'Query 3'")
        self.btn_bonus = QtWidgets.QPushButton("Custom Query (Bonus)")

        control_layout.addWidget(self.btn_1)
        control_layout.addWidget(self.combo_box)
        control_layout.addWidget(self.btn_2)
        control_layout.addWidget(self.btn_3)
        control_layout.addWidget(self.btn_bonus)

        main_layout.addLayout(control_layout)

        # Настройка виджета вкладок.
        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        # Инициализация пустых вкладок.
        for i in range(5):
            self.tabs.addTab(QtWidgets.QWidget(), f"Tab {i + 1}")

        # Подключение сигналов к слотам.
        self.btn_1.clicked.connect(self.run_query_1)
        self.combo_box.activated.connect(self.run_combo_query)
        self.btn_2.clicked.connect(self.run_query_2)
        self.btn_3.clicked.connect(self.run_query_3)
        self.btn_bonus.clicked.connect(self.run_custom_query)

        self.set_controls_enabled(False)

    def setup_database(self):
        # Инициализирует объект соединения с базой данных.
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')

    def set_controls_enabled(self, state):
        # Управляет доступностью элементов интерфейса.
        self.btn_1.setEnabled(state)
        self.combo_box.setEnabled(state)
        self.btn_2.setEnabled(state)
        self.btn_3.setEnabled(state)
        self.btn_bonus.setEnabled(state)

    def open_connection(self):
        # Открывает диалоговое окно для выбора файла базы данных.
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Выберите базу данных", 
            "", 
            "SQLite DataBases (*.sqlite *.db);;All Files (*)"
        )
        
        if file_name:
            self.db.setDatabaseName(file_name)
            if self.db.open():
                self.set_controls_enabled(True)
                # Автоматический запрос при успешном подключении.
                self.execute_query_to_tab(0, "SELECT * FROM sqlite_master", "Tab 1")
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Не удалось открыть базу данных")

    def close_connection(self):
        # Закрывает текущее соединение и очищает интерфейс.
        self.db.close()
        self.set_controls_enabled(False)
        self.models.clear()
        
        # Очистка всех вкладок.
        self.tabs.clear()
        for i in range(5):
            self.tabs.addTab(QtWidgets.QWidget(), f"Tab {i + 1}")

    def execute_query_to_tab(self, tab_index, query_string, tab_title):
        # Выполняет sql-запрос и размещает результат в указанной вкладке.
        model = QtSql.QSqlQueryModel()
        model.setQuery(query_string)

        if model.lastError().isValid():
            QtWidgets.QMessageBox.warning(self, "Ошибка запроса", model.lastError().text())
            return

        # Сохранение модели для защиты от сборщика мусора.
        self.models[tab_index] = model

        table_view = QtWidgets.QTableView()
        table_view.setModel(model)
        
        # Замена содержимого существующей вкладки.
        self.tabs.removeTab(tab_index)
        self.tabs.insertTab(tab_index, table_view, tab_title)
        self.tabs.setCurrentIndex(tab_index)

    def run_query_1(self):
        # Обрабатывает нажатие первой функциональной кнопки.
        self.execute_query_to_tab(1, "SELECT name FROM sqlite_master", "Tab 2")

    def run_combo_query(self):
        # Обрабатывает выбор элемента из выпадающего списка.
        column = self.combo_box.currentText()
        query = f"SELECT {column} FROM sqlite_master"
        self.execute_query_to_tab(2, query, "Tab 3")

    def run_query_2(self):
        # Обрабатывает нажатие второй функциональной кнопки.
        self.execute_query_to_tab(3, "SELECT type, name FROM sqlite_master", "Tab 4")

    def run_query_3(self):
        # Обрабатывает нажатие третьей функциональной кнопки.
        self.execute_query_to_tab(4, "SELECT tbl_name, sql FROM sqlite_master", "Tab 5")

    def run_custom_query(self):
        # Открывает модальное окно для ввода пользовательского запроса.
        query, ok = QtWidgets.QInputDialog.getText(
            self, 
            "Пользовательский запрос", 
            "Введите SQL-запрос:"
        )
        
        if ok and query.strip():
            # Добавление новой вкладки для пользовательского запроса.
            tab_index = self.tabs.count()
            self.execute_query_to_tab(tab_index, query, f"Custom {tab_index + 1}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())