"""
    On a 2D plane, there are n points with integer coordinates points[i] = [xi, yi]. 
    Return the minimum time in seconds to visit all the points in the order given by points.

    You can move according to these rules:

        In 1 second, you can either:
            move vertically by one unit,
            move horizontally by one unit, or
            move diagonally sqrt(2) units (in other words, move one unit vertically then one unit horizontally in 1 second).
        You have to visit the points in the same order as they appear in the array.
        You are allowed to pass through points that appear later in the order, but these do not count as visits.
"""

points = [[1,1],[3,4],[-1,0]]


# Time Complexity: O(n)
# Space Complexity: O(1) -> Constant 
def minTimeToVisitAllPoints(points: list[list[int]]) -> int:
    """
    :type points: List[List[int]]
    :rtype: int
    """

    spaces_moved: int = 0
    x1, y1: int = points.pop()

    while(points):
        x2, y2: int = points.pop()
        print(f"x2: {x2}, y2: {y2}")
        print((abs(y2 - y1)))
        print((abs(x2 - x1)))
        print(f"{max(abs(y2 - y1), abs(x2 - x1))}")
        spaces_moved += max(abs(y2 - y1), abs(x2 - x1))
        print(f"spaces_moved: {spaces_moved}")
        x1, y1 = x2, y2
    
    return spaces_moved


result = minTimeToVisitAllPoints(points)
print(result)
