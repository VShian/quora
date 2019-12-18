{% block script %}
<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script> 
<script>
	function sendVote(ele, url, vote_type, reply_id) {
		var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
		$.ajax({
			url: url,
			type: "POST",
			data: JSON.stringify({
				vote_type: vote_type,
				reply_id: reply_id
			}),
			headers:{"X-CSRFToken": csrf_token},
			contentType:"application/json; charset=utf-8",
			dataType:"json",
			success: function (data){
				console.log(data);
				parent = ele.parentElement;
				parent.children[0].text = data.upvote_count; 
				parent.children[1].text = data.downvote_count; 
			},
			error: function (data){
				console.log(data);
			}
		});
		return false;
	}
</script>
{% endblock %}
