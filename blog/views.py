from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm
from django.urls import reverse_lazy, reverse

# Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     # 나머지 요청
#     # 에러, 예외처리
#     return HttpResponse('No!!!')

### Post
class Index(View):
    def get(self, request):
        # return HttpResponse('Index page GET class')

        # 데이터베이스에 접근해서 값을 가져와야 합니다.
        # 게시판에 글들을 보여줘야하기 때문에 데이터베이스에서 '값 조회'
        # MyModel.object.all()
        post_objs = Post.objects.all()
        # context = 데이터베이스에서 가져온 값
        context = {
            'posts': post_objs,
            'title': 'Blog'
        }
        # print(post_objs) Queryset <[post 1, 2, 3]>
        return render(request, 'blog/post_list.html', context)
    
'''
class Index(LoginRequiredMixin, View):
    def get(self, request):
    # Post - User 연결 (ForeignKey)
    # User를 이용해서 Post를 가지고 온다.
    posts = Post.objects.filter(writer=request.user)
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
'''

# write
# post - form
# 글 작성 화면
# def write(request):
#     if request.method == 'POST':
#         # form 확인
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save()
#             return redirect('blog:list')
#     form = PostForm()
#     return render(request, 'blog/post_form.html', {'form': form})

# Django 자체의 클래스 뷰 기능도 강력, 편리
# model, template_name, context_object_name,
# paginate_by, form_class, form_valid(), get_queryset()
# django.views.generic -> ListView
# class List(ListView):
#     model = Post # 모델
#     template_name = 'blog/post_list.html' # 템플릿
#     context_object_name = 'posts' # 변수값의 이름


# class Write(CreateView):
#     model = Post # 모델
#     form_class = PostForm # 폼
#     success_url = reverse_lazy('blog:list') # 성공시 보내줄 url
    # post_form.html

class Write(LoginRequiredMixin, View):
    # Mixin: LoginRequiredMixin -> 로그인되지 않은 사용자가 /login
    # login_url = '/user/login'
    # redirect_field_name = 'next'

    def get(self, request):
        # next_path = request.GET.get('next')
        form = PostForm()
        context = {
            'form': form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request): # request -> HttpRequest 객체
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # 변수 할당만 우선 하고 이후에 수정가능
            post.writer = request.user
            post.save()
            return redirect('blog:list') # response -> HttpResponse 객체
        form.add_error(None, '폼이 유효하지 않습니다.')
        context = {
            'form': form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_form.html', context)


# class Detail(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'


# class Update(UpdateView):
#     model = Post
#     template_name = 'blog/post_edit.html'
#     fields = ['title', 'content']
#     # success_url = reverse_lazy('blog:list')

#     # initial 기능 -> form에 값을 미리 넣어주기 위해서
#     def get_initial(self):
#         initial = super().get_initial() # UpdateView(generic view)에서 제공하는 initial(딕셔너리)
#         post = self.get_object() # pk 기반으로 객체를 가져옴
#         initial['title'] = post.title
#         initial['content'] = post.content
#         return initial
    
#     def get_success_url(self): # get_absolute_url
#         post = self.get_object() # pk 기반으로 현재 객체 가져오기
#         return reverse('blog:detail', kwargs={'pk': post.pk})
    

class Update(View):
    def get(self, request, pk): # post_id
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title':post.title, 'content':post.content})
        context = {
            'form': form,
            'post': post,
            'title': 'Blog'
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk)
        
        form.add_error('폼이 유효하지 않습니다.')
        context = {
            'form': form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_edit.html', context)

# class Delete(DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:list')


class Delete(View):
    def post(self, request, pk): # post_id
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('blog:list')
    
    # 클래스 자체에 아예 접근하지 못하게 -> LoginRequiredMixin
    # Login이 되었을 때만 삭제 버튼이 보이게


class DetailView(View):
    def get(self, request, pk): # post_id: 데이터베이스 post_id 테이블 이름을 사용하고 싶어서
        # list -> object 상세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다갔다하지만, 하나의 인자

        # 데이터베이스 방문
        # 해당 글
        # 장고 ORM (pk: 무조건 pk로 작성해야한다.)
        post = Post.objects.get(pk=pk)
        # 댓글
        comments = Comment.objects.filter(post=post)
        # 해시태그
        hashtags = HashTag.objects.filter(post=post)

        # 댓글 Form
        comment_form = CommentForm()

        # 태그 Form
        hashtag_form = HashTagForm()

        context = {
            'title': 'Blog',
            'post': post,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': comment_form,
            'hashtag_form': hashtag_form
        }
        return render(request, 'blog/post_detail.html', context)


### Comment
class CommentWrite(View):
    # def get(self, request):
    #     pass
    def post(self, request, pk):
        form = CommentForm(request.POST)
        # 해당 아이디에 해당하는 글 불러옴
        post = Post.objects.get(pk=pk)

        if form.is_valid():
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']
            # 유저 정보 가져오기
            writer = request.user
            # 댓글 객체 생성, create 메서드를 사용할 때는 save 필요 없음
            comment = Comment.objects.create(post=post, content=content, writer=writer)
            # comment = Comment(post=post) -> comment.save()
            return redirect('blog:detail', pk=pk)
        
        # form.add_error(None, '폼이 유효하지 않습니다.')
        hashtag_form = HashTagForm()
        context = {
            'title': 'Blog',
            'post': post,
            'comments': post.comment_set.all(),
            'hashtags': post.hashtag_set.all(),
            'comment_form': form,
            'hashtag_form': hashtag_form
        }
        return render(request, 'blog/post_detail.html', context)
        

class CommentDelete(View):
    def post(self, request, pk):
        # 지울 객체를 찾아야 한다. -> 댓글 객체
        comment = Comment.objects.get(pk=pk)
        # 상세페이지로 돌아가기
        post_id = comment.post.id
        # 삭제
        comment.delete()

        return redirect('blog:detail', pk=post_id)
    

### Hashtag
class HashTagWrite(View):
    def post(self, request, pk): # post_id
        form = HashTagForm(request.POST)
        # 해당 아이디에 해당하는 글 불러옴
        post = Post.objects.get(pk=pk)

        if form.is_valid():
            # 사용자에게 태그 내용을 받아옴
            name = form.cleaned_data['name']
            # 작성자 정보 가져오기
            writer = request.user
            # 태그 객체 생성
            hashtag = HashTag.objects.create(post=post, name=name, writer=writer)
            # comment = Comment(post=post) -> comment.save()
            return redirect('blog:detail', pk=pk)
        
        # form.add_error(None, '폼이 유효하지 않습니다.')
        comment_form = CommentForm()
        context = {
            'title': 'Blog',
            'post': post,
            'comments': post.comment_set.all(),
            'hashtags': post.hashtag_set.all(),
            'comment_form': comment_form,
            'hashtag_form': form
        }
        return render(request, 'blog/post_detail.html', context)
        

class HashTagDelete(View):
    def post(self, request, pk): # hashtag_id
        # 해시태그의 pk(id)
        # 지울 객체 찾기
        hashtag = HashTag.objects.get(pk=pk)
        # 포스트의 pk(id)
        post_id = hashtag.post.id
        # 삭제
        hashtag.delete()
        # 응답
        return redirect('blog:detail', pk=post_id)
