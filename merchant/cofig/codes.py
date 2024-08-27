class ApplyStatus(Enum):
    APPLYING = 1
    NORMAL = 2
    LOCK = 3


class SupperNode(Enum):
    YES = 1
    NO = 2


class WithdrawalStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    REJECTED = 3
