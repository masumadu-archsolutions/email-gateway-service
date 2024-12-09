import enum

# App Environment
TESTING_ENVIRONMENT = "testing"
PRODUCTION_ENVIRONMENT = "production"
UAT_ENVIRONMENT = "uat"
DEVELOPMENT_ENVIRONMENT = "development"

KAFKA_TOPIC_PREFIX = "email"
EMAIL_REQUEST_SIZE = 50000
EMAIL_BATCH_SIZE = 1000


class RegularExpression(enum.Enum):
    phone_number = r"(((02)[034567]|(05)[0345679])\d{7}$)|((\+233)((2)[034567]|(5)[0345679])\d{7}$)"  # noqa
    placeholder = r"^(\d|\w)+$"


class SortOrderEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


class MessageTypePriority(enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
