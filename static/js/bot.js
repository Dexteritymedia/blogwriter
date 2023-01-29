function getBotResponse(){
	var myText = $("#text_").val();
	var userBubble = '<div class="d-flex flex-row justify-content-end mb-4"><div class="p-3 me-3 border" style="border-radius: 15px; background-color: #fbfbfb;"><p class="small mb-0">' + myText +'</p></div><img src="{% static 'images/cartoon me.jpg' %}" alt="avatar 1" style="width: 45px; height: 100%;"></div>';
	$("#text_").val("");
	%(".chat-view").append(userBubble);
	$(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
	
	$.get("/get", {msg: myText }).done(function(data){
		var botBubble  = '<div class="d-flex flex-row justify-content-start mb-4"><img src="{% static 'images/cartoon me.jpg' %}" alt="avatar 1" style="width: 45px; height: 100%;"><div class="p-3 ms-3" style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);"><p class="small mb-0">'+ data +'</p></div></div>';
		$(".chat-view").append(botBubble);
	});
}
$("#text_").keypress(function(e){
	if (e.which == 13){
		getBotResponse();
	}
});