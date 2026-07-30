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

# Unified single source of truth for your FSM transition engine
VALID_TRANSITIONS = {
    STATE_SUBMITTED: [STATE_UNDER_REVIEW],
    STATE_UNDER_REVIEW: [STATE_ACTION_REQUIRED, STATE_VERIFIED, STATE_REJECTED],
    STATE_ACTION_REQUIRED: [STATE_UNDER_REVIEW, STATE_REJECTED],
    STATE_VERIFIED: [STATE_APPROVED, STATE_REJECTED],
    # Terminal states cannot transition anywhere
    STATE_APPROVED: [],
    STATE_REJECTED: []
}


class InvalidStateTransitionError(Exception):
    """Raised when an application attempts an illegal state lifecycle shift."""
    pass


def get_allowed_next_states(current_state):

   
    return VALID_TRANSITIONS.get(current_state, [])


def validate_transition(current_state, target_state, user_role=None):
    """
    Ensures roles have permission to shift workflow lifecycles.
    """
    # Safeguard against unexpected state formats or case mismatches
    if current_state not in VALID_TRANSITIONS:
        raise InvalidStateTransitionError(f"Current state '{current_state}' is unrecognized by the workflow engine.")

    allowed_states = get_allowed_next_states(current_state)
    
    if target_state not in allowed_states:
        raise InvalidStateTransitionError(
            f"Illegal lifecycle transition from {current_state} to {target_state}."
        )
        
    return True