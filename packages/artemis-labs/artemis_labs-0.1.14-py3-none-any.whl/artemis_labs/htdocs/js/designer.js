import { DropBox } from "./Components/drop_box.js";
import { SelectorBox } from "./Components/selector_box.js";
import { GroupBox } from "./Components/group_box.js";
import { PopupMenu } from "./Components/popup_menu.js";
import { testIntersection, getElementBounds} from "./Math/bounds.js";
import { createElement, qs, qsa, download } from "./Helpers/helper.js";
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
import {createComponentFromPlacement, getComponentSizeClass, createComponentFromType} from './Components/component_manager.js';



(function($) {
    'use strict';    
    
    // Store login info
    let username;
    let token;
    let appKey;

    // Store app info
    let appContent;
    let projectState;

    // Core Components
    let dropBox;    
    let selectorBox;
    let groupBox;
    let popupMenu;

    // Designer Page
    let designerPage = null;
    let designerPages = [];

    // Placing Component Status
    let placingComponent = false;

    // Canvas status
    let mouseOverCanvas = false;

    // Drag item
    let componentBeingPlaced = null;

    // Active component
    let activeComponent = null;

    // Popup component
    let popupComponent = null;

    // Page counter
    let pageCounter = 0;

    // Track if click originated from right or left panel
    let clickOriginatedFromPanel = false;

    // Disable selecting
    let selectingDisabled = false;

    // Cloning
    let cloning = false;

    // Grid color
    let gridColor = '#e4e4e4';


    // Grouping
    let groupingInitiated = false;
    let grouping = false;
    let groupingStart = null;
    let groupedComponents = [];
    let groupDragging = false;
    let groupDraggingLeft = 0;
    let groupDraggingTop = 0;

    // Panning
    let panMode = false;
    let dragAreaLeft = 0;
    let dragAreaTop = 0;
    let dragAreaOffsetLeft = 0;
    let dragAreaOffsetTop = 0;

    // Copied components
    let copiedComponents = [];
    let copyPositionStart = null;

    // Zooming
    let scale = 1.0;

    // Hide aligners
    function hideAligners() {
        $("#aligner-left").css("left", "-1000px");
        $("#aligner-right").css("left", "-1000px");
        $("#aligner-top").css("left", "-1000px");
        $("#aligner-bottom").css("left", "-1000px");
        $("#aligner-middle-horizontal").css("left", "-1000px");
        $("#aligner-middle-vertical").css("left", "-1000px");
    }

    // Show aligners
    function showAligners() {

        // Get component bounds
        let componentLeft = $(activeComponent.getId()).offset().left;
        let componentRight = $(activeComponent.getId()).offset().left + parseInt($(activeComponent.getId()).css('width'));
        let componentTop = $(activeComponent.getId()).offset().top;
        let componentBottom = $(activeComponent.getId()).offset().top + parseInt($(activeComponent.getId()).css('height'));
        let componentBounds = {
            left: componentLeft,
            right: componentRight,
            top: componentTop,
            bottom: componentBottom
        };

        // Check alignment
        let alignment = designerPage.checkAlignment(componentBounds, [activeComponent]);

        if ('left' in alignment) {
            const leftLine = alignment['left'];
            $("#aligner-left").css('left', leftLine.left + 'px');
            $("#aligner-left").css('top', leftLine.top + 'px');
            $("#aligner-left").height((leftLine.bottom - leftLine.top) + 'px');
        } else {
            $("#aligner-left").css('left', '-1000px');
        }
        if ('right' in alignment) {
            const rightLine = alignment['right'];
            $("#aligner-right").css('left', rightLine.left + 'px');
            $("#aligner-right").css('top', rightLine.top + 'px');
            $("#aligner-right").height((rightLine.bottom - rightLine.top) + 'px');
        } else {
            $("#aligner-right").css('left', '-1000px');
        }
        if ('top' in alignment) {
            const topLine = alignment['top'];
            $("#aligner-top").css('left', topLine.left + 'px');
            $("#aligner-top").css('top', topLine.top + 'px');
            $("#aligner-top").width((topLine.right - topLine.left) + 'px');
        } else {
            $("#aligner-top").css('left', '-10000px');
        }
        if ('bottom' in alignment) {
            const bottomLine = alignment['bottom'];
            $("#aligner-bottom").css('left', bottomLine.left + 'px');
            $("#aligner-bottom").css('top', bottomLine.top + 'px');
            $("#aligner-bottom").width((bottomLine.right - bottomLine.left) + 'px');
        } else {
            $("#aligner-bottom").css('left', '-1000px');
        }
        if ('middleHorizontal' in alignment) {
            const middleLine = alignment['middleHorizontal'];
            $("#aligner-middle-horizontal").css('left', middleLine.left + 'px');
            $("#aligner-middle-horizontal").css('top', middleLine.top + 'px');
            $("#aligner-middle-horizontal").height((middleLine.bottom- middleLine.top) + 'px');
        } else {
            $("#aligner-middle-horizontal").css('left', '-1000px');
        }

        if ('middleVertical' in alignment) {
            const middleLine = alignment['middleVertical'];
            $("#aligner-middle-vertical").css('left', middleLine.left + 'px');
            $("#aligner-middle-vertical").css('top', middleLine.top + 'px');
            $("#aligner-middle-vertical").width((middleLine.right - middleLine.left) + 'px');
        } else {
            $("#aligner-middle-vertical").css('left', '-1000px');
        }
    }
   
    function showAlignersGroup() {

        // Skip if nothing in group
        if(groupedComponents.length == 0) {
            return;
        }

        // Init group bounds
        let groupLeft = $(groupedComponents[0].getId()).offset().left;
        let groupRight = $(groupedComponents[0].getId()).offset().left + parseInt($(groupedComponents[0].getId()).css('width'));
        let groupTop = $(groupedComponents[0].getId()).offset().top;
        let groupBottom = $(groupedComponents[0].getId()).offset().top + parseInt($(groupedComponents[0].getId()).css('height'));

        // Get group bounds
        for(let i = 1; i < groupedComponents.length; i++) {
            let componentLeft = $(groupedComponents[i].getId()).offset().left;
            let componentRight = $(groupedComponents[i].getId()).offset().left + parseInt($(groupedComponents[i].getId()).css('width'));
            let componentTop = $(groupedComponents[i].getId()).offset().top;
            let componentBottom = $(groupedComponents[i].getId()).offset().top + parseInt($(groupedComponents[i].getId()).css('height'));

            if(componentLeft < groupLeft) {
                groupLeft = componentLeft;
            }
            if(componentRight > groupRight) {
                groupRight = componentRight;
            }
            if(componentTop < groupTop) {
                groupTop = componentTop;
            }
            if(componentBottom > groupBottom) {
                groupBottom = componentBottom;
            }
        }

        let groupBounds = {
            left: groupLeft,
            right: groupRight,
            top: groupTop,
            bottom: groupBottom
        };

        // Check alignment
        let alignment = designerPage.checkAlignment(groupBounds, groupedComponents);
        if ('left' in alignment) {
            const leftLine = alignment['left'];
            $("#aligner-left").css('left', leftLine.left + 'px');
            $("#aligner-left").css('top', leftLine.top + 'px');
            $("#aligner-left").height((leftLine.bottom - leftLine.top) + 'px');
        } else {
            $("#aligner-left").css('left', '-1000px');
        }
        if ('right' in alignment) {
            const rightLine = alignment['right'];
            $("#aligner-right").css('left', rightLine.left + 'px');
            $("#aligner-right").css('top', rightLine.top + 'px');
            $("#aligner-right").height((rightLine.bottom - rightLine.top) + 'px');
        } else {
            $("#aligner-right").css('left', '-1000px');
        }
        if ('top' in alignment) {
            const topLine = alignment['top'];
            $("#aligner-top").css('left', topLine.left + 'px');
            $("#aligner-top").css('top', topLine.top + 'px');
            $("#aligner-top").width((topLine.right - topLine.left) + 'px');
        } else {
            $("#aligner-top").css('left', '-10000px');
        }
        if ('bottom' in alignment) {
            const bottomLine = alignment['bottom'];
            $("#aligner-bottom").css('left', bottomLine.left + 'px');
            $("#aligner-bottom").css('top', bottomLine.top + 'px');
            $("#aligner-bottom").width((bottomLine.right - bottomLine.left) + 'px');
        } else {
            $("#aligner-bottom").css('left', '-1000px');
        }
        if ('middleHorizontal' in alignment) {
            const middleLine = alignment['middleHorizontal'];
            $("#aligner-middle-horizontal").css('left', middleLine.left + 'px');
            $("#aligner-middle-horizontal").css('top', middleLine.top + 'px');
            $("#aligner-middle-horizontal").height((middleLine.bottom- middleLine.top) + 'px');
        } else {
            $("#aligner-middle-horizontal").css('left', '-1000px');
        }

        if ('middleVertical' in alignment) {
            const middleLine = alignment['middleVertical'];
            $("#aligner-middle-vertical").css('left', middleLine.left + 'px');
            $("#aligner-middle-vertical").css('top', middleLine.top + 'px');
            $("#aligner-middle-vertical").width((middleLine.right - middleLine.left) + 'px');
        } else {
            $("#aligner-middle-vertical").css('left', '-1000px');
        }
    }

    function showAlignersDropbox() {

        // Get component bounds
        let componentLeft = $("#drop-box").offset().left;
        let componentRight = $("#drop-box").offset().left + parseInt($("#drop-box").css('width'));
        let componentTop = $("#drop-box").offset().top;
        let componentBottom = $("#drop-box").offset().top + parseInt($("#drop-box").css('height'));
        let componentBounds = {
            left: componentLeft,
            right: componentRight,
            top: componentTop,
            bottom: componentBottom
        };

        // Check alignment
        let alignment = designerPage.checkAlignment(componentBounds, [activeComponent]);

        if ('left' in alignment) {
            const leftLine = alignment['left'];
            $("#aligner-left").css('left', leftLine.left + 'px');
            $("#aligner-left").css('top', leftLine.top + 'px');
            $("#aligner-left").height((leftLine.bottom - leftLine.top) + 'px');
        } else {
            $("#aligner-left").css('left', '-1000px');
        }
        if ('right' in alignment) {
            const rightLine = alignment['right'];
            $("#aligner-right").css('left', rightLine.left + 'px');
            $("#aligner-right").css('top', rightLine.top + 'px');
            $("#aligner-right").height((rightLine.bottom - rightLine.top) + 'px');
        } else {
            $("#aligner-right").css('left', '-1000px');
        }
        if ('top' in alignment) {
            const topLine = alignment['top'];
            $("#aligner-top").css('left', topLine.left + 'px');
            $("#aligner-top").css('top', topLine.top + 'px');
            $("#aligner-top").width((topLine.right - topLine.left) + 'px');
        } else {
            $("#aligner-top").css('left', '-10000px');
        }
        if ('bottom' in alignment) {
            const bottomLine = alignment['bottom'];
            $("#aligner-bottom").css('left', bottomLine.left + 'px');
            $("#aligner-bottom").css('top', bottomLine.top + 'px');
            $("#aligner-bottom").width((bottomLine.right - bottomLine.left) + 'px');
        } else {
            $("#aligner-bottom").css('left', '-1000px');
        }
        if ('middleHorizontal' in alignment) {
            const middleLine = alignment['middleHorizontal'];
            $("#aligner-middle-horizontal").css('left', middleLine.left + 'px');
            $("#aligner-middle-horizontal").css('top', middleLine.top + 'px');
            $("#aligner-middle-horizontal").height((middleLine.bottom- middleLine.top) + 'px');
        } else {
            $("#aligner-middle-horizontal").css('left', '-1000px');
        }

        if ('middleVertical' in alignment) {
            const middleLine = alignment['middleVertical'];
            $("#aligner-middle-vertical").css('left', middleLine.left + 'px');
            $("#aligner-middle-vertical").css('top', middleLine.top + 'px');
            $("#aligner-middle-vertical").width((middleLine.right - middleLine.left) + 'px');
        } else {
            $("#aligner-middle-vertical").css('left', '-1000px');
        }
    }

    // Sanity check
    function checkSanityElementSizing() {
        let componets = qsa("div[data-type=component]");
        for (let i = 0; i < componets.length; i++) {
            let component = componets[i];
            if (parseInt($(component).css('width')) % 8 != 0 || parseInt($(component).css('height')) % 8 != 0) {
                // console.log("Component " + component.id + " has invalid size");
            }
        }
    }

    // Helper
    function disableActiveComponent() {
        if(activeComponent == null) return;
        console.log(clickOriginatedFromPanel);
        activeComponent.removeEditableContent();
        activeComponent = null;
        selectorBox.hide();
        switchToContentTab();
        $("#drag-area").css("background-image", "none");
    }

    // Create component
    function createComponent() {

        // Create component
        let component = createComponentFromPlacement(componentBeingPlaced, designerPage.getComponentCounter());
        component.bindSelectbox(selectorBox);
        if(designerPage.getMaxZIndex() == -1) {
            $(component.getId()).css("z-index", 1);
        } else {
            $(component.getId()).css("z-index", designerPage.getMaxZIndex() + 1);
        }

        // Store component
        designerPage.addComponent(component);
        designerPage.incrementComponentCounter();

        // Position component
        let componentPosition = dropBox.getPlacementPosition();
        component.position(componentPosition);

        // Add mouse down callback
        component.bindMouseDownCallback(function() {

            // Control click
            if(event.ctrlKey) {
                // Add to group if grouped
                for (let i = 0; i < groupedComponents.length; i++) {
                    if(groupedComponents[i] == component) {
                        groupedComponents.splice(i, 1);
                        $(component.getId()).removeClass("grouped");
                        break;
                    }
                }
                console.log(groupedComponents);
                return;
            }

             // Shift click
             if(event.shiftKey) {
                // Add to group if grouped
                if (groupedComponents.length > 0 && !$(component.getId()).hasClass("grouped")) {
                    groupedComponents.push(component);
                    $(component.getId()).addClass("grouped");
                }
                return;
            }

            // Ignore if in grouping mode
            if(grouping) {
                return;
            }

            // Check for group drag
            if (groupedComponents.length > 0) {
                console.log(qs(component.getId()));
                // check if classlist has grouped
                if(qs(component.getId()).classList.contains("grouped")) {
                    groupDragging = true;
                    $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");
                    groupDraggingLeft = 0;
                    groupDraggingTop = 0;
                }
                return;
            }
        });

        // Add left click callback
        component.bindClickCallback(function() {

        });

        // Add right click callback
        component.bindRightClickCallback(function(event) {
            const cursorPos = { "x" : event.clientX, "y" : event.clientY };
            popupComponent = component;
            popupMenu.show(groupedComponents.length);
            popupMenu.position(cursorPos);
        });
    }

    // Create component from state
    function createComponentFromState(state) {

        // Create component
        let component = createComponentFromType(state["type"], state["index"]);
        component.bindSelectbox(selectorBox);
        component.loadState(state);

        // Store component
        designerPage.addComponent(component);
        designerPage.incrementComponentCounter();

        // Add mouse down callback
        component.bindMouseDownCallback(function() {

            // Control click
            if(event.ctrlKey) {
                // Add to group if grouped
                for (let i = 0; i < groupedComponents.length; i++) {
                    if(groupedComponents[i] == component) {
                        groupedComponents.splice(i, 1);
                        $(component.getId()).removeClass("grouped");
                        break;
                    }
                }
                console.log(groupedComponents);
                return;
            }

             // Shift click
             if(event.shiftKey) {
                // Add to group if grouped
                if (groupedComponents.length > 0 && !$(component.getId()).hasClass("grouped")) {
                    groupedComponents.push(component);
                    $(component.getId()).addClass("grouped");
                }
                return;
            }

            // Ignore if in grouping mode
            if(grouping) {
                return;
            }

            // Check for group drag
            if (groupedComponents.length > 0) {
                if(qs(component.getId()).classList.contains("grouped")) {
                    groupDragging = true;
                    $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");
                }
                return;
            }
        });

        // Add left click callback
        component.bindClickCallback(function() {
       
        });

        // Add right click callback
        component.bindRightClickCallback(function(event) {
            const cursorPos = { "x" : event.clientX, "y" : event.clientY };
            popupComponent = component;
            popupMenu.show(groupedComponents.length);
            popupMenu.position(cursorPos);
        });

        return component;
    }

    // Show available components
    function updateAvailableComponents() {
        let search = $(".form-control").val();
        let components = qsa("[data-drag-type=component]");
        for (let i = 0; i < components.length; i++) {
            let component = components[i];
            let componentName = $(component).attr("data-search").toLowerCase();
            if (componentName.indexOf(search) > -1) {
                $(component).removeClass("hidden");
            } else {
                $(component).addClass("hidden");
            }
        }
    }

    // Switch to content tab
    function switchToContentTab() {
    }

    // Switch page
    function switchPage(newDesignerPage) {
        // Save old designer page
        if(designerPage != null) {
            designerPage.saveState();
            designerPage.remove();
        }

        // Hide components
        if (activeComponent) {
            activeComponent.removeEditableContent();
            activeComponent = null;
        }

        // Remove remaining components
        let components = qsa("div[data-type=component]");
        for (let i = 0; i < components.length; i++) {
            let component = components[i];
            $(component).remove();
        }

        dropBox.hide();
        selectorBox.hide();
        switchToContentTab();
        $("#drag-area").css("background-image", "none");
        popupMenu.hide();
        popupComponent = null;
        componentBeingPlaced = null;

        // Update designer page
        designerPage = newDesignerPage; 

        // Activate page link
        designerPage.activatePage();    

        // Update designer page
        let state = designerPage.loadState();
        console.log(state);
        let stateKeys = Object.keys(state);
        for (let i = 0; i < stateKeys.length; i++) {
            if(stateKeys[i].includes("#component")) {
                createComponentFromState(state[stateKeys[i]]);
            }
        }
    }

    // Load page without saving previous page
    function loadPage(newDesignerPage) {
       
        // Hide components
        if (activeComponent) {
            activeComponent.removeEditableContent();
            activeComponent = null;
        }
        let components = qsa("div[data-type=component]");
        for (let i = 0; i < components.length; i++) {
            let component = components[i];
            $(component).remove();
        }

        dropBox.hide();
        selectorBox.hide();
        switchToContentTab();
        $("#drag-area").css("background-image", "none");
        popupMenu.hide();
        popupComponent = null;
        componentBeingPlaced = null;

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

     // Launch delete page popup
     function launchDeletePagePopup(callback) {
        $("#delete-app-popup").removeClass("hidden");
        $("#screen-film").removeClass("hidden");
        $(".delete-app-popup-content button").click(function() {
            $("#delete-app-popup").addClass("hidden");
            $("#screen-film").addClass("hidden");
            $(".delete-app-popup-content button").unbind();
            callback();
        });
    }

    // Create page
    function createPage() {

        // Create designer page
        let newDesignerPage = new DesignerPage(
            pageCounter            
        );

        // Store page
        designerPages.push(newDesignerPage);

        // Bind click callback
        newDesignerPage.bindClickCallback(() => { 
            switchPage(newDesignerPage);
        });

        // Bind delete callback
        newDesignerPage.bindDeleteButtonCallback(() => {
            launchDeletePagePopup(() => {
                let pageIndex = newDesignerPage.getPageIndex();
                let pageLink = qs("#page-" + pageIndex);        
                $(pageLink).remove();
                designerPages.splice(pageIndex, 1);
                if(designerPage == newDesignerPage) {
                    if (designerPages.length > 0) {
                        loadPage(designerPages[0]);
                    } else {
                        let newPage = createPage();
                        loadPage(newPage);
                    }
                }
            });
        });

        // Increment page counter
        pageCounter++;

        // Return page
        return newDesignerPage;
    }

    // Get state of project
    function getState() {
        let state = {};
        if (designerPage != null) {
            designerPage.saveState();
        }
        for(let i = 0; i < designerPages.length; i++) {
            state[i] = designerPages[i].loadState();
        }
        return state;
    }

    // Setup editor
    function setupEditor() {
        
        // Add page if project state empty
        if (Object.keys(projectState).length == 0) {
            projectState["0"] = {};
        }

        // Update designer menu when resizing browser
        $(window).resize(function() {

            // Position drag area
            dragAreaLeft = Math.floor(($(window).width() - $("#drag-area").width()) / 2);
            dragAreaTop = Math.floor(($(window).height() - $("#drag-area").height()) / 2);
            $("#drag-area").css("left", dragAreaLeft + dragAreaOffsetLeft);
            $("#drag-area").css("top", dragAreaTop + dragAreaOffsetTop);

            // Update component positions
            designerPage.updateComponentPositions();

            // Update selector box
            if (activeComponent) {
                const pos =  $(activeComponent.getId()).position();
                const boundingRect = qs(activeComponent.getId()).getBoundingClientRect();
                selectorBox.position(
                    pos,
                    boundingRect
                );
            }               
        });

        // Create popup menu
        popupMenu = new PopupMenu(
            () => {console.log("No page selected"); }
        );

        // Create new page
        $("#new-file-btn").click(function() {
            createPage();
        });

        // X button on page search
        $(".clear-backspace").click(function() {
            $(".form-control").val("");
            updateAvailableComponents();
        });

        // Bind page dump
        $("#download-btn").click(function() {
            let appState = getState();
            let appStateText = JSON.stringify(appState);
            download(appStateText, "app.json", appStateText);
        });

        // Bind page save
        $("#save-btn").click(function() {
            let state = getState();
            appContent[appKey] = state;
            updateApps(username, token, appContent);
            alert("Saved");
        });

        // Bind apps nav buttons
        $("#nav-apps-button").attr("href", "main.html?username=" + username + "&token=" + token);
        $("#nav-logout-button").click(()=>{
            logoutAccount(username, token, ()=>{
                window.location.href = "login.html";
            });
        });
        
        // Bind popup menu
        popupMenu.bindDeleteButtonCallback(
            () => {                
                if(groupedComponents.length > 0 && qs(popupComponent.getId()).classList.contains("grouped")) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        designerPage.deleteComponent(groupedComponents[i].getId());
                        groupedComponents[i].remove();
                        groupedComponents[i] = null;
                    }
                    groupedComponents = [];
                    groupDragging = false;
                } else if (popupComponent != null) {
                    designerPage.deleteComponent(popupComponent.getId());
                    popupComponent.remove();
                    popupComponent = null;
                }
                activeComponent = null;
                popupMenu.hide();
                selectorBox.hide();
                switchToContentTab();
                $("#drag-area").css("background-image", "none");
            }
        );
        popupMenu.bindCopyButtonCallback(
            () => {
                copiedComponents = [];
                copyPositionStart = popupMenu.getPosition();
                if(groupedComponents.length > 0) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        copiedComponents.push(groupedComponents[i]);
                    }
                } else {
                    if (activeComponent != null) {
                        copiedComponents.push(activeComponent);
                    }
                }
                popupMenu.hide();
            }
        );
        popupMenu.bindPasteButtonCallback(
            () => {
                if(copiedComponents.length == 0) {
                    popupMenu.hide();
                    return
                }
                clickOriginatedFromPanel = true;
                if(copyPositionStart == null) return;
                let pastePosition = popupMenu.getPosition();
                let delta = {
                    x: parseInt(pastePosition.x) - parseInt(copyPositionStart.x),
                    y: parseInt(pastePosition.y) - parseInt(copyPositionStart.y)
                };

                // Empty group
                let singleComponent = copiedComponents.length == 1;
                for(let i = 0; i < groupedComponents.length; i++) {
                    $(groupedComponents[i].getId()).removeClass("grouped");
                }
                groupedComponents = [];

                // Create pasted components
                for(let i = 0; i < copiedComponents.length; i++) {
                    let state = copiedComponents[i].getState();
                    let newComponentIndex = designerPage.getComponentCounter();
                    state["id"] = "#component-" + newComponentIndex;
                    state["index"] = newComponentIndex;
                    designerPage.incrementComponentCounter();
                    let newComponent = createComponentFromState(state);
                    designerPage.setNewComponentToTop(newComponent);
                    newComponent.move(delta.x, delta.y);
                    
                    // Add to group if non-single
                    if(!singleComponent) {
                        groupedComponents.push(newComponent);
                        $(newComponent.getId()).addClass("grouped");
                    } else {

                        // Update active component
                        if (activeComponent) {
                            activeComponent.removeEditableContent();
                        }
                        activeComponent = newComponent;
                        activeComponent.addEditableContent();

                        // Prepare grid and screen
                        $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");
                        let alerts = qsa(".no-selected-element");
                        for(let i = 0; i < alerts.length; i++) {
                            $(alerts[i]).addClass("hidden");
                        }

                        // Switch selection
                        switchToContentTab();
                        selectorBox.show(activeComponent.canResizeHorizontally(), activeComponent.canResizeVertically());
                        const pos =  $(activeComponent.getId()).position();
                        const boundingRect = qs(activeComponent.getId()).getBoundingClientRect();
                        selectorBox.position(
                            pos,
                            boundingRect
                        );
                    }
                }

                popupMenu.hide();
            }
        );
        popupMenu.bindSendBackCallback(
            () => {                
                if(groupedComponents.length > 0) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        designerPage.lowerZIndex(groupedComponents[i]);
                    }
                } else if (activeComponent != null) {
                    designerPage.lowerZIndex(activeComponent);
                }
                popupMenu.hide();
            }
        );
        popupMenu.bindSendToBackCallback(
            () => {                
                if(groupedComponents.length > 0) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        designerPage.lowerAllZIndex(groupedComponents[i]);
                    }
                } else if (activeComponent != null) {
                    designerPage.lowerAllZIndex(activeComponent);
                }
                popupMenu.hide();
            }
        );
        popupMenu.bindBringForwardCallback(
            () => {
                if(groupedComponents.length > 0) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        designerPage.raiseZIndex(groupedComponents[i]);
                    }
                } else if (activeComponent != null) {
                    designerPage.raiseZIndex(activeComponent);
                }
                popupMenu.hide();
            }
        );
        popupMenu.bindBringToFrontCallback(
            () => {
                if(groupedComponents.length > 0) {
                    designerPage.raiseAllZIndexGroup(groupedComponents);
                } else if (activeComponent != null) {
                    designerPage.raiseAllZIndex(activeComponent);
                }
                popupMenu.hide();
            }
        );

        // Disable selecting text
        document.onselectstart = function() { return false; };

        // Create dropbox
        dropBox = new DropBox();

        // Create selector box
        selectorBox = new SelectorBox();

        // Create group box
        groupBox = new GroupBox();

        // Bind selector box on leave callback
        selectorBox.bindOnLeaveCallback(() => {
            activeComponent = null;
        });
        
        // Selector box expand callbacks
        selectorBox.bindCallbackContractUp((expansion)=> {
            if(activeComponent != null) {
                let status = activeComponent.contractUp(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackExpandUp((expansion)=> {
            if(activeComponent != null) {                
                let status = activeComponent.expandUp(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackContractLeft((expansion)=> {
            if(activeComponent != null) {                
                let status = activeComponent.contractLeft(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackExpandLeft((expansion)=> {
            if(activeComponent != null) {                
                let status = activeComponent.expandLeft(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackExpandRight((expansion)=> {
            if(activeComponent != null) {
                let status = activeComponent.expandRight(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackExpandDown((expansion)=> {
            if(activeComponent != null) {
                let status = activeComponent.expandDown(expansion);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackContractRight((contraction)=> {
            if(activeComponent != null) {
                let status = activeComponent.contractRight(contraction);
                showAligners();
                return status;
            }
            return false;
        });
        selectorBox.bindCallbackContractDown((contraction)=> {
            if(activeComponent != null) {
                let status = activeComponent.contractDown(contraction);
                showAligners();
                return status;
            }
            return false;
        });

        // Position drag area
        dragAreaLeft = Math.floor(($(window).width() - $("#drag-area").width()) / 2);
        dragAreaTop = Math.floor(($(window).height() - $("#drag-area").height()) / 2);
        $("#drag-area").css("left", dragAreaLeft);
        $("#drag-area").css("top", dragAreaTop);

        // Remove selected callback
        $("#drag-area").click((event)=> {

            // Hide selector box
            $("#selector-box").removeClass("selected");
            selectorBox.hide();
            switchToContentTab();
            $("#drag-area").css("background-image", "none");

            // Remove editable content
            if(activeComponent != null) {
                activeComponent.removeEditableContent();
                activeComponent = null;
            }

            // Unhide alert
            let alerts = qsa(".no-selected-element");
            for(let i = 0; i < alerts.length; i++) {
                $(alerts[i]).removeClass("hidden");
            }
        });

        // Bind drag callback for selector
        selectorBox.bindDragCallback((event, ui) => {
            $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");
            if (activeComponent) {

                // Get drag area position
                let dragAreaPosition = $("#drag-area").offset();

                // Compute relative position
                let relativePositionX = ui.position.left - dragAreaPosition.left;
                let relativePositionY = ui.position.top - dragAreaPosition.top;

                // Position element
                activeComponent.position({"x" : relativePositionX, "y" : relativePositionY});

                // Check alignments               
                showAligners();
            }
        });

        // Mouse down on components
        let components = qsa("li[data-drag-type=component]");
        components.forEach((el) => {
            $(el).mousedown((event)=> {

                // Set component being dragged
                componentBeingPlaced = event.target;
                if ($(componentBeingPlaced).is("span")) {
                    componentBeingPlaced = componentBeingPlaced.parentElement;
                }
                placingComponent = true;

                // Compute cursor position relative to drag area
                const dragAreaExtents = qs('#drag-area').getBoundingClientRect();               

                // Update drag box
                const cursorPos = { "x" : event.originalEvent.clientX, "y" : event.originalEvent.clientY };
                showAlignersDropbox();
                dropBox.position(cursorPos, dragAreaExtents);

                // Disable active component
                disableActiveComponent();

                // Configure dropbox to component
                let componentSizeClass = getComponentSizeClass(componentBeingPlaced);
                qs("#drop-box").classList = [];
                qs("#drop-box").classList.add(componentSizeClass);
                
                // Show dropbox
                dropBox.show();
            });            
        });

        // Mouse up anywhere on canvas
        $(document).mouseup((event)=> {

            // Hide aligners
            hideAligners();

            // Disable cloning
            if (cloning) {
                cloning = false;
            }

            // Check cloning
            if ($(event.target).attr('type') == "clone-button") {
                cloning = true;
                return;
            }

            // Ignore if we're interacting with context menu
            if ($(event.target).hasClass("popup-menu-item")) {
                return;
            }    

            // End placing component
            if(placingComponent) {
                const cursorPos = { "x" : event.originalEvent.clientX, "y" : event.originalEvent.clientY };
                const dragAreaBox = getElementBounds("#drag-area");
                if (testIntersection(cursorPos, dragAreaBox)) {
                    createComponent();
                }
                placingComponent = false;
                dropBox.hide();
            }            

            // Hide popup when clicking out
            if(event.originalEvent.button != 2) {

                // Check interesction with popup menu
                const cursorPos = { "x" : event.originalEvent.clientX, "y" : event.originalEvent.clientY };

                // Extents of popup menu
                let popupMenuExtents = popupMenu.getExtents();
                let cursorOverPopupMenu = testIntersection(cursorPos, popupMenuExtents);
                if (!cursorOverPopupMenu) {
                    popupComponent = null;
                    popupMenu.hide();
                }
            }

            // Handle panning
            if( event.originalEvent.button == 1 ) {
                event.preventDefault();
                $('body').css('cursor', 'default');
                $(document).css('cursor', 'default');
                panMode = false;
            }

            // Handle grouping
            if( event.originalEvent.button == 0 ) {
                if (grouping) {

                    // Do not group if it's too small
                    if (Math.abs(groupBox.getTopLeftCorner().left - groupBox.getBottomRightCorner().left) < 10 && Math.abs(groupBox.getTopLeftCorner().top - groupBox.getBottomRightCorner().top) < 10) {
                        groupingInitiated = false;
                        grouping = false;
                        groupingStart = null;
                        groupBox.hide();
                        return;
                    }

                    // Group components
                    groupedComponents = designerPage.findGroupedElements(groupBox.getTopLeftCorner(), groupBox.getBottomRightCorner());
                    for(let i = 0; i < groupedComponents.length; i++) {
                        qs(groupedComponents[i].getId()).classList.add("grouped");
                    }
                    groupingInitiated = false;
                    grouping = false;
                    groupingStart = null;
                    groupBox.hide();
                } else{
                    groupingInitiated = false;
                    groupDragging = false;                    
                }
            } else if (event.originalEvent.button == 2) {
                groupDragging = false;
            }          
        });

        // Allow grouping
        $(document).on("mousedown", function(e) {

            // Mark if click originated from panel
            if (e.clientX > $("#left-panel").offset().left || e.clientX < $("right-panel").offset().left + $("#right-panel").width()) {
                clickOriginatedFromPanel = true;
            }

            // Check for shift click
            if(e.shiftKey) {                

                // Check if we're trying to group components
                let clickStart = { "left" : e.clientX, "top" : e.clientY };
                let clickEnd = { "left" : e.clientX + 4, "top" : e.clientY + 4};
                let component = designerPage.findTopLayerElementInGroup(clickStart, clickEnd);
                
                // If we're trying to group a component which isnt' the active component
                if (component != activeComponent) {

                    // Group active component
                    if (activeComponent != null && !($(activeComponent.getId()).hasClass("grouped"))) {
                        groupedComponents.push(activeComponent);
                        $(activeComponent.getId()).addClass("grouped");
                    }

                    // Disable active component if there is one
                    if (activeComponent) {
                        selectorBox.hide();
                        switchToContentTab();
                        if(activeComponent != null) {
                            activeComponent.removeEditableContent();
                            activeComponent = null;
                        }
                    }

                    // Group component
                    if (component != null && $(component.getId()).attr('data-type') == "component" && !($(component.getId()).hasClass("grouped"))) {
                        groupedComponents.push(component);
                        $(component.getId()).addClass("grouped");
                    }
                }               
                return;
            }
            if (e.ctrlKey) return;

            // Allow grouping
            if( e.originalEvent.button == 0 ) {

                // Check if we're clicking on group
                const groupStartSample = { "left" : e.originalEvent.clientX, "top" : e.originalEvent.clientY };
                const groupEndSample = { "left" : groupStartSample.left + 4, "top" : groupStartSample.top + 4 };
                let groupedElements = designerPage.findGroupedElements(groupStartSample, groupEndSample);
                let clickingOnGroup = false;
                for (let i = 0; i < groupedElements.length; i++) {
                    if ($(groupedElements[i].getId()).hasClass("grouped")) {
                        clickingOnGroup = true;
                        break;
                    }
                }

                // Ungroup if we're clicking out
                if (!clickingOnGroup && groupedComponents.length > 0 && !groupDragging && !popupMenu.isVisible()) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        qs(groupedComponents[i].getId()).classList.remove("grouped");
                    }
                    groupedComponents = [];
                }

                // Start grouping
                if(!clickingOnGroup && !$(e.target).hasClass("popup-menu-item") && activeComponent == null && !panMode && !placingComponent && !groupDragging && e.originalEvent.clientX < parseInt($("#right-panel").css("left")) && e.originalEvent.clientX > parseInt($("#left-panel").css("left")) + parseInt($("#left-panel").width())) {
                    groupingInitiated = true;
                    groupingStart = { "left" : e.originalEvent.clientX, "top" : e.originalEvent.clientY };
                    groupBox.setGroupStart(groupingStart);
                } 
            }

            // Handle panning
            if( e.originalEvent.button == 1 ) {
                e.preventDefault();
                $(document).css('cursor', 'grab');
                $('body').css('cursor', 'grab');
                panMode = true;
            }
        });
      
        // Mouse move on canvas
        $(document).mousemove((event)=>{

            // Check for group dragging
            if(groupDragging) {

                // Move components
                groupDraggingLeft += event.originalEvent.movementX;
                groupDraggingTop += event.originalEvent.movementY;
                if(Math.abs(groupDraggingLeft) > 8) {
                    for (let i = 0; i < groupedComponents.length; i++) {
                        groupedComponents[i].move(groupDraggingLeft, 0);
                    }
                    groupDraggingLeft = 0;
                }
                if(Math.abs(groupDraggingTop) > 8) {
                    for (let i = 0; i < groupedComponents.length; i++) {
                        groupedComponents[i].move(0, groupDraggingTop);
                    }
                    groupDraggingTop = 0;
                }

                // Update aligners
                showAlignersGroup();
            }

            // Check for grouping
            if(groupingInitiated && !grouping) {
                grouping = true;
                groupBox.setGroupEnd({
                    "left" : event.originalEvent.clientX,
                    "top" : event.originalEvent.clientY
                });
                groupBox.show();
            }

            // Update grouping
            if (grouping) {
                groupBox.setGroupEnd({
                    "left" : event.originalEvent.clientX,
                    "top" : event.originalEvent.clientY
                });
            }

            // Get cursor pos
            const cursorPos = { "x" : event.originalEvent.clientX, "y" : event.originalEvent.clientY };

            // Detect mouse over canvas
            let canvasExtents = qs("#canvas").getBoundingClientRect();

            // Detect intersection
            mouseOverCanvas = testIntersection(cursorPos, canvasExtents);

            // Handle drag and drop stuff
            if (mouseOverCanvas && placingComponent) {

                // Update grid
                $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");

                // Compute cursor position relative to drag area
                const dragAreaExtents = qs('#drag-area').getBoundingClientRect();               

                // Update drag box
                showAlignersDropbox();
                dropBox.position(cursorPos, dragAreaExtents);

                // Disable active component
                disableActiveComponent();
            }
            
            // Hide drag box if not dragging or off canvas
            if ((!mouseOverCanvas || !placingComponent) && !selectorBox.isSelected() && !groupDragging) {
                $("#drag-area").css("background-image", "none");
            }

            // Pan mode
            if (panMode) {
                
                // Update drag area position
                dragAreaOffsetLeft += event.originalEvent.movementX;
                dragAreaOffsetTop += event.originalEvent.movementY;
                $("#drag-area").css("left", dragAreaLeft + dragAreaOffsetLeft);
                $("#drag-area").css("top", dragAreaTop + dragAreaOffsetTop);
        
                // Update component positions
                designerPage.updateComponentPositions();

                // Update selector box
                if (activeComponent) {
                    const pos =  $(activeComponent.getId()).position();
                    const boundingRect = qs(activeComponent.getId()).getBoundingClientRect();
                    selectorBox.position(
                        pos,
                        boundingRect
                    );
                }    
            }
        });     

        // Create pages
        let pageKeys = Object.keys(projectState);
        for(let i = 0; i < pageKeys.length; i++) {
            let pageKey = pageKeys[i];
            createPage();
            designerPages[i].setState(projectState[pageKey]);
        }

        // Delete button
        document.addEventListener('keydown', function(event) {
            const key = event.key; 

            // Deleting
            if (key === "Delete") {
                if(activeComponent) {
                    designerPage.deleteComponent(activeComponent.getId());
                    activeComponent.remove();
                    activeComponent = null;
                    popupComponent = null;
                    selectorBox.hide();
                    switchToContentTab();
                    $("#drag-area").css("background-image", "none");

                }
                if(groupedComponents.length > 0) {
                    for(let i = 0; i < groupedComponents.length; i++) {
                        designerPage.deleteComponent(groupedComponents[i].getId());
                        groupedComponents[i].remove();
                        groupedComponents[i] = null;
                    }
                    groupedComponents = [];
                    console.log('clear');
                    groupDragging = false;
                }
            }

            // Escape
            if (key === "Escape") {
                selectorBox.hide();
                switchToContentTab();
                if(activeComponent != null) {
                    activeComponent.removeEditableContent();
                    activeComponent = null;
                }
                for(let i = 0; i < groupedComponents.length; i++) {
                    qs(groupedComponents[i].getId()).classList.remove("grouped");
                }
                groupBox.hide();
                placingComponent = false;
                componentBeingPlaced = null;
                dropBox.hide();
                groupDragging = false;
                $("#drag-area").css("background-image", "none");
            }
        });


        // Set first page active
        designerPage = designerPages[0];
        designerPage.activatePage();
        loadPage(designerPage);

        // Set page property listeners
        $("#page-name input").on("keyup", function(e) {
            $("#page-" + designerPage.getPageIndex() + " span").text(e.target.value);
        });
        $("#page-width input").on("keyup", function(e) {
            $("#drag-area").css("width", e.target.value);
        });
        $("#page-height input").on("keyup", function(e) {
            $("#drag-area").css("height", e.target.value);
        });
        $("#page-background-color input").on("input", function(e) {
            let newColor = e.target.value;
            $("#drag-area").css("background-color", newColor);
        });
        $("#grid-color input").on("input", function(e) {
            gridColor = e.target.value;
            if ($("#drag-area").hasClass("grid")) {
                $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");
            }
        });

        // Right click 
        $("#selector-box").on("contextmenu", function(e) {
            if(activeComponent) {
                const cursorPos = { "x" : event.clientX, "y" : event.clientY };
                e.preventDefault();
                popupComponent = activeComponent;
                popupMenu.show(groupedComponents.length);
                popupMenu.position(cursorPos);
            }
        });
        $("#drag-area").on("contextmenu", function(e) {
            const cursorPos = { "x" : event.clientX, "y" : event.clientY };
            e.preventDefault();
            popupComponent = null;
            popupMenu.show(groupedComponents.length);
            popupMenu.position(cursorPos);
        });

        // Scan for clicks
        $(document).click((event)=> {

            // Skip if selectin disabled
            if (selectingDisabled) return;

            // Skip if shift click
            if(event.ctrlKey || event.shiftKey) {
                clickOriginatedFromPanel = false;
                return;
            }

            // Ignore if we're interacting with context menu
            if ($(event.target).hasClass("popup-menu-item")) {
                clickOriginatedFromPanel = false;
                return;
            }

            // Find top layer element under click
            let component = designerPage.findTopLayerElementInGroup(
                { "left" : parseInt(event.clientX), "top" : parseInt(event.clientY) },
                { "left" : parseInt(event.clientX) + 1, "top" : parseInt(event.clientY) + 1 }
            );

            const cursorPos = { "x" : event.clientX, "y" : event.clientY };
            let dragAreaBounds = {
                "left" : $("#left-panel").offset().left + $("#left-panel").width(),
                "top" : parseInt($("#drag-area").offset().top),
                "right" : $("#right-panel").offset().left,
                "bottom" : parseInt($("#drag-area").offset().top) + parseInt($("#drag-area").css("height"))
            };
            if (!clickOriginatedFromPanel && component == null && activeComponent != null && testIntersection(cursorPos, dragAreaBounds)) {
                activeComponent.removeEditableContent();
                activeComponent = null;
                selectorBox.hide();
                switchToContentTab();
                $("#drag-area").css("background-image", "none");
                clickOriginatedFromPanel = false;
                return;
            } else if (component == null) {
                clickOriginatedFromPanel = false;
                return;
            }
            clickOriginatedFromPanel = false;


            // Ignore if in grouping mode
            if(groupedComponents.length > 0) {
                return;
            }

            // Switch back to content tab if open
            switchToContentTab();

            // Show selection box
            selectorBox.show(component.canResizeHorizontally(), component.canResizeVertically());

            // Position selection box
            const pos =  $(component.getId()).position();
            const boundingRect = qs(component.getId()).getBoundingClientRect();
            selectorBox.position(
                pos,
                boundingRect
            );

            // Set active component
            if (activeComponent) {
                activeComponent.removeEditableContent();
            }

            activeComponent = component;     
            activeComponent.addEditableContent();

            // Enable grid
            $("#drag-area").css("background-image", "linear-gradient(to right, " + gridColor + ", 1px, transparent 1px), linear-gradient(to bottom, " + gridColor + ", 1px, transparent 1px)");

            // Update content to hide alert
            let alerts = qsa(".no-selected-element");
            for(let i = 0; i < alerts.length; i++) {
                $(alerts[i]).addClass("hidden");
            }
        });
            
        // Make page tree sortable
        $( ".page-tree" ).sortable();
    }

    // Main Entry Point
    $(function() {

        //Create parser
        //const iconPicker = new IconPicker();

        //Bind to the input
        //iconPicker.iconPicker(document.querySelector('.icon-picker-my'));

        // Get cookie username and token
        try {
            username = getURLArg(0);
            token = getURLArg(1);
            appKey = getURLArg(2);
        } catch(err) {            
            window.location.href = "login.html";
        }

        // Set app name
        $("#app-name-span").text(appKey);

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
            setupEditor();
        });       

        // Sanity checker
        setInterval(()=>{
            checkSanityElementSizing();
        }, 1000);

        // Docs button
        $("#documentation-btn").click(() => {
            window.open("https://artemis-labs.readme.io/docs/welcome");
        });
        $("#preview-btn").click(() => {
            let designerURL = window.location.href;
            let launchURL = designerURL.replace("editor.html", "launcher.html");
            launchURL += '&active-page=' + designerPage.getPageIndex();
            window.open(launchURL);
        });

        // Exit warning
        window.addEventListener("beforeunload", function (e) {
            var confirmationMessage = 'It looks like you have been editing something. '
                                    + 'If you leave before saving, your changes will be lost.';
        
            (e || window.event).returnValue = confirmationMessage; //Gecko + IE
            return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
        });
    });

  })(jQuery);
  