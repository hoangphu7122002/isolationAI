def print_board(board):
        head_col = "      "
        for ele in range(0,len(board)):
            head_col += str(ele)
            head_col += '  '
        line = "    "
        line += "-" * 19
        line += '\n'
        head_col += '\n'
        head_col += line
        row = [""] * len(board)
        index = 0
        for i in range(len(board)):
            row[i] += str(i)
            row[i] += '   |'
            for ele in board[index]:
                if ele == 1:
                    row[i] += 'P1|'
                elif ele == -1:
                    row[i] += 'P2|'
                elif ele == 0:
                    row[i] += '  |'
                else:
                    row[i] += 'XX|'
            row[i] += '\n'
            index += 1
        for ele in row:
            head_col += ele
        line = "    "
        line += "-" * 19
        line += '\n'
        head_col += line
        print(head_col)