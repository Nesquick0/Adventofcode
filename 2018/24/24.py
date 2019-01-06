import re

class Group():
  def __init__(self):
    self.infection = False
    self.units = 0
    self.hp = 0
    self.weak = []
    self.immune = []
    self.dmg = 0
    self.attack = ""
    self.initiative = 0
    self.id = 0
    self.target = None
    self.isTarget = False

class Main():
  def __init__(self):
    self.immune = []
    self.infection = []

  def damage(self, target, group):
    if (group.attack in target.immune):
      return 0
    if (group.attack in target.weak):
      return group.units*group.dmg*2
    return group.units*group.dmg

  def printGroups(self):
    print("Immune:")
    for group in self.immune:
      print(group.id, group.units)
    print("Infection:")
    for group in self.infection:
      print(group.id, group.units)

  def run(self):
    with open("input.txt", "r") as file:
      input = file.readlines()

    pattern = re.compile(r"(\d+) units each with (\d+) hit points (\(.+\))? ?with an attack that does (\d+) (\w+) damage at initiative (\d+)")

    i = 1
    infection = False
    id = 1
    while (i<len(input)):
      line = input[i].strip()
      if ("Infection:" in line):
        infection = True
        id = 1
      if (not line):
        i += 1
        continue

      m = pattern.match(line)
      if (m):
        group = Group()
        group.infection = infection
        group.units = int(m.group(1))
        group.hp = int(m.group(2))
        group.dmg = int(m.group(4))
        group.attack = m.group(5)
        group.initiative = int(m.group(6))
        group.id = id

        info = m.group(3)
        if (info):
          info = info[1:-1].split("; ")
          for stat in info:
            if ("weak to " in stat):
              stat = stat.replace("weak to ", "")
              stat = stat.split(", ")
              for weak in stat:
                group.weak.append(weak)
            elif ("immune to " in stat):
              stat = stat.replace("immune to ", "")
              stat = stat.split(", ")
              for immune in stat:
                group.immune.append(immune)

        if (infection):
          self.infection.append(group)
        else:
          self.immune.append(group)
        id += 1

      i += 1

    # Fight
    while (len(self.infection) > 0 and len(self.immune) > 0):
      # Target
      groups = self.infection + self.immune
      groups.sort(key=lambda x: x.initiative, reverse=True)
      groups.sort(key=lambda x: x.units*x.dmg, reverse=True)
      for group in groups:
        targets = self.immune if group.infection else self.infection

        targets.sort(key=lambda x: x.initiative, reverse=True)
        targets.sort(key=lambda x: x.units*x.dmg, reverse=True)
        targets.sort(key=lambda x: self.damage(x, group), reverse=True)

        for target in targets:
          if (target.isTarget):
            continue
          if (self.damage(target, group) == 0):
            continue
          target.isTarget = True
          group.target = target
          break

      # Attack
      groups = self.infection + self.immune
      groups.sort(key=lambda x: x.initiative, reverse=True)

      for group in groups:
        if (group.units <= 0):
          continue
        if (not group.target):
          continue

        unitsKilled = self.damage(group.target, group) // group.target.hp
        group.target.units = max(group.target.units - unitsKilled, 0)
        if (group.target.units <= 0):
          if (group.target.infection):
            if (group.target in self.infection):
              self.infection.remove(group.target)
          else:
            if (group.target in self.immune):
              self.immune.remove(group.target)

      for group in groups:
        group.isTarget = False
        group.target = None

      #self.printGroups()

    # Result
    print("Immune:")
    for group in self.immune:
      print(group.id, group.units)
    print("Infection:")
    for group in self.infection:
      print(group.id, group.units)
    if (self.immune):
      units = sum(x.units for x in self.immune)
      print("Immune wins: %d" % (units))
    if (self.infection):
      units = sum(x.units for x in self.infection)
      print("Infection wins: %d" % (units))
    
  

if (__name__ == "__main__"):
  Main().run()