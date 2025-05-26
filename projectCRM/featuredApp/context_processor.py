def accessible_accounts(request):
    if request.user.is_authenticated:
        accounts = request.user.businessuser.accessible_accounts.select_related('owner', 'role')
        self_account = request.user.businessuser
    else:
        accounts = []
    return {
        'self_account': self_account,
        'accessible_accounts': accounts,
    }
