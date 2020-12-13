class Passport:
  byr = None
  iyr = None
  eyr = None
  hgt = None
  hcl = None
  ecl = None
  pid = None
  cid = None

  def valid(self):
    if (self.byr and self.iyr and self.eyr and self.hgt and self.hcl and self.ecl and self.pid):
      return True
    return False

  def valid2(self):
    if (not self.valid()):
      return False
    if (not (self.byr >= 1920 and self.byr <= 2002)):
      return False
    if (not (self.iyr >= 2010 and self.iyr <= 2020)):
      return False
    if (not (self.eyr >= 2020 and self.eyr <= 2030)):
      return False
    if (self.hgt[-2:] == "cm"):
      hgt = int(self.hgt[:-2])
      if (not (hgt >= 150 and hgt <= 193)):
        return False
    elif (self.hgt[-2:] == "in"):
      hgt = int(self.hgt[:-2])
      if (not (hgt >= 59 and hgt <= 76)):
        return False
    else:
      return False
    if (self.hcl[0] == "#"):
      if (len(self.hcl) != 7):
        return False
      for char in self.hcl[1:]:
        if (not ((char >= "0" and char <= "9") or (char >= "a" and char <= "f"))):
          return False
    else:
      return False
    if (not (self.ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])):
      return False
    if (len(self.pid) != 9):
      return False
    for char in self.pid:
      if (not (char >= "0" and char <= "9")):
        return False
    return True

  def setValue(self, key, value):
    if (key == "byr"):
      self.byr = int(value)
    if (key == "iyr"):
      self.iyr = int(value)
    if (key == "eyr"):
      self.eyr = int(value)
    if (key == "hgt"):
      self.hgt = value
    if (key == "hcl"):
      self.hcl = value
    if (key == "ecl"):
      self.ecl = value
    if (key == "pid"):
      self.pid = value
    if (key == "cid"):
      self.cid = value

def runFirst(passports):
  valids = 0
  for passport in passports:
    if (passport.valid()):
      valids += 1
  return valids

def runSecond(passports):
  valids = 0
  for passport in passports:
    if (passport.valid2()):
      valids += 1
  return valids


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  passports = [Passport()]
  for line in input:
    line = line.strip()
    if (not line):
      passports.append(Passport())
      continue
    for info in line.split(" "):
      k, v = info.split(":")
      passports[-1].setValue(k, v)
  
  result = runFirst(passports)
  print(result)
      
  result = runSecond(passports)
  print(result)

if (__name__ == "__main__"):
  main()