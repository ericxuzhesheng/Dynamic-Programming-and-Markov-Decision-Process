from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mdp_presentation.algorithms import policy_iteration
from mdp_presentation.examples import build_trading_mdp, solve_american_put


def print_title() -> None:
    title = "Dynamic Programming and Markov Decision Processes"
    subtitle = "Presentation Demo | Trading MDP and American Put"
    line = "=" * 72
    print(line)
    print(f"{title:^72}")
    print(f"{subtitle:^72}")
    print(line)


def main() -> None:
    print_title()

    trading_mdp = build_trading_mdp()
    trading_result = policy_iteration(trading_mdp)
    option_result = solve_american_put()

    print("\nTrading MDP")
    print("-" * 72)
    for state_name, action_index, value in zip(
        trading_mdp.state_names,
        trading_result.policy_actions,
        trading_result.values,
        strict=True,
    ):
        action_name = trading_mdp.action_names[action_index]
        print(f"State: {state_name:<8} | Optimal action: {action_name:<4} | Value: {value:>7.2f}")

    print("\nAmerican Put Option")
    print("-" * 72)
    print(f"Initial option value: {option_result.option_tree[0, 0]:.2f}")
    print(f"Early exercise at t=2, low-price node: {option_result.decision_tree[2, 2]}")

    print("\nGenerated presentation assets")
    print("-" * 72)
    print("Run `python main.py` to regenerate figures, tables, and slide assets.")
    print("Compile `slides/main.tex` to rebuild the Beamer presentation.")


if __name__ == "__main__":
    main()
