from ast import And
from http.client import responses
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404

from .serializers import IngredientSerializer, RecipeSerializer, RecipeDetailSerializer, RecipeIngredientSerializer, TipsSerializer
from .models import Ingredient, Recipe, RecipeDetail, RecipeIngredient, Tips
from recipes import serializers

# Create your views here.

# index.html (테스트용)
def index(request):
    ingre = Ingredient.objects.get(id=100)
    print(ingre.id)
    context = {
        'id': ingre.id,
        'name': ingre.name,
        'score':ingre.score
        }
    return render(request, 'recipes/index.html', context)


# 레시피 리스트 GET
class RecipeList(APIView):
    id = openapi.Parameter('id', openapi.IN_PATH, description='recipe id', required=True, type=openapi.TYPE_NUMBER)
    @swagger_auto_schema(operation_id="레시피 리스트 조회", operation_description="입력한 레시피 번호를 포함한 5개의 정보 조회", manual_parameters=[id], responses={200: '조회 성공'})
    def get(self, request, id):
        r_list = []
        for i in range(id, id+5):
            id = i
            recipes = Recipe.objects.get(pk=id)
            tmp_list = [recipes.id, recipes.food_name, recipes.level, recipes.servings, recipes.time, recipes.title_img_url]
            r_list.append(tmp_list)
        return Response(r_list)


# 상세 레시피 조회 POST
class RecipeDetailList(APIView):
    param = openapi.Schema(type=openapi.TYPE_OBJECT, required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_NUMBER, description="레시피 번호"),
    }) 
    def get_object(self, id):
        try:
            recipe = Recipe.objects.get(pk=id)
            ingredients = RecipeIngredient.objects.filter(recipe_id = recipe.id)
            recipe.view_count += 1  # 조회수 갱신
            recipe.save()           # DB에 새로운 조회수 저장
            ing_list = []
            for i in ingredients:
                ing_list.append([i.ingredient_id.name, i.ingredient_amount])
            
            steps = RecipeDetail.objects.filter(recipe_id = recipe.id)
            step_list = []
            for s in steps:
                step_list.append(s.recipe_content)

            detail_list = [recipe.id, recipe.food_name, recipe.level, recipe.servings, recipe.time, recipe.title_img_url, ing_list, step_list]
            return detail_list

        except Recipe.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_id="상세 레시피 정보", operation_description="레시피 번호로 상세 정보 불러오기", request_body=param)
    def post(self, request, format=None):
        ingredient = self.get_object(request.data['id'])
        return Response(ingredient)


# 레시피 단계별 조회 POST
class RecipeStepList(APIView):
    param = openapi.Schema(type=openapi.TYPE_OBJECT, required=['recipe_id', 'recipe_step'],
    properties={
        'recipe_id': openapi.Schema(type=openapi.TYPE_NUMBER, description="레시피 번호"),
        'recipe_step': openapi.Schema(type=openapi.TYPE_NUMBER, description="요리 단계"),
    }) 
    def get_object(self, rid, rstep):
        try:
            recipe = Recipe.objects.get(pk=rid)
            step = RecipeDetail.objects.get(recipe_id=rid, recipe_step=rstep)
            steps = RecipeDetail.objects.filter(recipe_id=rid)
            
            detail_list = [recipe.id, recipe.food_name, rstep, step.recipe_img_url, step.recipe_content, len(steps)]
            return detail_list

        except RecipeDetail.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(operation_id="레시피 단계별 정보", operation_description="단계별 정보 불러오기", request_body=param)
    def post(self, request, format=None):
        print(request)
        recipe_step = self.get_object(request.data['recipe_id'], request.data['recipe_step'])
        return Response(recipe_step)


# 상세 레시피 조회 POST
class RecipeCompleteList(APIView):
    param = openapi.Schema(type=openapi.TYPE_OBJECT, required=['id'],
    properties={
        'id': openapi.Schema(type=openapi.TYPE_NUMBER, description="레시피 번호"),
    }) 
    def get_object(self, id):
        try:
            recipe = Recipe.objects.get(pk=id)
            complete_list = [recipe.food_name, recipe.title_img_url]
            return complete_list

        except Recipe.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_id="음식 완성 정보", operation_description="음식 완성 페이지", request_body=param)
    def post(self, request, format=None):
        complete = self.get_object(request.data['id'])
        return Response(complete)


# 인기 레시피 조회 POST
class RecipePopularList(APIView):
    def get_object(self):
        try:
            pop_recipe = Recipe.objects.all().order_by('-view_count')[:5]
            pop_list = []
            for pop in pop_recipe:
                tmp_list = [pop.id, pop.food_name, pop.level, pop.servings, pop.time, pop.title_img_url, pop.view_count]
                pop_list.append(tmp_list)
            return pop_list

        except Recipe.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_id="인기 레시피 리스트 조회", operation_description="조회수에 따른 상위 n개의 레시피 리스트 불러오기")
    def post(self, request, format=None):
        pop_list = self.get_object()
        return Response(pop_list)


# 요리 꿀팁 정보 GET
class TipsInfo(APIView):
    id = openapi.Parameter('id', openapi.IN_PATH, description='tips id', required=True, type=openapi.TYPE_NUMBER)
    @swagger_auto_schema(operation_id="꿀팁 조회", operation_description="꿀팁 전체 조회", manual_parameters=[id], responses={200: '조회 성공'})
    def get(self, request, id):
        tip = Tips.objects.get(pk=id)
        return Response(tip.tip_content)