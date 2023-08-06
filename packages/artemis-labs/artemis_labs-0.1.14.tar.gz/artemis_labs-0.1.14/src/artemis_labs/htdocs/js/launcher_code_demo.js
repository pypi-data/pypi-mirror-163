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

    // Fake events
    let fakeEventQueue = [];
    let fakeEventQueueCounter = 0;

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

        // Insert
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

        // Make glow
        if (component.getId() == "#component-0") {
            console.log('glow');
            $(component.getId()).addClass("glow");
        }

        // Customize CSS
        $(component.getId()).css("position", "static");
        $(component.getId()).css("width", "95%");
        if(componentType == "card") {
            $(component.getId()).css("height", "auto");
            $(component.getId()).css("min-height", "40px");
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
        } else if (componentType == "image") {
            $(component.getId()).css('background-color', 'rgb(254, 254, 254)');
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
            let minimizeCardHeaderDOM = createElement("i", "", "fa-light fa-square-minus toggle-btn");

            // Setup minimize button
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
                    $(parentCard).attr('original-height', $(parentCard).height() + 20 + 2);
                    $(parentCard).css("height", "40px");
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

            // Store input card
            let inputCard  = this.parentElement;

            // Pipe contents home
            let input = $(".input-card input").val();
            let reply = {};
            reply["type"] = "submit";
            reply["content"] = input;
            sendSocket(JSON.stringify(reply));

            // Unselect
            inputCard.classList.remove("input-card-selected");
            $(inputCard.id + " input").prop("disabled", true);

            // Unbind submit
            $("#submit-btn").unbind("click");
        });
    }

    // Process socket message
    function processSocketMessage(event) {
        const message = JSON.parse(event.data);
        if(message.type == "heartbeat") return;
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
        if (outMessage == undefined) return;
        let outDict = JSON.parse(outMessage);
        if (outDict['type'] == 'ping') return;
        if (fakeEventQueueCounter == fakeEventQueue.length) return;
        if (fakeEventQueue[fakeEventQueueCounter - 1] == undefined) {
            return;
        };
        let lastMessage = JSON.parse(fakeEventQueue[fakeEventQueueCounter - 1]['data']);
        if (lastMessage['element'] == 'input' && lastMessage['type'] != 'hide' && outDict['type'] != 'submit') return;      
        popFakeMessage();
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
        $(".ace_text-layer").css("pointer-events","none");

        

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

    // Pop fake message
    function popFakeMessage() {

        // Avoid over popping
        if (fakeEventQueueCounter == fakeEventQueue.length) return;

        // Manual
        console.log(fakeEventQueueCounter);
        if (fakeEventQueueCounter == 4) {
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        } else if (fakeEventQueueCounter == 6) {
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        } else if (fakeEventQueueCounter == 9) {
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        } else if (fakeEventQueueCounter == 11) {
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        } else if (fakeEventQueueCounter == 14) {
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            $("#next-btn").prop("disabled", true);
        }
        
      

        // Pop all
        while (true) {

            // Get and validate message
            let message = fakeEventQueue[fakeEventQueueCounter++];
            if (message == undefined) {
                return;
            }

            // Pop message and process
            processSocketMessage(message);

            // Return if all done
            if (fakeEventQueueCounter == fakeEventQueue.length) return;

            // Disable if next is not an immediate subsequent documentation message
            let messageData = JSON.parse(message['data']);
            let nextMessageData = JSON.parse(fakeEventQueue[fakeEventQueueCounter]['data']);
            if (messageData['componentType'] == 'markdown' && nextMessageData['componentType'] == 'markdown' && (messageData['line'] + 1) == nextMessageData['line']) {
                continue;
            }
            return;
        }
    }

    // Create fake messages
    function createFakeMessages() {

        // Create fake init
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "init", "state": "from time import sleep\nimport numpy as np\nimport matplotlib.pyplot as plt \n\n# @doc #Interactive Artemis Tutorial\n# @doc ### This interactive code example is controlled from comments on the right. Click on any card to see the comment that generated it.\n\n# @doc ### Use the Continue button at the bottom of the screen to step through the tutorial\n\n# @doc ### Step 1: Enter a value for variable m, and press the Submit button \n# @input number\nm = 13\n\n# @doc ### Step 2: You'll notice the output for m was automatically generated below.\n# @output heading \nm\n\n# @doc ###Step 3: Now, enter a numerical input for variable b, and press the Submit button\n# @input number\nb = 13\n\n# @doc ### Step 4: Now, we will visualize this data using the @output table comment.\n# @output table\ndata = np.array([[i for i in range(5)], [3.5 * i + 5.5 for i in range(5)]])\n\nfig = plt.figure()\nplt.plot([i for i in range(10)])\n\n# @doc ### Step 5: Now, we will display the plot of this linear data using the @output graph comment\n# @output graph\nfig\n\nwhile True:\n    sleep(0.1)\n" }), "type" : "message" });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 5, "name": "", "value": "#Welcome to Artemis", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 6, "name": "", "value": "### This interactive code example is controlled from comments on the right. Click on any card to see the comment that generated it.", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 8, "name": "", "value": "### Use the Continue button at the bottom of the screen to step through the tutorial", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 10, "name": "", "value": "### Step 1: Enter a value for variable m, and press the Submit button. We created this input using the @input comment", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( {'data' : JSON.stringify({ "type": "create", "element": "input", "line": 12, "name": "Variable m", "comment": "" })});
        fakeEventQueue.push( { 'data' : JSON.stringify({ "type": "hide", "element": "input" })});
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 14, "name": "", "value": "### Step 2: You'll notice the output for m was automatically generated below.", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 16, "name": "m", "value": 13, "componentType": "heading", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 18, "name": "", "value": "###Step 3: Now, enter a numerical input for variable b, and press the Submit button", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { 'data' : JSON.stringify({ "type": "create", "element": "input", "line": 20, "name": "Variable b", "comment": "" })});
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "hide", "element": "input" })});
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 22, "name": "", "value": "### Step 4: Now, we will visualize this data using the @output table comment.", "componentType": "markdown", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 24, "name": "data", "value": "[[0.0, 1.0, 2.0, 3.0, 4.0], [5.5, 9.0, 12.5, 16.0, 19.5]]", "componentType": "table", "comment": "" }) });
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 29, "name": "", "value": "### Step 5: Now, we will display the plot of this linear data using the @output graph comment", "componentType": "markdown", "comment": "" }) });
        let data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAhYAAAGdCAYAAABO2DpVAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8qNh9FAAAACXBIWXMAAA9hAAAPYQGoP6dpAAA3jklEQVR4nO3dd3iUdaL28e/MpIckQCChJECogRBSaAp2UVQsWEAInmM567vHDd0GushhVSJ2Iay7uvu6vkcSitg7oqKISkkhlBA6oSWEkkkhk2Tmef/YPZzVFSVhkmfK/bmu/OGQIffFJJmv85tMLIZhGIiIiIi4gdXsASIiIuI7FBYiIiLiNgoLERERcRuFhYiIiLiNwkJERETcRmEhIiIibqOwEBEREbdRWIiIiIjbBLT2B3S5XBw+fJiIiAgsFktrf3gRERFpBsMwqKqqokuXLlitZ39cotXD4vDhw8THx7f2hxURERE3KC0tJS4u7qx/3uphERERAfx9WGRkZGt/eBEREWkGu91OfHz8mfvxs2n1sPif44/IyEiFhYiIiJf5tacx6MmbIiIi4jYKCxEREXEbhYWIiIi4jcJCRERE3EZhISIiIm6jsBARERG3UViIiIiI2ygsRERExG0UFiIiIuI2CgsRERFxG4WFiIiIuI3CQkRERNxGYSEiIuIDDMPgv7/bxyNvF5m6o9V/u6mIiIi4l72ugVkrN/NR0VEArh3YiYv7dDRli8JCRETEi20+eIrMnDxKT5wm0Gbh4WsSuah3B9P2KCxERES8kGEYvPbtPrI+3k6D0yCuXSjZGemkxrc1dZfCQkRExMucqq3nwTc3s2pbGQDXJHViwW2DiAoNNHmZwkJERMSr5B04yZScfA6dOk2QzcqjY/rz7xd2x2KxmD0NUFiIiIh4BZfL4C9r9/D0JztodBl0jw5jcUY6A7tGmT3tRxQWIiIiHu5ETT0PrCjki+JyAK4f1JmsW5KJCDH/6OOnFBYiIiIebMO+E0zNzedIZR1BAVbm3jCAjGHdPObo46cUFiIiIh7I5TJ4ec1unl9VgtNl0LNDONkZ6QzoEmn2tF+ksBAREfEwFdUOZiwr4JudFQDcnNaVJ8YOJDzY8++2PX+hiIiIH/lu93GmLc2nvMpBSKCVP9w4kHFD4jz26OOnFBYiIiIewOkyyP5iFy+tLsFlQJ+YNiyelE7f2AizpzWJwkJERMRk5VV1TF9awLrdxwEYNziOeTclERbkfXfT3rdYRETEh6zdWcH0ZQVUVDsIC7LxxNiB3JIeZ/asZlNYiIiImKDR6eKl1TvJ/nIXhgGJnSLIzkind0wbs6edF4WFiIhIKztaWcfUpfms33sCgInDujH3hgGEBNpMXnb+FBYiIiKt6Ksd5cxcXsiJmnrCg2xk3TqIG1O6mD3LbRQWIiIiraDB6eK5z0r405rdAAzoHMniSekkdAg3eZl7KSxERERa2OFTp5mSm8+m/ScB+PcLu/PIdf194ujjpxQWIiIiLejzbWU88GYhp2obiAgOYMFtg7guubPZs1qMwkJERKQF1De6ePqTYv6ydi8Ag+KiyJ6YTrfoMJOXtSyFhYiIiJuVnqhlcm4+haWnALhnZAKzrk0kKMBq7rBWoLAQERFxo0+2HOWhNwux1zUSGRLAs+NSuDqpk9mzWo3CQkRExA0cjU6yPirmb+v2AZDWrS2LJqYR1863jz5+SmEhIiJynvYfr2FyTj5FhyoB+O0lPXlgdD8Cbb5/9PFTCgsREZHz8MHmw8xaWUS1o5F2YYE8Nz6FKxJjzZ5lGoWFiIhIM9Q1OHn8g20s+eEAAEN7tGPhxDQ6R4WavMxcCgsREZEm2nOsmsycfLYfsWOxwO8u68WMUX0J8MOjj59SWIiIiDTBO/mHeOTtImrrnUSHB/HC7alc0rej2bM8hsJCRETkHJyud/Jf721l2cZSAC7o2Z6XJqQRGxli8jLPorAQERH5FbvKq8hcks+OsiosFph6RR+mXtkHm9Vi9jSPo7AQERH5BW9uOsicd7ZwusFJx4hgXro9lRG9O5g9y2MpLERERH5GbX0jv39nC2/lHQLgot4deOH2VDpGBJu8zLMpLERERH6i+KidzCV57D5Wg9UCM6/qy32X9dbRxzlo0s/FOJ1O5syZQ0JCAqGhofTq1YvHH38cwzBaap+IiEirMQyDpesPcFP2t+w+VkNsZDC5917A5Cv0fIpz1aRHLBYsWMDLL7/M66+/TlJSEhs3buTuu+8mKiqKqVOnttRGERGRFlftaOTRt4t4t+AwAJf27cjz41OIbqOjj6ZoUlisW7eOm266iTFjxgDQo0cPcnNzWb9+fYuMExERaQ1bD1cyOSefvRU12KwWHhzdj/9zcU+sepSiyZp0FDJixAhWr15NSUkJAIWFhaxdu5Zrr732rNdxOBzY7fYfvYmIiHgCwzD47+/3c/Mf17G3ooYuUSEs/+0F/OelvRQVzdSkRyxmzZqF3W4nMTERm82G0+nkySefZNKkSWe9TlZWFvPmzTvvoSIiIu5kr2tg9soiPiw6AsCo/jE8c1sK7cKDTF7m3ZoUFsuXL2fJkiXk5OSQlJREQUEB06dPp0uXLtx5550/e53Zs2czc+bMM/9tt9uJj48/v9UiIiLnYfPBU0zOyefAiVoCrBZmXZvIf1yUgMWiRynOl8Vowo90xMfHM2vWLDIzM89c9sQTT/DGG29QXFx8Tn+H3W4nKiqKyspKIiMjm75YRESkmQzD4G/r9jH/o+00OA3i2oWSnZFOanxbs6d5vHO9/27SIxa1tbVYrT9+WobNZsPlcjVvpYiISCuprG3gwTcL+WxbGQCjk2J5+rYUokIDTV7mW5oUFjfccANPPvkk3bp1Iykpifz8fJ5//nnuueeeltonIiJy3vIPnGRyTj6HTp0myGbl0TH9+fcLu+voowU06SikqqqKOXPm8Pbbb1NeXk6XLl2YOHEijz32GEFB5/ZkFx2FiIhIa3G5DP66di8LPimm0WXQPTqM7InpJMdFmT3N65zr/XeTwsIdFBYiItIaTtbUc/+KQr4oLgdgzKDOZN2STGSIjj6ao0WeYyEiIuINNu47wZTcfI5U1hEUYOWx6wcwaXg3HX20AoWFiIj4DJfL4E9f7+a5z0pwugx6dggnOyOdAV30CHlrUViIiIhPqKh2MHN5IV+XHANgbGoXnrg5mTbBuqtrTfrXFhERr/f9nuNMzc2nvMpBSKCVeTcmMX5IvI4+TKCwEBERr+V0GSz+chcvfl6Cy4DeMW1YnJFOv04RZk/zWwoLERHxSuVVdcxYVsC3u44DcNvgOP5wUxJhQbprM5P+9UVExOt8u6uCaUsLqKh2EBpo44mxA7l1cJzZswSFhYiIeJFGp4uFq3ey6MtdGAb0i41g8aQ0esfo6MNTKCxERMQrlNnrmJKbz/q9JwCYOCyeuTckERJoM3mZ/DOFhYiIeLyvdpQzc3khJ2rqCQ+yMf+WZG5K7Wr2LPkZCgsREfFYjU4Xz60q4eWvdgMwoHMk2Rlp9OzYxuRlcjYKCxER8UiHT51mam4+G/efBODfLujOo2P66+jDwyksRETE46zeXsb9Kwo5VdtARHAAT906iDGDOps9S86BwkJERDxGfaOLZz4t5tVv9gKQ3DWK7Iw0ukeHm7xMzpXCQkREPELpiVqm5OZTUHoKgLtH9mDWtYkEB+jow5soLERExHSfbj3KgysKsdc1EhkSwDPjUhid1MnsWdIMCgsRETGNo9FJ1kfF/G3dPgBS49uyaGIa8e3DzB0mzaawEBERU+w/XsPknHyKDlUCcO/FCTw4OpGgAKvJy+R8KCxERKTVfbj5CLNWbqbK0UjbsECeG5fClf1jzZ4lbqCwEBGRVlPX4OSJD7fxxvcHABjSvR0LJ6bRpW2oycvEXRQWIiLSKvYcqyYzJ5/tR+wA/O6yXsy4qi+BNh19+BKFhYiItLh3Cw7xyFtF1NQ7aR8exAu3p3Jp345mz5IWoLAQEZEWc7reybz3t7J0QykAwxPas3BiGrGRISYvk5aisBARkRaxq7yKzCX57CirwmKBKVf0YeoVvQnQ0YdPU1iIiIjbvbnpIHPe2cLpBicd2gTz0oRURvbuYPYsaQUKCxERcZva+kbmvLOVlXkHARjZO5oXbk8lJkJHH/5CYSEiIm6x42gVv1uyid3HarBaYPqovmRe3hub1WL2NGlFCgsRETkvhmGwbEMpc9/biqPRRWxkMC9NSOOCntFmTxMTKCxERKTZqh2NPPp2Ee8WHAbgkr4deWF8CtFtgk1eJmZRWIiISLNsPVzJlJx89lTUYLNauP/qvvznJb2w6ujDryksRESkSQzD4I0fDvD4B9uob3TROSqERRPTGNKjvdnTxAMoLERE5JzZ6xqYvbKID4uOAHBlYgzPjkuhXXiQycvEUygsRETknGw+eIrJOfkcOFFLgNXCw9ck8puLE7BYdPQh/0thISIiv8gwDP62bh/zP9pOg9Oga9tQFmWkkd6tndnTxAMpLERE5Kwqaxt4aGUhn24tA+DqAbE8c1sKUWGBJi8TT6WwEBGRn5V/4CSTc/I5dOo0gTYLj1zXn7tG9NDRh/wihYWIiPyIYRj85Zu9LPikmEaXQbf2YWRnpDEorq3Z08QLKCxEROSMkzX1PLCikNXF5QCMSe5M1q3JRIbo6EPOjcJCREQA2LjvBFNy8zlSWUdQgJU51w/gjuHddPQhTaKwEBHxcy6XwZ++3s1zn5XgdBkkdAgnOyONpC5RZk8TL6SwEBHxY8erHcxcXsiakmMA3JTahSdvTqZNsO4epHn0mSMi4qe+33OcaUvzKbM7CA6wMu/GJG4fGq+jDzkvCgsRET/jdBks/nIXL35egsuAXh3DWTwpncROkWZPEx+gsBAR8SPlVXXMWFbAt7uOA3BrehyPj00iLEh3B+Ie+kwSEfET3+6qYNrSAiqqHYQG2nh87EBuGxxn9izxMQoLEREf53QZvPR5CYu+3IVhQL/YCLIz0ugTG2H2NPFBCgsRER9WZq9jam4+P+w9AcCEofHMvSGJ0CCbycvEVyksRER81JqSY8xYVsCJmnrCg2zMvyWZm1K7mj1LfJzCQkTExzQ6XTy3qoSXv9oNQP/OkSzOSKNnxzYmLxN/oLAQEfEhh0+dZmpuPhv3nwTgjgu68fsxAwgJ1NGHtA6FhYiIj/iiuIyZyws5VdtARHAAWbcmc/2gLmbPEj+jsBAR8XINThdPf1LMq9/sBSC5axTZGWl0jw43eZn4I4WFiIgXKz1Ry5TcfApKTwFw14gezL4ukeAAHX2IORQWIiJe6tOtR3lwRSH2ukYiQwJ4+rYUrhnYyexZ4ucUFiIiXsbR6CTro2L+tm4fACnxbcmemEZ8+zBzh4mgsBAR8Sr7j9cwOSefokOVANx7cQIPjk4kKMBq8jKRv1NYiIh4iQ83H2HWys1UORppGxbIs7elMGpArNmzRH5EYSEi4uHqGpw88eE23vj+AACDu7dj0cQ0urQNNXmZyL9SWIiIeLC9FTVkLslj2xE7APdd1ouZV/Ul0KajD/FMCgsREQ/1bsEhHnmriJp6J+3Dg3h+fAqX9Ysxe5bIL1JYiIh4mNP1Tua9v5WlG0oBGJbQnoUT0ugUFWLyMpFfp7AQEfEgu8qryFySz46yKiwWmHJ5b6Ze2YcAHX2Il1BYiIh4iDc3HWTOO1s43eCkQ5tgXrw9lYv6dDB7lkiTNDmBDx06xB133EF0dDShoaEkJyezcePGltgmIuIXausbuX95IQ+sKOR0g5MRvaL5aNpFigrxSk16xOLkyZOMHDmSyy+/nI8//piOHTuyc+dO2rVr11L7RER82o6jVWTm5LGrvBqrBaaP6kvm5b2xWS1mTxNpliaFxYIFC4iPj+e11147c1lCQoLbR4mI+DrDMFi+sZTH3t2Ko9FFTEQwL01I48Je0WZPEzkvTToKee+99xgyZAjjxo0jJiaGtLQ0Xn311V+8jsPhwG63/+hNRMSfVTsambGsgIdXFuFodHFJ3458NO1iRYX4hCaFxZ49e3j55Zfp06cPn376Kffddx9Tp07l9ddfP+t1srKyiIqKOvMWHx9/3qNFRLzVtsN2bly0lncKDmOzWnjomn787a6hdGgTbPY0EbewGIZhnOs7BwUFMWTIENatW3fmsqlTp7Jhwwa+++67n72Ow+HA4XCc+W+73U58fDyVlZVERkaex3QREe9hGAZLfjjAHz7YRn2ji85RISycmMbQHu3NniZyTux2O1FRUb96/92k51h07tyZAQMG/Oiy/v37s3LlyrNeJzg4mOBglbiI+C97XQOz3yriw81HALgiMYbnxqXQLjzI5GUi7teksBg5ciQ7duz40WUlJSV0797draNERHxF0cFKMnPyOHCilgCrhYevSeQ/LkrAqp/6EB/VpLCYMWMGI0aMYP78+YwfP57169fzyiuv8Morr7TUPhERr2QYBq+v28f8j4qpd7ro2jaURRlppHfTj+eLb2vScywAPvjgA2bPns3OnTtJSEhg5syZ3Hvvved8/XM9oxER8VaVtQ08tLKQT7eWAXD1gFieuS2FqLBAk5eJNN+53n83OSzOl8JCRHxZ/oGTTMnN5+DJ0wTaLDxyXX/uGtEDi0VHH+LdWuTJmyIi8vMMw+Cva/fy1MfFNLoMurUPIzsjjUFxbc2eJtKqFBYiIufpZE09D6woZHVxOQDXJXfiqVsHERmiow/xPwoLEZHzsGn/Cabk5HO4so6gACtzrh/AHcO76ehD/JbCQkSkGVwugz9/vYdnP9uB02WQ0CGc7Iw0krpEmT1NxFQKCxGRJjpe7WDm8kLWlBwD4MaULsy/JZk2wfqWKqKvAhGRJvhhz3GmLs2nzO4gOMDKvBuTuH1ovI4+RP5BYSEicg6cLoM/frmLFz4vwWVAr47hLJ6UTmIn/di8yD9TWIiI/IpjVQ5mLCtg7a4KAG5J78rjNw0kXEcfIv9CXxUiIr9g3a4Kpi4toKLaQWigjcfHDuS2wXFmzxLxWAoLEZGf4XQZvLR6J4u+2IlhQN/YNizOSKdPbITZ00Q8msJCROQnyux1TFuaz/d7TgAwYWg8c29IIjTIZvIyEc+nsBAR+SdflxxjxrICjtfUEx5kY/4tydyU2tXsWSJeQ2EhIgI0Ol08v6qEP361G4D+nSNZnJFGz45tTF4m4l0UFiLi945UnmZqbj4b9p0EYNLwbsy5fgAhgTr6EGkqhYWI+LUvisu4f3khJ2sbaBMcwFO3JnP9oC5mzxLxWgoLEfFLDU4Xz3y6g1e+3gNActcosjPS6B4dbvIyEe+msBARv3PwZC1TcvPJP3AKgLtG9GD2dYkEB+joQ+R8KSxExK98tvUoD6woxF7XSGRIAE/flsI1AzuZPUvEZygsRMQv1De6yPp4O699uw+AlPi2ZE9MI759mLnDRHyMwkJEfN6B47VMzs1j88FKAO69OIEHRycSFGA1eZmI71FYiIhP+6joCA+/uZkqRyNtwwJ59rYURg2INXuWiM9SWIiIT6prcPLkh9v57+/3AzC4ezsWTkyja9tQk5eJ+DaFhYj4nL0VNUzOyWPrYTsA913Wi5lX9SXQpqMPkZamsBARn/Je4WFmr9xMTb2T9uFBPD8+hcv6xZg9S8RvKCxExCfUNTiZ9/42ctcfAGBYQnsWTkijU1SIyctE/IvCQkS83q7yaibn5FF8tAqLBSZf3ptpV/YhQEcfIq1OYSEiXu2tvIP8/p0t1NY76dAmmBdvT+WiPh3MniXitxQWIuKVausbmfvuVlZsOgjAiF7RvDghlZgIHX2ImElhISJep6Ssiswleewsr8ZqgWlX9mXyFb2xWS1mTxPxewoLEfEahmGwYuNBHntvC3UNLmIignlpQhoX9oo2e5qI/IPCQkS8Qo2jkUffLuKdgsMAXNynAy/cnkqHNsEmLxORf6awEBGPt+2wnck5eeypqMFmtTDzqr7cd2kvrDr6EPE4CgsR8ViGYZCz/gDz3t9GfaOLzlEhLJyYxtAe7c2eJiJnobAQEY9UVdfA7LeK+GDzEQCuSIzh2XEptA8PMnmZiPwShYWIeJwthyrJzMlj//FaAqwWHrqmH7+5qKeOPkS8gMJCRDyGYRj8v+/28+SH26l3uujaNpRFGWmkd2tn9jQROUcKCxHxCJWnG3j4zc18svUoAFcNiOXZ21KICgs0eZmINIXCQkRMV1B6isk5eRw8eZpAm4XZ1/bn7pE9sFh09CHibRQWImIawzD469q9LPikmAanQXz7ULInppMS39bsaSLSTAoLETHFqdp6Hlixmc+3lwFwXXInnrp1EJEhOvoQ8WYKCxFpdZv2n2RKTh6HK+sIslmZc31/7rigu44+RHyAwkJEWo3LZfDKN3t45tMdOF0GPaLDyM5IZ2DXKLOniYibKCxEpFUcr3Zw/4pCvtpxDIAbU7ow/5Zk2gTr25CIL9FXtIi0uPV7TzAlN48yu4PgACv/dWMSE4bG6+hDxAcpLESkxbhcBn/8ahfPryrBZUDPjuEszkinf+dIs6eJSAtRWIhIizhW5WDm8gK+2VkBwC1pXXl87EDCdfQh4tP0FS4ibrduVwXTlhVwrMpBaKCNP9yUxLgh8WbPEpFWoLAQEbdxugwWrt7Jwi92YhjQN7YNizPS6RMbYfY0EWklCgsRcYtyex3Tlhbw3Z7jANw+JJ7/ujGJ0CCbyctEpDUpLETkvH2z8xgzlhVQUV1PWJCN+TcnMzatq9mzRMQECgsRabZGp4sXP9/J4q92YRiQ2CmCxZPS6dWxjdnTRMQkCgsRaZYjlaeZllvA+n0nAJg0vBtzrh9ASKCOPkT8mcJCRJrsy+JyZi4v4GRtA22CA8i6JZkbUrqYPUtEPIDCQkTOWYPTxbOf7uDPX+8BYGDXSLInptOjQ7jJy0TEUygsROScHDp1mik5eeQdOAXAXSN6MPu6RIIDdPQhIv9LYSEiv2rVtjIeWFFI5ekGIkICeOa2QVwzsLPZs0TEAyksROSs6htdPPVxMf/3270ApMRFkZ2RTnz7MJOXiYinUliIyM8qPVHL5Jw8Cg9WAvAfFyXw8DWJBAVYTV4mIp5MYSEi/+KTLUd48M3NVNU1EhUayLPjUrhqQKzZs0TECygsROSMugYnWR9t5/Xv9gOQ3q0tizLS6do21ORlIuItFBYiAsC+ihoyc/LYetgOwG8v7ckDV/cj0KajDxE5dwoLEeH9wsPMfquIakcj7cODeG58Cpf3izF7loh4IYWFiB+ra3Dyhw+2kfPDAQCG9WjPwolpdIoKMXmZiHgrhYWIn9p9rJrMJXkUH63CYoHJl/dm2pV9CNDRh4ich/P6DvLUU09hsViYPn26m+aISGt4O/8gNyxaS/HRKjq0CeL/3TOM+6/up6gQkfPW7EcsNmzYwJ///GcGDRrkzj0i0oJO1zuZ+94Wlm88CMCFPaN5aUIqMZE6+hAR92jW/55UV1czadIkXn31Vdq1a+fuTSLSAnaWVXFj9lqWbzyIxQLTR/Xhjd8MV1SIiFs1KywyMzMZM2YMo0aN+tX3dTgc2O32H72JSOsxDIPlG0u5IXstO8ur6RgRzJLfDGf6qL7YrBaz54mIj2nyUcjSpUvJy8tjw4YN5/T+WVlZzJs3r8nDROT81TgamfPOFt7KPwTAxX068MLtqXRoE2zyMhHxVU16xKK0tJRp06axZMkSQkLO7eHT2bNnU1lZeeattLS0WUNFpGm2H7FzQ/Za3so/hNUCD47ux+t3D1NUiEiLshiGYZzrO7/zzjvcfPPN2Gy2M5c5nU4sFgtWqxWHw/GjP/s5drudqKgoKisriYyMbP5yEflZhmGQu76Uee9vxdHoolNkCAsnpjEsob3Z00TEi53r/XeTjkKuvPJKioqKfnTZ3XffTWJiIg8//PCvRoWItKyqugYeeXsL7xceBuCyfh15fnwq7cODTF4mIv6iSWERERHBwIEDf3RZeHg40dHR/3K5iLSuLYcqmZyTx77jtdisFh4a3Y97L+6JVU/QFJFWpFfeFPFyhmHw39/v54kPtlPvdNG1bSgLJ6YxuLt+FFxEWt95h8VXX33lhhki0hyVpxuY/dZmPio6CsCo/rE8O24QbcN09CEi5tAjFiJeqrD0FJNz8yg9cZpAm4VZ1/bnnpE9sFh09CEi5lFYiHgZwzD4v9/u46mPt9PgNIhvH0r2xHRS4tuaPU1ERGEh4k1O1dbzwIrNfL69DIBrB3biqVsHERUaaPIyEZG/U1iIeIlN+08yNTefQ6dOE2Sz8vvr+/NvF3TX0YeIeBSFhYiHc7kMXv1mD898uoNGl0H36DAWZ6QzsGuU2dNERP6FwkLEg52oqef+5QV8ueMYANcP6kzWLclEhOjoQ0Q8k8JCxEOt33uCqbn5HLXXERxgZe4NSUwcFq+jDxHxaAoLEQ/jchm8vGY3z68qweky6NkxnMUZ6fTvrN+tIyKeT2Eh4kEqqh3MWFbANzsrALglrSuPjx1IeLC+VEXEO+i7lYiHWLe7gmlLCzhW5SAk0MofbhrIuMFxOvoQEa+isBAxmdNlsOiLnSxcvROXAX1i2rB4Ujp9YyPMniYi0mQKCxETldvrmL6sgHW7jwMwfkgc824cSGiQzeRlIiLNo7AQMck3O48xY1kBFdX1hAXZeGLsQG5JjzN7lojIeVFYiLSyRqeLFz/fyeKvdmEYkNgpguyMdHrHtDF7mojIeVNYiLSio5V1TM3NZ/2+EwBkDO/GY9cPICRQRx8i4hsUFiKt5Msd5dy/vJATNfW0CQ5g/i3J3JjSxexZIiJupbAQaWENThfPfraDP6/ZA0BSl0gWZ6TTo0O4yctERNxPYSHSgg6dOs2UnDzyDpwC4M4LuzP7uv46+hARn6WwEGkhq7aV8cCKQipPNxAREsDTtw7i2uTOZs8SEWlRCgsRN6tvdLHgk2L+unYvAClxUSyamE636DCTl4mItDyFhYgblZ6oZXJuPoWlpwC4Z2QCs65NJCjAau4wEZFWorAQcZNPthzhwTc3U1XXSFRoIM+OS+GqAbFmzxIRaVUKC5Hz5Gh0Mv/D7bz+3X4A0ru1ZeHENOLa6ehDRPyPwkLkPOyrqGFybh5bDtkB+O2lPXng6n4E2nT0ISL+SWEh0kzvFx5m9ltFVDsaaRcWyPPjU7k8McbsWSIiplJYiDRRXYOTP3ywjZwfDgAwtEc7Fk5Mo3NUqMnLRETMp7AQaYLdx6rJXJJH8dEqLBbIvKw300f1IUBHHyIigMJC5Jy9nX+QR9/eQm29k+jwIF6ckMrFfTqaPUtExKMoLER+xel6J3Pf28LyjQcBuLBnNC9NSCUmMsTkZSIinkdhIfILdpZVkZmTR0lZNRYLTLuyD1Ou6IPNajF7moiIR1JYiJzFio2lzHl3C3UNLjpGBPPShFRG9Opg9iwREY+msBD5iRpHI3Pe3cJbeYcAuLhPB54fn0rHiGCTl4mIeD6Fhcg/2X7EzuScPHYfq8Fqgfuv7sd9l/bCqqMPEZFzorAQAQzDIHd9KfPe34qj0UWnyBAWTkxjWEJ7s6eJiHgVhYX4vaq6Bh55ewvvFx4G4LJ+HXl+fCrtw4NMXiYi4n0UFuLXthyqZHJOHvuO12KzWnhodD/uvbinjj5ERJpJYSF+yTAM3vh+P49/sJ16p4suUSEsykhncPd2Zk8TEfFqCgvxO/a6Bmat3MxHRUcBGNU/lmfHDaJtmI4+RETOl8JC/Eph6Skm5+ZReuI0gTYLD1+TyH9clIDFoqMPERF3UFiIXzAMg9e+3UfWx9tpcBrEtQslOyOd1Pi2Zk8TEfEpCgvxeadq63nwzc2s2lYGwDVJnVhw2yCiQgNNXiYi4nsUFuLT8g6cZEpOPodOnSbIZuX31/fn3y7orqMPEZEWorAQn+RyGfxl7R6e/mQHjS6D7tFhLM5IZ2DXKLOniYj4NIWF+JwTNfU8sKKQL4rLAbh+UGeybkkmIkRHHyIiLU1hIT5lw74TTM3N50hlHUEBVv7rhiQmDovX0YeISCtRWIhPcLkMXl6zm+dXleB0GfTsEM7iSen07xxp9jQREb+isBCvV1HtYMayAr7ZWQHAzWldeWLsQMKD9ektItLa9J1XvNp3u48zbWk+5VUOQgKt/OHGgYwbEqejDxERkygsxCs5XQbZX+zipdUluAzoE9OGxZPS6RsbYfY0ERG/prAQr1NeVcf0pQWs230cgHGD45h3UxJhQfp0FhExm74Ti1dZu7OC6cvyqaiuJyzIxhNjB3JLepzZs0RE5B8UFuIVGp0uXlq9k+wvd2EYkNgpguyMdHrHtDF7moiI/BOFhXi8o5V1TF2az/q9JwCYOKwbc28YQEigzeRlIiLyUwoL8Whf7Shn5vJCTtTUEx5kI+vWQdyY0sXsWSIichYKC/FIDU4Xz31Wwp/W7AYgqUsk2RnpJHQIN3mZiIj8EoWFeJzDp04zJTefTftPAvDvF3bnkev66+hDRMQLKCzEo3y+rYwH3izkVG0DEcEBLLhtENcldzZ7loiInCOFhXiE+kYXT39SzF/W7gVgUFwU2RPT6RYdZvIyERFpCoWFmK70RC2Tc/MpLD0FwD0jE5h1bSJBAVZzh4mISJMpLMRUn2w5ykNvFmKvayQyJIBnx6VwdVIns2eJiEgzKSzEFI5GJ1kfFfO3dfsASOvWlkUT04hrp6MPERFvprCQVrf/eA2Tc/IpOlQJwG8v6ckDo/sRaNPRh4iIt1NYSKv6cPMRZq3cTJWjkXZhgTw3PoUrEmPNniUiIm6isJBWUdfg5IkPt/HG9wcAGNqjHQsnptE5KtTkZSIi4k5Neuw5KyuLoUOHEhERQUxMDGPHjmXHjh0ttU18xJ5j1dz8x3VnouJ3l/Ui994LFBUiIj6oSWGxZs0aMjMz+f7771m1ahUNDQ1cffXV1NTUtNQ+8XLvFhzihkVr2X7ETnR4EK/fM4yHrkkkQM+nEBHxSRbDMIzmXvnYsWPExMSwZs0aLrnkknO6jt1uJyoqisrKSiIjI5v7ocXDna53Mu/9rSzdUArABT3b89KENGIjQ0xeJiIizXGu99/n9RyLysq/P6u/ffv2Z30fh8OBw+H40TDxbbvKq8hcks+OsiosFph6RR+mXtkHm9Vi9jQREWlhzQ4Ll8vF9OnTGTlyJAMHDjzr+2VlZTFv3rzmfhjxMm9uOsicd7ZwusFJhzbBvDQhlZG9O5g9S0REWkmzj0Luu+8+Pv74Y9auXUtcXNxZ3+/nHrGIj4/XUYiPqa1v5PfvbOGtvEMAXNS7Ay/cnkrHiGCTl4mIiDu06FHI5MmT+eCDD/j6669/MSoAgoODCQ7WnYsvKz5qJ3NJHruP1WC1wMyr+nLfZb119CEi4oeaFBaGYTBlyhTefvttvvrqKxISElpql3gBwzBYtqGUue9txdHoIjYymIUT0hjeM9rsaSIiYpImhUVmZiY5OTm8++67REREcPToUQCioqIIDdVrEviTakcjj75dxLsFhwG4tG9Hnh+fQnQbPTolIuLPmvQcC4vl5x/afu2117jrrrvO6e/Qj5t6v62HK5mck8/eihpsVgsPXN2P317SE6uOPkREfFaLPMfiPF7yQnyAYRi88cMBHv9gG/WNLrpEhbAoI43B3c/+48YiIuJf9LtC5JzY6xqYvbKID4uOADCqfwzP3JZCu/Agk5eJiIgnUVjIr9p88BSTc/I5cKKWAKuFWdcm8h8XJZz1aExERPyXwkLOyjAM/rZuH/M/2k6D06Br21CyM9JI69bO7GkiIuKhFBbysyprG3jwzUI+21YGwOikWJ6+NYWosECTl4mIiCdTWMi/yD9wksk5+Rw6dZogm5VHrkvkzhE9dPQhIiK/SmEhZxiGwV++2cuCT4ppdBl0ax/G4ox0kuOizJ4mIiJeQmEhAJysqeeBFYWsLi4HYMygzmTdkkxkiI4+RETk3CkshI37TjAlN58jlXUEBVh57PoBTBreTUcfIiLSZAoLP+ZyGfzp690891kJTpdBzw7hZGekM6CLXhFVRESaR2HhpyqqHcxcXsjXJccAGJvahSduTqZNsD4lRESk+XQv4oe+33Ocqbn5lFc5CAm0Mu/GJMYPidfRh4iInDeFhR9xugwWf7mLFz8vwWVA75g2LM5Ip1+nCLOniYiIj1BY+InyqjpmLCvg213HAbhtcBx/uCmJsCB9CoiIiPvoXsUPfLurgmlLC6iodhAaaOOJsQO5dXCc2bNERMQHKSx8WKPTxcLVO1n05S4MA/rFRrB4Uhq9Y3T0ISIiLUNh4aPK7HVMyc1n/d4TAEwcFs/cG5IICbSZvExERHyZwsIHfbWjnJnLCzlRU094kI35tyRzU2pXs2eJiIgfUFj4kEani+dWlfDyV7sB6N85ksUZafTs2MbkZSIi4i8UFj7i8KnTTM3NZ+P+kwD82wXdeXRMfx19iIhIq1JY+IDV28u4f0Uhp2obiAgO4KlbBzFmUGezZ4mIiB9SWHix+kYXz3xazKvf7AUguWsU2RlpdI8ON3mZiIj4K4WFlyo9UcuU3HwKSk8BcNeIHsy+LpHgAB19iIiIeRQWXujTrUd5cEUh9rpGIkMCeGZcCqOTOpk9S0RERGHhTRyNTrI+KuZv6/YBkBrflkUT04hvH2buMBERkX9QWHiJ/cdrmJyTT9GhSgDuvTiBB0cnEhRgNXmZiIjI/1JYeIEPNx9h1srNVDkaaRsWyHPjUriyf6zZs0RERP6FwsKD1TU4eeLDbbzx/QEAhnRvx8KJaXRpG2ryMhERkZ+nsPBQe45Vk5mTz/YjdgB+d1kvZlzVl0Cbjj5ERMRzKSw80LsFh3jkrSJq6p20Dw/ihdtTubRvR7NniYiI/CqFhQc5Xe9k3vtbWbqhFIDhCe1ZODGN2MgQk5eJiIicG4WFh9hVXkXmknx2lFVhscCUy3sz9co+BOjoQ0REvIjCwgO8uekgc97ZwukGJx3aBPPi7alc1KeD2bNERESaTGFhotr6Rua8s5WVeQcBGNk7mhduTyUmQkcfIiLinRQWJtlxtIrfLdnE7mM1WC0wfVRfMi/vjc1qMXuaiIhIsyksWplhGCzbUMrc97biaHQRGxnMSxPSuKBntNnTREREzpvCohVVOxp59O0i3i04DMAlfTvywvgUotsEm7xMRETEPRQWrWTr4Uqm5OSzp6IGm9XC/Vf35T8v6YVVRx8iIuJDFBYtzDAM3vjhAI9/sI36Rhedo0JYNDGNIT3amz1NRETE7RQWLche18Dst4r4cPMRAK5MjOHZcSm0Cw8yeZmIiEjLUFi0kKKDlWTm5HHgRC0BVgsPX5PIby5OwGLR0YeIiPguhYWbGYbB6+v2Mf+jYuqdLrq2DWVRRhrp3dqZPU1ERKTFKSzcqLK2gYdWFvLp1jIArh4QyzO3pRAVFmjyMhERkdahsHCT/AMnmZyTz6FTpwm0WXjkuv7cNaKHjj5ERMSvKCzOk2EY/OWbvSz4pJhGl0G39mFkZ6QxKK6t2dNERERancLiPJysqeeBFYWsLi4HYExyZ7JuTSYyREcfIiLinxQWzbRx3wmm5uZzuLKOoAArc64fwB3Du+noQ0RE/JrCoolcLoM/fb2b5z4rwekySOgQTnZGGkldosyeJiIiYjqFRRMcr3Ywc3kha0qOAXBTaheevDmZNsH6ZxQREQGFxTn7Yc9xpi7Np8zuIDjAyh9uSmL8kHgdfYiIiPwThcWvcLoM/vjlLl74vASXAb06hvPHSYPp1ynC7GkiIiIeR2HxC8qr6pixrIBvdx0H4Nb0OB4fm0RYkP7ZREREfo7uIc/i210VTFtaQEW1g9BAG4+PHchtg+PMniUiIuLRFBY/4XQZvLR6J4u+2IlhQL/YCLIz0ugTq6MPERGRX6Ow+Cdl9jqm5ubzw94TAEwYGs/cG5IIDbKZvExERMQ7KCz+YU3JMWYuK+B4TT3hQTbm35LMTaldzZ4lIiLiVfw+LBqdLp5bVcLLX+0GoH/nSBZnpNGzYxuTl4mIiHgfvw6Lw6dOMzU3n437TwJwxwXd+P2YAYQE6uhDRESkOfw2LL4oLmPm8kJO1TYQERxA1q3JXD+oi9mzREREvJrfhUWD08Uzn+7gla/3AJDcNYrsjDS6R4ebvExERMT7+VVYHDxZy+ScfApKTwFw14gezL4ukeAAHX2IiIi4g9+Exadbj/LgikLsdY1EhgTwzLgURid1MnuWiIiIT/H5sHA0Onnq42Je+3YfAKnxbVk0MY349mHmDhMREfFBPh0WB47XkpmTR9GhSgDuvTiBB0cnEhRgNXmZiIiIb2rWPezixYvp0aMHISEhDB8+nPXr17t713n7qOgIYxZ+Q9GhStqGBfLXO4fw6JgBigoREZEW1OR72WXLljFz5kzmzp1LXl4eKSkpjB49mvLy8pbY12R1DU7mvLOF3y3Jo8rRyJDu7fho6sVc2T/W7GkiIiI+z2IYhtGUKwwfPpyhQ4eSnZ0NgMvlIj4+nilTpjBr1qxfvb7dbicqKorKykoiIyObt/os9lbUkLkkj21H7AD87rJezLiqL4E2PUohIiJyPs71/rtJz7Gor69n06ZNzJ49+8xlVquVUaNG8d133/3sdRwOBw6H40fDWsK7BYd45K0iauqdtA8P4oXbU7m0b8cW+VgiIiLy85r0v/IVFRU4nU5iY398rBAbG8vRo0d/9jpZWVlERUWdeYuPj2/+2rM4WlnHQ29upqbeyfCE9nw87WJFhYiIiAla/Ixg9uzZVFZWnnkrLS11+8foFBXCvBuTmHpFb5b8ZjixkSFu/xgiIiLy65p0FNKhQwdsNhtlZWU/urysrIxOnX7+xaaCg4MJDg5u/sJzNGFYtxb/GCIiIvLLmvSIRVBQEIMHD2b16tVnLnO5XKxevZoLL7zQ7eNERETEuzT5BbJmzpzJnXfeyZAhQxg2bBgvvvgiNTU13H333S2xT0RERLxIk8Pi9ttv59ixYzz22GMcPXqU1NRUPvnkk395QqeIiIj4nya/jsX5asnXsRAREZGWca7333rlKBEREXEbhYWIiIi4jcJCRERE3EZhISIiIm6jsBARERG3UViIiIiI2ygsRERExG0UFiIiIuI2CgsRERFxmya/pPf5+p8X+rTb7a39oUVERKSZ/ud++9desLvVw6KqqgqA+Pj41v7QIiIicp6qqqqIioo665+3+u8KcblcHD58mIiICCwWi9v+XrvdTnx8PKWlpfodJB5At4fn0W3iWXR7eBbdHr/OMAyqqqro0qULVuvZn0nR6o9YWK1W4uLiWuzvj4yM1CeFB9Ht4Xl0m3gW3R6eRbfHL/ulRyr+h568KSIiIm6jsBARERG38ZmwCA4OZu7cuQQHB5s9RdDt4Yl0m3gW3R6eRbeH+7T6kzdFRETEd/nMIxYiIiJiPoWFiIiIuI3CQkRERNxGYSEiIiJu4zNhsXjxYnr06EFISAjDhw9n/fr1Zk/yS1lZWQwdOpSIiAhiYmIYO3YsO3bsMHuW/MNTTz2FxWJh+vTpZk/xW4cOHeKOO+4gOjqa0NBQkpOT2bhxo9mz/JbT6WTOnDkkJCQQGhpKr169ePzxx3/192HI2flEWCxbtoyZM2cyd+5c8vLySElJYfTo0ZSXl5s9ze+sWbOGzMxMvv/+e1atWkVDQwNXX301NTU1Zk/zexs2bODPf/4zgwYNMnuK3zp58iQjR44kMDCQjz/+mG3btvHcc8/Rrl07s6f5rQULFvDyyy+TnZ3N9u3bWbBgAU8//TSLFi0ye5rX8okfNx0+fDhDhw4lOzsb+PvvI4mPj2fKlCnMmjXL5HX+7dixY8TExLBmzRouueQSs+f4rerqatLT0/njH//IE088QWpqKi+++KLZs/zOrFmz+Pbbb/nmm2/MniL/cP311xMbG8tf//rXM5fdeuuthIaG8sYbb5i4zHt5/SMW9fX1bNq0iVGjRp25zGq1MmrUKL777jsTlwlAZWUlAO3btzd5iX/LzMxkzJgxP/o6kdb33nvvMWTIEMaNG0dMTAxpaWm8+uqrZs/yayNGjGD16tWUlJQAUFhYyNq1a7n22mtNXua9Wv2XkLlbRUUFTqeT2NjYH10eGxtLcXGxSasE/v7I0fTp0xk5ciQDBw40e47fWrp0KXl5eWzYsMHsKX5vz549vPzyy8ycOZNHHnmEDRs2MHXqVIKCgrjzzjvNnueXZs2ahd1uJzExEZvNhtPp5Mknn2TSpElmT/NaXh8W4rkyMzPZsmULa9euNXuK3yotLWXatGmsWrWKkJAQs+f4PZfLxZAhQ5g/fz4AaWlpbNmyhT/96U8KC5MsX76cJUuWkJOTQ1JSEgUFBUyfPp0uXbroNmkmrw+LDh06YLPZKCsr+9HlZWVldOrUyaRVMnnyZD744AO+/vpr4uLizJ7jtzZt2kR5eTnp6elnLnM6nXz99ddkZ2fjcDiw2WwmLvQvnTt3ZsCAAT+6rH///qxcudKkRfLggw8ya9YsJkyYAEBycjL79+8nKytLYdFMXv8ci6CgIAYPHszq1avPXOZyuVi9ejUXXnihicv8k2EYTJ48mbfffpsvvviChIQEsyf5tSuvvJKioiIKCgrOvA0ZMoRJkyZRUFCgqGhlI0eO/Jcfvy4pKaF79+4mLZLa2lqs1h/fFdpsNlwul0mLvJ/XP2IBMHPmTO68806GDBnCsGHDePHFF6mpqeHuu+82e5rfyczMJCcnh3fffZeIiAiOHj0KQFRUFKGhoSav8z8RERH/8vyW8PBwoqOj9bwXE8yYMYMRI0Ywf/58xo8fz/r163nllVd45ZVXzJ7mt2644QaefPJJunXrRlJSEvn5+Tz//PPcc889Zk/zXoaPWLRokdGtWzcjKCjIGDZsmPH999+bPckvAT/79tprr5k9Tf7h0ksvNaZNm2b2DL/1/vvvGwMHDjSCg4ONxMRE45VXXjF7kl+z2+3GtGnTjG7duhkhISFGz549jUcffdRwOBxmT/NaPvE6FiIiIuIZvP45FiIiIuI5FBYiIiLiNgoLERERcRuFhYiIiLiNwkJERETcRmEhIiIibqOwEBEREbdRWIiIiIjbKCxERETEbRQWIiIi4jYKCxEREXEbhYWIiIi4zf8HL5o39yXz6cwAAAAASUVORK5CYII=";
        fakeEventQueue.push( { "data" : JSON.stringify({ "type": "create", "element": "output", "line": 30, "name": "fig", "value": data, "componentType": "graph", "comment": "" })});
    }

    // Main Entry Point
    $(function() {

        // Create fake messages
        createFakeMessages();

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

            // Clear panel
            let outputList = qs("#outputs-list");
            for (let i = outputList.childElementCount - 1; i >= 0; i--) {
                outputList.removeChild(outputList.children[i]);
            }

            // Reset fake event queue counter
            fakeEventQueueCounter = 0;
            
            // Fake init
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
            processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);

            // Re-enable continue
            $("#next-btn").removeAttr("disabled");
        });

        $("#exit-btn").click(function() {
           
        });


        // Setup socket
        console.log("Version 1.13");
        createSocket();
        setInterval(()=>{
            let pingMessage = {'type': 'ping', 'data' : 'ping'};
            sendSocket(JSON.stringify(pingMessage));
        }, 20);

        // Fake init
        processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
        processSocketMessage(fakeEventQueue[fakeEventQueueCounter++]);
    });

  })(jQuery);
  