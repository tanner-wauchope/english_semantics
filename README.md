# protolanguage (alpha)
This is an experimental programming language for writing logic programs in natural language. Until the project is in beta, APIs may change frequently.

Example interpreter session:
```
>>> tanner is a child of glen
...
>>> the brother of tanner is a child of glen
...
>>> glen is a child of don
...
>>> don is a child of lowis
...
>>> X is a grandchild of Y
... 	X is a child of Z
... 	Z is a child of Y
...
>>> Who is a grandchild of Someone                   
...
tanner is a grandchild of don
the brother of tanner is a grandchild of don
glen is a grandchild of lowis
>>>
```
