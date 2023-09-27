import tkinter as tk
import random

NUM_PUZZLES = 9

def generate_puzzles():
    puzzles = []
    for _ in range(NUM_PUZZLES):
        puzzle = [[0] * 9 for _ in range(9)]
        solve_puzzle(puzzle)
        remove_cells(puzzle)
        puzzles.append(puzzle)
    
    return puzzles


def solve_puzzle(puzzle):
    if not find_empty_cell(puzzle):
        return True
    
    row, col = find_empty_cell(puzzle)
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    
    for num in numbers:
        if is_valid_move(puzzle, row, col, num):
            puzzle[row][col] = num
            
            if solve_puzzle(puzzle):
                return True
            
            puzzle[row][col] = 0
    
    return False

def find_empty_cell(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(puzzle, row, col, num):
    # 检查同一行是否存在相同数字
    for j in range(9):
        if puzzle[row][j] == num:
            return False
    
    # 检查同一列是否存在相同数字
    for i in range(9):
        if puzzle[i][col] == num:
            return False
    
    # 检查3x3小方格内是否存在相同数字
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == num:
                return False
    
    return True

def remove_cells(puzzle):
    # 随机移除一定数量的格子作为题目
    num_cells_to_remove = random.randint(30, 40)
    cells_removed = 0
    
    while cells_removed < num_cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            cells_removed += 1

def is_valid_solution():
    global entries, current_puzzle

    # 创建数独谜题并获取其值
    puzzle = [[int(entry.get()) if entry.get() else 0 for entry in row] for row in entries]

    # 检查每一行是否满足条件
    for row in puzzle:
        if not is_valid_row(row):
            result_label.config(text="错误", fg='red')
            return
    
    # 检查每一列是否满足条件
    for col in zip(*puzzle):
        if not is_valid_row(col):
            result_label.config(text="错误", fg='red')
            return
    
    # 检查每个3x3小方格是否满足条件
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [puzzle[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_row(square):
                result_label.config(text="错误", fg='red')
                return
    
    result_label.config(text="正确", fg='green')

def is_valid_row(row):
    # 检查是否包含1-9的数字，且没有重复
    return set(row) == set(range(1, 10))

def show_answer():
    global entries, current_puzzle

    # 创建数独答案窗口
    answer_window = tk.Toplevel(root)
    answer_window.title("查看答案")

    # 解决数独谜题并获取答案
    solved_puzzle = [[int(entry.get()) if entry.get() else 0 for entry in row] for row in entries]
    solve_puzzle(solved_puzzle)
    

    # 创建数独格子
    for i in range(9):
        for j in range(9):
            if solved_puzzle[i][j] == 0:
                entry_text = ""
            else:
                entry_text = str(solved_puzzle[i][j])
            entry = tk.Entry(answer_window, width=2, font=('Arial', 20, 'bold'), justify='center')
            entry.insert(tk.END, entry_text)
            entry.config(state='disabled')
            
        # 添加大正方形边框样式   
            padx = (5, 0) if j % 3 == 0 else (0, 0)
            pady = (5, 0) if i % 3 == 0 else (0, 0)

        # 添加最后一行和最后一列边界样式
            if i == 8:
                pady = (pady[0], 5)
            if j == 8:
                padx = (padx[0], 5)
            entry.grid(row=i, column=j, ipadx=5, ipady=5, padx=padx, pady=pady)

def switch_puzzle(puzzle_idx):
    global puzzles
    puzzles = generate_puzzles()

    global entries, current_puzzle

    current_puzzle = puzzle_idx

    # 刷新数独格子的值
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state='normal')
            if puzzles[current_puzzle][i][j] != 0:
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(tk.END, puzzles[current_puzzle][i][j])
                entries[i][j].config(state='disabled')
            else:
                entries[i][j].delete(0, tk.END)

def open_difficulty_window():
    global difficulty_window
    difficulty_window = tk.Toplevel()
    difficulty_window.title("选择难度")

    # 设置选择难度窗口在屏幕中央显示
    window_width = 300
    window_height = 300
    screen_width = difficulty_window.winfo_screenwidth()
    screen_height = difficulty_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    difficulty_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 创建难度选择按钮
    tk.Button(difficulty_window, text="简单", width=20, height=2, command=lambda: start_game("简单")).pack(pady=5)
    tk.Button(difficulty_window, text="普通", width=20, height=2, command=lambda: start_game("普通")).pack(pady=5)
    tk.Button(difficulty_window, text="困难", width=20, height=2, command=lambda: start_game("困难")).pack(pady=5)
    tk.Button(difficulty_window, text="大师", width=20, height=2, command=lambda: start_game("大师")).pack(pady=5)
    tk.Button(difficulty_window, text="地狱", width=20, height=2, command=lambda: start_game("地狱")).pack(pady=5)

def reset_puzzles():
    global puzzles, current_puzzle
    open_difficulty_window()

def start_game(difficulty):
    # 关闭选择难度窗口
    difficulty_window.destroy()
    start_window.destroy()
    # 在这里放置数独游戏窗口的代码
    # ...

# 创建开始游戏窗口
start_window = tk.Tk()
start_window.title("开始游戏")

# 创建开始游戏按钮
start_button = tk.Button(start_window, text="开始游戏", width=20, height=2, command=open_difficulty_window)
start_button.pack(padx=10, pady=10)

start_window.mainloop()


# 生成九道随机数独谜题
puzzles = generate_puzzles()

# 记录当前显示的数独谜题的索引
current_puzzle = 0

# 创建数独游戏窗口
root = tk.Tk()
root.title("数独游戏")

# 创建数独格子
entries = []
for i in range(9):
    row = []
    for j in range(9):
        if puzzles[current_puzzle][i][j] != 0:
            entry = tk.Entry(root, width=2, font=('Arial', 20, 'bold'), justify='center')
            entry.insert(tk.END, puzzles[current_puzzle][i][j])
            entry.config(state='disabled')
        else:
            entry = tk.Entry(root, width=2, font=('Arial', 20,'bold'), justify='center')

        # 添加大正方形边框样式
        padx = (5, 0) if j % 3 == 0 else (0, 0)
        pady = (5, 0) if i % 3 == 0 else (0, 0)

        # 添加最后一行和最后一列边界样式
        if i == 8:
            pady = (pady[0], 5)
        if j == 8:
            padx = (padx[0], 5)

        entry.grid(row=i, column=j, ipadx=5, ipady=5, padx=padx, pady=pady)
        row.append(entry)
    entries.append(row)

# 创建切换题目的按钮
switch_buttons = []
for i in range(NUM_PUZZLES):
    # 创建回调函数
    def switch_callback(idx):
        # 切换题目的逻辑
        def inner():
            global current_puzzle
            current_puzzle = idx
            for j, button in enumerate(switch_buttons):
                if j == idx:
                    button.config(relief=tk.SUNKEN)
                else:
                    button.config(relief=tk.RAISED)
            switch_puzzle(idx)
        return inner
    
    # 创建按钮并添加到列表中
    switch_button = tk.Button(root, text=str(i + 1), font=('Arial', 16), width=2, height=1, command=switch_callback(i))
    switch_buttons.append(switch_button)
    
    # 设置按钮样式
    if i == 0:
        switch_button.config(relief=tk.SUNKEN)  # 按钮1设置为按下状态
    else:
        switch_button.config(relief=tk.RAISED)
    
    # 在网格布局中定位按钮
    switch_button.grid(row=10, column=i, padx=5, pady=10)

def reset_puzzles():
    global puzzles, current_puzzle
    open_difficulty_window()

# 添加重置按钮
reset_button = tk.Button(root, text="重置", command=reset_puzzles)
reset_button.grid(row=12, column=1, padx=5, pady=10)  

# 添加验证按钮
validate_button = tk.Button(root, text="提交答案", command=is_valid_solution)
validate_button.grid(row=12, column=2, columnspan=5, pady=10)

# 添加显示答案按钮
answer_button = tk.Button(root, text="显示答案", command=show_answer)
answer_button.grid(row=12, column=6, columnspan=5, pady=10)

# 添加结果标签
result_label = tk.Label(root, text="", fg='black')
result_label.grid(row=11, columnspan=9)

root.mainloop()
