# import os

''' Inconsistent on Heroku >:|
for file in os.listdir('index'):
    gr = file[0]
    doc_count += 1
    if gr < file[0]:
        gr = file[0]
cat_count = int(gr)
'''

cat_count = 3
doc_count = 0

for file in os.listdir('index'):
    doc_count += 1