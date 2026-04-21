from __future__ import annotations

from pathlib import Path

from .algorithms import policy_iteration, value_iteration
from .examples import build_trading_mdp, solve_american_put
from .plotting import save_convergence_plot, save_option_tree_plot, save_reward_heatmap
from .reporting import write_option_table, write_trading_summary


def build_project_outputs(project_root: Path) -> None:
    """Generate figures and tables used by the presentation."""

    figures_dir = project_root / "assets" / "figures"
    output_dir = project_root / "output"

    mdp = build_trading_mdp()
    policy_result = policy_iteration(mdp)
    value_result = value_iteration(mdp)
    option_result = solve_american_put()

    save_reward_heatmap(mdp, figures_dir / "trading_reward_heatmap.png")
    save_convergence_plot(policy_result, value_result, figures_dir / "trading_convergence.png")
    save_option_tree_plot(option_result, figures_dir / "american_put_tree.png")

    write_trading_summary(mdp, policy_result, value_result, output_dir / "trading_summary.md")
    write_option_table(option_result, output_dir / "american_put_table.csv")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    build_project_outputs(project_root)


if __name__ == "__main__":
    main()
