import re

class Food():
  def __init__(self, ingredients, alergens):
    self.ingredients = ingredients
    self.alergens = alergens


def runFirst(foods):
  alergensOpt = {}
  alergens = {}
  allFood = set()
  allAlergens = set()
  for food in foods:
    allFood.update(food.ingredients)
    allAlergens.update(food.alergens)
  for alerg in allAlergens:
    alergensOpt[alerg] = list(allFood)
  for food in foods:
    for alerg in food.alergens:
      origIngredients = alergensOpt[alerg]
      alergensOpt[alerg] = list(filter(lambda x: x in food.ingredients, origIngredients))

  while (len(alergensOpt) > 0):
    found = None
    for alerg in alergensOpt:
      if (len(alergensOpt[alerg]) == 0):
        print("Error1 {}".format(alerg))
      if (len(alergensOpt[alerg]) == 1):
        found = alerg
        break

    if (found):
      foundIngred = alergensOpt[found][0]
      alergens[found] = foundIngred
      del alergensOpt[found]
      for alerg, value in alergensOpt.items():
        if (foundIngred in value):
          value.remove(foundIngred)
    else:
      print("Error2")

  allSafe = [x for x in allFood if (x not in alergens.values())]
  count = 0
  for food in foods:
    for ingred in food.ingredients:
      if (ingred in allSafe):
        count += 1
  return count, alergens


def runSecond(alergens):
  alergAlphabetical = sorted(alergens.keys())
  canonicalIngred = []
  for alerg in alergAlphabetical:
    canonicalIngred.append(alergens[alerg])
  return ",".join(canonicalIngred)


def main():
  with open("input.txt", "r") as file:
    input = file.readlines()

  foods = []
  for line in input:
    line = line.strip()
    m = re.match(r"(.+) \(contains (.+)\)", line)
    if (m):
      ingredients = m.group(1).split(" ")
      alergens = m.group(2).split(", ")
      foods.append(Food(ingredients, alergens))
    else:
      print(line)

  result, alergens = runFirst(foods)
  print(result)
  
  result = runSecond(alergens)
  print(result)


if (__name__ == "__main__"):
  main()