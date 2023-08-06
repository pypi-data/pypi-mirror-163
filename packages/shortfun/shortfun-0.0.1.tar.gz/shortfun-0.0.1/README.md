```py
from shortfun import sf

>>> filtered = filter(sf.gt(10), [1, 20, 10, 8, 30])
>>> list(filtered)
[20, 30]
```

```py
from shortfun import _

>>> mapped = map(sf.add(10), [1, 20, 10, 8, 30])
>>> list(mapped)
[11, 30, 20, 18, 40]
```
Using the shorter-hand method:

```py
from shortfun import _

>>> filtered = filter(_ > 10, [1, 20, 10, 8, 30])
>>> list(filtered)
[20, 30]
```

```py
from shortfun import _

>>> mapped = map(_ + 10, [1, 20, 10, 8, 30])
>>> list(mapped)
[11, 30, 20, 18, 40]
```
