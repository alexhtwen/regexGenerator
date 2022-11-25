with (open('file1.txt', 'r') as    fin ,
        open( 'file3.txt', 'w') as fout)  :
    fout.write(fin.read())
