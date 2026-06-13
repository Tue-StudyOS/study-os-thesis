# Papers For probabilistic-logic

Last updated: 2026-06-13

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
