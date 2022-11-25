start = {'char': '^', 'pos': 0}
end = {'char': '$', 'pos': -1}
anchors = {
    'include': '',
    'start': [start],
    'end': [end],
    'both': [start, end]
}

escapes = [r'\', '[', ']', '(', ')', '{', '}', '*', '+', '?', ' | ', ' ^ ', '$', '.', ]

while Ture:
    pattern = input('欄位：')
    position = input(
        '1.包含(include)  2.起始(start)  3.結束(end)  4.起始&結束(start & end)')


print(elements)
