# Hybrid ILS-SA for Book Scanning Problem

This repository presents a **hybrid optimization approach** for solving the Google Hash Code Book Scanning problem. It combines a custom initial solution generator and a set of tweak operators that use **Hill Climbing** and **Simulated Annealing**, and later transitions to an **Iterated Local Search (ILS)** implementation from a companion repository for deeper local exploration.

The final design leverages **multi-representation switching**, allowing the solution to benefit from diverse perspectives and neighborhood structures.

---

## Algorithm Overview

### Phase 1: Custom Initial Solution + Local Search

1. **Initial Solution (Custom Representation)**:
   - Libraries are ranked using a simple efficiency-based score:
     ```
     library_score = sum(book scores) / signup days
     ```
   - Libraries are greedily added based on this score, aiming to optimize early gain.

2. **Tweak Operators (Hill Climbing + Simulated Annealing)**:
   - **Shuffle Same Books**: Moves books between libraries to improve usage of high-score books.
   - **Replace Libraries**: Swaps one library for another to explore diverse scanning schedules.
   - **Reorder Libraries**: Changes the order of signed libraries to increase throughput.

3. **Search Control**:
   - **Hill Climbing**: Accepts only improving moves.
   - **Simulated Annealing**: Allows occasional worse solutions based on temperature schedule to escape local optima.

This phase balances quick gain with exploratory tweaks using lightweight operations.

---

### Phase 2: Conversion and ILS Optimization

Once the custom solution has been refined for a fixed number of iterations or time, it is:

- **Converted to the canonical representation** used by the companion ILS repository.
- **Optimized further using Iterated Local Search**, as detailed in [ils_book_scanning](https://github.com/dritonalija/ils_book_scanning).

ILS applies:
- GRASP-based reinitialization
- Multi-strategy perturbations (remove-insert, reorder, shuffle)
- Adaptive hill climbing with 7+ neighborhood operators
- Stagnation-aware search control and history-based acceptance

This layered approach strengthens solution quality by combining fast heuristics with deeper metaheuristic exploration.

---
## References

- Luke, S. (2014). *Essentials of Metaheuristics* (2nd ed.). [Book](https://cs.gmu.edu/~sean/book/metaheuristics/)
  - Algorithm 16: Iterated Local Search (ILS)
  - Algorithm 108: GRASP
- Original ILS Codebase: [ils_book_scanning](https://github.com/dritonalija/ils_book_scanning)
