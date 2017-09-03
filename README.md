# protolanguage (beta)
This is an interpreter for logic programs written in natural language.

To invoke the interpreter, run `python protolanguage.py`

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
