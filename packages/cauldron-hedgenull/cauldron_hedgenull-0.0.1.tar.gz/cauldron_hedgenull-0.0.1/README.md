# Cauldron: Simple singletons

Cauldron is a small, simple package that provides singleton functionality. Here's an example of how Cauldron can be used:

```py
>>> class MySingleton(other_base_classes, SingletonMixin):
...    def __init__(self, *args, **kwargs):
...        # do stuff here
...        pass
...
>>> singleton = MySingleton()
>>> other_singleton = MySingleton()
>>> id(singleton) == id(other_singleton)
True
```
