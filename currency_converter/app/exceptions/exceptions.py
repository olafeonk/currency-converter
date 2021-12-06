class RequestError(Exception):
    pass


class ParamNotFound(RequestError):
    def __init__(self, param):
        self.param = param
        super().__init__(f"Param {param} was not found in request")


class IncorrectRequestValue(RequestError):
    def __init__(self, value, message):
        self.value = value
        super().__init__(f"Value {value} should be a {message}")


class CurrencyNotFound(RequestError):
    def __init__(self, currency):
        self.currency = currency
        super().__init__(f"Currency {currency} was not found in database")


