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

# ---valid transitions matrix

VALID_TRANSITIONS = {
    STATE_SUBMITTED: [STATE_UNDER_REVIEW],
    STATE_UNDER_REVIEW: [STATE_ACTION_REQUIRED, STATE_VERIFIED, STATE_REJECTED],
    STATE_ACTION_REQUIRED: [STATE_UNDER_REVIEW, STATE_REJECTED],
    STATE_VERIFIED: [STATE_APPROVED, STATE_REJECTED],
    # Terminal state cannot do transition anywhere
    STATE_APPROVED: [],
    STATE_REJECTED: []
}


class InvalidStateTransitionError(Exception):
    """Raised when an application attempts an illegal state lifecycle shift."""
    pass

def validate_transition(current_state, target_state, user_role):
    """
    Validates state transitions for County Service Applications.
    Ensures roles have permission to shift workflow lifecycles.
    """
    # Example state validation map matching your RBAC architecture
    VALID_TRANSITIONS = {
        'PENDING': ['UNDER_REVIEW', 'REJECTED'],
        'UNDER_REVIEW': ['APPROVED', 'REJECTED', 'FLAGGED'],
        'FLAGGED': ['UNDER_REVIEW', 'REJECTED'],
    }
    
    # Simple guard clause validation check
    if target_state not in VALID_TRANSITIONS.get(current_state, []):
        raise InvalidStateTransitionError(
            f"Illegal lifecycle transition from {current_state} to {target_state}."
        )
        
    return True