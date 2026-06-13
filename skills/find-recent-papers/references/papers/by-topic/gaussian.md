# Papers For gaussian

Last updated: 2026-06-13

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

### Conditioning Gaussian Processes on Almost Anything
- Year: 2026
- Authors: Henry Moss, Lachlan Astfalck, Thomas Cowperthwaite, Colin Doumont, Sam Willis, Philipp Hennig, Christopher Nemeth, Andrew Zammit Mangion
- Source: arXiv (Cornell University)
- DOI: https://doi.org/10.48550/arxiv.2605.21041
- OpenAlex: https://openalex.org/W7162021825
- URL: https://doi.org/10.48550/arxiv.2605.21041
- Keywords: Probabilistic logic; Equivalence (formal languages); Gaussian; Predictive inference; Inference
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Gaussian processes (GPs) offer a principled probabilistic model over functions, but exact inference is restricted to the linear-Gaussian regime. We establish an explicit equivalence between GPs and a class of linear diffusion models, recasting predictive sampling as an ODE with closed-form Gaussian dynamics and a likelihood-dependent guidance term that admits a simple Monte Carlo approximation. In the linear-Gaussian setting, we recover standard GP conditioning exactly; beyond conjugacy, the same machinery handles any conditioning statement admitting point-wise likelihood evaluation -- including non-linear physics, and, for the first time, natural language via large language models. Whitening isolates the irreducible non-Gaussian dynamics, minimising Wasserstein-2 transport cost and eliminating numerical stiffness. The result is a general-purpose GP inference scheme requiring no bespoke derivations. Together, these results provide a general mechanism for incorporating the full richness of real-world knowledge as conditioning information, opening a new frontier for the probabilistic modelling of real-world problems.
