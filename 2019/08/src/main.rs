#![allow(non_snake_case)]
#![allow(unused_parens)]

fn main() {
  let input: String = std::fs::read_to_string("input.txt").expect("Bad file!");
  let digits: Vec<u32> = input.chars().map(|x| x.to_digit(10).unwrap()).collect();
  let (width, height): (i64, i64) = (25, 6);
  let layerSize = (width * height) as usize;
  let mut layers: Vec<[i64; 3]> = Vec::new();

  // First part:
  for l in 0..digits.len() / layerSize
  {
    layers.push([0, 0, 0]);
    for i in 0..layerSize
    {
      let pos: usize = i + (l * layerSize);
      layers[l][digits[pos] as usize] += 1;
    }
  }

  let mut leastZeroLayer = 0;
  let mut leastZero: i64 = std::i64::MAX;
  for (l, layer) in layers.iter().enumerate()
  {
    let zeros: i64 = layer[0];
    if (zeros < leastZero)
    {
      leastZero = zeros;
      leastZeroLayer = l;
    }
  }
  println!("Layer {}, result {}", leastZeroLayer, layers[leastZeroLayer][1] * layers[leastZeroLayer][2]);

  // Second part:
  let mut image: Vec<u32> = Vec::with_capacity(layerSize);
  for i in 0..layerSize
  {
    for l in 0..digits.len() / layerSize
    {
      let pos: usize = i + (l * layerSize);
      if (digits[pos] != 2)
      {
        image.push(digits[pos]);
        break;
      }
    }
  }
  // Draw image.
  for y in 0..height
  {
    for x in 0..width
    {
      match image[(x + (y * width)) as usize]
      {
        0 => print!(" "),
        1 => print!("#"),
        _ => print!("XXX"),
      }
    }
    println!("");
  }
} 