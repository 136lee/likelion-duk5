from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Category  # 카테고리 사용

# 지도 + 포스팅 폼 페이지
def list(request):
    categories = Category.objects.all()
    return render(request, 'map/list.html', {'categories': categories})