(function($,window){
    var selectTreeId = '';
    var selectDistrictId = '';
    var zNodes = null;
    var log, className = "dark";
    var newCount = 1;
    var columnDefs;
    var columns;
    var setting;
    var treeSetting;
    var idStr;
    var OperationId;
    var selectTreeIdAdd="";
    var startOperation;// 点击运营资质类别的修改按钮时，弹出界面时运营资质类别文本的内容
    var expliant;// 点击运营资质类别的修改按钮时，弹出界面时说明文本的内容
    var vagueSearchlast = $("#userType").val();
    var overlay;
    mapMonitor = {
        init: function(){
            // map
            var extent = [-2000, -2000, 2000, 2000];
            var projection = new ol.proj.Projection({
                code: 'xkcd-image',
                units: 'pixels',
                extent: extent
              });
            var centerr = ol.extent.getCenter(extent);
        
            map = new ol.Map({
                // layers: [
                //   new ol.layer.Image({
                //     source: new ol.source.ImageStatic({
                //       attributions: '© <a href="http://xkcd.com/license.html">xkcd</a>',
                //       url: "{% static 'virvo/images/bg_layer.png' %}",
                //       projection: projection,
                //       imageExtent: extent
                //     })
                //   })
                // ],
                view: new ol.View({
                    projection: projection,
                    center: ol.extent.getCenter(extent),
                    // center:  new ol.proj.transform(center,"EPSG:4326","EPSG:3857"),
                    maxZoom : 1,
                    zoom: 1
                }),
                // controls: ol.control.defaults({ attribution: false }).extend([attribution]),
                interactions: ol.interaction.defaults({mouseWheelZoom:false}),
                target:"js-map"
            });

            var extent2 = map.getView().calculateExtent(map.getSize());
            console.log("extent2:",extent2);

            map.addLayer(new ol.layer.Image({
                    source: new ol.source.ImageStatic({
                      attributions: '© <a href="http://xkcd.com/license.html">xkcd</a>',
                      url: "/static/virvo/images/bg_layer.png",
                      projection: projection,
                      imageExtent: extent2
                    })
                  }));

            var jingkai = new ol.Feature({
                geometry:new ol.geom.Point([-300,2200]),
                name:'经济开发区',
                population: 4000,
                rainfall: 500
            });
            var chengxizhu = new ol.Feature({
                geometry:new ol.geom.Point([-1000,-800]),
                name:'城西主城区片区',
                population: 4000,
                rainfall: 500
            });
            var gucheng = new ol.Feature({
                geometry:new ol.geom.Point([400,-300]),
                name:'古城片区',
                population: 4000,
                rainfall: 500
            });
            var piyunlu = new ol.Feature({
                geometry:new ol.geom.Point([-150,-1650]),
                name:'披云路片区',
                population: 4000,
                rainfall: 500
            });
            var chengxitie = new ol.Feature({
                geometry:new ol.geom.Point([-2350,150]),
                name:'皖赣铁路以西片区',
                population: 4000,
                rainfall: 500
            });
            var chengxigong = new ol.Feature({
                geometry:new ol.geom.Point([-2300,-1550]),
                name:'城西工业区片区',
                population: 4000,
                rainfall: 500
            });
            // var libya = new ol.Feature(new ol.geom.Point([512,384]));
            // var niger = new ol.Feature(new ol.geom.Point(ol.proj.transform([114.39709, 22.67306],"EPSG:4326","EPSG:3857")));

            
            chengxizhu.setStyle(mapMonitor.createIconStyle('chengxizhu','城西主城区'));
            jingkai.setStyle(mapMonitor.createIconStyle('jingkai','经济开发区'));
            chengxitie.setStyle(mapMonitor.createIconStyle('chengxitie','城西皖赣铁路以西片区'));
            gucheng.setStyle(mapMonitor.createIconStyle('gucheng','古城区'));
            piyunlu.setStyle(mapMonitor.createIconStyle('piyunlu','披云路片区'));
            chengxigong.setStyle(mapMonitor.createIconStyle('chengxigong','城西工业区'));

            var vectorLayer = new ol.layer.Vector({
                source: new ol.source.Vector({
                    features: [chengxizhu, jingkai, gucheng,piyunlu,chengxitie,chengxigong]
                })
            });

            map.addLayer(vectorLayer);

            // overlay
            overlay = new ol.Overlay({
                element:document.getElementById('js-overlay'),
                positioning: 'bottom-left',
            });

            

            overlay.setMap(map);
            map.on(['pointermove', 'singleclick'], mapMonitor.moveonmapevent);
            
        },
        moveonmapevent:function(evt) {
            var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                overlay.setPosition(evt.coordinate);
                // overlay.getElement().innerHTML = feature.get('name');
                console.log(feature.get('text'));
                name = feature.get('name');
                
                return feature;
              });
              // console.log(feature);
              mapMonitor.rebuildoverlay(name);
              overlay.getElement().style.display = 'block';
              (feature) ? overlay.setPosition(feature.getGeometry().getCoordinates()) : overlay.setPosition(undefined);
              // overlay.getElement().style.display = feature ? 'block' : 'none';
              // document.body.style.cursor = feature ? 'pointer' : '';
        },
        createIconStyle:function(country,description) {
            return new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 46],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    // opacity: 0.75,
                    src: "/static/virvo/images/" + country + '.png'
                }),
                text: new ol.style.Text({
                        font: '20px Calibri,sans-serif',
                        fill: new ol.style.Fill({ color: '#000' }),
                        stroke: new ol.style.Stroke({
                        color: '#fff', width: 2
                    }),
                // get the text from the feature - `this` is ol.Feature
                // and show only under certain resolution
                text: description

                // text: map.getView().getZoom() > 12 ? this.get('description') : ''
              })
            })
        },
        rebuildoverlay:function(name){
            console.log('name:',name);
            $("#dma_name span").html(name);
            
            var data={"dma_name":name,'csrfmiddlewaretoken': '{{ csrf_token }}'};
            var url="/dmam/getdmamapusedata/";
            json_ajax("GET", url, "json", true,data,mapMonitor.updateoverlay);
        },
        updateoverlay:function(data){
            console.log('updateoverlay',data);
        },
        userTree : function(){
            // 初始化文件树
            treeSetting = {
                async : {
                    url : "/dmam/district/dmatree/",
                    type : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                    data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
                    otherParam : {  // 是否可选 Organization
                        "isOrg" : "1",
                        // "csrfmiddlewaretoken": "{{ csrf_token }}"
                    },
                    dataFilter: mapMonitor.ajaxDataFilter
                },
                view : {
                    // addHoverDom : mapMonitor.addHoverDom,
                    // removeHoverDom : mapMonitor.removeHoverDom,
                    selectedMulti : false,
                    nameIsHTML: true,
                    fontCss: setFontCss_ztree
                },
                edit : {
                    enable : true,
                    editNameSelectAll : true,
                    showRemoveBtn : false,//mapMonitor.showRemoveBtn,
                    showRenameBtn : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeDrag : mapMonitor.beforeDrag,
                    beforeEditName : mapMonitor.beforeEditName,
                    beforeRemove : mapMonitor.beforeRemove,
                    beforeRename : mapMonitor.beforeRename,
                    // onRemove : mapMonitor.onRemove,
                    onRename : mapMonitor.onRename,
                    onClick : mapMonitor.zTreeOnClick
                }
            };
            $.fn.zTree.init($("#treeDemo"), treeSetting, zNodes);
            var treeObj = $.fn.zTree.getZTreeObj('treeDemo');treeObj.expandAll(true);
           
        },

        beforeDrag: function(treeId, treeNodes){
            return false;
        },
        beforeEditName: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            return tg_confirmDialog(null,userGroupDeleteConfirm);
        },
        // 组织树预处理函数
        ajaxDataFilter: function(treeId, parentNode, responseData){
            var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
            if (responseData) {
                for (var i = 0; i < responseData.length; i++) {
                        responseData[i].open = true;
                }
            }
            return responseData;
        },
        beforeRemove: function(treeId, treeNode){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                    + treeNode.name);
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.selectNode(treeNode);
            var result;
            layer.confirm(userGroupDeleteConfirm, {
                title :'操作确认',
                icon : 3, // 问号图标
                btn: ['确认','取消'] // 按钮
            }, function(index){
                selectTreeIdAdd="";
                var nodes = zTree.getSelectedNodes();
                var preNode = nodes[0].getPreNode();
                var nextNode = nodes[0].getNextNode();
                var parentNode = nodes[0].getParentNode();
                $.ajax({
                    type: 'POST',
                    url: 'district/delete/',
                    data: {"pId": treeNode.id},
                    async:false,
                    dataType: 'json',
                    success: function (data) {
                        var flag=data.success;      
                        if(flag==false){
                            layer.msg(data.msg,{move:false})
                        }
                        if(flag==true){
                            $('#simpleQueryParam').val("");
                            selectTreeId = "";
                            selectDistrictId = "";
                            $.ajax({
                                type: 'POST',
                                url: 'district/dmatree/',
                                data: {"isOrg" : "1"},
                                async:false,
                                dataType: 'json',
                                success: function (data) {
                                    var data2 = JSON.stringify(data);
                                    var addData = JSON.parse(data2);             
                                    var nodeName;
                                    if(preNode != null){
                                        nodeName = preNode.name;
                                    }else if(nextNode != null){
                                        nodeName = nextNode.name;
                                    }else{
                                        nodeName = parentNode.name;
                                    };
                                    $.fn.zTree.init($("#treeDemo"), treeSetting, addData);  
                                    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
                                    var nodes = treeObj.getNodes();
                                    for(var j=0;j<nodes.length;j++){
                                         zTree.expandNode(nodes[j], true, true, true);
                                    }
                                    // pengwl delete group and user refresh tabale
                                    myTable.requestData();
                                },      
                            });
                        }
                        layer.close(index,{move:false});
                    },
                    error: function () {
                        layer.msg(systemError, {move: false});
                    }
                });
            }, function(index){
                layer.close(index,{move:false});
            });
            return false;
        },
        onRemove: function(e, treeId, treeNode){
            selectTreeIdAdd="";
            mapMonitor.showLog("[ " + mapMonitor.getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
                + treeNode.name);
        },
        beforeRename: function(treeId, treeNode, newName, isCancel){
            className = (className === "dark" ? "" : "dark");
            mapMonitor.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapMonitor.getTime()
                    + " beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                    + (isCancel ? "</span>" : ""));
            if (newName.length == 0) {
                layer.msg(userNodeNameNull, {move: false});
                var zTree = $.fn.zTree.getZTreeObj("treeDemo");
                setTimeout(function() {
                    zTree.editName(treeNode)
                }, 10);
                return false;
            }
            return true;
        },
        onRename: function(e, treeId, treeNode, isCancel){
            mapMonitor.showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + mapMonitor.getTime()
                + " onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
                + (isCancel ? "</span>" : ""));
        },
        // 显示删除组织按钮
        showRemoveBtn: function(treeId, treeNode){
            return treeNode.children==undefined;
        },
        showRenameBtn: function(treeId, treeNode){
            return !treeNode.isLastNode;
        },
        showLog: function(str){
            if (!log)
                log = $("#log");
                log.append("<li class='"+className+"'>" + str + "</li>");
            if (log.children("li").length > 8) {
                log.get(0).removeChild(log.children("li")[0]);
            }
        },
        getTime: function(){
            var now = new Date(), h = now.getHours(), m = now.getMinutes(), s = now
                .getSeconds(), ms = now.getMilliseconds();
            return (h + ":" + m + ":" + s + " " + ms);
        },
        
        selectAll: function(){
            var zTree = $.fn.zTree.getZTreeObj("treeDemo");
            zTree.treeSetting.edit.editNameSelectAll = $("#selectAll").attr("checked");
        },
        //点击节点
        zTreeOnClick: function(event, treeId, treeNode){
            selectTreeId = treeNode.id;
            selectDistrictId = treeNode.districtid;
            selectTreeIdAdd=treeNode.uuid;
            $('#simpleQueryParam').val("");
            myTable.requestData();
        },
        // ajax参数
        ajaxDataParamFun: function(d){
            d.simpleQueryParam = $('#simpleQueryParam').val(); // 模糊查询
            d.groupName = selectTreeId;
            d.districtId = selectDistrictId;
        },
        findDownKey:function(event){
            if(event.keyCode==13){
                mapMonitor.findOperation();
            }
        }
    }
    $(function(){
        $('input').inputClear().on('onClearEvent',function(e,data){
            var id = data.id;
            if(id == 'search_condition'){
                search_ztree('treeDemo',id,'group');
            };
        });
        var map;
        mapMonitor.userTree();
        
        mapMonitor.init();
        
        // map.on(['pointermove', 'singleclick'], mapMonitor.moveonmapevent);
        
    })
})($,window)
