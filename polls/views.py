from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Question

def index(request):
    '''実際に動作するビュー'''
    ### render関数を使った書き方: HttpResponseやloaderをインポートする必要がない
    # 直近5件を取得
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # contextに渡す
    context = {'latest_question_list': latest_question_list}
    # index.htmlにcontextを渡す（arg1: request, arg2: テンプレート名, arg3: 辞書)
    return render(request, 'polls/index.html', context)
    
    # ### HttpResponseを使った基本的な書き方
    # # 直近5件の質問クエリを取得
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # # index.htmlをテンプレートとして取得
    # template = loader.get_template('polls/index.html')
    # # 5件分をcontextに渡す
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # # index.htmlにcontextを渡す
    # return HttpResponse(template.render(context, request))
    
    # ### デフォルト: テスト的に書いたコード
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # # '''単純なレスポンスを返す'''
    # return HttpResponse("Hello, world. You're at the polls index!")

def detail(request, question_id):
    '''詳細ページ'''
    ### Http404のショートカット的な書き方
    # オブジェクトがなければ404エラー送出
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    
    ### 基本の書き方
    try:
        # 受け取ったidをpkとしてデータを取得する
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        # question_idが存在しなかった場合404エラーを送出
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    
    # 質問番号を返す: テスト的に書いたコード
    return HttpResponse(f"You're looking at question {question_id}")

def results(request, question_id):
    '''結果表示ページ'''
    response = "You're looking at the result of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    '''投票ページ'''
    return HttpResponse(f"You're voting on question {question_id}.")

