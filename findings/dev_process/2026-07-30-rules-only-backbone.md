# Rules-Only Backbone

- **Date:** 2026-07-30
- **Context:** Static runtime backbones for BW companies and Tübingen faculty URLs
  were LLM/search-generated snapshots. They contained concrete URIs and entity
  selections that can stale quickly and require maintainer refresh work.
- **Finding:** The runtime backbone should be discovery logic, not a maintained
  company/faculty URI catalog. Candidate discovery now happens through dedicated
  skills that use multiple live source axes, verify official pages during each
  run, and return temporary candidate tables. "Top 100" company lists are
  allowed only as a minority source axis because they are size-, brand-, and
  ranking-source-biased.
- **Implication:** Student-facing discovery becomes more dependent on live
  search/browsing and less deterministic, but better matches the maintenance-free
  product goal. If live search is unavailable, skills must stop transparently
  rather than using stale model memory.
- **Follow-up:** Use the `/commands` simulation suite as the primary before/after
  performance gate for this architecture. Compare Jan, Simon, Maja, and Tina
  against a fresh `current main` baseline using
  `scripts/compare_command_simulation_performance.py`.
