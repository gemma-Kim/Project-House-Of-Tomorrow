import re, json, bcrypt, jwt

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse

from my_settings      import SECRET_KEY, ALGORITHM
from user.models      import User, Follow, Like, PostBookmark, ProductBookmark
from user.utils       import login_decorator


class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email     = data['email']
            username  = data['username']
            password  = data['password']

            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not re.match(email_validation, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if User.objects.filter(Q(email=email) | Q(username=username)).exists():
                return JsonResponse({'message':'EXIST_USER'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username = username,
                email    = email,
                password = hashed_password
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            signin_data      = json.loads(request.body)
            user             = User.objects.get(email=signin_data['email'])
            email            = signin_data['email']
            password         = signin_data['password']
            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not re.match(email_validation, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'WRONG_PASSWORD'}, status=400)

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message':'UNKNOWN_USER'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)




















































class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)

            if Like.objects.filter(user_id=user.id, post_id=data['id']).exists():
                return JsonResponse({'message':'INVALID_LIKE'}, status=400)

            Like.objects.create(user_id=user.id, post_id=data['id'])

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)

            if not Like.objects.filter(user_id=user.id, post_id=data['id']).exists():
                return JsonResponse({'message':'INVALID_DELETE'}, status=400)

            Like.objects.filter(user_id=user.id, post_id=data['id']).delete()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class BookmarkView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)

            if data['post_id']:
                if PostBookmark.objects.filter(user_id=user.id, post_id=data['post_id']).exists():
                    return JsonResponse({'messsage':'INVALID_BOOKMARK'}, status=400)

                PostBookmark.objects.create(user_id=user.id, post_id=data['post_id'])

                return JsonResponse({'message':'SUCCESS'}, status=200)

            elif data['product_id']:
                if ProductBookmark.objects.filter(user_id=user.id, product_id=data['product_id']).exists():
                    return JsonResponse({'messgae':'INVALID_BOOKMARK'}, status=400)

                ProductBookmark.objects.create(user_id=user.id, product_id=data['product_id'])

                return JsonResponse({'message':'SUCCESS'}, status=200)

            if CollectionBookmark.objects.filter(user_id=user.id, collection_id=data['collection_id'].exists():
                return JsonResponse({'message':'INVALID_BOOKMARK'}, status=400)

            CollectionBookmark.objects.create(user_id=user.id, collection_id=data['collection_id'])

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)

            if data['post_id']:
                if not PostBookmark.objects.filter(user_id=user.id, post_id=data['post_id']).exists():
                    return JsonResponse({'messsage':'INVALID_DELETE'}, status=400)

                PostBookmark.objects.filter(user_id=user.id, post_id=data['post_id']).delete()

                return JsonResponse({'message':'SUCCESS'}, status=200)

            elif data['product_id']:
                elif not ProductBookmark.objects.filter(user_id=user.id, product_id=data['product_id']).exists():
                    return JsonResponse({'messgae':'INVALID_BOOKMARK'}, status=400)

                ProductBookmark.objects.filter(user_id=user.id, product_id=data['product_id']).delete()

                return JsonResponse({'message':'SUCCESS'}, status=200)

            if not CollectionBookmark.objects.filter(user_id=user.id, collection_id=data['collection_id'].exists():
                return JsonResponse({'message':'INVALID_BOOKMARK'}, status=400)

            CollectionBookmark.objects.filter(user_id=user.id, collection_id=data['collection_id']).delete()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
