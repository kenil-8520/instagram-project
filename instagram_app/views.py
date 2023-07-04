from django.shortcuts import render
import instaloader

def followers_not_following_view(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        target_username = request.POST.get('target_username')

        loader = instaloader.Instaloader()
        loader.login(user, password)
        profile = instaloader.Profile.from_username(loader.context, target_username)
        followers = [follower.username for follower in profile.get_followers()]
        following = [followee.username for followee in profile.get_followees()]
        followers_not_following = list(set(following) - set(followers))

        context = {
            'total_users': len(followers_not_following),
            'followers_not_following': followers_not_following,
        }
        return render(request, 'followers_not_following.html', context)
    else:
        return render(request, 'followers_not_following.html')
