$(document).ready(function(){   
  $("#analysisTweet").click(
      function(){
          $.post({
            url: "Tweet",
            data: {"tweet": $("#tweet").val()},
            success: function(rsl){
                alert("success !", rsl)
            }
          }).done(function() {
            alert("Finish !")
          });

          
      }
  )
});
