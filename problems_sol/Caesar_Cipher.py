def caesar_cipher(msg, shift, mode='encode'):
    result = []
    shift = shift % 26
    if mode == 'decode':
        shift = -shift

    for char in msg:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            offset = (ord(char) - base + shift) % 26
            result.append(chr(base + offset))
        else:
            result.append(char)
    return ''.join(result)

mode = input("Enter mode: ").strip().lower()
msg = input("Enter msg: ")
shift = int(input("Enter shift len: "))

output = caesar_cipher(msg, shift, mode)
print(f"Res: {output}")
