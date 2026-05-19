from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


def set_table_headers(table: QTableWidget, headers: list[str]) -> None:
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setStretchLastSection(True)


def make_action_buttons(*buttons: QPushButton) -> QHBoxLayout:
    row = QHBoxLayout()
    for button in buttons:
        row.addWidget(button)
    row.addStretch()
    return row


class StubPage(QWidget):
    def __init__(self, title: str, headers: list[str], rows: list[list[str]], buttons: list[QPushButton]):
        super().__init__()
        root = QVBoxLayout(self)
        root.addWidget(QLabel(f"<h2>{title}</h2>"))

        table = QTableWidget()
        set_table_headers(table, headers)
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(value))
        root.addWidget(table)
        root.addLayout(make_action_buttons(*buttons))
