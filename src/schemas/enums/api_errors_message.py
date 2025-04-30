from enum import Enum

class ErrorMessage(str, Enum):
    INTERNAL_ERROR = "An unexpected error occurred. Please try again later."
    INVALID_INPUT = "The provided input is invalid."
    MODEL_PROCESSING_ERROR = "There was an error while processing your request."
    SESSION_EXPIRED = "The session has expired or is invalid."
    RESOURCE_NOT_FOUND = "The requested resource could not be found."
    UNAUTHORIZED_ACCESS = "You are not authorized to perform this action."
