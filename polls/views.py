from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # デフォルトはquestion_list。変更するには"context_object_name"属性を与える。
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """直近5件の質問を表示"""
        return Question.objects.filter(
            # 現在よりも前
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        '''過去日付の質問を表示しない'''
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
    
def vote(request, question_id):
    '''
    投票ページ
    '''
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 選択肢を取得 / 存在しなければKeyErrorを送出
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # エラーメッセージ付きの質問フォームを表示
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You didn`t select a choice.',
        })
    else:
        # modelsで設定したvotesに加える
        selected_choice.votes += 1
        selected_choice.save()
        # POSTに成功した後は大体redirect。reverseを使うことで"polls/id/results"を返す。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))











'''以下、urls.pyの書き換えに伴い削除'''
# def index(request):
#     '''
#     /polls/トップページで実際に動作するビュー
#     '''
#     ### render関数を使った書き方: HttpResponseやloaderをインポートする必要がない
#     # 直近5件を取得
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # contextに渡す
#     context = {'latest_question_list': latest_question_list}
#     # index.htmlにcontextを渡す（arg1: request, arg2: テンプレート名, arg3: 辞書)
#     return render(request, 'polls/index.html', context)
    
#     # ### HttpResponseを使った基本的な書き方
#     # # 直近5件の質問クエリを取得
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # # index.htmlをテンプレートとして取得
#     # template = loader.get_template('polls/index.html')
#     # # 5件分をcontextに渡す
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # # index.htmlにcontextを渡す
#     # return HttpResponse(template.render(context, request))
    
#     # ### デフォルト: テスト的に書いたコード
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     # # '''単純なレスポンスを返す'''
#     # return HttpResponse("Hello, world. You're at the polls index!")

# def detail(request, question_id):
#     '''
#     詳細ページ
#     '''
#     ### Http404のショートカット的な書き方
#     # オブジェクトがなければ404エラー送出
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
    
#     ### 基本の書き方
#     try:
#         # 受け取ったidをpkとしてデータを取得する
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         # question_idが存在しなかった場合404エラーを送出
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})
    
#     # 質問番号を返す: テスト的に書いたコード
#     return HttpResponse(f"You're looking at question {question_id}")

# def results(request, question_id):
#     '''
#     結果表示ページ
#     '''
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
    
#     # # ダミー実装
#     # response = "You're looking at the result of question %s."
#     # return HttpResponse(response % question_id)

# def vote(request, question_id):
#     '''
#     投票ページ
#     '''
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         # 選択肢を取得 / 存在しなければKeyErrorを送出
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # エラーメッセージ付きの質問フォームを表示
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': 'You didn`t select a choice.',
#         })
#     else:
#         # modelsで設定したvotesに加える
#         selected_choice.votes += 1
#         selected_choice.save()
#         # POSTに成功した後は大体redirect。reverseを使うことで"polls/id/results"を返す。
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
    
#     # # ダミー実装
#     # return HttpResponse(f"You're voting on question {question_id}.")

