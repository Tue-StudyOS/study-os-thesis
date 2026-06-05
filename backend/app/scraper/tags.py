"""Canonical tag vocabulary for the paper enrichment pipeline.

These tags are seeded into the `tags` DB table on first use and are the only
values the LLM is allowed to assign to papers. Extend this list to add new
subject areas; the fuzzy matcher in LLMPaperEnricher will handle minor LLM
phrasing variations automatically.
"""

CANONICAL_TAGS: frozenset[str] = frozenset(
    {
        # Core ML / AI
        "machine learning",
        "deep learning",
        "reinforcement learning",
        "supervised learning",
        "unsupervised learning",
        "semi-supervised learning",
        "self-supervised learning",
        "transfer learning",
        "meta-learning",
        "continual learning",
        "federated learning",
        "active learning",
        # Model families
        "neural networks",
        "transformers",
        "convolutional networks",
        "graph neural networks",
        "recurrent networks",
        "generative models",
        "diffusion models",
        "large language models",
        # NLP / Language
        "natural language processing",
        "text classification",
        "machine translation",
        "question answering",
        "information retrieval",
        # Vision & Multimodal
        "computer vision",
        "object detection",
        "image segmentation",
        "video understanding",
        "multimodal learning",
        # Robotics & Control
        "robotics",
        "control theory",
        "motion planning",
        "autonomous systems",
        "human-robot interaction",
        # Math & Theory
        "optimization",
        "statistics",
        "mathematics",
        "bayesian methods",
        "causal inference",
        "information theory",
        "graph theory",
        "signal processing",
        "statistical learning theory",
        "approximation theory",
        # Systems & Engineering
        "distributed systems",
        "hardware accelerators",
        "efficient inference",
        "model compression",
        # Data
        "data augmentation",
        "synthetic data",
        "dataset",
        # Applications
        "medical imaging",
        "bioinformatics",
        "climate science",
        "scientific computing",
    }
)
