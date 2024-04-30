import sys

def reverse_modify_content(content):
    original_content = b""
    offset = content[0]
    for i in range(1, len(content)):
        original_char = content[i] ^ ((offset + i-1) % 256)
        original_content += bytes([original_char])
    return offset, original_content

def read_file(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

if __name__ == '__main__':
    file_content = read_file('secret.txt')

    if file_content:
        offset, original_content = reverse_modify_content(file_content)
        try:
            print("Offset: ", hex(offset))
            print("Original Content:", original_content.decode('utf-8'))
        except UnicodeDecodeError:
            print("Unable to decode UTF-8")
            print("Original Content:", original_content)