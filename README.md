# MD5 Measure app

Hash calculation service for files

## Explanation of strange decisions (and problems):
Explanation of why the work with the database is moved to the backend, and not to the workers:
- In short DRY. In more detail, I didn’t figure out how to solve the problem of duplication of functionality, except for the formation of functionality in a separate library or shared directory

It is still not very clear how much the radish is needed:
- in theory, if the upper part is completed. That radish will remain only on the locks between services. And in theory it can be replaced, for example, with file locks or locks through rabbitmq



## Services:

- [backend](./backend/README.md)
- [frontend](./frontend/README.md)
- [worker](./worker/README.md)

## Roadmap:

- [ ] Write tests
- [ ] Add CI/CD

## Installation:

- Install from source:
```bash
poetry install
```
After that, u can use package builded in dist

## Build:

- Build docker-compose:
```bash
docker-compose build
```

## Launch methods:
- Primitive way:
```bash
docker-compose up -d
```

- With setting the number of workers:
```bash
docker-compose up -d --scale worker=2
```

## Development:

- Install dependencies:
```bash
make -f Makefile install-deps
```
- Run pre-commit:
```bash
make -f Makefile pre-commit
```
