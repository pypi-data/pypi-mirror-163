# Build

We use official python docker image to avoid installing things on deverloper machines or build agents.

```
# In python directory as current
docker run --rm --workdir /home -v $(pwd):/home python:3 ./build.sh
```

# Deploy
```
# In python directory as current
docker run --rm --workdir /home -v $(pwd):/home python:3 ./deploy.sh
```

# Development

Using the package from the repo
```
pip3 install lime_trading_api --force-reinstall
```

**Note:** the Listener class receives callbacks via delegate functions, for three reasons:
1. So that the C API doesn't have to know about Python Objects.
2. The Listener Python class methods can't be registered as C callbacks directly, because Python allows prototype-style method overriding on a per-Object basis, and users shouldn't be responsible for re-invoking the C-API listener callback registration methods (called by \_\_init\_\_).
3. Python's ctypes automatically converts char ptrs to strings, ints to native python ints, but does not implicitly unpack struct pointers into the structs themselves (struct.contents). Better not to leave it up to the clients.

**TODO'S**
Order Properties:
- Add nyse closing offset
- Add retail price offset