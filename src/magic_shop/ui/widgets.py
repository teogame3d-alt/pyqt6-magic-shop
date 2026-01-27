from __future__ import annotations

from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox


class ArtifactDialog(QDialog):
    def __init__(self, title: str, name: str = "", rarity: str = "", price: int = 0, stock: int = 0):
        super().__init__()
        self.setWindowTitle(title)
        layout = QFormLayout(self)

        self.name_input = QLineEdit(name)
        self.rarity_input = QLineEdit(rarity)
        self.price_input = QSpinBox()
        self.price_input.setRange(1, 100000)
        self.price_input.setValue(max(1, price))
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 100000)
        self.stock_input.setValue(stock)

        layout.addRow("Name", self.name_input)
        layout.addRow("Rarity", self.rarity_input)
        layout.addRow("Price", self.price_input)
        layout.addRow("Stock", self.stock_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self) -> tuple[str, str, int, int]:
        return (
            self.name_input.text().strip(),
            self.rarity_input.text().strip(),
            int(self.price_input.value()),
            int(self.stock_input.value()),
        )
