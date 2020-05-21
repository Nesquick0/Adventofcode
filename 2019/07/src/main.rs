#![allow(non_snake_case)]
#![allow(unused_parens)]

extern crate permutohedron;

struct Computer
{
  index: usize,
  values: Vec<i64>,
  input: Vec<i64>,
  output: Vec<i64>,
}

impl Computer
{
  fn new(inValues: &Vec<i64>) -> Computer
  {
    return Computer {
      index: 0,
      values: inValues.clone(),
      input: Vec::new(),
      output: Vec::new(),
    };
  } 

  fn run(&mut self) -> bool
  {
    loop
    {
      let value: i64 = self.values[self.index];
      let opCode: i64 = value % 100;
      let mut paramMode: Vec<u32> = (value / 100).to_string().chars().map(|x| x.to_digit(10).unwrap()).collect();
      paramMode.reverse();
      match opCode
      {
        1 => self.index = add(&mut self.values, self.index, &paramMode),
        2 => self.index = mult(&mut self.values, self.index, &paramMode),
        3 => {
          if (self.input.len() == 0)
          {
            return false; // Wait for more input.
          }
          self.index = input(&mut self.values, self.index, self.input.remove(0));
        }
        4 => {
          let result = output(&mut self.values, self.index, &paramMode);
          self.index = result.0;
          self.output.push(result.1);
        }
        5 => self.index = jumpIfTrue(&mut self.values, self.index, &paramMode, true),
        6 => self.index = jumpIfTrue(&mut self.values, self.index, &paramMode, false),
        7 => self.index = lessThan(&mut self.values, self.index, &paramMode),
        8 => self.index = equals(&mut self.values, self.index, &paramMode),
        99 => {
          return true;
        }
        _ => panic!("Error! {}", opCode),
      };
    }
  }
}

fn add(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  
  values[target] = first + second;
  return i+4;
}

fn mult(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  
  values[target] = first * second;
  return i+4;
}

fn input(values: &mut Vec<i64>, i: usize, inValue: i64) -> usize
{
  let target: usize = values[i+1] as usize;
  values[target] = inValue;
  return i+2;
}

fn output(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> (usize, i64)
{
  if (paramMode.len() >= 1 && paramMode[0] == 1)
  {
    return (i+2, values[i+1]);  
  }
  else
  {
    let target: usize = values[i+1] as usize;
    return (i+2, values[target]);
  }
}

fn jumpIfTrue(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>, ifTrue: bool) -> usize
{
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};
  if (ifTrue)
  {
    if (first != 0)
    {
      return second as usize;
    }
  }
  else
  {
    if (first == 0)
    {
      return second as usize;
    }
  }
  return i+3;
}

fn lessThan(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};

  values[target] = if (first < second) {1} else {0};
  
  return i+4;
}

fn equals(values: &mut Vec<i64>, i: usize, paramMode: &Vec<u32>) -> usize
{
  let target: usize = values[i+3] as usize;
  let first: i64 = if (paramMode.len() >= 1 && paramMode[0] == 1) {values[i+1]} else {values[values[i+1] as usize]};
  let second: i64 = if (paramMode.len() >= 2 && paramMode[1] == 1) {values[i+2]} else {values[values[i+2] as usize]};

  values[target] = if (first == second) {1} else {0};
  
  return i+4;
}

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let valuesStr: Vec<&str> = input.split(",").collect();
  let values: Vec<i64> = valuesStr.iter().map(|x| x.trim().parse::<i64>().unwrap()).collect();

  // First part:
  let mut inputSequence: [i64; 5] = [0, 1, 2, 3, 4];
  let mut permutations: Vec<i64> = Vec::new();
  let mut maxOutput: i64 = 0;

  loop
  {
    use permutohedron::LexicalPermutation;
    permutations.clear();
    permutations.extend(inputSequence.to_vec());
    let mut lastOutput: i64 = 0;
    for phase in &permutations
    {
      let mut comp = Computer::new(&values);
      comp.input.push(*phase);
      comp.input.push(lastOutput);
      comp.run();
      lastOutput = comp.output.pop().unwrap();
    }
    maxOutput = std::cmp::max(lastOutput, maxOutput);

    // New iteration.
    if (!inputSequence.next_permutation())
    {
      break;
    }
  }
  println!("Max output {}", maxOutput);

  // Second part:
  let mut inputSequence: [i64; 5] = [5, 6, 7, 8, 9];
  //let inputSequence: [i64; 5] = [9,8,7,6,5];
  let mut permutations: Vec<i64> = Vec::new();
  let mut maxOutput: i64 = 0;

  loop
  {
    use permutohedron::LexicalPermutation;
    permutations.extend(inputSequence.to_vec());

    let mut lastOutput: Vec<i64> = vec![0];
    let mut compI: usize = 0;
    let mut comps: Vec<Computer> = Vec::new();
    for _ in 0..5
    {
      comps.push(Computer::new(&values))
    }
    //for phase in &permutations
    loop
    {
      let comp: &mut Computer = &mut comps[compI];
      if (permutations.len() > 0)
      {
        comp.input.push(permutations.remove(0));
      }
      comp.input.extend(lastOutput);
      let result: bool = comp.run();
      lastOutput = comp.output.drain(..).collect();

      if (result == true && compI == 4)
      {
        break;
      }
      // Increase active computer index.
      compI = (compI + 1) % 5;
    }
    maxOutput = std::cmp::max(lastOutput[0], maxOutput);

    // New iteration.
    if (!inputSequence.next_permutation())
    {
      break;
    }
  }
  println!("Max output {}", maxOutput);
} 