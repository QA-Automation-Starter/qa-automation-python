# /bdd.specify

Generate BDD test scenarios using Given-When-Then Gherkin structure.

When the user provides a feature description or test scenario goal, generate a complete BDD scenario following the structure below.

## Format

Output scenarios in plain text Gherkin format:

```
Scenario: [Clear scenario name]
Given [initial state]
And [additional setup]
When [abstracted action]
And [additional action]
Then [observable outcome]
And [additional assertion]
When [next action sequence]
Then [next verification]
```

## Principles & Examples

See [BDD Guide](../../qa-pytest-examples/.specify/memory/bdd-guide.md) for:
- Given/When/Then section guidelines
- UI blocker rule (include if blocking, exclude if just implementation)
- Correct vs wrong examples
- Validation checklist
