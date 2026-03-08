from __future__ import annotations

"""Arcade mini-game integrated in the Magic Shop UI.

The game is intentionally lightweight and dependency-free (PyQt only):
- click moving targets to gain score
- misses reduce lives
- score can be converted into shop stock rewards
"""

from random import randint

from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..game_logic import reward_from_score


class ArcadeCanvas(QWidget):
    """Simple moving-target canvas with click scoring."""

    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(560, 320)
        self.setMouseTracking(True)

        self.target_center = QPointF(120.0, 120.0)
        self.target_radius = 22.0
        self.velocity = QPointF(3.6, 2.9)
        self.target_color = QColor("#7c5cff")

        self.score = 0
        self.hits = 0
        self.misses = 0
        self.combo = 1
        self.running = False

        self._tick = QTimer(self)
        self._tick.timeout.connect(self._step)

    def start(self) -> None:
        self.running = True
        self._tick.start(16)

    def stop(self) -> None:
        self.running = False
        self._tick.stop()

    def reset(self) -> None:
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.combo = 1
        self.target_center = QPointF(120.0, 120.0)
        self.velocity = QPointF(3.6, 2.9)
        self.target_color = QColor("#7c5cff")
        self.update()

    def _step(self) -> None:
        if not self.running:
            return

        x = self.target_center.x() + self.velocity.x()
        y = self.target_center.y() + self.velocity.y()

        if x - self.target_radius <= 0 or x + self.target_radius >= self.width():
            self.velocity.setX(-self.velocity.x())
            x = max(self.target_radius, min(self.width() - self.target_radius, x))
        if y - self.target_radius <= 0 or y + self.target_radius >= self.height():
            self.velocity.setY(-self.velocity.y())
            y = max(self.target_radius, min(self.height() - self.target_radius, y))

        self.target_center = QPointF(x, y)
        self.update()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if not self.running:
            return

        pos = event.position()
        dx = pos.x() - self.target_center.x()
        dy = pos.y() - self.target_center.y()
        inside = (dx * dx + dy * dy) <= (self.target_radius * self.target_radius)

        if inside:
            self.hits += 1
            self.combo = min(8, self.combo + 1)
            self.score += 10 * self.combo
            self.velocity.setX(self.velocity.x() * 1.03)
            self.velocity.setY(self.velocity.y() * 1.03)
            self.target_color = QColor(randint(60, 255), randint(60, 255), randint(60, 255))
        else:
            self.misses += 1
            self.combo = 1

        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#12131b"))

        pen = QPen(QColor("#2b2e3b"))
        pen.setWidth(1)
        painter.setPen(pen)
        for x in range(0, self.width(), 24):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 24):
            painter.drawLine(0, y, self.width(), y)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.target_color)
        painter.drawEllipse(self.target_center, self.target_radius, self.target_radius)

        painter.setBrush(QColor(255, 255, 255, 210))
        painter.drawEllipse(self.target_center, self.target_radius * 0.35, self.target_radius * 0.35)


class ArcadeDialog(QDialog):
    """Arcade challenge dialog with score-to-reward conversion."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Arcade Mode")
        self.resize(700, 460)

        self.canvas = ArcadeCanvas()
        self.time_left = 30

        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet("font-weight: 600;")
        self.lbl_hint = QLabel("Hit the moving orb. Misses reduce lives. Higher combo = more points.")
        self.lbl_hint.setStyleSheet("color: #616a77;")

        self.btn_start = QPushButton("Start")
        self.btn_restart = QPushButton("Restart")
        self.btn_close = QPushButton("Close")

        self.btn_start.clicked.connect(self.start_game)
        self.btn_restart.clicked.connect(self.restart_game)
        self.btn_close.clicked.connect(self.accept)

        top = QVBoxLayout()
        top.addWidget(self.lbl_status)
        top.addWidget(self.lbl_hint)
        top.addWidget(self.canvas, 1)

        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.btn_start)
        row.addWidget(self.btn_restart)
        row.addWidget(self.btn_close)
        top.addLayout(row)
        self.setLayout(top)

        self._clock = QTimer(self)
        self._clock.timeout.connect(self._tick_second)
        self._hud = QTimer(self)
        self._hud.timeout.connect(self.refresh_status)
        self._hud.start(120)

        self.refresh_status()

    def start_game(self) -> None:
        if not self.canvas.running:
            self.canvas.start()
            self._clock.start(1000)
            self.btn_start.setEnabled(False)

    def restart_game(self) -> None:
        self._clock.stop()
        self.time_left = 30
        self.canvas.stop()
        self.canvas.reset()
        self.btn_start.setEnabled(True)
        self.refresh_status()

    def _tick_second(self) -> None:
        if not self.canvas.running:
            return
        self.time_left -= 1
        if self.time_left <= 0 or self.canvas.misses >= 12:
            self.time_left = max(0, self.time_left)
            self.canvas.stop()
            self._clock.stop()
            self.btn_start.setEnabled(True)
        self.refresh_status()

    def refresh_status(self) -> None:
        reward = self.reward_units()
        self.lbl_status.setText(
            f"Time: {self.time_left}s | Score: {self.canvas.score} | "
            f"Hits: {self.canvas.hits} | Misses: {self.canvas.misses} | "
            f"Reward units: {reward}"
        )

    def reward_units(self) -> int:
        return reward_from_score(self.canvas.score)
