export function internalAlgorithm(stage2Result: any) {
  if (!stage2Result || !stage2Result.value) return { score: 0 };
  return { score: stage2Result.value * 2 };
}