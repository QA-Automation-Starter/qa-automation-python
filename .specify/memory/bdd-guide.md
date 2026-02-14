# BDD Scenario Definition Guide

## BDD Scenario Structure

A scenario specifies **setup, actions, and verifications** across one or more systems using Given-When-Then sections.

```
Given [initial state/precondition]
And [additional setup]
And [more setup - browser, APIs, queues, etc.]
When [action/trigger]
And [additional action]
Then [observable outcome/assertion]
And [additional assertion]
When [next action sequence]
And [more actions]
Then [next verification]
And [more assertions]
```

## Key Principles

### Given Section: Setup Only
Specifies ONLY initial state/precondition (no actions):
- Browser location, API endpoints, queues, databases
- Initial data/state only
- No user actions or system triggers

### When Section: Abstracted Intent
User/system actions abstracted to meaningful business intent:
- Abstract repeated patterns: "logs in as X@Y.com with password Z" (not: enters email, enters password, clicks button)
- Avoid implementation details (selectors, internal modal mechanics)
- Express intent, not mechanics
- **Low-level protocol mechanics handled internally**: Don't expose TCP acks, producer acknowledgments, or other transport-layer details (e.g., "When publishing a message" handles Kafka producer acks internally, just like "When posting to /api/users" handles HTTP mechanics)

### Then Section: Observable Outcomes
Observable outcomes that matter to business or functionality:
- Focus on business value and blocking issues
- **Include UI details IF they block subsequent actions** (e.g., "cookies banner disappears" prevents interaction with site)
- **Exclude UI details that are just implementation** (e.g., "modal styling", "submenu shows exact item list")
- Abstract results: "no connected stations" (not: "message displays exact text X")
- **Complex objects verified in single statement**: When verifying multiple properties of one object, use a single Then statement with all properties, not multiple Then/And statements. Example: "Then the message from test-events partition 1 matches:" with table of all properties (content, headers, key, offset) - not separate statements for each property
- **Retrieval as verification**: In integration testing, retrieval operations are often verifications, not actions. Example: "Then the message from test-events partition 1 matches..." (verification) rather than "When consuming from partition 1" (action)
- **Matching rules are implementation details**: Express WHAT to verify (expected values), not HOW to match (matching strategy). Example: "Then the messages from test-events partition 0 match:" (not "match in order", "match exactly", "match any order"). The table row order defines expected order; implementation chooses appropriate matchers (e.g., `contains_exactly_in_order`)

### UI Blocker Rule
**Include UI details that prevent continuation:**
- Cookies banner blocks interaction → include: "cookies banner disappears"
- Error message blocks submission → include: "error message displays"
- Dialog blocks page access → include: "dialog is dismissed"

**Exclude UI details that are internal implementation:**
- Modal styling/appearance → exclude
- Exact text content of messages → exclude (too brittle)
- Internal navigation options → exclude
- Exact form field layout → exclude

### Multiple When-Then Pairs
Each meaningful interaction cycle gets its own When-Then pair, allowing sequential scenarios without nesting.

### Stateful Operations Rule
**Avoid verifications that consume or modify state needed by subsequent steps:**
- Don't verify state if the verification consumes/modifies what later steps need
- Let the actual action step prove the intermediate state existed
- **Example**: "When consuming from partition 1" proves the message exists - no need for "Then message exists" before it
- **Applies to**: Message queues (Kafka, RabbitMQ), databases with row locks, file systems with exclusive locks, any system where verification modifies state

## Implementation Pattern

Gherkin scenarios are implemented using a consistent architecture across all BDD step modules. For detailed class structure, extension patterns, and code examples, see [Architecture documentation](../../docs/architecture.md).

**Key principle**: The fluent API (`.given`, `.when`, `.then`) mirrors Gherkin structure, enabling test code to read like natural language specifications.

## Correct Example: Abstracted, Focused BDD

```
Scenario: User login and account access
Given a browser
When opening https://holfuy.com/en
And accepting all cookies
Then the cookies banner disappeared
When logging in as adrian.herscu@gmail.com with password 123456
Then the logged in user is adrian.herscu@gmail.com
When opening MyAccount
Then no connected stations are displayed
```

**Why this works:**
- "cookies banner disappeared" is included because it's a **blocking issue** — if it doesn't disappear, the site is unusable
- "Login modal appears" is excluded because it's just implementation detail that doesn't block the overall flow
- Actions are abstracted to business intent: "logs in" not "enters email, enters password, clicks button"
- Assertions are business-focused: "no connected stations" not exact message text

## Wrong Example: Over-detailed, Redundant

```
Given browser at https://holfuy.com/en
And cookies are accepted
When user clicks Login button in header
And login modal appears with email and password fields
And user enters email "adrian.herscu@gmail.com" in email field
And user enters password "123456" in password field
And user clicks Login button in modal
Then user is successfully authenticated
And login modal closes
And header displays username "Adrian"
And Logout link appears in header
And MyAccount link appears in navigation with submenu items
When user clicks MyAccount link
Then user is redirected to https://holfuy.com/en/my-stations
And page title displays "My Holfuy Stations"
And MyAccount submenu shows "MyStations", "Orders", and "Settings" options
And message displays "There is no station connected to this account yet!"
```

**Problems:**
- Implementation details mixed with business outcomes
- Step-by-step instructions instead of abstracted intent
- Over-verification of UI mechanics (modal appearance, submenu options)
- Brittle assertions tied to exact text ("There is no station connected...")
- Redundant verification of UI state changes that don't block functionality

## Validation Checklist

When reviewing a BDD scenario:
- [ ] **Given section has no actions** — only setup/preconditions
- [ ] **When section uses business intent** — abstracted user goals, not step-by-step
- [ ] **Then section focuses on observable outcomes** — not internal mechanics
- [ ] **Complex objects named explicitly** — "the X topic has Y partitions" not "the topic exists with partition count Y"
- [ ] **UI blockers are included** — if it prevents next action, include it
- [ ] **UI mechanics are excluded** — if it's just internal detail, leave it out
- [ ] **Assertions are business-focused** — not tied to exact text or styling
- [ ] **Language is concise** — removed irrelevant details
- [ ] **Multiple When-Then pairs** — each meaningful interaction cycle is separate
- [ ] **Stateful operations don't interfere** — verifications don't consume state needed by later steps
