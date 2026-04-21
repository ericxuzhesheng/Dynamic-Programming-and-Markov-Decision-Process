from __future__ import annotations

from pathlib import Path

import numpy as np

from .algorithms import PolicyIterationResult, ValueIterationResult
from .models import FiniteMDP, OptionResult


def _format_policy(mdp: FiniteMDP, policy_actions: np.ndarray) -> list[str]:
    return [
        f"{state}: {mdp.action_names[action]}"
        for state, action in zip(mdp.state_names, policy_actions, strict=True)
    ]


def write_trading_summary(
    mdp: FiniteMDP,
    policy_result: PolicyIterationResult,
    value_result: ValueIterationResult,
    output_path: Path,
) -> None:
    """Write a plain-text summary for the toy trading example."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Trading MDP Summary",
        "",
        f"Discount factor: {mdp.discount:.2f}",
        "",
        "Optimal policy from policy iteration:",
        *[f"- {entry}" for entry in _format_policy(mdp, policy_result.policy_actions)],
        "",
        "Optimal policy from value iteration:",
        *[f"- {entry}" for entry in _format_policy(mdp, value_result.policy_actions)],
        "",
        "Optimal state values:",
        *[
            f"- {state}: {value:.4f}"
            for state, value in zip(mdp.state_names, policy_result.values, strict=True)
        ],
        "",
        f"Policy improvement steps: {policy_result.improvement_steps}",
        f"Policy evaluation iterations recorded: {len(policy_result.evaluation_trace)}",
        f"Value iteration steps: {len(value_result.trace)}",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_option_table(option_result: OptionResult, output_path: Path) -> None:
    """Export a CSV table for the American put example."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["time_step,down_moves,stock_price,intrinsic_value,continuation_value,option_value,decision"]

    steps = option_result.stock_tree.shape[0] - 1
    for time_step in range(steps + 1):
        for down_moves in range(time_step + 1):
            stock_price = option_result.stock_tree[time_step, down_moves]
            intrinsic_value = option_result.intrinsic_tree[time_step, down_moves]
            continuation_value = option_result.continuation_tree[time_step, down_moves]
            option_value = option_result.option_tree[time_step, down_moves]
            decision = option_result.decision_tree[time_step, down_moves]

            continuation_text = (
                ""
                if np.isnan(continuation_value)
                else f"{continuation_value:.4f}"
            )
            rows.append(
                ",".join(
                    [
                        str(time_step),
                        str(down_moves),
                        f"{stock_price:.4f}",
                        f"{intrinsic_value:.4f}",
                        continuation_text,
                        f"{option_value:.4f}",
                        decision,
                    ]
                )
            )

    output_path.write_text("\n".join(rows), encoding="utf-8")
