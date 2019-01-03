# Policy-and-Value-Iteration
an agent moves in a grid, with specific actions and rewards for each move, the goal is to reach a specific cell, with the highest reward possible.
 
problem definition : 
The agent may start in any cell. It can choose between four actions: moving one cell up, moving one cell down, moving one cell left, and moving one cell right. When it reaches cell G, it will receive 100 points and the episode ends. When it reaches a cell marked *, it will receive 5 points and the episode continues. When it attempts to enter a cell marked X, it will receive -20 points and stay in the cell it came from. When it attempts to leave the grid, it will receive -10 points and stay where it is. All actions entering an unmarked cell will receive -1 point. 

in file #1:
The expected value of all cells for a policy that chooses with probability 0.5 a random action and otherwise moves towards the right is Computed. The discount parameter is γ=0.8.
also it uses Policy Iteration algorithm to compute the optimal value V*(s) for each cell. The resulting optimal policy π*(s) is Indicated with arrows in each cell.

in file #2:
The action set is Extended by also allowing diagonal moves, such that the agent can move to its eight neighboring cells. The Value Iteration algorithm is used to compute the optimal value V*(s) for each cell. The resulting optimal policy π*(s) is indicated with arrows in each cell. 

in file #3:
non-deterministic actions are considered, where the agent moves with probability 0.6 into the desired direction, but with probability 0.2 deviates 45° to the left and with probability 0.2 deviates 45° to the right of the desired direction. V*(s) is computed and π*(s) is indicated with arrows.
