$(document).ready(
  function(){
    // Request the server to grab the article sources.
		$.ajax({
  		url:"/info/getinfo",
  		method:"get",
  		success: function(stories){
          news = $('#news');
          for(var i = 0; i < stories.length; i++)
          {
            // Build up the html paragraph tag representing the story.
            var html = "<p>"
            html += "<b><a target='_blank' href=" + stories[i].url + ">" + stories[i].title + "</a></b>";
            html += "<p>";
            html += "<b>" + stories[i].source + ": </b>";
            html += stories[i].description.replace(stories[i].highlight_text, "<span class='highlight_text'>" + stories[i].highlight_text + "</span></p>");

            // Add the above html into the DOM.
            $(news).append(html)
          }
          $('#loader').attr("hidden", true);
 	 		},
 	 		error: function(){
 	 			$('#news').append("<p>\n\rUnable to get news from the selected sources.</p>");
        $('#loader').attr("hidden", true);
 	 		}
		});
  });
