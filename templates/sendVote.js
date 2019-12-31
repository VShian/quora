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
				parent = ele.parentElement;
				votesCountElement = parent.getElementsByClassName('votes')[0]; 
				votesCountElement.textContent = data.vote_count;
			},
			error: function (data){
				alert("Some error occured. Please reload the page and try again!");
			}
		});
		return false;
	}
</script>
