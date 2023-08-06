import { createElement, qs, qsa } from "./Helpers/helper.js";
import {validateAccount, registerAccount, logoutAccount, getApps, updateApps, createAccount} from './Networking/networking.js'
import {getURLArg} from './URL/url.js'

(function($) {
    'use strict';    

    // Username and password
    let username;
    let token;

    // App content
    let appContent;

    // Add organization member
    function addOrganizationMember(memberName, memberIndex) {

        // Create page DOM element
        let memberItem = createElement("li", "member-" + memberIndex, "member-item active");

        let memberIcon = createElement("img", "", "member-item-icon");
        $(memberIcon).attr("src", "libs/builder/icons/user.svg");
        $(memberItem).append(memberIcon);
    
        let memberSpan = createElement("span", "", "active-member");
        $(memberSpan).text(memberName);
        $(memberItem).append(memberSpan);
    
        let memberTree = qs("#treemanager .tree ol");
        $(memberTree).append(memberItem);
    }

    // Add appliction
    function addApplication(applicationName, applicationIndex) {

        // Create app container
        let appDiv = createElement("div", "application-" + applicationIndex, "app");
        appDiv.setAttribute("app-key", applicationName);

        // Create title and button containers
        let appTitleBoxDiv = createElement("div", "", "app-title-box");
        let appButtonBoxDiv = createElement("div", "", "app-button-box");
        appDiv.appendChild(appTitleBoxDiv);
        appDiv.appendChild(appButtonBoxDiv);

        // Create app buttons
        let appLaunchButton = createElement("button", "", "app-launch-button");
        $(appLaunchButton).text("Launch");
        $(appButtonBoxDiv).append(appLaunchButton);
        let appLaunchButtonIcon = createElement("i", "", "fa-light fa-rocket-launch app-button-icon");
        $(appLaunchButton).append(appLaunchButtonIcon);

        let appEditButton = createElement("button", "", "app-edit-button");
        $(appEditButton).text("Edit");
        let appEditButtonIcon = createElement("i", "", "fa-light fa-pen-to-square app-button-icon");
        $(appEditButton).append(appEditButtonIcon);
        $(appButtonBoxDiv).append(appEditButton);

        let appDeleteButton = createElement("button", "", "app-delete-button");
        $(appDeleteButton).text("Delete");
        let appDeleteButtonIcon = createElement("i", "", "fa-light fa-trash-can app-button-icon");
        $(appDeleteButton).append(appDeleteButtonIcon);
        $(appButtonBoxDiv).append(appDeleteButton);

        // Create app title
        let appTitleSpan = createElement("span", "", "app-title");
        $(appTitleSpan).text(applicationName);
        appTitleBoxDiv.appendChild(appTitleSpan);

        // Add application before app button
        let appGrid = qs(".app-grid");
        let addAppButton = qs("#application-create");
        appGrid.insertBefore(appDiv, addAppButton);

        // Handle deletion
        $(appDeleteButton).click(function() {
            launchAppDeletePopup(()=>{
                let appKey = $(this).parent().parent().attr("app-key");
                delete appContent[appKey];
                $(this).parent().parent().remove();
                updateApps(username, token, appContent);
            });
        });

        // Handle launch
        $(appLaunchButton).click(function() {
            let appKey = $(this).parent().parent().attr("app-key");
            window.location.href = "launcher.html?username=" + username + "&token=" + token + "&appKey=" + appKey;
        });

        // Handle edit
        $(appEditButton).click(function() {
            let appKey = $(this).parent().parent().attr("app-key");
            window.location.href = "editor.html?username=" + username + "&token=" + token + "&appKey=" + appKey;
        });
    }

    // Create appliction
    function addCreateApplicationButton() {

        // Create app container
        let appDiv = createElement("div", "application-create", "app");

        // Create app buttons
        let appCreateButton = createElement("button", "app-create-button", "");
        $(appCreateButton).text("Create App");
        $(appDiv).append(appCreateButton);

        // Create add icon for button
        let appCreateIcon = createElement("i", "", "fa-light fa-plus app-button-icon");
        $(appCreateButton).append(appCreateIcon);

        // Add application to app grid
        let appGrid = qs(".app-grid");
        appGrid.appendChild(appDiv);

        // Click listener
        $(appCreateButton).click(function() {

            // Launch app create
            launchAppCreatePopup(
                (appName)=> {
                    // Create app
                    appContent[appName] = {};

                    // Update app
                    updateApps(username, token, appContent);

                    // Create app
                    addApplication(appName, Object.keys(appContent).length);
                }
            )           
        });
    }

    // Populate app grid
    function populateAppGrid() {
        
        // Populate app button
        addCreateApplicationButton();

        // Populate app grid
        let appKeys = Object.keys(appContent);
        console.log(appKeys);
        for(let i = 0; i < appKeys.length; i++) {
            let appKey = appKeys[i];
            addApplication(appKey, i);
        }
    }

     // Launch activate account popup
     function launchCreateAccount() {
        $("#activate-account-popup").removeClass("hidden");
        $("#screen-film").removeClass("hidden");
        $(".activate-account-popup-content #error-msg").addClass("hidden");

        $(".activate-account-popup-content button").click(function() {
            let productKey = $(".activate-account-popup-content input").val();
            registerAccount(username, token, productKey, (resp) => {
                if (resp.status === 'invalid key') {
                    $(".activate-account-popup-content #error-msg").text("Error: Invalid API key");
                    $(".activate-account-popup-content #error-msg").removeClass("hidden");
                } else if (resp.status === "success"){
                    $(".activate-account-popup-content #error-msg").removeClass("hidden");
                    $(".activate-account-popup-content #error-msg").text("");
                    $("#activate-account-popup").addClass("hidden");
                    $("#screen-film").addClass("hidden");
                    $(".activate-account-popup-content button").unbind();
                    setupMain();
                } else {
                    $(".activate-account-popup-content #error-msg").text("Error: API key in use");
                    $(".activate-account-popup-content #error-msg").removeClass("hidden");
                }
            });        
        });
    }

    // Setup app create popup
    function setupAppPopups() {
        $("#create-app-popup .close").click(function() {
            $("#create-app-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            $(".create-app-popup-content button").unbind();
        });
        $("#delete-app-popup .close").click(function() {
            $("#delete-app-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            $(".delete-app-popup-content button").unbind();
        });
        $("#activate-account-popup .close").click(function() {
            $("#activate-account-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            $("#activate-account-popup-popup-content button").unbind();
        });
    }

    // Launch app popup
    function launchAppCreatePopup(callback) {
        $("#create-app-popup").removeClass("hidden");
        $("#screen-film").removeClass("hidden");
        $(".create-app-popup-content #error-msg").addClass("hidden");

        $(".create-app-popup-content button").click(function() {
            let appName = $(".create-app-popup-content input").val();
            $(".create-app-popup-content input").val("");
            if (appName in appContent) {
                $(".create-app-popup-content #error-msg").text("Error: App already exists");
                $(".create-app-popup-content #error-msg").removeClass("hidden");
                return;
            } 
            $("#create-app-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            callback(appName);
            $(".create-app-popup-content button").unbind();
        });
    }

    // Launch delete app popup
    function launchAppDeletePopup(callback) {
        $("#delete-app-popup").removeClass("hidden");
        $("#screen-film").removeClass("hidden");
        $(".delete-app-popup-content button").click(function() {
            $("#delete-app-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            $(".delete-app-popup-content button").unbind();
            callback();
        });
    }

    // Main setup
    function setupMain() {
        // Query apps
        getApps(username, token, (resp)=>{          
            appContent = JSON.parse(resp["content"]);
            populateAppGrid();
        });

        // Populate organization members
        addOrganizationMember(username, 1);

        // Setup popups
        setupAppPopups();

        // Setup apps button
        $("#nav-apps-button").attr("href", "main.html?username=" + username + "&token=" + token);
        $("#nav-logout-button").click(()=>{
            console.log("er");
            logoutAccount(username, token, ()=>{
                window.location.href = "login.html";
            });
        });
    }


    // Main Entry Point
    $(function() {

        // Get cookie username and token
        try {
            username = getURLArg(0);
            token = getURLArg(1);
        } catch(err) {            
           window.location.href = "login.html";
        }

        // Validate account
        validateAccount(username, token, (resp)=>{
            console.log(resp);
            if (resp.status === "Account subscription expired") {
                launchCreateAccount();
                return;
            }
            if(resp.status != "success") {
                window.location.href = "login.html";
            }
            if(resp.status == "success") {
                setupMain();
            }
        });
       
    });

  })(jQuery);
  