from __future__ import annotations

"""RO: Fereastra principala pentru administrarea inventarului.
EN: Main window for inventory management.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QInputDialog,
)

from ..services import ShopService
from .widgets import ArtifactDialog


class MainWindow(QMainWindow):
    """RO: UI pentru listare, adaugare si operatii pe stoc.
    EN: UI for listing, adding, and stock operations.
    """
    def __init__(self, service: ShopService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Magic Shop")
        self.resize(900, 540)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Rarity", "Price", "Stock"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        toolbar = QToolBar("Actions")
        self.addToolBar(toolbar)

        btn_add = QPushButton("Add")
        btn_edit = QPushButton("Edit")
        btn_delete = QPushButton("Delete")
        btn_buy = QPushButton("Buy")
        btn_restock = QPushButton("Restock")

        btn_add.clicked.connect(self.add_artifact)
        btn_edit.clicked.connect(self.edit_artifact)
        btn_delete.clicked.connect(self.delete_artifact)
        btn_buy.clicked.connect(self.buy_artifact)
        btn_restock.clicked.connect(self.restock_artifact)

        for b in [btn_add, btn_edit, btn_delete, btn_buy, btn_restock]:
            toolbar.addWidget(b)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.table)
        self.setCentralWidget(container)

        self.refresh()

    def refresh(self) -> None:
        """RO: Reincarca tabelul cu datele curente.
        EN: Reload the table with current data.
        """
        data = self.service.list_inventory()
        self.table.setRowCount(len(data))
        for r, art in enumerate(data):
            self.table.setItem(r, 0, QTableWidgetItem(str(art.id)))
            self.table.setItem(r, 1, QTableWidgetItem(art.name))
            self.table.setItem(r, 2, QTableWidgetItem(art.rarity))
            self.table.setItem(r, 3, QTableWidgetItem(str(art.price)))
            self.table.setItem(r, 4, QTableWidgetItem(str(art.stock)))
        self.table.resizeColumnsToContents()

    def selected_id(self) -> int | None:
        """RO: Intoarce id-ul selectat sau None.
        EN: Return selected id or None.
        """
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

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
        art_id = self.selected_id()
        if art_id is None:
            return
        items = [a for a in self.service.list_inventory() if a.id == art_id]
        if not items:
            return
        art = items[0]
        dlg = ArtifactDialog("Edit Artifact", art.name, art.rarity, art.price, art.stock)
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
        art_id = self.selected_id()
        if art_id is None:
            return
        if QMessageBox.question(self, "Confirm", "Delete selected artifact?"):
            try:
                self.service.delete_artifact(art_id)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def buy_artifact(self) -> None:
        """RO: Cumpara o cantitate (scade stocul).
        EN: Buy a quantity (decrease stock).
        """
        art_id = self.selected_id()
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
        art_id = self.selected_id()
        if art_id is None:
            return
        qty, ok = QInputDialog.getInt(self, "Restock", "Quantity", 1, 1, 10000)
        if ok:
            try:
                self.service.restock(art_id, qty)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))
