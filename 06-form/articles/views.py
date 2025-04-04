from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


# 메인 페이지를 응답하는 함수 (+ 전체 게시글 목록)
def index(request):
    # DB에 전체 게시글 요청 후 가져오기
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


# 특정 단일 게시글의 상세 페이지를 응답 (+ 단일 게시글 조회)
def detail(request, pk):
    # pk로 들어온 정수 값을 활용 해 DB에 id(pk)가 pk인 게시글을 조회 요청 
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


# 게시글을 작성하기 위한 페이지를 제공하는 함수
# def new(request):
#     form = ArticleForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'articles/new.html', context)


# 사용자로부터 데이터를 받아 저장하고 저장이 완료되었다는 페이지를 제공하는 함수
# def create(request):
#     # 사용자로 부터 받은 데이터를 추출
#     # title = request.POST.get('title')
#     # content = request.POST.get('content')
    
#     # 사용자로부터 받은 데이터를 통째로 인자로 넣어 form 인스턴스 생성
#     form = ArticleForm(request.POST)
    
#     # 통째로 넣었으니까... 데이터가 제대로 돼 있는지 검사해야 함. 즉, 유효성 검사를 수행해야 함.
#     if form.is_valid():
#         article = form.save()  # 통과하면 저장. 아래의 pk 를 넘겨주기 위해 변수화.
#         return redirect("articles:detail", article.pk)
    
#     context = {
#         'form': form, 
#     }

#     return render(request, "articles/new.html", context)

    # DB에 저장 요청 (3가지 방법)
    # 1.
    # article = Article()
    # article.title = title
    # article.content = content
    # article.save()

    # 2.
    # article = Article(title=title, content=content)
    # article.save()
    
    # 3.
    # Article.objects.create(title=title, content=content)
    # return render(request, 'articles/create.html')
    # return redirect('articles:index')
    # return redirect('articles:detail', article.pk)


def create(request):
    # 1. 요청 메서드가 POST 라면
    if request.method == 'POST':

        # 1.1. 받은 데이터를 인자로 통째로 넣어서 form 인스턴스 생성
        form = ArticleForm(request.POST)
        # 1.2. 유효성 검사
        if form.is_valid():
            # 1.3. 유효성 검사가 통과한다면 저장
            article = form.save()
            # 1.4. 상세 페이지로 리다이렉트.
            return redirect('articles:detail', article.pk)
    # 2. POST 가 아니라면
    else:
        # 2.1. ArticleForm 인스턴스를 생성.
        form = ArticleForm()
    # 1.5. 에러메시지를 담은 form 을 전달.
    # 2.2. 빈 form 을 전달.
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def delete(request, pk):
    # 어떤 게시글을 지우는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # DB에 삭제 요청
    article.delete()
    return redirect('articles:index')


# def edit(request, pk):
#     # 몇번 게시글 정보를 보여줄지 조회
#     article = Article.objects.get(pk=pk)
#     form = ArticleForm(instance=article)
#     context = {
#         'article': article,
#         'form': form, 
#     }
#     return render(request, 'articles/edit.html', context)


# def update(request, pk):
#     # 어떤 글을 수정하는지 먼저 조회
#     article = Article.objects.get(pk=pk)
#     # 사용자 입력 데이터를 기존 인스턴스 변수에 새로 갱신 후 저장
#     form = ArticleForm(request.POST, instance=article)

#     if form.is_valid():
#         form.save()
#         return redirect("articles:detail", article.pk)
    
#     context = {
#         'article': article, 
#         'form': form, 
#     }

#     return render(request, 'articles/edit.html', context)


def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form
    }
    return render(request, 'articles/update.html', context)