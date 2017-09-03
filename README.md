# protolanguage (alpha)
This is an experimental programming language for writing logic programs in natural language. Until the project is in beta, APIs may change frequently.

Example interpreter session:
```
>>> tanner is a child of glen
>>> glen is a child of don
>>> X is Y's grandchild
...     X is a child of Z
...     Z is a child of Y
...     
>>> Who is Someone's grandchild
...     
tanner is don's grandchild
```
