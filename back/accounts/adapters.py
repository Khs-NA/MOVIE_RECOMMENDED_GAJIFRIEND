from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname 필드를 추가
        image = data.get("image")
        image = data.get("image")
        nickname = data.get("nickname")
        age = data.get("age")
        genre = data.get("genre")
        gender = data.get("gender")
        location = data.get("location")
        longitude_x = data.get("longitude_x")
        latitude_y = data.get("latitude_y")
        followings = data.get("followings")
        gender = data.get("gender")
        location = data.get("location")
        longitude_x = data.get("longitude_x")
        latitude_y = data.get("latitude_y")
        followings = data.get("followings")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if image:
            user_field(user, "image", image)
        if image:
            user_field(user, "image", image)
        if nickname:
            user_field(user, "nickname", nickname)
        if age:
            user_field(user, "age", age)
        if genre:
            user_field(user, "genre", genre)
        if gender:
            user_field(user, "gender", gender)
        if location:
            user_field(user, "location", location)
        if longitude_x:
            user_field(user, "longitude_x", longitude_x)
        if latitude_y:
            user_field(user, "latitude_y", latitude_y)
        if followings:
            user_field(user, "followings", followings)
        if "password1" in data:
         user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
        # Ability not to commit makes it easier to derive from
        # this adapter by adding
            user.save()
        return user






    # def save_user(self, request, user, form, commit=True):
    #     data = form.cleaned_data
    #     # 기본 저장 필드: username, email
    #     user = super().save_user(request, user, form, False)
    #     # 추가 저장 필드: nickname, profile_image, age, genre, gender
    #     nickname = data.get('nickname')
    #     profile_image = data.get('profile_image')
    #     age = data.get('age')
    #     genre = data.get('genre')
    #     gender = data.get('gender')

    #     if nickname:
    #         user.nickname = nickname
    #     if profile_image:
    #         user.profile_image = profile_image
    #     if age:
    #         user.age = age
    #     if genre:
    #         user.genre = genre
    #     if gender:
    #         user.gender = gender

    #     if commit:
    #         user.save()
    #     return user
