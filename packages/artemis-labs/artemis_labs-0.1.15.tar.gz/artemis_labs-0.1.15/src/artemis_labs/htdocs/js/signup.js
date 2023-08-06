import {createAccount} from './Networking/networking.js'

(function($) {
    'use strict';    
   
    // Main Entry Point
    $(function() {

      
       // Create account
       $("#create-account-button").click(function() {
          createAccount($("#email").val(), $("#password").val(), (resp)=>{
            console.log('here');
            if(resp["status"] === "success") {
             console.log('success');
               window.location.href = "login.html";
            } else {
             console.log(resp);
               $(".error-msg").text("Error: Account already exists");
            }            
          });
       });
        
    });

  })(jQuery);
  