import { createElement, qs, qsa } from "./Helpers/helper.js";
import {validateAccount, logoutAccount, getApps, updateApps} from './Networking/networking.js'
import {getURLArg} from './URL/url.js'

// Components
import { Button } from "./Components/Designer/button.js";
import { Input } from "./Components/Designer/input.js";
import { SelectInput } from "./Components/Designer/select_input.js";
import { Image } from "./Components/Designer/image.js";
import { Header } from "./Components/Designer/header.js";
import { HorizontalRule } from "./Components/Designer/horizontal_rule.js";
import { TextArea } from "./Components/Designer/text_area.js";
import { RadioButton } from "./Components/Designer/radio_button.js";
import { Checkbox } from "./Components/Designer/checkbox.js";
import { Box } from "./Components/Designer/box.js";

// Pages
import { DesignerPage } from "./Pages/page.js";

// Component manager
import {createComponentFromPlacement, getComponentSizeClass, createComponentFromType} from './Components/component_manager_launcher.js';


(function($) {
    'use strict';    

    // Socket
    let ws;

    // Store login info
    let username;
    let token;
    let appKey;

    // Store app info
    let appContent;
    let projectState;

    // Designer Page
    let designerPage = null;
    let designerPages = [];

    // Page counter
    let pageCounter = 0;

    // Active page
    let activePage = 0;

    // Switch page callback
    function switchPageCallback(page) {
        let targetPage = null;
        for(let i = 0; i < designerPages.length; i++) {
            if(designerPages[i].getPageName() === page) {
                targetPage = designerPages[i];
                break;
            }
        }
        if(targetPage !== null) {
            loadPage(targetPage);
        }
    }

    // Create component from state
    function createComponentFromState(state) {

        // Create component
        let component = createComponentFromType(state["type"], state["index"]);
        component.loadState(state);

        // Bind next page callback
        if (state["type"] === "button") {
            component.bindNextPageCallback(switchPageCallback);
        }

        // Store component
        designerPage.addComponent(component, true);
        designerPage.incrementComponentCounter();
    }


    // Load page without saving previous page
    function loadPage(newDesignerPage) {
       
        // Remove old components
        let components = qsa("div[data-type=component]");
        for(let i = 0; i < components.length; i++) {
            components[i].remove();
        }

        // Update designer page
        designerPage = newDesignerPage; 

        // Activate page link
        designerPage.activatePage();    

        // Update designer page
        let state = designerPage.loadState();
        let stateKeys = Object.keys(state);
        for (let i = 0; i < stateKeys.length; i++) {
            if(stateKeys[i].includes("#component")) {
                createComponentFromState(state[stateKeys[i]]);
            }
        }
    }

    // Create page
    function createPage() {

        // Create designer pageg51
        let newDesignerPage = new DesignerPage(
            pageCounter            
        );
        // Store page
        designerPages.push(newDesignerPage);

        // Bind click callback
        newDesignerPage.bindClickCallback(() => { 
            switchPage(newDesignerPage);
        });

        // Increment page counter
        pageCounter++;
    }

    // Get state
    function getState() {
        let state = {};
        let componentInputs = qsa(".component-input");
        let componentSelectInputs = qsa(".component-select-input");
        let componentCheckboxes = qsa(".component-checkbox");
        let componentTextAreas = qsa(".component-text-area");
        let componentRadios = qsa(".component-radio-button");
        componentRadios.forEach(function(radio) {
            let radioButton = radio.children[0];
            let radioName = $(radio).attr("component-name");
            let radioValue = radioButton.checked;
            state[radioName] = radioValue;
        });
        componentInputs.forEach(function(componentInput) {
            let input = componentInput.children[0];
            state[$(componentInput).attr("component-name")] = input.value;
        });
        componentSelectInputs.forEach(function(componentSelectInput) {
            let selectedValue = $("#" + componentSelectInput.id + " > select").val();
            if(selectedValue == null) {
                selectedValue = document.querySelector("#" + componentSelectInput.id + " > select > option").text;
            }
            state[$(componentSelectInput).attr("component-name")] = selectedValue;
        });
        componentCheckboxes.forEach(function(componentCheckbox) {
            let checkbox = componentCheckbox.children[0];
            let isChecked = $(checkbox).is(":checked")
            state[$(componentCheckbox).attr("component-name")] = isChecked;
        });
        componentTextAreas.forEach(function(componentTextArea) {
            let textArea = componentTextArea.children[0];
            state[$(componentTextArea).attr("component-name")] = textArea.value;
        });
        return state;
    }

    // Create via socket  
    function createSocket(){
        ws = new WebSocket("ws://127.0.0.1:5678/");
        ws.onmessage = processSocketMessage;
    }

    // Process socket message
    function processSocketMessage(event) {
        const message = JSON.parse(event.data);
        console.log('[Client] ');
        console.log(message);
        if(message.type == "callback") {
            let callbackType = message.attribute;
            let elementName = message.name;
            $("[component-name='" + elementName + "']").on("click", function() {
                let appState = getState();
                let appStateStr = JSON.stringify(appState);
                let outMessage = JSON.stringify({"type": "callback", "attribute": callbackType, "name": elementName, "state" : appStateStr});
                sendSocket(outMessage);
            });
        } else if (message.type == "update") {
            let updateElement = qs("[component-name='" + message.name + "']");
            if(updateElement != null) {
                let updateElementType = $(updateElement).attr("class");
                switch(updateElementType) {
                    case "component-image":
                        let imageComponent = qs("[component-name='" + message.name + "']");
                        let image = imageComponent.children[0];
                        image.src = message.value;
                        break;
                    case "component-header":
                        let headerComponent = qs("[component-name='" + message.name + "'] h1");
                        $(headerComponent).text(message.value);
                        break;
                    case "component-input":
                        let inputComponent = qs("[component-name='" + message.name + "'] input");
                        $(inputComponent).val(message.value);
                        break;
                    case "component-select-input":
                        let selectInputComponent = qs("[component-name='" + message.name + "'] select");
                        $(selectInputComponent).val(message.value);
                        break;
                    case "component-checkbox":
                        let checkboxComponent = qs("[component-name='" + message.name + "'] input");
                        $(checkboxComponent).prop("checked", message.value);
                        break;
                    case "component-text-area":
                        let textAreaComponent = qs("[component-name='" + message.name + "'] textarea");
                        $(textAreaComponent).val(message.value);
                        break;
                    default:
                        console.log("Element type " + updateElementType + " not supported");
                }
            } else {
                console.log("Element " + message.name + " not found");
            }
        } else if (message.type == "init") {
            console.log(message.state);
        } else if (message.type === "ping") {
            console.log("[Client] Ping received");
        }
    }

    // Send via socket
    function sendSocket(outMessage){
        try {
            ws.send(outMessage);
        } catch (error) {
            console.log("[Error sending message to server]", error)
        }
    }


    // Setup editor
    function setupLauncher() {
        
        // Add page if project state empty
        if (Object.keys(projectState).length == 0) {
            projectState["0"] = {};
        }

        // Update designer menu when resizing browser
        $(window).resize(function() {
            designerPage.updateComponentPositions();
        });

        // Bind apps nav buttons
        $("#nav-apps-button").attr("href", "main.html?username=" + username + "&token=" + token);
        $("#nav-logout-button").click(()=>{
            logoutAccount(username, token, ()=>{
                window.location.href = "login.html";
            });
        });

        // Create pages
        let pageKeys = Object.keys(projectState);
        for(let i = 0; i < pageKeys.length; i++) {
            let pageKey = pageKeys[i];;
            createPage();
            designerPages[i].setState(projectState[pageKey]);
        }

        // Set first page active
        designerPage = designerPages[activePage];
        designerPage.activatePage();
        loadPage(designerPage);
    }

    // Main Entry Point
    $(function() {

        // Get cookie username and token
        try {
            username = getURLArg(0);
            token = getURLArg(1);
            appKey = getURLArg(2);
            if (window.location.href.indexOf('active-page') != -1) {
                activePage = getURLArg(3);
            }
        } catch(err) {            
            window.location.href = "login.html";
        }

        // Validate account
        validateAccount(username, token, (resp)=>{
            if(resp.status != "success") {
                window.location.href = "login.html";
            }
        });

        // Query apps
        getApps(username, token, (resp)=>{
            appContent = JSON.parse(resp["content"]);
            projectState = appContent[appKey];
            setupLauncher();
        });       

        // Setup socket
        createSocket();
        setInterval(()=>{
            let pingMessage = {'type': 'ping'};
            sendSocket(JSON.stringify(pingMessage));
        }, 500);
    });

  })(jQuery);
  