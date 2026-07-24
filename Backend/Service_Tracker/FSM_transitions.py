import logging
logger = logging.getLogger(__name__)

STATE_SUBMITTED = "SUBMIT"
STATE_UNDER_REVIEW = "UNDER_REVIEW"
STATE_ACTION_REQUIRED = "ACTION_REQUIRED"
STATE_VERIFIED = "VERIFIED"
STATE_APPROVED = "APPROVED"
STATE_REJECTED = "REJECTED"

VALID_STATES = {
    STATE_SUBMITTED,
    STATE_UNDER_REVIEW,
    STATE_ACTION_REQUIRED,
    STATE_VERIFIED,
    STATE_APPROVED,
    STATE_REJECTED
}

# ---valid transactions matrix

VALID_TRANSACTIONS = {
    STATE_SUBMITTED: [STATE_UNDER_REVIEW],
    STATE_UNDER_REVIEW: [STATE_ACTION_REQUIRED, STATE_VERIFIED, STATE_REJECTED],
    STATE_ACTION_REQUIRED: [STATE_UNDER_REVIEW, STATE_REJECTED],
    STATE_VERIFIED: [STATE_APPROVED, STATE_REJECTED],
    # Terminal state cannot do transaction anywhere
    STATE_APPROVED: [],
    STATE_REJECTED: []
}


class InvalidStateTransactionError(Exception):
    pass


def valid_transaction(current_state: str, target_state: str):
    current = (current_state or "").upper().strip()
    target = (target_state or "").upper().strip()

    # Enforce basic sanity boundary

    if current not in VALID_STATES:
        raise InvalidStateTransactionError(f'Original state {current_state} not recognised in system state')

    if target not in VALID_STATES:
        raise InvalidStateTransactionError(f'Original state {target_state} is not recognised in system state')

    # check mapping matrix
    allowed_next_states = VALID_TRANSACTIONS.get(current, [])

    if target not in allowed_next_states:
        error_msg = f"Illegal Workflow Bypass: Cannot transition directly from '{current}' to '{target}'."
        logger.error(error_msg)
        raise InvalidStateTransactionError(error_msg)

    return True

def get_allowed_next_status(current_state: str):
    """
    Help utility to dynamically tell the frontend UI which action buttons 
    to render in the pipeline.
    """
    cleaned_state = (current_state or "").upper().strip()
    return VALID_TRANSACTIONS.get(cleaned_state, [])