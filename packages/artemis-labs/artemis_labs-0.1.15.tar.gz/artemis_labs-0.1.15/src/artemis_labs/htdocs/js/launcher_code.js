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
import { getElementBounds, testIntersection } from "./Math/bounds.js";


(function($) {
    'use strict';    

    // Editor
    let editor;
    let editor_language = 'python';

    // Components
    let componentCounter = 0;
    let componentX = 0;
    let componentY = 0;

    // Inputs
    let inputCounter = 0;

    // Component states
    let defaultComponentStates = {
        "card" : {
            "top": "0px",
            "left": "0px",
            "width": 400,
            "height": 80,
            "id": "",
            "index": 12,
            "zIndex": 1,
            "name": "card",
            "type": "card",
            "cardTitle": "Title",
            "borderRadius": 1,
            "borderWidth": 1,
            "borderColor": "#eeeeee",
            "borderStyle": "solid",
            "backgroundColor": "#fefefe",
            "boxShadow": true,
            "cardTitleAlignment": "left",
            "cardHeaderEnabled": false,
            "cardHeaderBorderEnabled": true,
            "headerColor": "#fefefe",
            "headerTextColor": "#000000"
        },
        "heading" : {
            "top": componentY,
            "left": componentX + 15,
            "width": 800,
            "height": 20,
            "id": "",
            "index": 26,
            "zIndex": 1,
            "name": "Default",
            "type": "heading",
            "headingText": "",
            "fontSize": 1,
            "headingAlignment": "start",
            "fontUnit": "rem",
            "textColor": "#000000",
            "backgroundColor": "#ffffff",
            "fontWeight": "600"
        },
        "table" : {
            "top": 336,
            "left": 384,
            "width": 320,
            "height": 128,
            "id": "#component-8",
            "index": 8,
            "zIndex": 5,
            "name": "Default",
            "type": "table",
            "headerHighlighted": false,
            "striped": true,
            "bordered": true,
            "hoverableRows": true,
            "numberOfDummyRows": 2
        },
        "image": {
            "top": 128,
            "left": 184,
            "width": 128,
            "height": 128,
            "id": "",
            "index": 26,
            "zIndex": 14,
            "name": "image",
            "type": "image",
            "imageURL": "",
            "imageTiling": "no-repeat",
            "imageFit": "contain",
            "imagePosition": "left",
            "borderRadius": 0,
            "borderWidth": 1,
            "borderColor": "#dee2e6",
            "borderStyle": "dashed",
            "showImageInDesigner": true
        },
    };

    // Socket
    let ws;

    // Exit
    let exit = false;
    let restarting = false;

    // Clear window
    function clearWindow() {
        let outputList = qs("#outputs-list");
        if(outputList) {
            for (let i = outputList.children.length; i >= 0; i--) {
                if (outputList.children[i] == undefined) continue;
                outputList.removeChild(outputList.children[i]);
            }
        }
    }

    // Create via socket  
    function createSocket(){
        console.log("Creating socket");
        ws = new WebSocket("ws://127.0.0.1:5678/");
        ws.onmessage = processSocketMessage;
        ws.onclose = function(e) {
            clearWindow();
            if (!restarting) window.close();
            console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
            setTimeout(function() {
                createSocket();
            }, 100);
            setTimeout(function() {
                if (restarting) {
                    window.close();
                }
            }, 3000);
        };
    }

    // DOM Helpers
    function createInputCard(inputCardTitle, inputCardComment, inputCardComponentDOM) {
        
        // Create input card
        let inputCardDOM = createElement('div', '' + inputCounter++, 'input-card');

        // Create card header
        let cardHeaderDOM = createElement("div", "card-header-" + (inputCounter-1), "card-header-bar");
        inputCardDOM.appendChild(cardHeaderDOM);

        // Create card header contents 
        let variableNameCardHeaderDOM = createElement("span", "", "card-header-element");
        $(variableNameCardHeaderDOM).html(inputCardTitle);

        let endTab = createElement("div", "", "card-header-end-tab");
        let lineCardHeaderDOM = createElement("span", "", "card-header-element-bold");
        $(lineCardHeaderDOM).html(inputCardComment);

        // Setup minimize button
        let minimizeCardHeaderDOM = createElement("i", "", "fa-light fa-square-minus toggle-btn");
        $(minimizeCardHeaderDOM).click(()=>{
            let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
            if ($(parentCard).attr("minimized") == "true") {
                let originalHeight = $(parentCard).attr('original-height');
                $(parentCard).css("height", originalHeight + 'px');
                $(parentCard).attr("minimized", "false");
                $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                $(minimizeCardHeaderDOM).css("color", "red");
            } else {
                $(parentCard).attr('minimized', 'true');
                $(parentCard).attr('original-height', $(parentCard).height() + 12);
                $(parentCard).css("height", "30px");
                $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                $(minimizeCardHeaderDOM).css("color", "green");
            }
        });

        // Add elements to header
        endTab.appendChild(minimizeCardHeaderDOM);
        endTab.appendChild(variableNameCardHeaderDOM);

        cardHeaderDOM.appendChild(endTab);
        cardHeaderDOM.appendChild(lineCardHeaderDOM);

        // Add card component to card
        inputCardDOM.appendChild(inputCardComponentDOM);

        let hoveredInputCard = qs('.input-card-hover');
        if(hoveredInputCard) {
            hoveredInputCard.classList.remove('input-card-hover');
        }

        return inputCardDOM;
    }

    /* Create Input DOM Elements */
    function createInputText() {
        let input = createElement('input', '', 'form-control');
        input.setAttribute('type', 'text');
        input.setAttribute('placeholder', 'Input');
        input.setAttribute('aria-label', 'Input');
        return input;
    }


    /* Create Component Type Specific Input Cards */

    function createInputTextCard(inputCardTitle, inputCardComment) {
        let inputElement = createInputText();
        let inputCard = createInputCard("Input: " + inputCardTitle, inputCardComment, inputElement);
        inputCard.appendChild(createInputSubmitButton());
        return inputCard;
    }

    /* Create Input Submit Button */
    function createInputSubmitButton() {
        let submitButton = createElement('button', 'submit-btn', 'btn btn-primary');
        submitButton.innerHTML = 'Submit';
        return submitButton;
    }

    // Update input
    function createInput(line, name, comment){

        // Go to line
        editor.gotoLine(parseInt(line));

        // Create card
        let inputCardDOM = createInputTextCard(name, line);
        $(inputCardDOM).attr('line', line);

        // Link card to line
        $(inputCardDOM).click(()=>{
            editor.gotoLine(line);
        });

        // Add to DOM and scroll
        qs("#outputs-list").appendChild(inputCardDOM);
        qs("#outputs-list").scrollTop = $("#outputs-list").height();
    }

    function hideInput() {
        $(qs("#submit-btn").parentElement.children[1]).prop('readonly', 'true');
        $(qs("#submit-btn").parentElement).css("height", "auto");
        $("#submit-btn").remove();
    }

    // Outputs
    function createOutputComponentDOM(in_componentType, outputValue, parentElementSelector, startTop=false) {

        // Store component type
        let componentType = in_componentType;

        // Convert type
        if(componentType == "table") {
            outputValue = JSON.parse(outputValue);
        } else if (componentType == "graph") {
            componentType = "image";
        }

        // Create output element
        let component = createComponentFromType(componentType, componentCounter);        
        let componentState = defaultComponentStates[componentType];

        // Set id and load
        componentState['id'] = "#component" + componentCounter++
        component.loadState(componentState);

        // Customize CSS
        $(component.getId()).css("position", "static");
        $(component.getId()).css("width", "95%");
        if(componentType == "card") {
            $(component.getId()).css("height", "auto");
            $(component.getId()).css("min-height", "30px");
            $(component.getId()).css("resize", "vertical");
            $(component.getId()).css("overflow", "hidden");
        } else if (in_componentType == "graph") {
            const aspectRatio = 8 / 3;
            $(component.getId()).css("height", "200px");
            $(component.getId()).css("flex-grow", "1");
        }
        componentY += 10;

        // Move to output section
        let oldOutput = qs(component.getId());
        oldOutput.remove();
        qs(parentElementSelector).appendChild(oldOutput);
        let outputsList = qs(parentElementSelector).parentElement;
        $(outputsList).scrollTop($(outputsList).height());

        // Update with value
        component.updateValue(outputValue);

        // Make final udpates
        if(componentType == "table") {
            component.removeHeader();
            let numberOfRows = qsa(component.getId() + " tbody tr").length;
            let height = Math.min(40 * numberOfRows + 10, 80);
            $(component.getId() + " table").css("height", height + "px");
            $(component.getId()).css("height", "auto");
            if ($(component.getId()).height() > 160) {
                $(component.getId()).css("height", "160px");
            }
        } else if (componentType == "image") {
            $(component.getId()).css('background-color', 'rgb(254, 254, 254)');
        }

        // Zoom when right click
        if (componentType == "card") {


            $(component.getId()).on('contextmenu', function(e) {

                // Ensure zoom doesnt exist
                if (qs("#zoom") != null) return;

                // Get DOM and aspect
                let componentDOM = this;
                let componentDOMAspectRatio = $(componentDOM).width() / $(componentDOM).height();

                // Clone DOM
                let copyCard = componentDOM.cloneNode(true);

                // Create Zoom Menu
                let zoomMenu = createElement('div', 'zoom', '');
                console.log($(document).width() / 2);
                $(zoomMenu).css("position", "absolute");
                $(zoomMenu).css("width", "40" + "vw");
                $(zoomMenu).css("height", "30vh");
                $(zoomMenu).css("position", "absolute");               
                $(zoomMenu).css("z-index", "100000");

                // Update clone
                $(copyCard).attr('id', 'zoom-card');
                $(copyCard).css("height", "100%");
                $(copyCard).css("display", "flex");               
                $(copyCard).css("flex-direction", "column");               
                $(copyCard).css("justify-content", "start");
                $(copyCard).css("align-items", "center");

                // Add DOM to Zoom
                zoomMenu.appendChild(copyCard);
                qs("body").appendChild(zoomMenu);
                $(zoomMenu).css("top", ($(document).height() / 2 - $(zoomMenu).height() / 2) + "px");
                $(zoomMenu).css("left", ($(document).width() / 2 - $(zoomMenu).width() / 2) + "px");

                // Custom
                if ($(copyCard).attr('type') == 'table') {
                    $('#zoom-card .component-table').css("margin-top", "10px");
                    $('#zoom-card .component-table').css("height", "calc(100% - 10px)");

                    console.log("table");
                }              
            });
        }
    
        return qs(component.getId());
    }

    function setupOutputComponentDOMCard(component) {
        $("#" + component.id).css("margin-top", "10px");
        $("#" + component.id).css("padding", "10px");
        $("#" + component.id).css("display", "flex");
        $("#" + component.id).css("flex-direction", "column");
    }

    function setupOutputComponentDOMHeading(component, name) {
        let heading  = qs("#" + component.id + " h1");
        console.log("#" + component.id + " h1");
        heading.innerHTML = name;
    }

    function createOutputComponent(outputLine, outputName, outputValue, outputComment, outputComponentType) {
        
        // Reset pos
        if(componentX == -1 && componentY == -1) {
            componentX = $("#outputs h3").offset().left;
            componentY = $("#outputs h3").offset().top + 30;
        }

        // Set line
        editor.gotoLine(outputLine);

        // Destroy old card if it exists
        if (qs("div[name='" + outputName + "']")) {
            qs("div[name='" + outputName + "']").remove();
        }

        // Create card or merge
        let outputCard;
        if (outputComponentType == "markdown" && qs("div[name=markdown-" + (outputLine - 1) + "]")) {
            outputCard = qs("div[name=markdown-" + (outputLine - 1) + "]");
        } else {

            // Create new card
            outputCard = createOutputComponentDOM("card", "output-card", "#outputs-list", true);
            $(outputCard).attr('name', outputName);
            $(outputCard).attr('type', outputComponentType);

             // Link card to line
            setupOutputComponentDOMCard(outputCard);
            $(outputCard).click(()=>{
                let previousOutputCardSelected = qs('.output-card-selected');
                if (previousOutputCardSelected) {
                    $(previousOutputCardSelected).removeClass('output-card-selected');
                }
                $(outputCard).addClass("output-card-selected");
                editor.gotoLine(outputLine);
            });
            $(outputCard).mouseenter(()=>{
                $(outputCard).addClass("output-card-hover");
            });
            $(outputCard).mouseleave(()=>{
                $(outputCard).removeClass("output-card-hover");
            });

            // Get line
            let lineEditorDOM = qsa(".ace_line")[outputLine - 1];
            $(lineEditorDOM).css("pointer-events", "default");
            $(lineEditorDOM).click((e)=> {
                e.preventDefault();
                console.log('click');
            });

           // Create card header
           let cardHeaderDOM = createElement("div", outputCard.id + "-card-header", "card-header-bar");
           qs("#" + outputCard.id).appendChild(cardHeaderDOM);

           // Create end tab
           let endTab = createElement("div", "", "card-header-end-tab");
           cardHeaderDOM.appendChild(endTab);

           // Create card header contents             
           let variableNameCardHeaderDOM = createElement("span", "", "card-header-element");
           let variableName = (outputName.trim().length > 0) ? "Variable: " + outputName : "Documentation";
           $(variableNameCardHeaderDOM).html(variableName);

           // Setup minimize button
           let minimizeCardHeaderDOM = createElement("i", "", "fa-light fa-square-minus toggle-btn");
           $(minimizeCardHeaderDOM).click(()=>{
               let parentCard = minimizeCardHeaderDOM.parentElement.parentElement.parentElement;
                if ($(parentCard).attr("minimized") == "true") {
                   let originalHeight = $(parentCard).attr('original-height');
                   $(parentCard).css("height", originalHeight + 'px');
                   $(parentCard).attr("minimized", "false");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).css("color", "red");
                } else {
                   $(parentCard).attr('minimized', 'true');
                   $(parentCard).attr('original-height', $(parentCard).height() + 12);
                   $(parentCard).css("height", "30px");
                   $(minimizeCardHeaderDOM).removeClass("fa-square-minus");
                   $(minimizeCardHeaderDOM).addClass("fa-square-plus");
                   $(minimizeCardHeaderDOM).css("color", "green");
                }
            });

           // Add elements to header
           endTab.appendChild(minimizeCardHeaderDOM);
           endTab.appendChild(variableNameCardHeaderDOM);
           
           // Create line number
           let lineCardHeaderDOM = createElement("span", "", "card-header-element-bold");
           $(lineCardHeaderDOM).html(outputLine);
           cardHeaderDOM.appendChild(lineCardHeaderDOM);
        }
        
        // Create card body
        let valueDOM;
        if (outputComponentType == "markdown") {

            // Set name
            $(outputCard).attr('name', outputComponentType + "-" + outputLine);

            // Primary header
            if (outputValue.trim()[0] == "#" && outputValue.trim()[1] != "#") {
                valueDOM = createOutputComponentDOM("heading", outputValue.substring(1), "#" + outputCard.id);
                $(valueDOM.firstChild).css("font-size", "1.8rem");             
            }

            // Secondary header
            else if (outputValue.trim()[0] == "#" && outputValue.trim()[1] == "#" && outputValue.trim()[2] != "#") {
                valueDOM = createOutputComponentDOM("heading", outputValue.substring(2), "#" + outputCard.id);
                $(valueDOM.firstChild).css("font-size", "1.4rem");             
            }

            // Third header
            else if (outputValue.trim()[0] == "#" && outputValue.trim()[1] == "#" && outputValue.trim()[2] == "#" && outputValue.trim()[3] != "#") {
                valueDOM = createOutputComponentDOM("heading", outputValue.substring(3), "#" + outputCard.id);
                $(valueDOM.firstChild).css("font-size", "1.2rem");             
            }

            // Main
            else {
                valueDOM = createOutputComponentDOM("heading", outputValue, "#" + outputCard.id);
                $(valueDOM.firstChild).css("font-size", "1rem");       
            }

            // Auto-adjust height
            $("#" + outputCard.id + " .component-element-header").css("height", "auto");
            $("#" + outputCard.id + " .component-element-header").css("user-select", "none");
            $("#" + outputCard.id + " .component-header").css("height", "auto");
            $("#" + outputCard.id + " .component-element").css("user-select", "none");
            $("#" + outputCard.id).css("height", "auto");
        } else {
            valueDOM = createOutputComponentDOM(outputComponentType, outputValue, "#" + outputCard.id);
            if (outputComponentType == "heading") {
                $("#" + outputCard.id + " h1").css("user-select", "none");
            }
        }
        componentY += 30;

        // Update scroll
        let outputsList = qs("#outputs-list");
        $(outputsList).scrollTop($(outputsList).height());
    }

    function createSubmitCallback() {
        $("#submit-btn").mousedown(function() {

            // Pipe contents home
            let input = $(".input-card input").val();
            let reply = {};
            reply["type"] = "submit";
            reply["content"] = input;
            console.log(JSON.stringify(reply));
            sendSocket(JSON.stringify(reply));

            // Unselect
            this.parentElement.classList.remove("input-card-selected");
            $(this.parentElement.id + " input").prop("disabled", true);

            // Unbind submit
            $("#submit-btn").unbind("click");
        });
    }

    // Process socket message
    function processSocketMessage(event) {
        const message = JSON.parse(event.data);
        if(message.type == "heartbeat") return;
        console.log(message);
        if (message.type != 'ping' && message.type != 'heartbeat') {
            if (message.type == "create" && message.element == 'input') {
                let line = message.line;
                let name = message.name;
                let comment = message.comment;
                createInput(line, name, comment);
                createSubmitCallback();
            } else if (message.type == "quit") {
                window.close();
            } else if (message.type == "hide" && message.element == "input") {
                hideInput();
            } else if (message.type == "create" && message.element == "output") {
                let outputLine = parseInt(message.line);
                let outputValue = message.value;
                let outputName = message.name;
                let outputComment = message.comment;
                let outputComponentType = message.componentType;
                createOutputComponent(outputLine, outputName, outputValue, outputComment, outputComponentType);
                let outputsList = qs("#outputs-list");
                $(outputsList).scrollTop(100000);
            } else if (message.type == "callback" && message.name == "submit-btn") {
                
            } else if (message.type == "init") {
                restarting = false;
                editor.setValue(message.state);                
                editor.gotoLine(1);
            }
        }
    }

    // Send via socket
    function sendSocket(outMessage){
        try {       
            if(exit && (ws.readyState == ws.CLOSED || ws.readyState == ws.CLOSING)) {
                window.close();
            }   
            ws.send(outMessage);
        } catch (error) {
            console.log("[Error sending message to server]", error)
        }
    }

    // Update cards
    function updateCards(){

        // Get tags from tag bar
        let tagsDOM = qs("#tag-bar tags");
        let tags = [];
        for (let i = 0; i < tagsDOM.children.length; i++) {
            let tagTitle = $(tagsDOM.children[i]).attr('title');
            if (tagTitle != undefined) {
                tags.push(tagTitle.toLowerCase());
            }
        }
        
        // Filter if all is not a tag
        if (tags.includes("all")) {
            console.log('has all');
            return;
        }
    }

    // Setup tab list
    function setupTabs() {
        var input = document.querySelector('input[name=tags]');
        $(input).change(()=> {
            updateCards();
        });
        new Tagify(input)
    }

    // Create editor
    function createEditor() {
        // Create editor
        editor = ace.edit("editor");
        editor.setOptions({
            autoScrollEditorIntoView: true,
            copyWithEmptySelection: true,
        });
        editor.setTheme("ace/theme/twilight");
        editor.session.setMode("ace/mode/python");
        editor.setReadOnly(true);  // false to make it editable
        let code = "";
        editor.setValue(code);
        editor.gotoLine(1);
        editor.getSession().setUseSoftTabs(true);
        document.getElementById('editor').style.fontSize='12px';
        editor.resize();
        editor.setOptions({
            fontSize: "12pt"
        });

        $(".ace_content").css("pointer-events","none");
        $(".ace_scroller").css("pointer-events","none");
        $(".ace_editor").css("pointer-events","none");
        $(".code-previewer").css("pointer-events","none");

    }

    // Remove zoom if exists
    function removeZoomIfExists(evt) {
        let zoom = qs("#zoom");
        if (zoom != null) {
            let zoomExtents = getElementBounds("#zoom");
            let cursorPos = {"x" : evt.clientX, "y" : evt.clientY};
            if (!testIntersection(cursorPos, zoomExtents)) {
                qs("#zoom").remove();
            }
        }
    }

    // Main Entry Point
    $(function() {

        // Create editor
        createEditor();

        // Setup tabs
        setupTabs();

        // Zoom responder
        $(document).click((evt)=>{
            removeZoomIfExists(evt);
        });

        // Initialize component spot
        componentX = -1;
        componentY = -1;

        // Initialize next button
        $("#next-btn").click(function() {
            let reply = {};
            reply["type"] = "next";
            sendSocket(JSON.stringify(reply));
        });
        
        $("#reload-btn").click(function() {
            let reply = {};
            reply["type"] = "reload";
            restarting = true;
            sendSocket(JSON.stringify(reply));
        });

        $("#exit-btn").click(function() {
            exit = true
            let reply = {};
            reply["type"] = "exit";
            sendSocket(JSON.stringify(reply));
        });


        // Setup socket
        console.log("Version 1.13");
        createSocket();
        setInterval(()=>{
            let pingMessage = {'type': 'ping', 'data' : 'ping'};
            sendSocket(JSON.stringify(pingMessage));
        }, 20);
    });

  })(jQuery);
  