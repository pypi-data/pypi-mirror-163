"use strict";(self["webpackChunk_quetz_frontend_main_app"]=self["webpackChunk_quetz_frontend_main_app"]||[]).push([[8136,5836],{28136:(t,e,n)=>{n.r(e);n.d(e,{App:()=>f,QuetzServiceManager:()=>u,Shell:()=>m});var i=n(85168);var s=n(79450);var r=n(18303);var a=n(18470);var o=n(4135);var d=n(57e3);var h=n(98078);class u{constructor(){this._isDisposed=false;this._connectionFailure=new d.Signal(this);this.settings=new h.SettingManager({serverSettings:this.serverSettings})}get connectionFailure(){return this._connectionFailure}get isDisposed(){return this._isDisposed}get serverSettings(){return h.ServerConnection.makeSettings()}get isReady(){return true}get ready(){return Promise.resolve()}dispose(){if(this.isDisposed){return}this._isDisposed=true;d.Signal.clearData(this)}}var c=n(62867);var l=n(61389);var p=n(32151);const g=900;class m extends l.Widget{constructor(){super();this.id="main";const t=new l.BoxLayout;this._top=new _.PanelHandler;this._bottom=new _.PanelHandler;this._main=new l.Panel;this._bottom.panel.id="bottom-panel";this._top.panel.id="top-panel";this._main.id="main-panel";l.BoxLayout.setStretch(this._top.panel,0);l.BoxLayout.setStretch(this._bottom.panel,0);l.BoxLayout.setStretch(this._main,1);t.spacing=0;t.addWidget(this._top.panel);t.addWidget(this._main);t.addWidget(this._bottom.panel);this.layout=t}activateById(t){}add(t,e,n){var i;const s=(i=n===null||n===void 0?void 0:n.rank)!==null&&i!==void 0?i:g;if(e==="top"){return this._top.addWidget(t,s)}if(e==="bottom"){return this._bottom.addWidget(t,s)}if(e==="main"||e===undefined){this._addToMainArea(t)}return}get currentWidget(){return this._main.widgets[0]}get top(){return this._topWrapper}get bottom(){return this._bottomWrapper}widgets(t){if(t==="top"){return(0,c.iter)(this._top.panel.widgets)}return(0,c.iter)(this._main.widgets)}_addToMainArea(t){if(!t.id){console.error("Widgets added to the app shell must have unique id property.");return}const e=this._main;const{title:n}=t;n.dataset=Object.assign(Object.assign({},n.dataset),{id:t.id});if(n.icon instanceof a.LabIcon){n.icon=n.icon.bindprops({stylesheet:"mainAreaTab"})}else if(typeof n.icon==="string"||!n.icon){n.iconClass=(0,a.classes)(n.iconClass,"jp-Icon")}if(e.widgets.length){e.widgets[0].dispose()}e.addWidget(t)}}var _;(function(t){function e(t,e){return t.rank-e.rank}t.itemCmp=e;class n{constructor(){this._panelChildHook=(t,e)=>{switch(e.type){case"child-added":{const t=e.child;if(this._items.find((e=>e.widget===t))){break}const n=this._items[this._items.length-1].rank;this._items.push({widget:t,rank:n})}break;case"child-removed":{const t=e.child;c.ArrayExt.removeFirstWhere(this._items,(e=>e.widget===t))}break;default:break}return true};this._items=new Array;this._panel=new l.Panel;p.MessageLoop.installMessageHook(this._panel,this._panelChildHook)}get panel(){return this._panel}addWidget(e,n){e.parent=null;const i={widget:e,rank:n};const s=c.ArrayExt.upperBound(this._items,i,t.itemCmp);c.ArrayExt.insert(this._items,s,i);this._panel.insertWidget(s,e)}}t.PanelHandler=n})(_||(_={}));class f extends o.Application{constructor(t={}){var e;super(Object.assign(Object.assign({},t),{shell:(e=t.shell)!==null&&e!==void 0?e:new m}));this.name=r.PageConfig.getOption("appName")||"Quetz";this.namespace=r.PageConfig.getOption("appNamespace")||this.name;this.registerPluginErrors=[];this.version=r.PageConfig.getOption("appVersion")||"unknown";this._formatChanged=new d.Signal(this);this.serviceManager=new u;this.contextMenu=new a.ContextMenuSvg({commands:this.commands,renderer:t.contextMenuRenderer,groupByTarget:false,sortBySelector:false});const n=new Promise((t=>{requestAnimationFrame((()=>{t()}))}));this.commandLinker=t.commandLinker||new s.CommandLinker({commands:this.commands});this.restored=t.restored||this.started.then((()=>n)).catch((()=>n))}get format(){return this._format}set format(t){if(this._format!==t){this._format=t;document.body.dataset["format"]=t;this._formatChanged.emit(t)}}get formatChanged(){return this._formatChanged}get paths(){return i.JupyterLab.defaultPaths}contextMenuHitTest(t){if(!this._contextMenuEvent||!(this._contextMenuEvent.target instanceof Node)){return undefined}let e=this._contextMenuEvent.target;do{if(e instanceof HTMLElement&&t(e)){return e}e=e.parentNode}while(e&&e.parentNode&&e!==e.parentNode);return undefined}evtContextMenu(t){this._contextMenuEvent=t;if(t.shiftKey){return}const e=this.contextMenu.open(t);if(e){const e=this.contextMenu.menu.items;if(e.length===1&&e[0].command===i.JupyterFrontEndContextMenu.contextMenu){this.contextMenu.menu.close();return}t.preventDefault();t.stopPropagation()}}registerPluginModule(t){let e=t.default;if(!Object.prototype.hasOwnProperty.call(t,"__esModule")){e=t}if(!Array.isArray(e)){e=[e]}e.forEach((t=>{try{this.registerPlugin(t)}catch(e){this.registerPluginErrors.push(e)}}))}registerPluginModules(t){t.forEach((t=>{this.registerPluginModule(t)}))}}}}]);