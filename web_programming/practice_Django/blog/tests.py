from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_biden = User.objects.create_user(
            username='Biden',
            password='somepassword',
        )
        self.user_sanders = User.objects.create_user(
            username='Sanders',
            password='somepassword',
        )

        self.category_programming = Category.objects.create(
            name='programming', slug='programming'
        )

        self.category_music = Category.objects.create(
            name='music', slug='music'
        )

        self.post_001 = Post.objects.create(
            title = "첫번째 포스트 입니다.",
            content = "Hello, World. We are the world.", 
            category = self.category_programming,
            author = self.user_biden,

        )
        
        self.post_002 = Post.objects.create(
            title = "두번째 포스트 입니다.",
            content = "I like rice noodle.", 
            category = self.category_music,
            author = self.user_sanders,
        )

        self.post_003 = Post.objects.create(
            title = "세번째 포스트 입니다.",
            content = "Category가 없을 수도 있지요.", 
            author = self.user_sanders,

        )





    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        logo_btn = navbar.find('a', text="범내려온다")
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text="About me")
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')



    def category_card_test(self, soup):
        categories_card = soup.find('div')



    def test_post_list_with_posts(self):
        self.assertEqual(2, 2)
        self.assertEqual(Post.objects.count(), 3)

        # 1.1 포스트 목록 페이지(post list)를 연다.
        response = self.client.get('/blog/')

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)
        
        self.navbar_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn("미분류", post_003_card.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)



    def test_post_list_without_posts(self):
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0) # 새로운 DB를 만들어서 테스트함.

        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.assertIn('Blog', soup.title.text)

        # 2.2 메인 영역에 "아직 게시물이 없습니다" 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)




    def test_post_detail(self):
        self.assertEqual(Post.objects.count(), 3)

        # 1.2. 그 포스트의 url 은 '/blog/1/' 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')


        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 포스트의 url로 접근하면 정상적으로 response가 온다.(status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)

        # 2.3. 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4. 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)

        # 2.5. 첫 번째 포스트의 작성자(suthor)가 포스트 영역에 있다.(아직 구현할 수 없음.)
        self.assertIn(self.user_biden.username.upper(), post_area.text)

        # 2.6. 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)

        



