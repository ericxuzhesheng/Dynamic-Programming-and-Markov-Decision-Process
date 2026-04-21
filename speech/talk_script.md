# Talk Script

## Slide 1 - Title
Good afternoon everyone. Today our topic is dynamic programming and Markov decision processes. Instead of presenting them as separate definitions, I will show them as one coherent algorithmic story. The goal is to understand how sequential decisions under uncertainty can be modeled, solved, and interpreted, with two finance-related examples at the end.

## Slide 2 - Presentation Roadmap
The presentation has four parts. First, I explain why dynamic programming and Markov structure belong together. Second, I introduce the MDP model and the Bellman equations. Third, I compare policy iteration and value iteration. Finally, I apply the framework to a trading toy model and to an American put option.

## Slide 3 - Motivation
Many real problems are not single-step optimization problems. We need to make a decision now, the environment changes, and then we decide again. That creates a sequence of interdependent choices. Dynamic programming helps because it breaks the full problem into smaller continuation problems. Markov modeling helps because it tells us what information the state must contain so that the future depends only on the present, not on the full history.

## Slide 4 - Dynamic Programming in One Slide
Here I want to compress dynamic programming into four elements: stage, state, decision, and value function. The value function is the key object because it represents the best future outcome from the current state onward. The two structural conditions are also important. Optimal substructure means the global optimum is built from optimal subproblems. No aftereffect means once the current state is known, we do not need the full past path anymore.

## Slide 5 - Why Markov Structure Matters
This is the probabilistic side of the story. A Markov process has the memoryless property: conditional on the current state, the next state does not depend on earlier states. That property is not just mathematically elegant. It is exactly what allows recursive optimization. If the state captures all relevant information, then future value can be written as a function of the current state alone.

## Slide 6 - Markov Decision Process Formulation
Once we add actions and rewards to a Markov process, we obtain a Markov decision process. An MDP contains a state space, an action space, transition probabilities, a reward rule, and a discount factor. A policy tells us how actions are chosen in each state. From that point on, the whole optimization problem becomes: choose a policy that maximizes expected discounted return.

## Slide 7 - Bellman Expectation and Optimality Equations
These two equations are the mathematical center of the presentation. The Bellman expectation equation evaluates a fixed policy. It says the value of a state equals expected immediate reward plus discounted expected continuation value. The Bellman optimality equation goes one step further by replacing the policy average over actions with a maximization. That single change turns evaluation into optimization.

## Slide 8 - Two Standard Dynamic Programming Algorithms
Now we move from equations to algorithms. Policy iteration alternates between two phases: evaluate the current policy, then improve it greedily. Value iteration skips full policy evaluation and directly applies the Bellman optimality operator to the value function. Both are standard dynamic programming methods for finite MDPs. The difference is mainly computational style rather than objective.

## Slide 9 - Computational Perspective
This slide gives a realistic computational interpretation. Dynamic programming is efficient when the model is explicit and the state space is manageable. But the state space matters a lot. A Bellman sweep scales with the number of states squared times the number of actions in the finite case shown here. So the framework is elegant, but scaling remains the central practical challenge.

## Slide 10 - Example 1: A Two-State Trading MDP
The first example is deliberately small. We only keep two market regimes: bull and bear. The action set is buy or sell. This is not meant to be a realistic trading system. It is meant to make the algorithm visible. With such a small model, we can write down the rewards, transitions, and optimal policy completely and see how the Bellman logic works end to end.

## Slide 11 - Reward Structure and Transition Logic
This slide combines the economic intuition and the model inputs. Buying in a bull market receives a positive immediate reward, while buying in a bear market is penalized. Selling has the opposite interpretation. The heatmap is useful because it lets the audience see immediately that the reward structure favors trend-following in the bull state and defensive action in the bear state, although the final policy still depends on future transitions as well.

## Slide 12 - Algorithmic Result for the Trading Example
After running both policy iteration and value iteration, we obtain the same optimal policy: buy in the bull state and sell in the bear state. The state values are approximately 86.5 and 81.5. The convergence figure matters because it shows that the result is not just asserted. It is generated by a reproducible algorithm, and both iterative procedures stabilize toward the same solution.

## Slide 13 - Why an American Put Fits Dynamic Programming
The second example is more financially meaningful. For an American put, the holder has a decision at every node: exercise now or continue to hold the option. That makes the problem a natural dynamic program. The Bellman recursion compares intrinsic value with discounted continuation value. Once that recursion is written down, backward induction gives the solution.

## Slide 14 - Model Setup
Here I briefly introduce the numerical setup. We use a three-step binomial tree with an initial stock price of 100, strike 95, three months to maturity, twelve percent annual interest rate, and twenty percent volatility. The point is not the exact calibration. The point is to show how a clean state-transition model produces a transparent exercise rule.

## Slide 15 - Backward-Induction Result
The output shows where early exercise becomes optimal. In this example, the option should be exercised only in the deep in-the-money branch near maturity. At earlier nodes, holding is more valuable because it preserves upside from future price moves. The initial option value is about 1.18. This example highlights that dynamic programming handles both valuation and decision timing in one framework.

## Slide 16 - Main Conclusions
To conclude, dynamic programming is the computational principle, Markov structure is the modeling principle, and Bellman equations are the bridge between them. The trading example showed optimal action selection in an MDP, while the American put example showed optimal stopping through backward induction. Together they illustrate the same core idea: solve a sequential problem by writing the value of today in terms of the value of tomorrow.

## Slide 17 - End
Thank you for listening. I am happy to take questions.
