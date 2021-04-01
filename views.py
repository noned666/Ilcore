from django.shortcuts import render
from .forms import CommentForm, ContactForm
from .models import  Article, Category, Comment
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Подключение новой формы для регистрации
from .forms import RegistrForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, DetailView
from django.core.mail import send_mail, BadHeaderError

genre = Category.objects.all()

# Главная страница, Вывод пагинатора
def index(request):
        news = Article.objects.all()
        paginator = Paginator(news, 5) # Show 5 contacts per page

        page = request.GET.get('page')
        try:
         news = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
                news = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
         news = paginator.page(paginator.num_pages)
        #Вывод категорий
      
        return render(request, 'index.html', {'news': news, 'genre':genre})

#вывод по категориям
def list(reguest, slug):
    category = Category.objects.get(slug=slug)
    news = Article.objects.filter(category=category)
   

    paginator = Paginator(news, 2)
    page = reguest.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(reguest, 'category.html', {
        'category': category,
        'page': page,
        'news': news,
        'genre':genre})

#Страница с постом в деталиях и комментарии
def post_detail(request, pk):
        post = get_object_or_404(Article, pk=pk)
  
        comment = Comment.objects.filter(post=post)
        if request.method == "POST":
                form = CommentForm(request.POST)
                if form.is_valid():
                        com = form.save(commit=False)
                        com.user = request.user
                        com.post = post
                        com.save()
                        return HttpResponseRedirect(request.path_info)
        else:
                form = CommentForm()
        return render(request, 'post_detail.html', {'post': post,
                 'form': form,
                'comment': comment, 'genre':genre})

# Функция регистрации
def regist(request):
    # Массив для передачи данных шаблонны
    data = {}
    
    # Проверка что есть запрос POST
    if request.method == 'POST':
        # Создаём форму
        form = RegistrForm(request.POST)
        # Валидация данных из формы
        if  form.is_valid():
            # Сохраняем пользователя
            form.save()
            # Передача формы к рендару
            data['form'] = form
            # Передача надписи, если прошло всё успешно
            data['res'] = "Всё прошло успешно"
            # Рендаринг страницы
            return render(request, 'registration/regist.html', data)
    else: # Иначе
        # Создаём форму
        form = RegistrForm()
        # Передаём форму для рендеринга
        data['form'] = form
        # Рендаринг страницы
        return render(request, 'registration/regist.html', data, {'genre':genre})



#Вывод записей по категориям
class CategoryDetailView(DetailView):
        model = Category
        queryset = Category.objects.all()
        context_object_name = 'category'
        template_name = 'category.html'
        slug_url_kwarg = 'slug'
     

def profile(request):
   
        return render(request, 'profile.html', {'genre':genre})


def about(request):
       
        return render(request, 'about.html', {'genre':genre})


def contactView(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		#Если форма заполнена корректно, сохраняем все введённые пользователем значения
		if form.is_valid():
			subject = form.cleaned_data['subject']
			sender = form.cleaned_data['sender']
			message = form.cleaned_data['message']
			copy = form.cleaned_data['copy']

			recipients = ['kleymoments@gmail.com']
			#Если пользователь захотел получить копию себе, добавляем его в список получателей
			if copy:
				recipients.append(sender)
			try:
				send_mail(subject, message, 'kleymoments@gmail.com', recipients)
			except BadHeaderError: #Защита от уязвимости
				return HttpResponse('Invalid header found')
			#Переходим на другую страницу, если сообщение отправлено
			return render(request, 'index.html')
	else:
		#Заполняем форму
		form = ContactForm()
	#Отправляем форму на страницу
	return render(request, 'contact.html', {'form': form,
         'genre':genre})


 

class Search(ListView):

    model = Article
    template_name = 'article_list.html'
    context_object_name = 'news'
     
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(full_text__icontains=query)
        )
        return object_list

   
    