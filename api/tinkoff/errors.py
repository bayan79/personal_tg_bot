from application.errors import Error, ErrorFactory


class TinkoffError(Error):
    codes = {

    }


class TinkoffErrorFactory(ErrorFactory):
    base_error = TinkoffError
