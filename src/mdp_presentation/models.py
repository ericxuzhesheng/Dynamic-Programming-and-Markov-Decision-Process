from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FiniteMDP:
    """A finite discounted Markov decision process."""

    state_names: list[str]
    action_names: list[str]
    transition_probabilities: np.ndarray
    rewards: np.ndarray
    discount: float

    def __post_init__(self) -> None:
        transition_shape = self.transition_probabilities.shape
        reward_shape = self.rewards.shape
        state_count = len(self.state_names)
        action_count = len(self.action_names)

        if transition_shape != (state_count, action_count, state_count):
            raise ValueError(
                "Transition tensor must have shape "
                f"({state_count}, {action_count}, {state_count})."
            )
        if reward_shape != (state_count, action_count):
            raise ValueError(
                f"Reward matrix must have shape ({state_count}, {action_count})."
            )
        if not np.allclose(self.transition_probabilities.sum(axis=2), 1.0):
            raise ValueError("Transition probabilities must sum to 1 along next-state axis.")
        if not 0.0 <= self.discount < 1.0:
            raise ValueError("Discount factor must lie in [0, 1).")

    @property
    def state_count(self) -> int:
        return len(self.state_names)

    @property
    def action_count(self) -> int:
        return len(self.action_names)


@dataclass(frozen=True)
class IterationTrace:
    """Stores diagnostics from iterative dynamic programming algorithms."""

    iteration: int
    values: np.ndarray
    delta: float


@dataclass(frozen=True)
class PolicyIterationResult:
    """Outputs from policy iteration."""

    policy_actions: np.ndarray
    values: np.ndarray
    policy_matrix: np.ndarray
    evaluation_trace: list[IterationTrace]
    evaluation_segments: list[list[IterationTrace]]
    improvement_steps: int


@dataclass(frozen=True)
class OptionResult:
    """Outputs from backward induction on an American put option."""

    stock_tree: np.ndarray
    option_tree: np.ndarray
    decision_tree: np.ndarray
    continuation_tree: np.ndarray
    intrinsic_tree: np.ndarray
    risk_neutral_probability: float
    up_factor: float
    down_factor: float
    discount_factor: float
