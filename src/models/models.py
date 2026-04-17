from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Subsystem:
    """
    Acts as a registry for folder result. It records a specific part of a codebase.
    """
    name: str
    path: str
    file_count: int
    notes: str


@dataclass(frozen=True)
class PortingModule:
    """
    This represents a single unit of work (e.g., a specific file or feature) that needs to be moved or translated.
    """
    name: str
    responsibility: str
    source_hint: str
    status: str = 'planned'


@dataclass(frozen=True)
class PermissionDenial:
    """
    A specialized error-tracking object. If the CLI tries to use a tool (like reading a sensitive file) and gets blocked, it stores the tool's name and the reason here rather than just crashing.
    """
    tool_name: str
    reason: str


@dataclass(frozen=True)
class UsageSummary:
    input_tokens: int = 0
    output_tokens: int = 0

    def add_turn(self, prompt: str, output: str) -> 'UsageSummary':
        return UsageSummary(
            input_tokens=self.input_tokens + len(prompt.split()),
            output_tokens=self.output_tokens + len(output.split()),
        )


@dataclass
class PortingBacklog:
    """
    This is mutable (not frozen). It is the master list of everything that needs to be ported.
    """
    title: str
    modules: list[PortingModule] = field(default_factory=list)

    def summary_lines(self) -> list[str]:
        return [
            f'- {module.name} [{module.status}] — {module.responsibility} (from {module.source_hint})'
            for module in self.modules
        ]