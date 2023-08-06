function load_jsplumb_flowchart(){
    (function () {

        var listDiv = document.getElementById("list"),

            showConnectionInfo = function (s) {
                listDiv.innerHTML = s;
                listDiv.style.display = "block";
            },
            hideConnectionInfo = function () {
                listDiv.style.display = "none";
            },
            connections = [],
            updateConnections = function (conn, remove) {
                if (!remove) connections.push(conn);
                else {
                    var idx = -1;
                    for (var i = 0; i < connections.length; i++) {
                        if (connections[i] === conn) {
                            idx = i;
                            break;
                        }
                    }
                    if (idx !== -1) connections.splice(idx, 1);
                }
                if(connections.length > 0){
                    question_mapping = {}
                    jsplumb_connections = {}
                    for (var j = 0; j < connections.length; j++) {
                        s = connections[j].sourceId + "-" + connections[j].targetId;
                        var source = connections[j].sourceId
                        var target = connections[j].targetId
                        jsplumb_connections[source] = target
                        source = source.split("_")
                        var mapping = {}
                        var next_question = target
                        var source_question = source[0]
                        if(source.length > 1){
                            mapping[source[1]] = target
                        }
                        mapping['default'] = target

                        if(question_mapping[source_question] != undefined){
                            default_question = Object.keys(question_mapping[source_question][0])[0]
                            default_question = question_mapping[source_question][0][default_question]
                            mapping['default'] = default_question
                            question_mapping[source_question].push(mapping)
                        }else{
                            question_mapping[source_question] = [mapping]
                        }


                    }
                    console.log(jsplumb_connections)
                    console.log(question_mapping)
                }
                {% comment %} if (connections.length > 0) {
                    var s = "<span><strong>Connections</strong></span><br/><br/><table><tr><th>Source</th><th>Target</th></tr>";
                    for (var j = 0; j < connections.length; j++) {
                        s = s + "<tr><td>" + connections[j].sourceId + "</td><td>" + connections[j].targetId + "</td></tr>";
                    }
                    showConnectionInfo(s);
                } else
                    hideConnectionInfo(); {% endcomment %}


            };

        jsPlumbBrowserUI.ready(function () {

            var instance = window.j = jsPlumbBrowserUI.newInstance({
                dragOptions: { cursor: 'pointer', zIndex: 2000 },
                paintStyle: { stroke: '#666' },
                endpointHoverStyle: { fill: "orange" },
                hoverPaintStyle: { stroke: "orange" },
                endpointStyle: { width: 20, height: 16, stroke: '#666' },
                endpoint: "Blank",
                anchors: ["TopCenter", "TopCenter"],
                container: canvas,
                dropOptions:{activeClass:"dragActive", hoverClass:"dropHover" ,tolerance:"touch"},
                connectionOverlays: [{
                    type: "Arrow",
                    options: {
                      location: 1,
                      visible: false,
                      width: 15,
                      length: 15,
                      id: "ARROW",
                      events: {
                        click: function click() {
                          //alert("you clicked on the arrow overlay");
                        }
                      }
                    }
                  }],
            });

            // suspend drawing and initialise.
            instance.batch(function () {

                // bind to connection/connectionDetached events, and update the list of connections on screen.
                instance.bind("connection", function (info, originalEvent) {
                    updateConnections(info.connection);
                });
                instance.bind("connection:detach", function (info, originalEvent) {
                    updateConnections(info.connection, true);
                   // alert()
                });

                instance.bind("connection:move", function (info, originalEvent) {
                    //  only remove here, because a 'connection' event is also fired.
                    // in a future release of jsplumb this extra connection event will not
                    // be fired.
                    updateConnections(info.connection, true);
                });

                instance.bind("click", function (component, originalEvent) {
                    alert("click!")
                });

                // configure some drop options for use by all endpoints.
                var exampleDropOptions = {
                    tolerance: "touch",
                    hoverClass: "dropHover",
                    activeClass: "dragActive"
                };

                var color2 = "#67B22C";
                var exampleEndpointSource = {
                    endpoint: {type:"Dot", options:{ radius: 6 }},
                    anchor: "Right",
                    paintStyle: { fill: color2 },
                    source: true,
                    scope: "blue",
                    connectorStyle: { stroke: color2, strokeWidth: 3 },
                    connector: {type:"Flowchart", options:{stub: [40, 60],gap: 10,cornerRadius: 5,alwaysRespectStubs: true } },
                    maxConnections: 1,
                    target: false,
                    dropOptions: exampleDropOptions,
                    // beforeDrop: function (params) {
                    //     return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
                    // },
                    // beforeDetach: function (conn) {
                    //     return confirm("Detach connection?");
                    // },
                };
                var color2 = "#ccc";
                var exampleEndpointTarget = {
                    endpoint: {type:"Rectangle", options:{ radius: 6 , width:10}},
                    anchor: "Top",
                    paintStyle: { fill: color2 },
                    source: false,
                    scope: "blue",
                    connectorStyle: { stroke: color2, strokeWidth: 3 },
                    connector: {type:"Flowchart", options:{ stub: [40, 60],gap: 10,cornerRadius: 5,alwaysRespectStubs: true} },
                    maxConnections: 100,
                    target: true,
                    dropOptions: exampleDropOptions,

                    // beforeDrop: function (params) {
                    //     return confirm("Connect " + params.sourceId + " to " + params.targetId + "?");
                    // },
                    // beforeDetach: function (conn) {
                    //     return confirm("Detach connection?");
                    // },
                };
                $('.plumb-connector').each(function(){
                    var is_option = $(this).attr('data-option');
                    var is_no_option = $(this).attr('data-no-option');
                    uuid1 = $(this).attr('id')
                    var count = $('#'+uuid1+' .option').length
                    //console.log(count)
                    if(is_option == 1){
                        uuid1 = uuid1+"_1"
                        instance.addEndpoint(this, {uuid:uuid1}, exampleEndpointSource);
                        console.log(uuid1)
                    }else if(is_no_option == 0){
                        uuid2 = uuid1+"_1"
                        uuid3 = uuid1+"_2"
                        instance.addEndpoint(this, {uuid:uuid2}, exampleEndpointSource);
                        instance.addEndpoint(this, {uuid:uuid3}, exampleEndpointTarget);
                    }
                    else{
                        uuid1 = uuid1+"_2"
                        console.log(uuid1)
                        instance.addEndpoint(this, {uuid:uuid1}, exampleEndpointTarget);

                    }
                })
                
                {%if jsplumb_connections%}
                    {%for x in jsplumb_connections%}
                        var is_option = '{{x.source}}'.split('_')
                        console.log('{{x.source}}_{{x.target}}_'+is_option.length)
                        instance.connect({uuids:['{{x.source}}_1','{{x.target}}_2']});
                    {%endfor%}
                {%endif%}

                // setup some empty endpoints.  again note the use of the three-arg method to reuse all the parameters except the location
                // of the anchor (purely because we want to move the anchor around here; you could set it one time and forget about it though.)

                // setup some DynamicAnchors for use with the blue endpoints
                // and a function to set as the maxConnections callback.

                var hideLinks = document.querySelectorAll(".drag-drop-demo .hide");
                instance.on(hideLinks, "click", function (e) {
                    instance.toggleVisible(this.parentNode);
                    instance.consume(e);
                });

                var dragLinks = document.querySelectorAll(".drag-drop-demo .drag");
                instance.on(dragLinks, "click", function (e) {
                    var s = instance.toggleDraggable(this.parentNode);
                    this.innerHTML = (s ? 'disable dragging' : 'enable dragging');
                    instance.consume(e);
                });

                var detachLinks = document.querySelectorAll(".drag-drop-demo .detach");
                instance.on(detachLinks, "click", function (e) {
                    instance.deleteConnectionsForElement(this.parentNode);
                    instance.consume(e);
                });

                // instance.on(document.getElementById("clear"), "click", function (e) {
                //     instance.deleteEveryConnection();
                //     showConnectionInfo("");
                //     instance.consume(e);
                // });

            });

        });
    })();
}