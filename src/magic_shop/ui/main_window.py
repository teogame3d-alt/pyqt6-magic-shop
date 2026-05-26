from __future__ import annotations

"""RO: Fereastra principala pentru administrarea inventarului.
EN: Main window for inventory management.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ..services import ShopService
from .arcade_dialog import ArcadeDialog
from .widgets import ArtifactDialog

MAGIC_SHOP_STYLE = """
QMainWindow {
    background: #eef3f0;
}
QToolBar {
    background: #18231f;
    border: 0;
    padding: 8px;
    spacing: 8px;
}
QPushButton {
    background: #ffffff;
    color: #1f2933;
    border: 1px solid #c8d3cf;
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 700;
}
QPushButton:hover {
    background: #e8fff5;
    border-color: #10b981;
}
QLineEdit {
    background: #ffffff;
    border: 1px solid #bfcbc6;
    border-radius: 6px;
    padding: 9px 11px;
}
QTableWidget {
    background: #ffffff;
    border: 1px solid #cfd8d4;
    border-radius: 6px;
    gridline-color: #e3e9e6;
    selection-background-color: #d9f99d;
    selection-color: #17211d;
}
QHeaderView::section {
    background: #24352f;
    color: #ffffff;
    border: 0;
    padding: 8px;
    font-weight: 700;
}
QFrame#hero {
    background: #18231f;
    border-radius: 8px;
}
QFrame#metricCard {
    background: #ffffff;
    border: 1px solid #ccd8d3;
    border-radius: 8px;
}
QLabel#heroTitle {
    color: #ffffff;
    font-size: 22px;
    font-weight: 900;
}
QLabel#heroSubtitle {
    color: #c8d8d1;
}
QLabel#metricLabel {
    color: #65736f;
    font-size: 11px;
    font-weight: 700;
}
QLabel#metricValue {
    color: #18231f;
    font-size: 20px;
    font-weight: 900;
}
"""


class MainWindow(QMainWindow):
    """RO: UI pentru listare, adaugare si operatii pe stoc.
    EN: UI for listing, adding, and stock operations.
    """

    def __init__(self, service: ShopService):
        super().__init__()
        self.service = service
        self.summary_labels: dict[str, QLabel] = {}
        self.setWindowTitle("Arcana Inventory Studio")
        self.resize(1080, 680)
        self.setStyleSheet(MAGIC_SHOP_STYLE)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Rarity", "Price", "Stock"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setAlternatingRowColors(True)

        toolbar = QToolBar("Actions")
        self.addToolBar(toolbar)

        btn_add = QPushButton("Add")
        btn_edit = QPushButton("Edit")
        btn_delete = QPushButton("Delete")
        btn_buy = QPushButton("Buy")
        btn_restock = QPushButton("Restock")
        btn_arcade = QPushButton("Arcade")

        btn_add.clicked.connect(self.add_artifact)
        btn_edit.clicked.connect(self.edit_artifact)
        btn_delete.clicked.connect(self.delete_artifact)
        btn_buy.clicked.connect(self.buy_artifact)
        btn_restock.clicked.connect(self.restock_artifact)
        btn_arcade.clicked.connect(self.open_arcade)

        for b in [btn_add, btn_edit, btn_delete, btn_buy, btn_restock, btn_arcade]:
            toolbar.addWidget(b)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)
        layout.addWidget(self._build_hero())
        layout.addWidget(self._build_filter_row())
        layout.addWidget(self.table)
        self.setCentralWidget(container)

        self.refresh()

    def _build_hero(self) -> QFrame:
        """Build the recruiter-friendly summary band above the inventory table."""

        hero = QFrame()
        hero.setObjectName("hero")

        title = QLabel("Arcana Inventory Studio")
        title.setObjectName("heroTitle")
        subtitle = QLabel(
            "PyQt6 desktop CRUD, SQLite persistence, tested service rules, and arcade reward flow."
        )
        subtitle.setObjectName("heroSubtitle")

        text_col = QVBoxLayout()
        text_col.addWidget(title)
        text_col.addWidget(subtitle)
        text_col.addStretch(1)

        metrics = QGridLayout()
        metrics.setHorizontalSpacing(10)
        metrics.setVerticalSpacing(10)
        metrics.addWidget(self._metric_card("items", "ITEMS", "0"), 0, 0)
        metrics.addWidget(self._metric_card("stock", "TOTAL STOCK", "0"), 0, 1)
        metrics.addWidget(self._metric_card("value", "INVENTORY VALUE", "0"), 0, 2)
        metrics.addWidget(self._metric_card("low", "LOW STOCK", "0"), 0, 3)

        row = QHBoxLayout(hero)
        row.setContentsMargins(18, 16, 18, 16)
        row.addLayout(text_col, 2)
        row.addLayout(metrics, 3)
        return hero

    def _metric_card(self, key: str, label: str, value: str) -> QFrame:
        """Create one compact KPI card and keep its value label for refresh()."""

        card = QFrame()
        card.setObjectName("metricCard")

        label_widget = QLabel(label)
        label_widget.setObjectName("metricLabel")
        value_widget = QLabel(value)
        value_widget.setObjectName("metricValue")
        self.summary_labels[key] = value_widget

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        return card

    def _build_filter_row(self) -> QWidget:
        """Build the search row used to demonstrate small UI/UX workflow polish."""

        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Filter inventory")
        label.setStyleSheet("font-weight: 800; color: #24352f;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by name, rarity, price, or stock..."
        )
        self.search_input.textChanged.connect(self.refresh)

        layout.addWidget(label)
        layout.addWidget(self.search_input, 1)
        return row

    def refresh(self) -> None:
        """RO: Reincarca tabelul cu datele curente.
        EN: Reload the table with current data.
        """
        inventory = self.service.list_inventory()
        self._refresh_summary(inventory)

        query = self.search_input.text().strip().casefold()
        data = [art for art in inventory if self._matches_filter(art, query)]
        self.table.setRowCount(len(data))
        for r, art in enumerate(data):
            values = [
                str(art.id),
                art.name,
                art.rarity,
                self._format_currency(art.price),
                str(art.stock),
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignVCenter
                    | (
                        Qt.AlignmentFlag.AlignRight
                        if column in {0, 3, 4}
                        else Qt.AlignmentFlag.AlignLeft
                    )
                )
                if column == 2:
                    item.setBackground(self._rarity_color(art.rarity))
                if art.stock <= 2:
                    item.setToolTip(
                        "Low stock: restock or play Arcade Mode for reward units."
                    )
                self.table.setItem(r, column, item)
        if data and self.table.currentRow() < 0:
            # Keep actions usable right after load by preselecting the first row.
            self.table.selectRow(0)

    def _refresh_summary(self, data) -> None:
        """Update KPI cards from the service data, not from the filtered table."""

        total_stock = sum(art.stock for art in data)
        total_value = sum(art.price * art.stock for art in data)
        low_stock = sum(1 for art in data if art.stock <= 2)
        self.summary_labels["items"].setText(str(len(data)))
        self.summary_labels["stock"].setText(str(total_stock))
        self.summary_labels["value"].setText(self._format_currency(total_value))
        self.summary_labels["low"].setText(str(low_stock))

    def _matches_filter(self, art, query: str) -> bool:
        """Return True when a row should remain visible for the current filter."""

        if not query:
            return True
        haystack = (
            f"{art.id} {art.name} {art.rarity} {art.price} {art.stock}".casefold()
        )
        return query in haystack

    def _format_currency(self, value: int) -> str:
        """Format numbers consistently for the UI while keeping storage numeric."""

        return f"{value:,} gold".replace(",", " ")

    def _rarity_color(self, rarity: str) -> QColor:
        """Map rarity labels to subtle row accents for faster visual scanning."""

        palette = {
            "common": "#ecfccb",
            "rare": "#dbeafe",
            "epic": "#ede9fe",
            "legendary": "#fef3c7",
            "mythic": "#ffe4e6",
        }
        return QColor(palette.get(rarity.strip().casefold(), "#f8fafc"))

    def selected_id(self) -> int | None:
        """RO: Intoarce id-ul selectat sau None.
        EN: Return selected id or None.
        """
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

    def require_selected_id(self, action_name: str) -> int | None:
        """RO: Cere selectie valida inainte de o actiune.
        EN: Require a valid selection before an action.
        """
        art_id = self.selected_id()
        if art_id is None:
            QMessageBox.information(
                self,
                "No selection",
                f"Select an artifact row first, then use {action_name}.",
            )
            return None
        return art_id

    def add_artifact(self) -> None:
        """RO: Deschide dialogul de adaugare.
        EN: Open the add dialog.
        """
        dlg = ArtifactDialog("Add Artifact")
        if dlg.exec():
            name, rarity, price, stock = dlg.values()
            try:
                self.service.add_artifact(name, rarity, price, stock)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def edit_artifact(self) -> None:
        """RO: Editeaza artefactul selectat.
        EN: Edit the selected artifact.
        """
        art_id = self.require_selected_id("Edit")
        if art_id is None:
            return
        items = [a for a in self.service.list_inventory() if a.id == art_id]
        if not items:
            return
        art = items[0]
        dlg = ArtifactDialog(
            "Edit Artifact", art.name, art.rarity, art.price, art.stock
        )
        if dlg.exec():
            name, rarity, price, stock = dlg.values()
            try:
                self.service.update_artifact(art_id, name, rarity, price, stock)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def delete_artifact(self) -> None:
        """RO: Sterge artefactul selectat (cu confirmare).
        EN: Delete selected artifact (with confirmation).
        """
        art_id = self.require_selected_id("Delete")
        if art_id is None:
            return
        confirm = QMessageBox.question(self, "Confirm", "Delete selected artifact?")
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_artifact(art_id)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def buy_artifact(self) -> None:
        """RO: Cumpara o cantitate (scade stocul).
        EN: Buy a quantity (decrease stock).
        """
        art_id = self.require_selected_id("Buy")
        if art_id is None:
            return
        qty, ok = QInputDialog.getInt(self, "Buy", "Quantity", 1, 1, 1000)
        if ok:
            try:
                self.service.buy(art_id, qty)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def restock_artifact(self) -> None:
        """RO: Reaprovizioneaza stocul pentru artefact.
        EN: Restock the artifact.
        """
        art_id = self.require_selected_id("Restock")
        if art_id is None:
            return
        qty, ok = QInputDialog.getInt(self, "Restock", "Quantity", 1, 1, 10000)
        if ok:
            try:
                self.service.restock(art_id, qty)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def open_arcade(self) -> None:
        """RO: Deschide mini-game-ul arcade si ofera reward pe stoc.
        EN: Open arcade mini-game and offer stock reward.
        """
        dlg = ArcadeDialog(self)
        dlg.exec()
        reward = dlg.reward_units()
        if reward <= 0:
            return

        art_id = self.selected_id()
        if art_id is None:
            QMessageBox.information(
                self,
                "Arcade reward",
                f"You earned {reward} stock units. Select an artifact row, then play again to apply.",
            )
            return

        try:
            self.service.restock(art_id, reward)
            self.refresh()
            QMessageBox.information(
                self,
                "Arcade reward applied",
                f"Added +{reward} stock units to selected artifact.",
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))
