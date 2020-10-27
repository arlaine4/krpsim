def update_R(R, t, r, remove=False):
  sign = -1 if remove else 1
  for k, amount in r.items():
    if t not in R:
      R[t] = {}
    if k not in R[t]:
      R[t][k] = sign * amount
    else:
      R[t][k] += sign * amount
  return R


def available_R(R, t, r):
  for k, amount in r.items():
    if R[t][k] < amount:
      return False
  return True


def check(tg, R0, S, verbose=False):
  R = {tg: dict(R0)}
  prevT = {tg}
  idx = 0
  try:
    for t, j in S:
      if verbose:
        print(f"Evaluating: {t}:{j.name}")
      to_remove = []
      for T in prevT:
        if T < t:
          to_remove.append(T)
          for k, amount in R[T].items():
            if k not in R[t]:
              R[t][k] = 0
            R[t][k] += amount
      for T in to_remove:
        prevT.remove(T)
        del R[T]
      if not available_R(R, t, j.needs):
        return idx
      R = update_R(R, t, j.needs, remove=True)
      R = update_R(R, t + j.delay, j.results)
      prevT.add(t + j.delay)
      idx += 1
  except:
    return idx
  return -1
