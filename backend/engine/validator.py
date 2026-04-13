from backend.engine.action_schemas import SUPPORTED_ACTIONS

def validate_steps(steps):
    for i, step in enumerate(steps, start=1):
        action = step.get("action")
        if action not in SUPPORTED_ACTIONS:
            raise ValueError(f"Unsupported action at step {i}: {action}")
