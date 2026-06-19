# Papers For computer-science

Last updated: 2026-06-13

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

### Robustness in Both Domains: CLIP Needs a Robust Text Encoder
- Year: 2025
- Authors: Elias Abad Rocamora, Christian Schlarmann, Naman Deep Singh, Yongtao Wu, Matthias Hein, Volkan Cevher
- Source: Infoscience (Ecole Polytechnique Federale de Lausanne)
- DOI: 
- OpenAlex: https://openalex.org/W7119299730
- URL: https://infoscience.epfl.ch/handle/20.500.14299/257602
- Keywords: Computer science; Robustness (evolution); Adversarial system; Embedding; Encoder
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Adversarial input attacks can cause a significant shift of CLIP embeddings. This can affect the downstream robustness of models incorporating CLIP in the pipeline, such as text-to-image generative models or large vision language models. While some efforts have been done towards making the CLIP image encoders robust, the robustness of text encoders remains unexplored. In this work, we cover this gap in the literature. We propose LEAF: an efficient adversarial finetuning method for the text domain, with the ability to scale to large CLIP models. Our models significantly improve the zero-shot adversarial accuracy in the text domain, while maintaining the vision performance provided by robust image encoders. When combined with text-to-image diffusion models, we can improve the generation quality under adversarial noise. In multimodal retrieval tasks, LEAF improves the recall under adversarial noise over standard CLIP models. Finally, we show that robust text encoders facilitate better reconstruction of input text from its embedding via direct optimization. We open-source our code and models.

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

### Personalizing Text-to-Image Generation to Individual Taste
- Year: 2026
- Authors: Anne-Sofie Maerten, Juliane Verwiebe, Shyamgopal Karthik, Ameya Prabhu, Johan Wagemans, Matthias Bethge
- Source: arXiv (Cornell University)
- DOI: 
- OpenAlex: https://openalex.org/W7153670010
- URL: http://arxiv.org/abs/2604.07427
- Keywords: Personalization; Computer science; Quality (philosophy); Artificial intelligence; Taste
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Modern text-to-image (T2I) models generate high-fidelity visuals but remain indifferent to individual user preferences. While existing reward models optimize for "average" human appeal, they fail to capture the inherent subjectivity of aesthetic judgment. In this work, we introduce a novel dataset and predictive framework, called PAMELA, designed to model personalized image evaluations. Our dataset comprises 70,000 ratings across 5,000 diverse images generated by state-of-the-art models (Flux 2 and Nano Banana). Each image is evaluated by 15 unique users, providing a rich distribution of subjective preferences across domains such as art, design, fashion, and cinematic photography. Leveraging this data, we propose a personalized reward model trained jointly on our high-quality annotations and existing aesthetic assessment subsets. We demonstrate that our model predicts individual liking with higher accuracy than the majority of current state-of-the-art methods predict population-level preferences. Using our personalized predictor, we demonstrate how simple prompt optimization methods can be used to steer generations towards individual user preferences. Our results highlight the importance of data quality and personalization to handle the subjectivity of user preferences. We release our dataset and model to facilitate standardized research in personalized T2I alignment and subjective visual quality assessment.
