# Papers For artificial-intelligence

Last updated: 2026-06-13

### Using predictive multiplicity to measure individual performance within the AI Act
- Year: 2026
- Authors: Karolin Frohnapfel, Mara Seyfert, Sebastian Bordt, Ulrike von Luxburg, Kristof Meding
- Source: Open MIND
- DOI: https://doi.org/10.48550/arxiv.2602.11944
- OpenAlex: https://openalex.org/W7128793395
- URL: https://doi.org/10.48550/arxiv.2602.11944
- Keywords: Computer science; Artificial intelligence; Machine learning; Arbitrariness; Predictive modelling
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: When building AI systems for decision support, one often encounters the phenomenon of predictive multiplicity: a single best model does not exist; instead, one can construct many models with similar overall accuracy that differ in their predictions for individual cases. Especially when decisions have a direct impact on humans, this can be highly unsatisfactory. For a person subject to high disagreement between models, one could as well have chosen a different model of similar overall accuracy that would have decided the person's case differently. We argue that this arbitrariness conflicts with the EU AI Act, which requires providers of high-risk AI systems to report performance not only at the dataset level but also for specific persons. The goal of this paper is to put predictive multiplicity in context with the EU AI Act's provisions on accuracy and to subsequently derive concrete suggestions on how to evaluate and report predictive multiplicity in practice. Specifically: (1) We argue that incorporating information about predictive multiplicity can serve compliance with the EU AI Act's accuracy provisions for providers. (2) Based on this legal analysis, we suggest individual conflict ratios and $$-ambiguity as tools to quantify the disagreement between models on individual cases and to help detect individuals subject to conflicting predictions. (3) Based on computational insights, we derive easy-to-implement rules on how model providers could evaluate predictive multiplicity in practice. (4) Ultimately, we suggest that information about predictive multiplicity should be made available to deployers under the AI Act, enabling them to judge whether system outputs for specific individuals are reliable enough for their use case.

### Only Brains Align with Brains: Cross-Region Alignment Patterns Expose Limits of Normative Models
- Year: 2026
- Authors: Larissa Hofling, Matthias Tangemann, Lotta Piefke, Susanne Keller, Katrin Franke, Matthias Bethge
- Source: arXiv (Cornell University)
- DOI: https://doi.org/10.48550/arxiv.2604.21780
- OpenAlex: https://openalex.org/W7155485083
- URL: https://doi.org/10.48550/arxiv.2604.21780
- Keywords: Discriminative model; Artificial intelligence; Computer science; Benchmarking; Computational model
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Neuroscientists and computer vision researchers use model-brain alignment benchmarks to compare artificial and biological vision systems. These benchmarks rank models according to alignment measures such as the similarity of representational geometry or the predictability of neural responses from model activations. However, recent works have identified a number of problems with these rankings, among them their lack of discriminative power and robustness, raising the conceptual question of what it means for a model to be brain-aligned. Here we introduce alignment patterns -- characteristic functional relationship profiles of each brain region to all others -- and propose that models should reproduce these patterns to qualify as brain-aligned. First, we apply a standard benchmarking pipeline to a broad spectrum of vision models of the BOLD Moments video fMRI dataset across visual regions of interest (ROIs). We find diverse models appear equivalent in their brain alignment, reflecting the lack of discriminative power of conventional alignment benchmarking pipelines. In contrast, alignment pattern analysis (APA) is a second-order structural consistency test: a model aligned to a given ROI should reproduce that ROI's characteristic cross-region alignment profile. Applying APA, we find that, while these patterns are highly stable across brains of different subjects, even top-ranked models often fail to capture them. Finally, we argue for a clearer distinction between the criteria a model must meet to serve as a tool versus as a computational model for human visual cortex. Conventional alignment measures may be sufficient for identifying neurally predictive models, but claims about computational or algorithmic similarity may require a stronger basis of evidence, including the reproducibility of relational alignment patterns.
