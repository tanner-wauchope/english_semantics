from types import ModuleType
from . import (
    complementizer,
    determiner,
    noun,
    number,
    possessive,
    quote,
    subordinating_conjunction,
    topic,
    verb,
)

word_classes = {}
keywords = {}
for name, module in locals():
    if isinstance(module, ModuleType) and not name.startswith('_'):
        class_name = name.title()
        word_class = getattr(module, class_name)
        word_classes[class_name] = word_class
        if hasattr(module, 'keywords'):
            for keyword in module.keywords:
                keywords[keyword] = word_class
