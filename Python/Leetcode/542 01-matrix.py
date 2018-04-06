# -*- coding: utf-8 -*-
import collection

def updateMatrix(matrix):
    """
    :type matrix: List[List[int]]
    :rtype: List[List[int]]
    """
    queue = collections.deque([])
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            if matrix[i][j] == 0:
                queue.append((i, j))
            else:
                matrix[i][j] = float("inf")

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cell = queue.popleft()
        for dir in dirs:
            i, j = cell[0]+dir[0], cell[1]+dir[1]
            if not (0 <= i < len(matrix)) or not (0 <= j < len(matrix[0])) or \
               matrix[i][j] <= matrix[cell[0]][cell[1]]+1:
                    continue
            queue.append((i, j))
            matrix[i][j] = matrix[cell[0]][cell[1]]+1
    
    return matrix


if __name__ == '__main__':
    matrix = [[0,0,0],
              [0,1,0],
              [0,0,0]
             ]
    print (updateMatrix(matrix))