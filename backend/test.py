import bcrypt

h = bcrypt.hashpw("Heroday@1256".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
print(h)