from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

CODE = r"^[A-Z0-9-]{2,20}$"
Side = Literal["short", "long"]


class StripSubmission(BaseModel):
    """One instrument report: a single wash side of one strip.

    The legacy complete-pair body is still accepted so an offline queue that
    already holds both sides can be replayed without change.
    """

    code: str = Field(pattern=CODE)
    side: Side | None = None
    temp: Decimal | None = Field(default=None, ge=4, le=70)
    density: Decimal | None = Field(default=None, ge=0, le=2)
    fade: Decimal | None = Field(default=None, ge=0, le=1)
    short_temp: Decimal | None = Field(default=None, ge=4, le=70)
    long_temp: Decimal | None = Field(default=None, ge=4, le=70)
    short_density: Decimal | None = Field(default=None, ge=0, le=2)
    long_density: Decimal | None = Field(default=None, ge=0, le=2)
    long_fade: Decimal | None = Field(default=None, ge=0, le=1)

    def readings(self):
        if self.side is not None:
            return [self._side(self.side, *self._values(self.side))]
        rows = [
            self._side("short", self.short_temp, self.short_density, None),
            self._side("long", self.long_temp, self.long_density, self.long_fade),
        ]
        rows = [row for row in rows if row is not None]
        if not rows:
            raise ValueError("未包含可登记的读数")
        return rows

    def _values(self, side):
        if side == "short":
            return (
                self.temp if self.temp is not None else self.short_temp,
                self.density if self.density is not None else self.short_density,
                None,
            )
        return (
            self.temp if self.temp is not None else self.long_temp,
            self.density if self.density is not None else self.long_density,
            self.fade if self.fade is not None else self.long_fade,
        )

    def _side(self, side, temp, density, fade):
        if temp is None and density is None and fade is None:
            return None
        if temp is None or density is None:
            raise ValueError("读数缺少水温或密度")
        if side == "long" and fade is None:
            raise ValueError("长洗读数缺少掉色")
        if side == "short":
            fade = None
        return (side, temp, density, fade)


class Selection(BaseModel):
    """Reviewer keeps one reading per side; the others stay on file."""

    reading: int | None = None
    reading_ids: list[int] | None = None
    short: int | None = None
    long: int | None = None

    def requested(self):
        pairs = []
        for side in ("short", "long"):
            value = getattr(self, side)
            if value is not None:
                pairs.append((side, value))
        extra = [self.reading] if self.reading is not None else []
        extra.extend(self.reading_ids or [])
        pairs.extend((None, value) for value in extra)
        return pairs
