from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .algorithms import ValueIterationResult
from .models import FiniteMDP, OptionResult, PolicyIterationResult


plt.rcParams.update(
    {
        "figure.dpi": 150,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "font.size": 10,
    }
)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_convergence_plot(
    policy_result: PolicyIterationResult,
    value_result: ValueIterationResult,
    output_path: Path,
) -> None:
    """Plot convergence diagnostics for the trading MDP."""

    _ensure_parent(output_path)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    final_segment = policy_result.evaluation_segments[-1]
    policy_iterations = [item.iteration for item in final_segment]
    policy_values = np.vstack([item.values for item in final_segment])
    value_iterations = [item.iteration for item in value_result.trace]
    value_values = np.vstack([item.values for item in value_result.trace])

    axes[0].plot(policy_iterations, policy_values[:, 0], label="Bull state")
    axes[0].plot(policy_iterations, policy_values[:, 1], label="Bear state")
    axes[0].set_title("Policy Evaluation Trace")
    axes[0].set_xlabel("Iteration")
    axes[0].set_ylabel("State value")
    axes[0].legend(frameon=False)

    axes[1].plot(value_iterations, value_values[:, 0], label="Bull state")
    axes[1].plot(value_iterations, value_values[:, 1], label="Bear state")
    axes[1].set_title("Value Iteration Trace")
    axes[1].set_xlabel("Iteration")
    axes[1].set_ylabel("State value")
    axes[1].legend(frameon=False)

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_reward_heatmap(mdp: FiniteMDP, output_path: Path) -> None:
    """Visualize the trading reward matrix."""

    _ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    image = ax.imshow(mdp.rewards, cmap="RdYlGn", aspect="auto")

    ax.set_xticks(range(mdp.action_count), mdp.action_names)
    ax.set_yticks(range(mdp.state_count), mdp.state_names)
    ax.set_title("Immediate Reward by State and Action")

    for row in range(mdp.state_count):
        for col in range(mdp.action_count):
            ax.text(col, row, f"{mdp.rewards[row, col]:.0f}", ha="center", va="center")

    fig.colorbar(image, ax=ax, shrink=0.85, label="Reward")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_option_tree_plot(option_result: OptionResult, output_path: Path) -> None:
    """Visualize the stock and option values on the binomial tree."""

    _ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    steps = option_result.stock_tree.shape[0] - 1

    for time_step in range(steps + 1):
        for down_moves in range(time_step + 1):
            x_coord = time_step
            y_coord = time_step - 2 * down_moves
            stock_price = option_result.stock_tree[time_step, down_moves]
            option_value = option_result.option_tree[time_step, down_moves]
            decision = option_result.decision_tree[time_step, down_moves]
            color = "#b22222" if decision == "Exercise" else "#1f4e79"

            ax.scatter(x_coord, y_coord, s=320, color=color, alpha=0.90, edgecolor="white")
            ax.text(
                x_coord,
                y_coord,
                f"S={stock_price:.1f}\nV={option_value:.2f}",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )

            if time_step < steps:
                ax.plot([x_coord, x_coord + 1], [y_coord, y_coord + 1], color="#8a8a8a", lw=1)
                ax.plot([x_coord, x_coord + 1], [y_coord, y_coord - 1], color="#8a8a8a", lw=1)

    ax.set_title("American Put via Backward Induction")
    ax.set_xlabel("Time step")
    ax.set_ylabel("Tree node")
    ax.set_xticks(range(steps + 1))
    ax.set_yticks([])
    ax.text(steps + 0.1, 1.2, "Blue: Hold", color="#1f4e79", fontsize=9)
    ax.text(steps + 0.1, 0.4, "Red: Exercise", color="#b22222", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
