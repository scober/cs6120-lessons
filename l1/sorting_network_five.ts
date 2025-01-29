import * as mem from "../../bril/bril-ts/mem";

function compare_and_swap(array: mem.Pointer<bigint>, l: bigint, r:bigint) {
  let left = mem.load(mem.ptradd(array, l))
  let right = mem.load(mem.ptradd(array, r))
  if (right < left) {
    mem.store(mem.ptradd(array, l), right)
    mem.store(mem.ptradd(array, r), left)
  }
}

function sorting_network_five(array: mem.Pointer<bigint>) {
    let zero: bigint = 0n
    let one: bigint = 1n
    let two: bigint = 2n
    let three: bigint = 3n
    let four: bigint = 4n
    compare_and_swap(array, zero, three)
    compare_and_swap(array, one, four)
    compare_and_swap(array, zero, two)
    compare_and_swap(array, one, three)
    compare_and_swap(array, zero, one)
    compare_and_swap(array, two, four)
    compare_and_swap(array, one, two)
    compare_and_swap(array, three, four)
    compare_and_swap(array, two, three)
}
