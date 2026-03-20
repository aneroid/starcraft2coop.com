<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="robots" content="index, follow">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png"/>
<link rel='shortcut icon' href='/images/favicon.ico' type='image/x-icon' />
<link rel="stylesheet"  media="all" type="text/css" href="/styles/mainstyle.css?v=1.28">
<link href='https://fonts.googleapis.com/css?family=Convergence' rel='stylesheet' type='text/css'>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://www.google.com/recaptcha/api.js?render=6LcWQfEUAAAAAKrJ7sgdGyROvE7wuzopdDeAV0qd"></script>
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-165288360-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-165288360-1');
</script>
<script>
    grecaptcha.ready(function() {
        $(".captchaForm").each(function(){
            currentID = $(this).attr('id');
            if(currentID=="reportForm"){
                $(this).submit(function(event){
                    $("#submitbtn").attr("disabled", true);
                    grecaptcha.execute('6LcWQfEUAAAAAKrJ7sgdGyROvE7wuzopdDeAV0qd', { action: currentID }).then(function (token) {
                        $("#reportFormRecaptchaResponse").val(token);
                        var path = window.location.pathname;
                        var page = path.split("/").pop();
                        var x = document.forms["errorReport"]["comment"].value;
            		    var y = document.forms["errorReport"]["url"].value;
            			var z = $("#reportFormRecaptchaResponse").val();
            			$.ajax({  
                            type: 'POST',
                            url: '/scripts/addreport.php', 
                            data: { 
                                comment: x,
                                errorpage: page,
                                url:y, 
                                recaptcha_response:z},
                            success: function(data) {
                                $("#reportForm").hide();
                                $("#errorReport").append(data);
                                return false;
                            }
                        });
                        return false;
                        $("#submitbtn").attr("disabled", false);
                    });
                    
                })
            }
            else{
                $(this).submit(function(event){
                    var currentID = $(this).attr('id');
                    var currentForm = $(this);
                    event.preventDefault();
                    grecaptcha.execute('6LcWQfEUAAAAAKrJ7sgdGyROvE7wuzopdDeAV0qd', { action: currentID }).then(function (token) {
                        $("#" + currentID + "RecaptchaResponse").val(token);
                        currentForm.off("submit");
                        currentForm.submit();
                    });
                })
            }
            
        })
    },false)
</script>