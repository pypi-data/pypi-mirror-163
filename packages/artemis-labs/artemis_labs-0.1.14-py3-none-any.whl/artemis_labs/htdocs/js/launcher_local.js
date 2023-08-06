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

    // Store app info
    let projectState;

    // Designer Page
    let designerPage = null;
    let designerPages = [];

    // Page counter
    let pageCounter = 0;

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
        return designerPage.getValue();
    }

    // Create via socket  
    function createSocket(){
        console.log("Creating socket");
        ws = new WebSocket("ws://127.0.0.1:5678/");
        ws.onmessage = processSocketMessage;
    }

    // Process socket message
    function processSocketMessage(event) {
        const message = JSON.parse(event.data);
        if (message.type != 'ping' && message.type != 'heartbeat') {
        }
        if(message.type == "callback") {
            console.log('setting callback');
            let callbackType = message.attribute;
            let elementName = message.name;
            $("[component-name='" + elementName + "']").on(message.attribute, function() {
                let appState = getState();
                let appStateStr = JSON.stringify(appState);
                let outMessage = JSON.stringify({"type": "callback", "attribute": callbackType, "name": elementName, "state" : appStateStr});
                sendSocket(outMessage);
            });
        } else if (message.type == "update") {
            console.log(message);
            let updateElement = qs("[component-name='" + message.name + "']");
            if(updateElement != null) {
                console.log(updateElement);
                let updateComponent = designerPage.getComponentById('#' + updateElement.id);
                console.log(updateComponent);
                console.log(message.value);
                updateComponent.updateValue(message.value);
            } else {
                console.log("Element " + message.name + " not found");
            }
        } else if (message.type == "init") {
            console.log('[Server] State received');
            console.log(message.state);
            projectState = JSON.parse(message.state);
            setupLauncher();
        } else if (message.type == "navigate") {
            console.log('Navigating to ' + message.pageName);
            switchPageCallback(message.pageName);
        } else if (message.type == "query") {
            let appState = getState();
            let appStateStr = JSON.stringify(appState);
            let outMessage = JSON.stringify({"type": "query", "state" : appStateStr});
            console.log(outMessage);
            sendSocket(outMessage);
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
        
        // Version
        console.log("Version 1.13");

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
        designerPage = designerPages[0];
        designerPage.activatePage();
        loadPage(designerPage);
    }

    // Main Entry Point
    $(function() {

        // Setup socket
        createSocket();
        setInterval(()=>{
            let pingMessage = {'type': 'ping', 'data' : 'ping'};
            sendSocket(JSON.stringify(pingMessage));
        }, 20);
    });

  })(jQuery);
  