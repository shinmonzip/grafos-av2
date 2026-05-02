from dataclasses import dataclass


@dataclass(frozen=True)
class DirectedEdge:
    """Representa uma aresta dirigida e ponderada."""

    source: str
    target: str
    weight: int

    def __str__(self) -> str:
        return f"{self.source} -> {self.target} ({self.weight})"
