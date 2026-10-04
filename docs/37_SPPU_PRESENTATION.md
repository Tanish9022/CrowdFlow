# 37. SPPU Presentation

## 1. Presentation Structure for Project Defense
This slide-by-slide structure aligns directly with the SPPU CS-331-FP final examination rubric:

- **Slide 1: Title & Project Identity**
  - Project Title: Crowd Flow — AI-Based Traffic and Route Management System Using CCTV
  - Students: Tanish Dhende (Roll 98), Palavi Jadhav (Roll 108)
  - Guide / Department: Department of Computer Science, SPPU
- **Slide 2: Problem Identification & Industrial Relevance**
  - Conventional CCTV surveillance is passive and reactive.
  - Road closures cause chaotic uncoordinated spillover onto unprepared secondary roads.
- **Slide 3: Project Vision: The Dynamic Jigsaw Paradigm**
  - Roads as interlocking capacity puzzle pieces.
  - Missing pieces trigger dynamic recalculation, simulation, and signal advisory.
- **Slide 4: System Architecture & Data Flow**
  - Video $\to$ YOLO $\to$ Tracker $\to$ Features $\to$ State $\to$ Graph $\to$ Dijkstra $\to$ Sim $\to$ UI.
- **Slide 5: Computer Vision Pipeline & Distinctions**
  - Detection $\neq$ Traffic.
  - Explaining feature extraction: occupancy, speed, stationary fraction, and queue persistence.
- **Slide 6: Dynamic Jigsaw Graph & Routing**
  - Mathematical cost formula: BPR capacity-delay function + blocked state penalties.
- **Slide 7: What-If Disruption Simulator**
  - Macroscopic capacity-constraint redistribution modeling.
- **Slide 8: Advisory Signal Timing Engine**
  - Webster equisaturation formula rebalancing detour bottlenecks.
- **Slide 9: Experimental Results & Performance**
  - FPS benchmarks on CPU, latency, and route recalculation speed.
- **Slide 10: Live Demonstration**
  - Step-by-step walkthrough of the 5-act disruption scenario.
- **Slide 11: Limitations & Future Scope**
  - Real-world camera calibration challenges, multi-agent reinforcement learning.
- **Slide 12: Conclusion & Acknowledgments**
