from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .models import FiniteMDP, IterationTrace, PolicyIterationResult


@dataclass(frozen=True)
class ValueIterationResult:
    """Outputs from value iteration."""

    values: np.ndarray
    policy_actions: np.ndarray
    trace: list[IterationTrace]


def policy_evaluation(
    mdp: FiniteMDP,
    policy_matrix: np.ndarray,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> tuple[np.ndarray, list[IterationTrace]]:
    """Evaluate a stochastic policy by iterative Bellman expectation updates."""

    values = np.zeros(mdp.state_count, dtype=float)
    trace: list[IterationTrace] = []

    for iteration in range(1, max_iterations + 1):
        action_values = mdp.rewards + mdp.discount * np.einsum(
            "sak,k->sa", mdp.transition_probabilities, values
        )
        updated_values = np.sum(policy_matrix * action_values, axis=1)
        delta = float(np.max(np.abs(updated_values - values)))
        values = updated_values
        trace.append(IterationTrace(iteration=iteration, values=values.copy(), delta=delta))

        if delta < tolerance:
            break
    else:
        raise RuntimeError("Policy evaluation failed to converge within the iteration budget.")

    return values, trace


def greedy_policy(mdp: FiniteMDP, values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute a deterministic greedy policy with respect to a value function."""

    action_values = mdp.rewards + mdp.discount * np.einsum(
        "sak,k->sa", mdp.transition_probabilities, values
    )
    policy_actions = np.argmax(action_values, axis=1)
    policy_matrix = np.zeros((mdp.state_count, mdp.action_count), dtype=float)
    policy_matrix[np.arange(mdp.state_count), policy_actions] = 1.0
    return policy_actions, policy_matrix


def policy_iteration(
    mdp: FiniteMDP,
    tolerance: float = 1e-10,
    max_policy_steps: int = 100,
) -> PolicyIterationResult:
    """Run classical Howard policy iteration for a finite discounted MDP."""

    policy_matrix = np.zeros((mdp.state_count, mdp.action_count), dtype=float)
    policy_matrix[:, 0] = 1.0
    evaluation_trace: list[IterationTrace] = []
    evaluation_segments: list[list[IterationTrace]] = []

    for improvement_step in range(1, max_policy_steps + 1):
        values, latest_trace = policy_evaluation(mdp, policy_matrix, tolerance=tolerance)
        evaluation_trace.extend(latest_trace)
        evaluation_segments.append(latest_trace)
        policy_actions, improved_policy = greedy_policy(mdp, values)

        if np.array_equal(improved_policy, policy_matrix):
            return PolicyIterationResult(
                policy_actions=policy_actions,
                values=values,
                policy_matrix=policy_matrix,
                evaluation_trace=evaluation_trace,
                evaluation_segments=evaluation_segments,
                improvement_steps=improvement_step,
            )

        policy_matrix = improved_policy

    raise RuntimeError("Policy iteration failed to stabilize within the policy-step budget.")


def value_iteration(
    mdp: FiniteMDP,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> ValueIterationResult:
    """Run Bellman optimality updates until the value function converges."""

    values = np.zeros(mdp.state_count, dtype=float)
    trace: list[IterationTrace] = []

    for iteration in range(1, max_iterations + 1):
        action_values = mdp.rewards + mdp.discount * np.einsum(
            "sak,k->sa", mdp.transition_probabilities, values
        )
        updated_values = np.max(action_values, axis=1)
        delta = float(np.max(np.abs(updated_values - values)))
        values = updated_values
        trace.append(IterationTrace(iteration=iteration, values=values.copy(), delta=delta))

        if delta < tolerance:
            break
    else:
        raise RuntimeError("Value iteration failed to converge within the iteration budget.")

    policy_actions, _ = greedy_policy(mdp, values)
    return ValueIterationResult(values=values, policy_actions=policy_actions, trace=trace)
