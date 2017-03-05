import hashlib

def main():
  input = "uqwqemis"
  #input = "abc"
  index = 0
  password = ""
  
  while (len(password) < 8):
    hash = hashlib.md5("%s%d" % (input, index)).hexdigest()
    if (hash[:5] == "00000"):
      password += hash[5]
      print(hash)
      print(password)
    index += 1
    
  print(password)

if (__name__ == "__main__"):
  main()