<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
function getBotResponse(){
	var myText = $("#my-text").val();
	var userBubble = '<div class="your-container"><div class="your-msg">' + myText +'</div></div>';
	$("#my-text").val("");
	%(".chat-view").append(userBubble);
	$(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
	
	$.get("/get", {msg: myText }).done(function(data){
		var botBubble  = '<div class="bot-container"><div class="bot-msg">'+ data +'</div></div>';
		$(".chat-view").append(botBubble);
	});
}
$("#my-text").keypress(function(e){
	if (e.which == 13){
		getBotResponse();
	}
});


$(document).ready(function(){
	$("form").on("submit",
	function(event) {
		var rawText = 
	$("#text").val();
	var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
	$("#text").val("");
	
	%("#chatbot").append(userHtml);
	
	document.getElementById("userInput").scrollIntoView({
		block: "start",
		behavior: "smooth",
	});
	$.ajax({
		data: {
			msg: rawText,
		},
		type: "POST",
		url: "/get",
	}).done(function(data)
	
	{
		var botHtml = '<p class="botText"><span>' + data + "</span></p>";
		
		$("#chatbot").append($.parseHTML(botHtml));
		
		document.getElementById("userInput").scrollIntoView({
			block: "start",
			behavior: "smooth",
		});
	});
	event.preventDefault();
	});
});