$(document).ready(function(){   
  $("#analysisTweet").click(
      function(){
          $.post({
            url: "Tweet",
            data: {"tweet": $("#tweet").val()},
            beforeSend: function(){
                //
            },
            complete: function(){
                // Statement
               }
          }).done(function(data) {
              // score, fee, word
              console.log(data)
              $("#topic").html(data["score"])
              $("#word").html(data["word"])
              $("#fee").html(data["fee"])
          });
      }
  )
});
