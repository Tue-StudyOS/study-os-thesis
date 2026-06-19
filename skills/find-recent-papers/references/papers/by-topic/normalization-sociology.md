# Papers For normalization-sociology

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
