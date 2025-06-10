# Example Tests

Below are example test cases demonstrating BDD-style usage with this framework:

## UI search test

```python
def should_find(self):
    (self.login_section(self.configuration.random_user)
        .when.clicking_search())

    for word in ["hello", "kitty"]:
        (self.steps
            .when.searching_for(word)
            .then.the_search_hints(yields_item(traced(
                contains_string_ignoring_case(word)))))
```

## API add test

```python
def should_add(self):
    random_pet = SwaggerPetstorePet.random()
    (self.steps
        .given.swagger_petstore(self.rest_session)
        .when.adding(random_pet)
        .then.the_available_pets(yields_item(traced(is_(random_pet)))))
```

---
