import {loginAccount} from './Networking/networking.js'

(function($) {
    'use strict';    
   
    // Login
    function login() {
        // Validate email input is email format
        if(!$("#email").val().match(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/)) {
            $(".error-msg").text("Error: Please enter a proper email address");
            return;
        }                

        // Login
        loginAccount($("#email").val(), $("#password").val(), (resp)=>{
            if (resp.status === "Account does not exist") {
                $(".error-msg").text("Error: Account does not exist");
            } else if (resp.status == "Incorrect password") {                    
                $(".error-msg").text("Error: Incorrect password");
            } else {
                const token = resp["status"];
                console.log(token);
                window.location.href = "main.html?/username=" + $("#email").val() + "&token=" + token;
            }
        });
    }

    // Main Entry Point
    $(function() {

        // Login
        $("#login-button").click(function() {
            login();
        });

        // Login if enter key is pressed in password input
        $("#password").keypress(function(e) {
            if(e.which == 13) {
                login();
            }
        });
    });

  })(jQuery);
  