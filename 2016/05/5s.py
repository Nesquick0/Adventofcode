import hashlib

def main():
  input = "uqwqemis"
  #input = "abc"
  index = 0
  password = ["_"] * 8
  foundChars = 0
  
  while (foundChars < 8):
    hash = hashlib.md5("%s%d" % (input, index)).hexdigest()
    if (hash[:5] == "00000"):
      if ((hash[5] >= "0") and (hash[5] <= "9")):
        position = int(hash[5])
        if ((position < len(password)) and (password[position] == "_")):
          password[position] = hash[6]
          foundChars += 1
      print(index),
      print(hash)
      print("".join(password))
    index += 1
    
  print("".join(password))

if (__name__ == "__main__"):
  main()