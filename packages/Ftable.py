
class Ftable :
    def __init__(self):
        self.title = False
        self.columns = []
    def disp(self,style='{:.4g}'):
        headers=[i for col in self.columns for i in col]
        transpose = [[] for i  in self.columns[0]]

        for col in self.columns :
            for i, val in enumerate(col) :
                transpose[i].append(val)
        data_rows = transpose.pop()
        header_rows = transpose
        data_rows = [[style.format(j) for j in i] for i in data_rows]
        table_len = max([len(i) for i in data_rows])
        for i in data_rows :
            if len(i) < table_len :
                i += ['' for j in range(table_len-len(i))]
        data_rows = [list(i) for i in zip(*data_rows)]
        row_struc = header_rows[0]
        self.col_size = max(max([len(string) for j in header_rows for string in j]),max([len(string) for j in data_rows for string in j ]))+2

        if self.title != False :
            self.sprint(self.title,'top')
            print('├' + '┬'.join(['{:─^{}}'.format('',self.col_size) for string in row_struc]) + '┤')
        else : lprint(row_struc,typ='top',style = '{:─^'+str(self.col_size)+'}')
        for row in header_rows :
            rprint(row,style = '{:^'+str(self.col_size)+'}')
            lprint(row_struc,typ='inter',style = '{:╌^'+str(self.col_size)+'}')
        for row in data_rows :
            rprint(row,style = '{:^'+str(self.col_size)+'}')
        lprint(row_struc,typ='bot',style = '{:─^'+str(self.col_size)+'}')
        return


    def add_col(self,values,*args):
        headers = list(args)
        col = headers + [values] 
        self.columns.append(col)
        return

    def set_title(self,title):
        self.title = title


    def sprint(self,string,typ='mid'):
        self.col_num = len(self.columns)
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
        if typ=='top' :
            print('┌'+'{:─^{}}'.format('',self.col_num*self.col_size+self.col_num-1) + '┐')
        print('│'+'{:^{}}'.format(string,self.col_num*self.col_size+self.col_num-1)+'│')
        return
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

def lprint(row,typ='mid',style='{:^30}',bars='s'):
    if bars == 's' :
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
        middle ={
                'top' : '┬',
                'inter' : '┼',
                'mid': '│',
                'bot'  : '┴',
                }
    if bars == 'c' :
        left = {
                'top' : '╭',
                'inter' : '├',
                'mid': '│',
                'bot'  : '╰',
                }
        right = {
                'top' : '╮',
                'inter' : '┤',
                'mid': '│',
                'bot'  : '╯',
                }
        middle ={
                'top' : '┬',
                'inter' : '┼',
                'mid': '│',
                'bot'  : '┴',
                }
    print(left[typ] + middle[typ].join([style.format('') for string in row]) + right[typ])

