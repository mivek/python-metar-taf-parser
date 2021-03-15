class TranslationError(Exception):
    """Exception raised when a translation is not available
    Attributes:
        translation -- the missing string in the translation file
        message -- explanation of the error
    """
    def __init__(self, translation: str, message: str):
        self.message = message
        self.translation = translation
