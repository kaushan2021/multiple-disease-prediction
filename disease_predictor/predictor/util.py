from predictor.models import User

def is_user_name_unique(username):
    all_users = User.objects.all()
    all_usernames = [user.username for user in all_users]
    return username not in all_usernames
    


