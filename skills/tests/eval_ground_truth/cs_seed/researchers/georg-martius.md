# Georg Martius

## Metadata
- Role: professor
- Chair: autonomous-learning
- Website:
- OpenAlex author id: https://openalex.org/A5001474340
- Last updated: 2026-06-13

## Research Areas
- Keywords: robotics; reinforcement learning; representation learning; autonomous systems

## Selected Recent Papers
### Scaling Laws and Tradeoffs in Recurrent Networks of Expressive Neurons
- Year: 2026
- Authors: Aaron Spieler, Georg Martius, Anna Levina
- Source: arXiv (Cornell University)
- DOI: 
- OpenAlex: https://openalex.org/W7161204943
- URL: https://arxiv.org/abs/2605.12049
- Keywords: Computer science; Scaling; Monotonic function; Hyperparameter; Recurrent neural network
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Cortical neurons are complex, multi-timescale processors wired into recurrent circuits, shaped by long evolutionary pressure under stringent biological constraints. Mainstream machine learning, by contrast, predominantly builds models from extremely simple units, a default inherited from early neural-network theory. We treat this as a normative architectural question. How should one split a fixed parameter budget $P$ between the number of units $N$, per-unit effective complexity $k_e$, and per-unit connectivity $k_c$? What controls the optimal allocation? This calls for a model in which per-unit complexity can be tuned independently of width and connectivity. Accordingly, we introduce the ELM Network, whose recurrent layer is built from Expressive Leaky Memory (ELM) neurons, chosen to mirror functional components of cortical neurons. The architecture allows for individually adjusting $N$, $k_e$, and $k_c$ and trains stably across orders of magnitude in scale. We evaluate the model on two qualitatively different sequence benchmarks: the neuromorphic SHD-Adding task and Enwik8 character-level language modeling. Performance improves monotonically along each of the three axes individually. Under a fixed budget, a clear non-trivial optimum emerges in their tradeoff, and larger budgets favor both more and more complex neurons. A closed-form information-theoretic model captures these tradeoffs and attributes the diminishing returns at two ends to: per-neuron signal-to-noise saturation and across-neuron redundancy. A hyperparameter sweep spanning three orders of magnitude in trainable parameters traces a near-Pareto-frontier scaling law consistent with the framework. This suggests that the simple-unit default in ML is not obviously optimal once this tradeoff surface is probed, and offers a normative lens on cortex's reliance on complex spatio-temporal integrators.

### Scaling Laws and Tradeoffs in Recurrent Networks of Expressive Neurons
- Year: 2026
- Authors: Aaron Spieler, Georg Martius, Anna Levina
- Source: arXiv (Cornell University)
- DOI: https://doi.org/10.48550/arxiv.2605.12049
- OpenAlex: https://openalex.org/W7161031680
- URL: https://doi.org/10.48550/arxiv.2605.12049
- Keywords: Computer science; Scaling; Monotonic function; Hyperparameter; Recurrent neural network
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Cortical neurons are complex, multi-timescale processors wired into recurrent circuits, shaped by long evolutionary pressure under stringent biological constraints. Mainstream machine learning, by contrast, predominantly builds models from extremely simple units, a default inherited from early neural-network theory. We treat this as a normative architectural question. How should one split a fixed parameter budget $P$ between the number of units $N$, per-unit effective complexity $k_e$, and per-unit connectivity $k_c$? What controls the optimal allocation? This calls for a model in which per-unit complexity can be tuned independently of width and connectivity. Accordingly, we introduce the ELM Network, whose recurrent layer is built from Expressive Leaky Memory (ELM) neurons, chosen to mirror functional components of cortical neurons. The architecture allows for individually adjusting $N$, $k_e$, and $k_c$ and trains stably across orders of magnitude in scale. We evaluate the model on two qualitatively different sequence benchmarks: the neuromorphic SHD-Adding task and Enwik8 character-level language modeling. Performance improves monotonically along each of the three axes individually. Under a fixed budget, a clear non-trivial optimum emerges in their tradeoff, and larger budgets favor both more and more complex neurons. A closed-form information-theoretic model captures these tradeoffs and attributes the diminishing returns at two ends to: per-neuron signal-to-noise saturation and across-neuron redundancy. A hyperparameter sweep spanning three orders of magnitude in trainable parameters traces a near-Pareto-frontier scaling law consistent with the framework. This suggests that the simple-unit default in ML is not obviously optimal once this tradeoff surface is probed, and offers a normative lens on cortex's reliance on complex spatio-temporal integrators.

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

### Novel Algorithms for Smoothly Differentiable and Efficiently Vectorizable Contact Manifold Construction
- Year: 2026
- Authors: Onur Beker, A. Rene Geist, Anselm Paulus, Georg Martius
- Source: arXiv (Cornell University)
- DOI: 
- OpenAlex: https://openalex.org/W7155246010
- URL: https://arxiv.org/abs/2604.17538
- Keywords: Bottleneck; Computer science; Collision detection; Manifold (fluid mechanics); Differentiable function
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Generating intelligent robot behavior in contact-rich settings is a research problem where zeroth-order methods currently prevail. Developing methods that make use of first/second order information about rigid-body dynamics in the presence of contact holds great promise in terms of increasing the solution speed and computational efficiency. The main bottleneck in this research direction is the difficulty in obtaining gradients and Hessians that are actually useful for numerical optimization, due to pathologies in all three steps of a common simulation pipeline: i) collision detection, ii) contact dynamics, iii) time integration. This abstract proposes a method that aims to address the collision detection part of the puzzle, via a novel pipeline designed from scratch with smooth (i.e. twice) differentiability and massive vectorizability on GPUs as the main priorities. This is in contrast to standard collision detection routines that are instead optimized for runtime on CPUs and minimal memory footprint, but do employ logic and control flow that hinder differentiability and vectorization. The proposed pipeline consists of the following contributions: i) highly expressive and compute efficient SDF representations, ii) differentiable broad-phase and narrow-phase routines that use these representations to generate vertex-SDF and edge-SDF contacts, iii) a differentiable routine for convex decomposition based contact blending.

### Drifting Fields are not Conservative
- Year: 2026
- Authors: Leonard Franz, Sebastian Hoffmann, Georg Martius, Bernhard Scholkopf, Georg Martius
- Source: ArXiv.org
- DOI: 
- OpenAlex: https://openalex.org/W7153671899
- URL: https://arxiv.org/abs/2604.06333
- Keywords: Normalization (sociology); Scalar (mathematics); Gaussian; Mathematics; Algorithm
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Drifting models have recently gained attention for generating high-quality samples in a single forward pass. During training, they learn a push-forward map by following a vector-valued field, the drift field. We ask whether this procedure is equivalent to optimizing a scalar loss and find that, in general, it is not: drift fields are not conservative and cannot be written as the gradient of any scalar potential. We identify the position-dependent normalization as the source of non-conservatism, with the Gaussian kernel as the unique radial exception. Guided by this, we introduce the sharp kernel $k^\#$ and a sharp-normalized drift field that is conservative for general radial kernels. The resulting vector field is the gradient of a scalar potential that can be optimized directly using stochastic gradient descent. Moreover, the field has the form of a score difference of kernel density estimates, and gives exact equilibrium identifiability. Thus, sharp normalization closes the gap to related literature, such as Wasserstein gradient-flows and denoising score matching, also for non-Gaussian kernels. Empirically, sharp normalization preserves the performance of the original drifting objective, suggesting that the non-conservative flexibility is not required for high-quality generation.


## Caveats
- Affiliation uncertainty: Verify against official university pages before contacting.
- Missing data: Generated from OpenAlex metadata; source pages may have richer context.
