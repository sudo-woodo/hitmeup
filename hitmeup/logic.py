def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.profile
        # if profile is None:
        #     profile = Profile(user_id=user.id)
        # profile.gender = response.get('gender')
        # profile.link = response.get('link')
        # profile. = response.get('timezone')
        profile.fb_id = response.get('id')
        profile.save()
        print profile.fb_id
        # print user.id
