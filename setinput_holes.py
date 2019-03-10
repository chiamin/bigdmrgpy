def stripe_holes (xs,ys):
  holes = []
  for x in xs:
    for y in ys:
      holes.append ([x,y])
  return holes
