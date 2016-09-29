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
              // Multiple keywords can be highlighted, so handle them separately.
              // Only a comma is currently supported as a keyword delimiter.
              var highlights = []
              if (stories[location][i].highlight_text)
                highlights = stories[location][i].highlight_text.split(",")

              // Build the html markup representing the story.
              var html = "<a target='_blank' href=" + stories[location][i].url + ">" + stories[location][i].title + "</a>";
              html += "<p>";

              // Highlight each specified keyword.
              for(var k = 0; k < highlights.length; k++)
              {
                var regex = new RegExp(highlights[k], 'gi' );
                html += stories[location][k].description.replace(regex, "<span class='highlight_text'>" + highlights[k] + "</span>");
              }

              html += "</p>"
              // Add the above html into the DOM.
              $(div).append(html)
          }
        }
    });
