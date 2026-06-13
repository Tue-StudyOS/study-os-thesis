# Papers For causal-inference

Last updated: 2026-06-13

### Validity Threats for Foundation Model Research
- Year: 2026
- Authors: Gunnar Konig, Martin Pawelczyk, Ulrike von Luxburg, Sebastian Bordt
- Source: arXiv (Cornell University)
- DOI: https://doi.org/10.48550/arxiv.2606.05029
- OpenAlex: https://openalex.org/W7163516053
- URL: https://doi.org/10.48550/arxiv.2606.05029
- Keywords: Causal inference; External validity; Internal validity; Face validity; Construct validity
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Controlled experiments are the backbone of machine learning research, but at the scale of modern foundation models, they have become prohibitively expensive. Instead, the community increasingly relies on research strategies that approximate the ideal experiment at a fraction of the cost: proxy experiments and scaling laws, observational studies with publicly available models, and single-run designs that leverage variation within individual training runs. In this work, we argue that there is no free lunch when approximating large-scale experiments on a compute budget. Specifically, savings in compute come at the cost of validity threats -- hidden and sometimes untestable assumptions that, when violated, can invalidate research claims. To help navigate such threats, we propose an evaluation framework that casts foundation model research as a causal inference problem. Within this framework, we evaluate different research strategies through four types of validity adapted from the empirical social sciences -- statistical, internal, external, and construct validity. We find that each strategy comes with a characteristic validity profile: proxy experiments trade external and construct validity for statistical and internal validity; observational studies face confounding and effect heterogeneity; and single-run designs are strained by interference between treated units. This analysis reveals several validity threats that have received insufficient attention in the literature. Overall, our evaluation framework provides researchers with a practical toolkit for scrutinizing validity threats in foundation model research~designs.

### Causality is Key for Interpretability Claims to Generalise
- Year: 2026
- Authors: Shruti Joshi, Aaron Mueller, David Klindt, Wieland Brendel, Patrik Reizinger, Dhanya Sridhar
- Source: Open MIND
- DOI: https://doi.org/10.48550/arxiv.2602.16698
- OpenAlex: https://openalex.org/W7130538568
- URL: https://doi.org/10.48550/arxiv.2602.16698
- Keywords: Interpretability; Counterfactual thinking; Causal inference; Causality (physics); Causal model
- Thesis angle: Use this paper as evidence for a thesis conversation; refine the angle with the supervisor.
- Abstract: Interpretability research on large language models (LLMs) has yielded important insights into model behaviour, yet recurring pitfalls persist: findings that do not generalise, and causal interpretations that outrun the evidence. Our position is that causal inference specifies what constitutes a valid mapping from model activations to invariant high-level structures, the data or assumptions needed to achieve it, and the inferences it can support. Specifically, Pearl's causal hierarchy clarifies what an interpretability study can justify. Observations establish associations between model behaviour and internal components. Interventions (e.g., ablations or activation patching) support claims how these edits affect a behavioural metric (e.g., average change in token probabilities) over a set of prompts. However, counterfactual claims -- i.e., asking what the model output would have been for the same prompt under an unobserved intervention -- remain largely unverifiable without controlled supervision. We show how causal representation learning (CRL) operationalises this hierarchy, specifying which variables are recoverable from activations and under what assumptions. Together, these motivate a diagnostic framework that helps practitioners select methods and evaluations matching claims to evidence such that findings generalise.
