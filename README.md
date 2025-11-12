# 💾 RAM Tetris — Memory Allocation Visualizer

A fun and interactive **Operating System project** built with **Python + Pygame**, demonstrating **memory allocation**, **process management**, and **compaction (defragmentation)** in an engaging, visual way.

---

## 🧠 Project Overview

**RAM Tetris** simulates how an Operating System handles processes in **main memory (RAM)** using:
- **First-Fit Allocation**
- **Process Deallocation**
- **Memory Compaction**

Each process is represented as a colored block in a 10×10 RAM grid.  
The program allows you to spawn, kill, and compact memory — just like managing real RAM fragmentation.

---

## 🎮 Features

✅ **Spawn Process (+)**  
Creates a new process with a random size (4–12 blocks).  
Allocates it in the first available contiguous free space (First-Fit algorithm).

✅ **Kill Random (-)**  
Terminates a random active process, freeing its occupied memory blocks.

✅ **DEFRAGMENT RAM**  
Starts a visual animation that compacts all allocated memory blocks toward the left, merging free spaces.

✅ **Live Memory Stats**  
Displays the percentage of used memory and a real-time visualization of process distribution.

---

## 🧩 Core Concepts Demonstrated

| Concept | Description |
|----------|--------------|
| **First-Fit Allocation** | Finds the first suitable contiguous block of memory for a process |
| **Deallocation** | Frees memory occupied by a terminated process |
| **Compaction (Defragmentation)** | Moves processes to merge scattered free blocks into a single large free area |
| **Process Visualization** | Each process has a unique PID and color, displayed in a memory grid |

---

## 🖼️ Demo Preview

*(Add a screenshot or GIF of the game window here)*  
Example:
