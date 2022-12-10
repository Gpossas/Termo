with open('./br-utf8.txt', 'r', encoding="utf8") as data:
    words = data.read().split()

with open('./br-utf8.txt-5-letras.txt', 'w', encoding="utf8") as writing:
    writing.write('\n'. join(word for word in words if len(word) == 5))