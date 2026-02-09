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

### Then Section: Observable Outcomes
Observable outcomes that matter to business or functionality:
- Focus on business value and blocking issues
- **Include UI details IF they block subsequent actions** (e.g., "cookies banner disappears" prevents interaction with site)
- **Exclude UI details that are just implementation** (e.g., "modal styling", "submenu shows exact item list")
- Abstract results: "no connected stations" (not: "message displays exact text X")

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

## Correct Example: Abstracted, Focused BDD

```
Scenario: User login and account access
Given browser at https://holfuy.com/en
When user accepts all cookies
Then the cookies banner disappears
When user logs in as adrian.herscu@gmail.com with password 123456
Then adrian.herscu@gmail.com user is logged in
When user opens MyAccount
Then no connected stations are displayed
```

**Why this works:**
- "cookies banner disappears" is included because it's a **blocking issue** — if it doesn't disappear, the site is unusable
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
- [ ] **UI blockers are included** — if it prevents next action, include it
- [ ] **UI mechanics are excluded** — if it's just internal detail, leave it out
- [ ] **Assertions are business-focused** — not tied to exact text or styling
- [ ] **Language is concise** — removed irrelevant details
- [ ] **Multiple When-Then pairs** — each meaningful interaction cycle is separate
