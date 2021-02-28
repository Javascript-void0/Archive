import os

doc_count = 0
cat_count = 0

for file in os.listdir('index'):
    ct = []
    ct.append(file[0])
    ct.sort()
    cat_count = (int(ct[-1]))
    doc_count += 1