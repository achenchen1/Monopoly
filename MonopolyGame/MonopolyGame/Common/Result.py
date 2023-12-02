class Result:
    default_message = ""

    def __str__(self) -> str:
        return self.__class__.default_message

    def __repr__(self) -> str:
        return self.__class__.default_message


class Error(Result):
    def __bool__(self) -> bool:
        return False


class Ok(Result):
    def __bool__(self) -> bool:
        return True
