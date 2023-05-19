"""
* user:  napoli_codeek89@gmail.com
* fname: Luigi
* lname: Cuomo
* task:  evolution
* score: 0.0
* date:  2021-02-02 16:54:33.192948
"""
#!/bin/env python3

import sys

# def is_border_cell(n_pos, m_pos, N, M) -> bool:
#     return (n_pos == 0 or n_pos == N-1) or (m_pos == 0 or m_pos == M-1)

def is_angle_cell(n_pos, m_pos, N, M) -> bool:
    return (n_pos == 0 or n_pos == N-1) and (m_pos == 0 or m_pos == M-1)

def is_first_column(n_pos, m_pos, N, M) -> bool:
    return (m_pos == 0) and (n_pos > 0 or n_pos < (N-1))

def is_last_column(n_pos, m_pos, N, M) -> bool:
    return (m_pos == M-1) and (n_pos > 0 or n_pos < N-1)

def is_first_row(n_pos, m_pos, N, M) -> bool:
    return (n_pos == 0) and (m_pos > 0 or m_pos < M-1)

def is_last_row(n_pos, m_pos, N, M) -> bool:
    return (n_pos == N-1) and (m_pos > 0 or m_pos < M-1)



def count_not_empty_cell(grid, row_pos, col_pos, N, M):
    if is_first_row(row_pos, col_pos, N, M):
        counter = 0
        if grid[row_pos][col_pos-1] != '.':
            counter += 1
        if grid[row_pos][col_pos+1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos] != '.':
            counter += 1
        if grid[row_pos+1][col_pos+1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos-1] != '.':
            counter += 1
        return counter
    
    elif is_first_column(row_pos, col_pos, N, M):
        print(f"row_pos: {row_pos}, col_pos:{col_pos}")
        counter = 0
        if grid[row_pos][col_pos+1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos] != '.':
            counter += 1
        if grid[row_pos-1][col_pos] != '.':
            counter += 1
        if grid[row_pos-1][col_pos+1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos] != '.':
            counter += 1
        return counter
    
    elif is_last_row(row_pos, col_pos, N, M):
        counter = 0
        if grid[row_pos][col_pos-1] != '.':
            counter += 1
        if grid[row_pos-1][col_pos-1] != '.':
            counter += 1
        if grid[row_pos-1][col_pos] != '.':
            counter += 1
        if grid[row_pos-1][col_pos+1] != '.':
            counter += 1
        if grid[row_pos][col_pos+1] != '.':
            counter += 1
        return counter

    elif is_last_column(row_pos, col_pos, N, M):
        counter = 0
        if grid[row_pos-1][col_pos] != '.':
            counter += 1
        if grid[row_pos-1][col_pos-1] != '.':
            counter += 1
        if grid[row_pos][col_pos-1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos-1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos] != '.':
            counter += 1
        return counter 
    
    elif not is_angle_cell(row_pos, col_pos, N, M):
        counter = 0
        if grid[row_pos-1][col_pos-1] != '.':
            counter += 1
        if grid[row_pos-1][col_pos] != '.':
            counter += 1
        if grid[row_pos-1][col_pos+1] != '.':
            counter += 1
        if grid[row_pos][col_pos-1] != '.':
            counter += 1
        if grid[row_pos][col_pos+1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos-1] != '.':
            counter += 1
        if grid[row_pos+1][col_pos] != '.':
            counter += 1
        if grid[row_pos+1][col_pos+1] != '.':
            counter += 1
        return counter 


def update(grid, N, M):
    updated_grid = grid[:][:]
    for index_row, row in enumerate(grid):
        for index_column, el in enumerate(row):
            if el == '.':
                if not is_angle_cell(n_pos=index_row, m_pos=index_column, N=N, M=M):
                    if count_not_empty_cell(grid, index_row, index_column, N, M) > 4:
                        updated_grid[index_row][index_column] = '+'
                else:
                    updated_grid[index_row][index_column] = '.'
            elif el == '+':
                cnt = count_not_empty_cell(grid, index_row, index_column, N, M)
                if not is_angle_cell(n_pos=index_row, m_pos=index_column, N=N, M=M):
                    if cnt > 4:
                        updated_grid[index_row][index_column] = '*'
                    elif cnt < 4:
                        updated_grid[index_row][index_column] = '.'
                else:
                    updated_grid[index_row][index_column] = '.'
            elif el == '*':
                cnt = count_not_empty_cell(grid, index_row, index_column, N, M)
                if not is_angle_cell(n_pos=index_row, m_pos=index_column, N=N, M=M):
                    if cnt > 4:
                        updated_grid[index_row][index_column] = '+'
                    elif cnt < 4:
                        updated_grid[index_row][index_column] = '.'
                else:
                    updated_grid[index_row][index_column] = '.'
    return updated_grid

def solve(fin, fout):

    (N, M, rounds) = map(int, fin.readline().strip().split())

    G = []
    for _ in range(N):
        G.append(list(fin.readline().strip()))

    for _ in range(rounds):
        G = update(grid=G, N=N, M=M)

    for r in G:
        print("".join(r))

if __name__ == "__main__":
    solve(sys.stdin, sys.stdout)
