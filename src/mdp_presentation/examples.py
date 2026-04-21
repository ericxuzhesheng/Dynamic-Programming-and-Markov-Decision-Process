from __future__ import annotations

import math

import numpy as np

from .models import FiniteMDP, OptionResult


def build_trading_mdp(discount: float = 0.90) -> FiniteMDP:
    """Create the two-state trading example used in the presentation."""

    state_names = ["Bull", "Bear"]
    action_names = ["Buy", "Sell"]

    transition_probabilities = np.array(
        [
            [[0.70, 0.30], [0.30, 0.70]],
            [[0.30, 0.70], [0.70, 0.30]],
        ],
        dtype=float,
    )

    rewards = np.array(
        [
            [10.0, -5.0],
            [-10.0, 5.0],
        ],
        dtype=float,
    )

    return FiniteMDP(
        state_names=state_names,
        action_names=action_names,
        transition_probabilities=transition_probabilities,
        rewards=rewards,
        discount=discount,
    )


def solve_american_put(
    steps: int = 3,
    initial_price: float = 100.0,
    strike: float = 95.0,
    annual_rate: float = 0.12,
    volatility: float = 0.20,
    maturity_years: float = 0.25,
) -> OptionResult:
    """Solve a small American put by backward induction on a binomial tree."""

    dt = maturity_years / steps
    up_factor = math.exp(volatility * math.sqrt(dt))
    down_factor = 1.0 / up_factor
    discount_factor = math.exp(-annual_rate * dt)
    growth = math.exp(annual_rate * dt)
    risk_neutral_probability = (growth - down_factor) / (up_factor - down_factor)

    if not 0.0 < risk_neutral_probability < 1.0:
        raise ValueError("Risk-neutral probability must lie in (0, 1).")

    stock_tree = np.full((steps + 1, steps + 1), np.nan, dtype=float)
    option_tree = np.full((steps + 1, steps + 1), np.nan, dtype=float)
    continuation_tree = np.full((steps + 1, steps + 1), np.nan, dtype=float)
    intrinsic_tree = np.full((steps + 1, steps + 1), np.nan, dtype=float)
    decision_tree = np.full((steps + 1, steps + 1), "", dtype=object)

    for time_step in range(steps + 1):
        for down_moves in range(time_step + 1):
            stock_tree[time_step, down_moves] = (
                initial_price
                * (up_factor ** (time_step - down_moves))
                * (down_factor ** down_moves)
            )

    intrinsic_tree[steps, : steps + 1] = np.maximum(strike - stock_tree[steps, : steps + 1], 0.0)
    option_tree[steps, : steps + 1] = intrinsic_tree[steps, : steps + 1]
    decision_tree[steps, : steps + 1] = "Exercise"

    for time_step in range(steps - 1, -1, -1):
        for down_moves in range(time_step + 1):
            continuation_value = discount_factor * (
                risk_neutral_probability * option_tree[time_step + 1, down_moves]
                + (1.0 - risk_neutral_probability) * option_tree[time_step + 1, down_moves + 1]
            )
            intrinsic_value = max(strike - stock_tree[time_step, down_moves], 0.0)

            continuation_tree[time_step, down_moves] = continuation_value
            intrinsic_tree[time_step, down_moves] = intrinsic_value

            if intrinsic_value > continuation_value:
                option_tree[time_step, down_moves] = intrinsic_value
                decision_tree[time_step, down_moves] = "Exercise"
            else:
                option_tree[time_step, down_moves] = continuation_value
                decision_tree[time_step, down_moves] = "Hold"

    return OptionResult(
        stock_tree=stock_tree,
        option_tree=option_tree,
        decision_tree=decision_tree,
        continuation_tree=continuation_tree,
        intrinsic_tree=intrinsic_tree,
        risk_neutral_probability=risk_neutral_probability,
        up_factor=up_factor,
        down_factor=down_factor,
        discount_factor=discount_factor,
    )
