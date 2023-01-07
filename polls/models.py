import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    '''質問'''
    question_text = models.CharField(max_length=20)   # 質問文（最大20文字）
    pub_date = models.DateTimeField('date published') # 投稿日
    def __str__(self):
        '''オブジェクトを質問文で返す'''
        return self.question_text
    def was_published_recently(self):
        '''独自メソッド: 作成日の確認'''
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    '''選択肢'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Questionクラスに紐付け（CASCADE: 削除時、関連するテーブルも削除）
    choice_text = models.CharField(max_length=200)                    # 選択肢文（最大200文字）
    votes = models.IntegerField(default=0)                           # 投票数（初期値0）
    def __str__(self):
        '''オブジェクトを選択肢文で返す'''
        return self.choice_text