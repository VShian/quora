from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from app.models import Answer, Vote, Reply


class VoteAPI(APIView):
	# login_url = '/accounts/login/'
	# redirect_field_name = '/'
	queryset = Vote.objects.all()
	authentication_classes = (authentication.SessionAuthentication, authentication.BasicAuthentication)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, **kwargs):
		vote_type = request.data.get('vote_type')
		reply_id = request.data.get('reply_id')

		obj, created = Vote.objects.get_or_create(user=request.user, reply_id=reply_id, vote_type=vote_type)
		if created:
			other_vote_type = (vote_type + 1) % 2
			other_vote = Vote.objects.filter(user=request.user, reply_id=reply_id, vote_type=other_vote_type)

			if other_vote.exists():
				other_vote.delete()

		else:
			obj.delete()

		return Response(data={'vote_count': Reply.objects.get(id=reply_id).upvotes()}) 
