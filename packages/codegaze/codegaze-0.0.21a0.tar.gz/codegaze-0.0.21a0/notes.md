## Questions

- For n=100 completions, how varied are the completions? Can we plot a distribution of the variace for each generated program for the same prompt?

  - Reason: if all the completions are the same, pass@k for larger k is not very informative.

- For cases where pass at 10 is zero, but pass at higher k is non-zero, why is pass at 10 zero?

  - Reason: the generated code is not very good.

- What is the correlation between block and cat metrics?
- How are OpenAI completions currently ordered? Is there some notion of relevance used to sort them? Is there meaning to the orfder?

  - Reason: if unordered, then we may be getting random information from computing metric@k especially for small k... we dont know what drives the decision inwhat is included in k. What does the Codex paper say?

## TODO

Each experiment config should have a set of models.

- for each experiment
  - for each problem, show
    - Functions
      - A list of completions for each problem with markings on if it passed or failed.
    - Blocks
      - A list of block completions for each problem with markings on if it passed or failed.
  - Ability to filter
    - E.g. show only problems for which the metric at k is non-zero.
  - Implementation
    - Experiment abstraction (given a config and a model)
      - list completions

## Library Design

Current design decisions on the library

- Models : uses open ai models for code completion
- Dataset: humaneval dataset
- Evaluation metrics:
  - functional eval implementation from Huggingface eval library
  - CAT metrics
