$(document).ready(function(){   
  $("#analysisTweet").click(
      function(){
          $.post({
            url: "Tweet",
            data: {"tweet": $("#tweet").val()},
            success: function(rsl){
                alert("success !")
            }
          }).done(function(data) {
              
            console.log(data["score"])
              console.log(data)
          });

          
      }
  )
});
