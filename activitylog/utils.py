from .models import Log

def log_activity(user, transaction_type, reference_id, action):
    print(f"[DEBUG] Logging activity: user={user}, transaction_type={transaction_type}, reference_id={reference_id}, action={action}")
    try:
        Log.objects.create(
            user=user,
            transaction_type=transaction_type,
            reference_id=reference_id,
            action=action
        )
    except Exception as e:
        print(f"[ERROR] Failed to log activity: {e}")
