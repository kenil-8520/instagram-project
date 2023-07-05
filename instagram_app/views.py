from django.shortcuts import render, redirect
import instaloader

def login_view(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')

        try:
            loader = instaloader.Instaloader()
            loader.login(user, password)

            request.session['user'] = user
            request.session['password'] = password

            return redirect('search_target')
        except instaloader.exceptions.BadCredentialsException:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def search_target_view(request):
    if 'user' in request.session and 'password' in request.session:
        if request.method == 'POST':
            target_username = request.POST.get('target_username')

            user = request.session['user']
            password = request.session['password']

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
            return render(request, 'search_target.html')
    else:
        return redirect('login')
