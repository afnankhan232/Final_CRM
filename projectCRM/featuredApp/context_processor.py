def accessible_accounts(request):
    if request.user.is_authenticated:
        accounts = request.user.businessuser.accessible_accounts.select_related('owner', 'role')
        self_account = request.user.businessuser
    else:
        accounts = []
        self_account = None
    return {
        'self_account': self_account,
        'accessible_accounts': accounts,
    }

from accounts.forms import FeedbackForm

def feedback_form_processor(request):
    return {'feedback_form': FeedbackForm()}