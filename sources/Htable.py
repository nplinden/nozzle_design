class Htable :
    def __init__(self,matrix):
        self.matrix = matrix
        mat_len = max([len(i) for i in matrix])
        for row in matrix :
            for i, string in enumerate(row) :
                if type(string) is float :
                    row[i] = '{:.4g}'.format(string)
        for row in matrix :
            if len(row) < mat_len :
                row += ['' for i in range(mat_len - len(row))]
        self.mat_struc = [['' for j in i] for i in self.matrix]
        self.col_size = max([len(i) for j in matrix for i in j])
        self.display()

    def display(self):
        rprint(self.mat_struc[0],style = '{:─^'+str(self.col_size+2)+'}',typ='top',sep='┬')
        for row in self.matrix :
            rprint(row,style = '{:^'+str(self.col_size+2)+'}')
        rprint(self.mat_struc[0],style = '{:─^'+str(self.col_size+2)+'}',typ='bot',sep='┴')



def rprint(row,typ='mid',style='{:^30}',sep='│'):
    left = {
            'top' : '┌',
            'inter' : '├',
            'mid': '│',
            'bot'  : '└',
            }
    right = {
            'top' : '┐',
            'inter' : '┤',
            'mid': '│',
            'bot'  : '┘',
            }
    print(left[typ] + sep.join([style.format(string) for string in row])+right[typ])

