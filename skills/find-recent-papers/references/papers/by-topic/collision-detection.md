# Papers For collision-detection

Last updated: 2026-06-13

### Novel Algorithms for Smoothly Differentiable and Efficiently Vectorizable Contact Manifold Construction
- Year: 2026
- Authors: Onur Beker, A. Rene Geist, Anselm Paulus, Georg Martius
- Source: arXiv (Cornell University)
- DOI: https://doi.org/10.48550/arxiv.2604.17538
- OpenAlex: https://openalex.org/W7155064697
- URL: https://doi.org/10.48550/arxiv.2604.17538
- Keywords: Bottleneck; Computer science; Collision detection; Manifold (fluid mechanics); Differentiable function
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Generating intelligent robot behavior in contact-rich settings is a research problem where zeroth-order methods currently prevail. Developing methods that make use of first/second order information about rigid-body dynamics in the presence of contact holds great promise in terms of increasing the solution speed and computational efficiency. The main bottleneck in this research direction is the difficulty in obtaining gradients and Hessians that are actually useful for numerical optimization, due to pathologies in all three steps of a common simulation pipeline: i) collision detection, ii) contact dynamics, iii) time integration. This abstract proposes a method that aims to address the collision detection part of the puzzle, via a novel pipeline designed from scratch with smooth (i.e. twice) differentiability and massive vectorizability on GPUs as the main priorities. This is in contrast to standard collision detection routines that are instead optimized for runtime on CPUs and minimal memory footprint, but do employ logic and control flow that hinder differentiability and vectorization. The proposed pipeline consists of the following contributions: i) highly expressive and compute efficient SDF representations, ii) differentiable broad-phase and narrow-phase routines that use these representations to generate vertex-SDF and edge-SDF contacts, iii) a differentiable routine for convex decomposition based contact blending.
