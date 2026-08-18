"""
Given an m x n 2D binary grid grid which represents a map
of '1's (land) and '0's (water),
return the number of islands.

An island is surrounded by water and is formed by connecting
adjacent lands horizontally or vertically. You may assume all
four edges of the grid are all surrounded by water.
"""

from collections import deque


grid: list[list[str]] = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

# Choose iterative as recursion can crash your memory with
# an accidental infinite loop... whoops!
# Call stack safety, lower overhead, and explicit control are what we gain
# For trading in brevity and elegance
def numIslands(grid: list[list[str]]) -> int:
    """
        Time Complexity: O(M * N) - Every cell is processed at most once.

        Space Complexity: O(min(M, N)) - Maximum size of the queue in worst case.
    """

    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    num_of_islands: int = 0

    for row in range(rows):
        for col in range(cols):
            # Found a new island!
            if grid[row][col] == "1":
                num_of_islands += 1
                grid[row][col] = "0" # Sink starting land immediately

                # Initialize queue with starting land
                queue = deque([(row, col)])

                # BFS loop to sink all connected land
                while queue:
                    curr_row, curr_col = queue.popleft()

                    # Direction Vectors: Up, Down, Left, Right
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                    for direction_row, direction_col in directions:
                        neighbor_row, neighbor_col = curr_row + direction_row, curr_col + direction_col

                        # Check if neighbor is inside grid bounds and is land "1"
                        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and grid[neighbor_row][neighbor_col] == "1":
                            grid[neighbor_row][neighbor_col] = "0" # Sink BEFORE adding to queue!
                            queue.append((neighbor_row, neighbor_col))
                            
    return num_of_islands



print(numIslands(grid))


# def sinkIslands(row, col, grid):
#     # 1. Base Case: Stop if out of bounds OR on water "0" 🌊
#     if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]) or grid[row][col] == "0":
#         return
    
#     # 2. Sink the land 🏝️ -> 🌊
#     grid[row][col] = "0"

#     # 3. Explore neighbors 🧭
#     # (Up, Down, Left, Right)

#     # UP
#     sinkIslands(row - 1, col, grid)
#     # DOWN
#     sinkIslands(row + 1, col, grid)
#     # LEFT
#     sinkIslands(row, col - 1, grid)
#     # RIGHT
#     sinkIslands(row, col + 1, grid)



# def numIslands(grid: list[list[str]]) -> int:
#     """
#     :type grid: list[list[str]]
#     :rtype: int

#     Time Complexity: O(M * N)
#     - M is the number of rows, N is the number of columns.
#     - We visit each cell in the grid. Sinking land ('1' -> '0') 
#     ensures that no land cell is explored by DFS more than once.

#     Space Complexity: O(M * N)
#     - In the worst case (e.g., the entire grid is one huge island of '1's), 
#     the recursive call stack depth can reach M * N.
#     - Modifying the grid in-place avoids extra memory for a 'visited' set.
#     """

#     if not grid:
#             return []

#     num_of_islands: int = 0

#     for row in range(len(grid)):
#         for col in range(len(grid[0])):
#             if grid[row][col] == "1":
#                 # 1. We found a new island! Increment counter ➕
#                 num_of_islands += 1

#                 # 2. Sink the ENTIRE island so we don't count it again 🌊
#                 sinkIslands(row, col, grid)

#     return num_of_islands


