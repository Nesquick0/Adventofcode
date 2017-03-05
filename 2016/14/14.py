import hashlib

def main():
  salt = "yjdafjpo"
  #salt = "abc"
  index = 0
  possibleKeys = []
  keys = []
  
  while (len(keys) < 64):
    hash = hashlib.md5("%s%d" % (salt, index)).hexdigest()
    
    # Remove old possible keys.
    possibleKeys = filter(lambda x: x[1]+1000 >= index, possibleKeys)
    
    for key in possibleKeys[:]:
      char = key[0]
      
      for i in xrange(len(hash)-4):
        if ((char == hash[i]) and
            (char == hash[i+1]) and
            (char == hash[i+2]) and
            (char == hash[i+3]) and
            (char == hash[i+4])):
            
          keys.append( [key[0], key[1], index, hash])
          possibleKeys.remove(key)
          break
    
    for i in xrange(len(hash)-2):
      char = hash[i]
      if ((char == hash[i+1]) and (char == hash[i+2])):
        possibleKeys.append([char, index])
        break
    
    index += 1
      
  keys = sorted(keys, key=lambda x: x[1])
  for key in keys[:64]:
    print(key)
  print(len(keys))
    
  
if (__name__ == "__main__"):
  main()