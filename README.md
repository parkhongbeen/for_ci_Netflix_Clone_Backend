[![codecov](https://codecov.io/gh/parkhongbeen/for_ci_Netflix_Clone_Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/parkhongbeen/for_ci_Netflix_Clone_Backend)


codecov를 붙이기 위한 repository


### pytest-cov
```
# poetry add codecov pytest-cov

# pytest, pytest-django, coverage를 사용해서 codecov에 올릴 리포트 생성
$ pytest --cov app

# codecov에 생성된 리포트를 전송
$ CODECOV_TOEKN=<codecov.io Token> codecov
```
