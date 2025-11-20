# Testing Concepts

## Concepts
- Testing Pyramid
- Test Driven Development
- Red-Green-Refactor cycle
- Arrange-Act-Assert pattern
- Need for mocking external dependencies

## Learn
1. Testing Pyramid:
    - Hirearchy for types of testing
    - unit -> integration -> End-2-End tests
    - the amount of tests also increases in the same order

2. Test Driven Development(TDD):
    - Process of writing tests before actual code

3. Red-Green-Refactor Cycle:
    - Process of implementing TDD.
        1. Red: failing test first
        2. Green: then implement a simple solution 
        3. Refactor: optimize if needed

4.  Arrang-Act-Assert pattern: A common structure for writing clean and readable tests
    - Arrange: Arrage your data
    - Act: by runnig it
    - Assert: the expected result

5. Need for mocking external dependancies:
    - Mocking helps isolate the unit of code being tested by replacing external systems (APIs, DB, network, file I/O) with fake controlled versions.
    - Makes tests independent of actual code.


## Best practices
- use a conftest.py file to place all the fixtures in one place ([pytest.fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html))


### Resources
- [testing pyramid blog](https://www.headspin.io/blog/the-testing-pyramid-simplified-for-one-and-all)
- [AAA blog](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
