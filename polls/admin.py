from django.contrib import admin
from .models import Question, Choice


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    '''コンパクトなテーブルとして表示させる'''
    model = Choice
    # 入力用として空のフォームを3つ用意する
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    # タイトルをつける
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    
    # pub_dateを並び替え可能にする
    list_filter = ['pub_date']
    
    # 検索機能: likeクエリを使ってる
    search_fields = ['question_text']
    
    # 各フィールドの値を表示させる
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    
    # # 単純に表示順序を変えるだけなら以下
    # fields = ['pub_date', 'question_text']


# adminにQuestionを表示する
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)