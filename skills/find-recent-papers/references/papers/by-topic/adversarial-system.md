# Papers For adversarial-system

Last updated: 2026-06-13

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
