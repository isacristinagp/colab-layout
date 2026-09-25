"""Caminhos do GDS passivo.

O bloco sai do notebook `gds_passivo.ipynb`. A inclusão na máscara
de fabricação fica em `main/main.py`.
"""

from __future__ import annotations

from pathlib import Path

import photonforge as pf

HERE = Path(__file__).resolve().parent
SAIDA = HERE / "saida"
AREA_W_UM = 1500.0
AREA_H_UM = 1800.0
CELL_NAME = "mzi_o4_passivo"

PASSIVO_GDS = SAIDA / "passivo.gds"


def repo_root() -> Path:
    for base in (HERE, *HERE.parents):
        host = (
            base
            / "MZI-Estagio-layout-nanotools"
            / "layout-main"
            / "CircuitoLucivaldoV1.gds"
        )
        if host.is_file():
            return base
    raise FileNotFoundError("repositório MZI-Estagio não encontrado a partir de circuito-isa-jose-v1")


def nano_root() -> Path:
    return repo_root() / "MZI-Estagio-layout-nanotools"


def box(comp: pf.Component) -> tuple[float, float, float, float]:
    blo, bhi = comp.bounds()
    return float(blo[0]), float(blo[1]), float(bhi[0]), float(bhi[1])


def walk_components(comp: pf.Component, seen: set[int] | None = None):
    seen = set() if seen is None else seen
    if id(comp) in seen:
        return
    seen.add(id(comp))
    yield comp
    for ref in comp.references:
        yield from walk_components(ref.component, seen)


def assert_no_layer6(comp: pf.Component) -> None:
    used: set[tuple[int, int]] = set()
    for cell in walk_components(comp):
        used.update(cell.structures.keys())
    if (6, 0) in used:
        raise RuntimeError("camada 6/0 presente — exige aprovação ANT")
