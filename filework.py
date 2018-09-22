with open('referat.txt', 'r', encoding='utf-8') as f:
    origin_text = f.read()

length = len(origin_text)
new_text = origin_text.split()
word_count = len(new_text)
print(length, word_count)
origin_text = origin_text.replace('.', '!')

with open('referat2.txt', 'w', encoding='utf-8') as f2:
        f2.write(origin_text)
