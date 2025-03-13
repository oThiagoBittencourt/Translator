import keyboard
from translator import translate

while True:
    print("Pressione 'Enter' para continuar...")
    key = keyboard.read_key()
    if key == 'enter':
        result = translate()
        print(result)
        continue
    if key == 'q':
        break