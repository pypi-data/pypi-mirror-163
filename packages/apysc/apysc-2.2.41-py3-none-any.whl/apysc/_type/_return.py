"""This module is for the `return` expression class
implementation.
"""


class Return:
    """
    Class for the return expression.

    References
    ----------
    - Return document
        - https://simon-ritchie.github.io/apysc/en/return.html
    """

    def __init__(self) -> None:
        """
        Class for the return expression.

        Notes
        -----
        This class can be instantiated only in an event handler scope.

        References
        ----------
        - Return document
            - https://simon-ritchie.github.io/apysc/en/return.html

        Examples
        --------
        >>> import apysc as ap
        >>> def on_timer(e: ap.TimerEvent, options: dict) -> None:
        ...     '''
        ...     The handler that the timer calls.
        ...
        ...     Parameters
        ...     ----------
        ...     e : ap.TimerEvent
        ...         Event instance.
        ...     options : dict
        ...         Optional arguments dictionary.
        ...     '''
        ...     with ap.If(e.this.current_count > 10):
        ...         ap.Return()
        ...     ap.trace("Not returned.")
        >>> ap.Timer(on_timer, delay=100).start()
        """
        import apysc as ap

        self._validate_current_scope_is_event_handler()
        ap.append_js_expression(expression="return;")

    def _validate_current_scope_is_event_handler(self) -> None:
        """
        Validate whether the current scope is an event handler
        scope or not.
        """
        from apysc._expression import event_handler_scope

        event_handler_scope_count: int = (
            event_handler_scope.get_current_event_handler_scope_count()
        )
        if event_handler_scope_count > 0:
            return
        raise Exception(
            "The `Return` class can be instantiated only in an event " "handler scope."
        )
