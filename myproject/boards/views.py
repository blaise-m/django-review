from django.shortcuts import render, get_object_or_404, redirect
# from django.http import Http404   #HttpResponse
from django.contrib.auth.models import User
from boards.models import Board, Topic, Post


def boards(request):	
	
	boards_list = Board.objects.all()	

	# boards_names = list()
	# for board in boards:
	# 	boards_names.append(board.name)
	# response_html = '<br>'.join(boards_names)	
	# return HttpResponse(response_html)

	return render(request, 'boards.html', {'boards': boards_list})


def board_topics(request, pk):
	
	# try:
	# 	board = Board.objects.get(pk=pk)
	# except Board.DoesNotExist:
	# 	raise Http404

	board = get_object_or_404(Board, pk=pk)
	topics = board.topics.all()
	return render(request, 'topics.html', {'board': board, 'topics': topics})


def new_topic(request, pk):		
	
	board = get_object_or_404(Board, pk=pk)

	if request.method == 'POST':
		subject = request.POST['subject']
		message = request.POST['message']

		# TODO: Get the currently logged in user
		user = User.objects.first()

		topic = Topic.objects.create(subject=subject, board=board, starter=user)
		post = Post.objects.create(message=message, topic=topic, created_by=user)

		# TODO: Redirect to the created topic page
		return redirect('board_topics', pk=board.pk)

	return render(request, 'new_topic.html', {'board': board})