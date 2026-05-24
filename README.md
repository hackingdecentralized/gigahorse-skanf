# Gigahorse-SKANF

A Gigahorse-based tool for recovering explicit control flow from EVM bytecode that uses indirect `JUMP` and `JUMPI` instructions.

This repository builds on the [Gigahorse toolchain](https://github.com/nevillegrech/gigahorse-toolchain/), which lifts low-level EVM bytecode into a higher-level three-address representation and supports custom client analyses. It contains the Gigahorse-based implementation of the control-flow deobfuscation tool described in Section 3.2 of [*Insecurity Through Obscurity: Veiled Vulnerabilities in Closed-Source Contracts*](https://arxiv.org/abs/2504.13398).

## High-level idea

The tool follows a branch-table based deobfuscation strategy:

1. Find all `JUMP` and `JUMPI` instructions in the lifted Gigahorse representation.
2. Identify jump targets that are not statically known constants.
3. Track whether such jump targets depend on dynamic values such as calldata, call value, memory, or storage.
4. Collect all legal EVM jump destinations marked by `JUMPDEST`.
5. For each indirect jump site, create an explicit set of possible edges from the jump site to legal destinations.
6. Emit recovered control-flow facts that can be consumed by later Gigahorse analysis or external scripts.

## Installation

Note that this is a modified version of Gigahorse; please follow its [official documentation](https://github.com/nevillegrech/gigahorse-toolchain/) to install.
