file_name = input("File name: ").lower().strip().split(".")
extension = file_name[-1]
if extension in ['gif','png']:
    print(f"image/{extension}")
elif extension in ['jpeg', 'jpg']:
    print(f"image/jpeg")
elif extension in ['pdf', 'zip']:
    print(f"application/{extension}")
elif extension == 'txt':
    print("text/plain")
else:
    print("application/octet-stream")