### Env Create 
```bash
pip install pipenv
pipenv install

```


We only need pytest for dev env. And we don't need for prod.
```bash
pipenv install --dev pytest

```


Generate pipenv to requirements.txt
```bash
pipenv run pip freeze > requirements.txt
```