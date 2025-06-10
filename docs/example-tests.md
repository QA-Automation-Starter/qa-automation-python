## Example Tests

Below are example test cases demonstrating BDD-style usage with this framework:

```python
# Example: UI search test
# (Assumes self.login_section and self._configuration.users are defined)
def should_find(self):
    self.login_section(random.choice(self._configuration.users))
    for word in ["hello", "kitty"]:
        (self.steps
            .when.searching_for(word)
            .then.the_search_hints(
                yields_item(contains_string_ignoring_case(word))))
```

```python
# Example: API add test
def should_add(self):
    random_pet = SwaggerPetstorePet.random()
    (self.steps
        .when.adding(random_pet)
        .then.the_available_pets(yields_item(is_(random_pet))))
```

---
