$(document).ready(
    function() {
        // Request the server to grab the article sources.
        $.ajax({
            url: "/info/getinfo",
            method: "get",
            success: function(stories) {
                news = $('.news_box');

                // For each enabled news source, grab the
                // stories and add them to the home page.
                if(stories["Bing"])
                  addStoriesToDOM("Bing", stories, news);

                if(stories["CNN"])
                  addStoriesToDOM("CNN", stories, news);

                if(stories["NPR"])
                  addStoriesToDOM("NPR", stories, news);

                // Hide the spinner used while fetching stories.
                $('#loader').attr("hidden", true);
            },
            error: function() {
                $('#news_box').append("<p>\n\rUnable to get news from the selected sources.</p>");
                $('#loader').attr("hidden", true);
            }
        });

        function addStoriesToDOM(location, stories, div)
        {
          $(div).append("<h4>" + location + "</h4>");
          for (var i = 0; i < stories[location].length; i++)
          {
              // Build the html markup representing the story.
              var html = "<a target='_blank' href=" + stories[location][i].url + ">" + stories[location][i].title + "</a>";
              html += "<p>";
              html += stories[location][i].description.replace(stories[location][i].highlight_text, "<span class='highlight_text'>" + stories[location][i].highlight_text + "</span>");
              html += "</p>"
              // Add the above html into the DOM.
              $(div).append(html)
          }
        }
    });
