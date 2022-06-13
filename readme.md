**strava api cli**

![tests](https://github.com/atefkbenothman/strava/actions/workflows/tests.yml/badge.svg)

---

```
roadmap:
  0.2.0:
  [ ] convert models to pydantic models
  [ ] create clean readme
  [ ] add segments api
  [ ] integrate openmapbox

  0.3.0:
  [ ] finish adding all api endpoints from strava
  [ ] add tests to new endpoints
  [ ] refactor all files
  [ ] get printer to a basic working point (does not need to be overkill)
  [x] convert models to pydantic models

  0.5.0
  [ ] webapp
    [ ] backend - fastapi?
    [ ] frontend - react, tailwind (css)

notes:
[x] use `python3 -i <file_name>` to test your program interactively

todo:
[ ] modify gh actions so tests only run when submitting PR to the develop branch
[ ] write tests
[ ] refactor printer class. should not take a list of activities...
[ ] refactor Printer class. init should not take activities, print function should take activities
[x] create a plan for branch strategy
[x] add linter to project, add linter check to tox
[x] split classes in api.py into their own files
```
