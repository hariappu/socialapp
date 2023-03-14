from socialweb.models import Post,Comments
def activities(request):
    if request.user.is_authenticated:
        cnt=Post.objects.filter(user=request.user).count()
        acnt=Comments.objects.filter(user=request.user).count()
        return {"pcount":cnt,"ccount":acnt}
    else:
        return{"qcount":0}