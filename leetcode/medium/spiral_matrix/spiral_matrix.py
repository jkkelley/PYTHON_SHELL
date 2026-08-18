"""
    Given an m x n matrix, 
    return all elements of the matrix in spiral order.

    ### Questions to ask during an interview

"""

matrix: list[list[int]] = [[1,2,3],[4,5,6],[7,8,9]]
# Expected output: [1,2,3,6,9,8,7,4,5]

# matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
# # Expected output: [1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,12]

# matrix = [[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20],[21,22,23,24,25,26,27,28,29,30],[31,32,33,34,35,36,37,38,39,40],[41,42,43,44,45,46,47,48,49,50],[51,52,53,54,55,56,57,58,59,60],[61,62,63,64,65,66,67,68,69,70],[71,72,73,74,75,76,77,78,79,80],[81,82,83,84,85,86,87,88,89,90],[91,92,93,94,95,96,97,98,99,100]]
# # Expected output: [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,99,98,97,96,95,94,93,92,91,81,71,61,51,41,31,21,11,12,13,14,15,16,17,18,19,29,39,49,59,69,79,89,88,87,86,85,84,83,82,72,62,52,42,32,22,23,24,25,26,27,28,38,48,58,68,78,77,76,75,74,73,63,53,43,33,34,35,36,37,47,57,67,66,65,64,54,44,45,46,56,55]


def spiralOrder(matrix: list[list[int]]) -> list[int]:
    """
    :type matrix: list[list[int]]
    :rtype: list[int]
    """

    if not matrix:
            return []

    ret_list: list[int] = []
    
    top_boundary_point = 0
    left_boundary_point = 0
    bottom_boundary_point = len(matrix) - 1
    right_boundary_point = len(matrix[0]) - 1

    while top_boundary_point <= bottom_boundary_point and left_boundary_point <= right_boundary_point:
        
        # --- CHORE 1: Walk the Top Fence (Left to Right) ---
        for col in range(left_boundary_point, right_boundary_point + 1):
            ret_list.append(matrix[top_boundary_point][col])
        top_boundary_point += 1

        # --- CHORE 2: Walk the Right Fence (Top to Bottom) ---
        for row in range(top_boundary_point, bottom_boundary_point + 1):
            ret_list.append(matrix[row][right_boundary_point])
        right_boundary_point -= 1

        # SAFETY CHECK: Did the top and bottom fences cross while doing Chore 1 or 2?
        if top_boundary_point <= bottom_boundary_point:
            
            # --- CHORE 3: Walk the Bottom Fence (Right to Left) ---
            for col in range(right_boundary_point, left_boundary_point - 1, -1):
                ret_list.append(matrix[bottom_boundary_point][col])
            bottom_boundary_point -= 1

        # SAFETY CHECK: Did the left and right fences cross while doing Chore 1 or 2?
        if left_boundary_point <= right_boundary_point:
            
            # --- CHORE 4: Walk the Left Fence (Bottom to Top) ---
            for row in range(bottom_boundary_point, top_boundary_point - 1, -1):
                ret_list.append(matrix[row][left_boundary_point])
            left_boundary_point += 1

    return ret_list


result: list[int] = spiralOrder(matrix)
print(result)