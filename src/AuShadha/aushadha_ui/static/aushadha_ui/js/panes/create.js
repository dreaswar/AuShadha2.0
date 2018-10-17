// The module loader for AuShadha scripts
define(['dojo/dom',
        'dojo/dom-construct',
        'dojo/dom-style',
        'dojo/on',
        'dojo/json',
        'dojo/_base/array',
        'dijit/registry',
        'dijit/layout/BorderContainer',
        'dojox/layout/ContentPane',
        'dijit/layout/TabContainer',
        'dijit/form/FilteringSelect',

        "dojo/parser",

        "dojox/grid/DataGrid",
        "dojo/store/JsonRest",
        "dojo/data/ObjectStore",
        "dojo/request",
        "dojo/json",

       "aushadha/main",
       "aushadha/grid/generic_grid_setup",
       "aushadha/grid/grid_structures",
       "aushadha/under_construction/pane_and_widget_creator",

       "dojo/ready",
       'dojo/domReady!'
    ],
    function (dom,
        domConstruct,
        domStyle,
        on,
        JSON,
        array,
        registry,
        BorderContainer,
        ContentPane,
        TabContainer,
        FilteringSelect,

        parser,
        DataGrid,
        JsonRest,
        ObjectStore,
        request,
        JSON,
       
        auMain,
        auGenericGridSetup,
        GRID_STRUCTURES,
        paneAndWidgetCreator,

        ready){


      var pane = {

        panes: [],

        constructor: function() {

              var appObj = window.INSTALLED_APPS ? window.INSTALLED_APPS: [];

<<<<<<< HEAD
              console.log( appObj );
=======
//               console.log( appObj );
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

              var centerMainPane = registry.byId('centerMainPane');
              var centerTopTabPane= registry.byId("centerTopTabPane");

              if ( !centerTopTabPane ) {

                if (! dom.byId('centerTopTabPane') ) {

                  domConstruct.create('div',
                                      {id:'centerTopTabPane'},
                                      'centerMainPane',0
                                     );

                }

                centerTopTabPane = new TabContainer({ tabPosition:'top',
                                                      tabStrip:true
                                                    },
                                                    'centerTopTabPane'
                                                   );

                centerMainPane.addChild( centerTopTabPane );
                centerTopTabPane.startup();

              }

              for ( var x=0; x < appObj.length; x++ ) {

                appPaneCreator( appObj[x] );
                console.log("Created " + appObj[x].app + " Pane");
              }

              if ( centerTopTabPane.hasChildren() ) {

                centerTopTabPane.selectChild( centerTopTabPane.getChildren()[0] );

              }

        },

        destroyPane: function(){
          for( var x = 0; x < pane.panes.length; x++ ) {
            registry.byId( pane.panes[x].domNode ).destroyRecursive();
          }
        }

      }

      function appPaneCreator( appObj ) {
<<<<<<< HEAD
          console.log(appObj);
	  
=======

>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
        var title = appObj.app;
        var url = appObj.url;
        var domId = appObj.app.replace(' ','_').toLowerCase();
        var uiSections = appObj.ui_sections;            

        var layoutSections = uiSections.layout;
        var appType = uiSections.app_type;

        var loadFirst = uiSections.load_first;
        var loadAfter = uiSections.load_after;

        var gridEnabled = uiSections.widgets.grid;
        var searchEnabled = uiSections.widgets.search;
        var treeEnabled = uiSections.widgets.tree;
        var summaryEnabled = uiSections.widgets.summary;

        var d = dom.byId(domId);
        var p = registry.byId(domId);

<<<<<<< HEAD
          console.log("Creating pane with domId: " + domId);
	  console.log("Is App a main module ? : " + appType);
	  console.log("Is App going to load first ? : " + loadFirst);
	  
=======
        console.log("Creating pane with domId: " + domId);
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

        // This Basically parses the json.pane from the AuShadha/apps/search/views's render_search_pane and creates a search UI with 
        // search forms, widgets etc..
        function runMainModulePaneCreator(){

<<<<<<< HEAD
          if ( loadFirst ){

             //if (title == 'Search' ){
=======
          if ( loadFirst == true ){

              if (title == 'Search' ){
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

                if ( uiSections.widgets.pane ){

                  request(uiSections.widgets.pane).then(
                    function(json){
                      var jsondata  = JSON.parse(json);
<<<<<<< HEAD
			paneAndWidgetCreator.constructor(jsondata.pane);
			console.log("CALLING PANE CONSTRUCTOR WITH JSON: ");
			console.log(jsondata);
			/*
			auMain.auEventBinders.headerPaneSearchWidget( jsondata.pane.url,'Search for:  '+ title);
                      if ( dom.byId('search_form') ){
                          auMain.auEventBinders.searchWidget( jsondata.pane.url,'Search for:  '+ title);
=======
                      paneAndWidgetCreator.constructor(jsondata.pane);
                      auMain.auEventBinders.headerPaneSearchWidget( searchEnabled,'Search for:  '+ title);
                      if ( dom.byId('search_form') ){
                        auMain.auEventBinders.searchWidget( searchEnabled,'Search for:  '+ title);
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
                      }
                      else{
                        alert("Dom is not ready for searching");
                      }
<<<<<<< HEAD
*/
=======
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
                    }
                  );

                }

<<<<<<< HEAD
              //}
=======
              }
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

          }

        }

        if ( appType == 'main_module' && loadFirst == true ){
          runMainModulePaneCreator();
        }

//         else if( appType == 'main_module' && loadFirst == false ){
//           runMainModulePaneCreator();
//         }

//         else if( appType == 'sub_module' ){
//           createSubModulePane( d,p,title,domId );
//         }

    }

    return pane.constructor ;

});
