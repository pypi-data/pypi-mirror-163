webpackJsonp([22,31],{898:function(e,t,o){var s,i;s=o(1478),i=o(1575),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},982:function(e,t,o){var s,i;o(998),s=o(990),i=o(995),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},983:function(e,t,o){var s,i;s=o(989),i=o(994),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},989:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=300,s=5e3;t.default={name:"alert-box",data:function(){return{closing:!1}},props:{alert:Object},computed:{closable:function(){return void 0===this.alert.closable||this.alert.closable},classes:function classes(){var classes={"alert-dismissable":this.closable,in:!this.closing};return classes["alert-"+(this.alert.type||"success")]=!0,classes},details:function(){if(this.alert&&this.alert.details)return this.alert.details.replace(/\n/g,"<br/>")}},methods:{close:function(){var e=this;this.closing=!0,setTimeout(function(){e.$dispatch("notify:close",e.alert)},o)}},ready:function(){var e=this;this.alert.autoclose&&setTimeout(function(){e.$dispatch("notify:close",e.alert)},s)}}},990:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"box",props:{title:String,icon:null,boxclass:{type:String,default:""},bodyclass:{type:String,default:""},footerclass:{type:String,default:""},loading:Boolean,footer:null}}},991:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(983),i=_interopRequireDefault(s);t.default={name:"notification-zone",components:{Alert:i.default}}},992:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".box .box-tools>*{float:right}.box .box-tools .text-muted{color:#777!important}.box .box-tools .box-search{width:180px;display:inline-block}.box .box-tools .box-search input:focus{box-shadow:none;border-color:transparent!important}.box .box-tools .box-search .btn,.box .box-tools .box-search input[type=text]{box-shadow:none;background-color:#fbfbfb;border:1px solid #fbfbfb}.box .box-tools .box-search .btn:focus,.box .box-tools .box-search input[type=text]:focus{background-color:#fff;color:#666}.box .box-tools .box-search .btn:focus+.input-group-btn .btn,.box .box-tools .box-search input[type=text]:focus+.input-group-btn .btn{background-color:#fff;border-left-color:#fff;color:#666}.box .box-tools .box-search>*{border-top:1px solid #eee;border-bottom:1px solid #eee}.box .box-tools .box-search>:first-child{border-left:1px solid #eee}.box .box-tools .box-search>:last-child{border-right:1px solid #eee}.box .box-tools .btn-box-tool{font-size:14px;padding:6px 8px}.box .box-tools .btn-group{vertical-align:inherit}.box form{margin:10px}","",{version:3,sources:["/./js/components/containers/box.vue"],names:[],mappings:"AAAA,kBAAkB,WAAW,CAAC,4BAA4B,oBAAqB,CAAC,4BAA4B,YAAY,oBAAoB,CAAC,wCAAwC,gBAAgB,kCAAmC,CAAC,8EAAgF,gBAAgB,yBAAyB,wBAAwB,CAAC,0FAA4F,sBAAsB,UAAU,CAAC,sIAAwI,sBAAsB,uBAAuB,UAAU,CAAC,8BAA8B,0BAA0B,4BAA4B,CAAC,yCAA0C,0BAA0B,CAAC,wCAAyC,2BAA2B,CAAC,8BAA8B,eAAe,eAAe,CAAC,2BAA2B,sBAAsB,CAAC,UAAU,WAAW,CAAC",file:"box.vue",sourcesContent:['.box .box-tools>*{float:right}.box .box-tools .text-muted{color:#777 !important}.box .box-tools .box-search{width:180px;display:inline-block}.box .box-tools .box-search input:focus{box-shadow:none;border-color:transparent !important}.box .box-tools .box-search input[type="text"],.box .box-tools .box-search .btn{box-shadow:none;background-color:#fbfbfb;border:1px solid #fbfbfb}.box .box-tools .box-search input[type="text"]:focus,.box .box-tools .box-search .btn:focus{background-color:#fff;color:#666}.box .box-tools .box-search input[type="text"]:focus+.input-group-btn .btn,.box .box-tools .box-search .btn:focus+.input-group-btn .btn{background-color:#fff;border-left-color:#fff;color:#666}.box .box-tools .box-search>*{border-top:1px solid #eee;border-bottom:1px solid #eee}.box .box-tools .box-search>*:first-child{border-left:1px solid #eee}.box .box-tools .box-search>*:last-child{border-right:1px solid #eee}.box .box-tools .btn-box-tool{font-size:14px;padding:6px 8px}.box .box-tools .btn-group{vertical-align:inherit}.box form{margin:10px}'],sourceRoot:"webpack://"}])},993:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".notification-zone{padding:15px 15px 0;position:fixed;right:15px;bottom:15px;width:350px;z-index:10000}.notification-zone .alert:last-child{margin-bottom:0}.notification-zone .alert:not(:last-child){margin-bottom:5px}","",{version:3,sources:["/./js/components/notification-zone.vue"],names:[],mappings:"AAAA,mBAAmB,oBAAoB,eAAe,WAAW,YAAY,YAAY,aAAa,CAAC,qCAAqC,eAAe,CAAC,2CAA2C,iBAAiB,CAAC",file:"notification-zone.vue",sourcesContent:[".notification-zone{padding:15px 15px 0;position:fixed;right:15px;bottom:15px;width:350px;z-index:10000}.notification-zone .alert:last-child{margin-bottom:0}.notification-zone .alert:not(:last-child){margin-bottom:5px}"],sourceRoot:"webpack://"}])},994:function(e,t){e.exports=' <div class="alert fade" :class=classes> <button type=button class=close aria-hidden=true @click=close>×</button> <h4> <span class="icon fa fa-{{alert.icon || \'check\'}}"></span> {{alert.title}} </h4> {{{ details }}} </div> '},995:function(e,t){e.exports=' <div class="box {{ boxclass }}"> <header class=box-header v-show="title || icon"> <i v-show=icon class="fa fa-{{icon}}"></i> <h3 class=box-title>{{title}}</h3> <div class=box-tools> <slot name=tools></slot> </div> </header> <div class="box-body {{bodyclass}}"> <slot></slot> </div> <div class=overlay v-show=loading> <span class="fa fa-refresh fa-spin"></span> </div> <div class="box-footer clearfix {{footerclass}}" v-show=footer> <slot name=footer></slot> </div> </div> '},996:function(e,t){e.exports=' <div v-show="$root.notifications && $root.notifications.length > 0" class=notification-zone> <alert v-for="n in $root.notifications" :alert=n></alert> </div> '},997:function(e,t,o){var s,i;o(999),s=o(991),i=o(996),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},998:function(e,t,o){var s=o(992);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},999:function(e,t,o){var s=o(993);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1036:function(e,t,o){var s,i;o(1175),s=o(1111),i=o(1152),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1072:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(997),i=_interopRequireDefault(s);t.default={name:"layout",props:{title:String,subtitle:String,page:String,actions:{type:Array,default:function(){return[]}},badges:Array},components:{NotificationZone:i.default},computed:{menu_actions:function(){if(this.actions&&this.actions.length>1)return this.actions}}}},1073:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".content-header h1 a{color:#000}.content-header h1 a .fa{font-size:.4em}","",{version:3,sources:["/./js/components/layout.vue"],names:[],mappings:"AAAA,qBAAqB,UAAW,CAAC,yBAAyB,cAAc,CAAC",file:"layout.vue",sourcesContent:[".content-header h1 a{color:black}.content-header h1 a .fa{font-size:.4em}"],sourceRoot:"webpack://"}])},1074:function(e,t){e.exports=' <div class=content-wrapper> <router-view></router-view> <section class=content-header> <div class="btn-group btn-group-sm btn-actions pull-right clearfix"> <div v-if=menu_actions class="btn-group btn-group-sm" role=group> <button type=button class="btn btn-info dropdown-toggle" data-toggle=dropdown> {{_(\'Edit\')}} <span class=caret></span> </button> <ul class="dropdown-menu dropdown-menu-right" role=menu> <li v-for="action in menu_actions" :role="action.divider ? \'separator\' : false" :class="{ \'divider\': action.divider }"> <a class=pointer v-if=!action.divider @click=action.method> <span v-if=action.icon class="fa fa-fw fa-{{action.icon}}"></span> {{action.label}} </a> </li> </ul> </div> </div> <h1> <a v-if=page :href=page :title="_(\'See on the site\')"> {{ title }} <span class="fa fa-external-link"></span> </a> <span v-if=!page>{{title}}</span> <small v-if=subtitle>{{subtitle}}</small> <small v-if=badges> <span v-for="badge in badges" class="label label-{{badge.class}}">{{badge.label}}</span> </small> </h1> </section> <notification-zone></notification-zone> <section class=content> <slot></slot> </section> </div> '},1075:function(e,t,o){var s,i;o(1076),s=o(1072),i=o(1074),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1076:function(e,t,o){var s=o(1073);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1092:function(e,t,o){function webpackContext(e){return o(webpackContextResolve(e))}function webpackContextResolve(e){return s[e]||function(){throw new Error("Cannot find module '"+e+"'.")}()}var s={"./avatar.vue":1155,"./date.vue":1156,"./datetime.vue":1157,"./deletable-text.vue":1158,"./label.vue":1159,"./metric.vue":1160,"./playpause.vue":1161,"./progress-bars.vue":1162,"./since.vue":1163,"./text.vue":1164,"./thumbnail.vue":1165,"./timeago.vue":1166,"./visibility.vue":1167};webpackContext.keys=function(){return Object.keys(s)},webpackContext.resolve=webpackContextResolve,e.exports=webpackContext,webpackContext.id=1092},1095:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(57),i=(_interopRequireDefault(s),o(311)),a=_interopRequireDefault(i);t.default={name:"datatable-cell",default:"",props:{field:Object,item:Object},computed:{value:function(){if(!this.field||!this.item)return this.$options.default;if(this.field.key)if(a.default.isFunction(this.field.key))t=this.field.key(this.item);else for(var e=this.field.key.split("."),t=this.item,o=0;o<e.length;o++){var s=e[o];if(!t||!t.hasOwnProperty(s)){t=null;break}t=t[s]}else t=this.item;return t||this.$options.default}}}},1096:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={attached:function(){this.$el.closest("td").classList.add("avatar-cell")}}},1097:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-date"}},1098:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-datetime"}},1099:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-deletable-text"}},1100:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-label",filters:{format:function(e){return this.field.hasOwnProperty("label_func")?this.field.label_func(e):e},color:function(e){return this.field.hasOwnProperty("label_type")?this.field.label_type(e):"default"}},computed:{labels:function(){return this.value instanceof Array?this.value:[this.value]}}}},1101:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-metric",default:0}},1102:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-playpause",default:!1}},1103:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-progress-bars",computed:{progress_class:function(){return this.value<2?"danger":this.value<5?"warning":this.value<9?"primary":"success"}}}},1104:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-since"}},1105:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-text"}},1106:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(101),i=_interopRequireDefault(s);t.default={attached:function(){this.$el.closest("td").classList.add("thumbnail-cell")},computed:{src:function(){return this.value?this.value:this.field.placeholder?i.default.getFor(this.field.placeholder):i.default.generic}}}},1107:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={name:"datatable-cell-timeago"}},1108:function(e,t,o){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=o(133),i={deleted:{label:(0,s._)("Deleted"),type:"danger"},archived:{label:(0,s._)("Archived"),type:"warning"},private:{label:(0,s._)("Private"),type:"info"},public:{label:(0,s._)("Public"),type:"success"}};t.default={name:"datatable-cell-visibility",computed:{status:function(){if(this.item)return this.item.deleted?i.deleted:this.item.archived?i.archived:this.item.private?i.private:i.public}}}},1109:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(200),i=_interopRequireDefault(s),a=o(57),n=_interopRequireDefault(a),r=o(1154),l=_interopRequireDefault(r);t.default={name:"datatable-row",props:{item:Object,fields:Array,selected:{type:Boolean,default:!1}},created:function(){var e=!0,t=!1,o=void 0;try{for(var s,a=(0,i.default)(this.fields);!(e=(s=a.next()).done);e=!0){var n=s.value;this.load_cell(n.type||"text")}}catch(r){t=!0,o=r}finally{try{!e&&a.return&&a.return()}finally{if(t)throw o}}},methods:{item_click:function(e){this.$dispatch("datatable:item:click",e)},load_cell:function(e){if(!this.$options.components.hasOwnProperty(e)){var t=o(1092)("./"+e+".vue");t.hasOwnProperty("mixins")||(t.mixins=[]),l.default in t.mixins||t.mixins.push(l.default),this.$options.components[e]=n.default.extend(t)}}}}},1110:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1168),i=_interopRequireDefault(s);t.default={name:"datatable",components:{Row:i.default},props:{p:Object,fields:Array,track:{type:null,default:"id"}},data:function(){return{selected:null}},computed:{remote:function(){return this.p&&this.p.serverside},trackBy:function(){return this.track||""}},events:{"datatable:item:click":function(e){return this.selected=e,!0}},methods:{header_click:function(e){e.sort&&this.p.sort(this.sort_for(e))},sort_for:function(e){return this.remote?e.sort:e.key},classes_for:function(e){var t={pointer:Boolean(e.sort)},o=e.align||"left";return t["text-"+o]=!0,t},sort_classes_for:function(e){var t={};return this.p.sorted!=this.sort_for(e)?t["fa-sort"]=!0:this.p.reversed?this.p.reversed&&(t["fa-sort-desc"]=!0):t["fa-sort-asc"]=!0,t}},filters:{thwidth:function(e){switch(e){case void 0:return"";case 0:return 0;default:return e+5}}}}},1111:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(982),i=_interopRequireDefault(s),a=o(1169),n=_interopRequireDefault(a),r=o(1170),l=_interopRequireDefault(r);t.default={name:"datatable-widget",components:{Box:i.default,Datatable:n.default,PaginationWidget:l.default},data:function(){return{search_query:null,selected:null}},computed:{has_footer_children:function(){return this.$els.footer_container&&this.$els.footer_container.children.length},show_footer:function(){return this.p&&this.p.pages>1||this.has_footer_children},boxclasses:function(){return["datatable-widget",this.tint?"box-"+this.tint:"box-solid",this.boxclass].join(" ")}},props:{p:Object,title:String,icon:String,fields:Array,boxclass:String,tint:String,empty:String,loading:{type:Boolean,default:void 0},track:{type:null,default:"id"},downloads:{type:Array,default:function(){return[]}}},methods:{search:function(){this.p.search(this.search_query)}},watch:{search_query:function(e){this.p.search(e)}}}},1112:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var o=2;t.default={name:"pagination-widget",props:{p:Object},computed:{start:function(){return this.p?this.p.page<=o?1:this.p.page-o:-1},end:function(){return this.p?this.p.page+o>this.p.pages?this.p.pages:this.p.page+o:-1},range:function(){var e=this;return isNaN(this.start)||isNaN(this.end)||this.start>=this.end?[]:Array.apply(0,Array(this.end+1-this.start)).map(function(t,o){return o+e.start})}}}},1129:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".datatable td.ellipsis{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:0}","",{version:3,sources:["/./js/components/datatable/cell.vue"],names:[],mappings:"AAAA,uBAAuB,mBAAmB,gBAAgB,uBAAuB,WAAW,CAAC",file:"cell.vue",sourcesContent:[".datatable td.ellipsis{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:0}"],sourceRoot:"webpack://"}])},1130:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".datatable td.avatar-cell{padding:3px}","",{version:3,sources:["/./js/components/datatable/cells/avatar.vue"],names:[],mappings:"AAAA,0BAA0B,WAAW,CAAC",file:"avatar.vue",sourcesContent:[".datatable td.avatar-cell{padding:3px}"],sourceRoot:"webpack://"}])},1131:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".datatable td.thumbnail-cell{padding:3px}","",{version:3,sources:["/./js/components/datatable/cells/thumbnail.vue"],names:[],mappings:"AAAA,6BAA6B,WAAW,CAAC",file:"thumbnail.vue",sourcesContent:[".datatable td.thumbnail-cell{padding:3px}"],sourceRoot:"webpack://"}])},1132:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".datatable th{white-space:nowrap}","",{version:3,sources:["/./js/components/datatable/table.vue"],names:[],mappings:"AAAA,cAAc,kBAAkB,CAAC",file:"table.vue",sourcesContent:[".datatable th{white-space:nowrap}"],sourceRoot:"webpack://"}])},1133:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".datatable-widget .datatable-header>.row{width:100%}","",{version:3,sources:["/./js/components/datatable/widget.vue"],names:[],mappings:"AAAA,yCAAyC,UAAU,CAAC",file:"widget.vue",sourcesContent:[".datatable-widget .datatable-header>.row{width:100%}"],sourceRoot:"webpack://"}])},1134:function(e,t,o){t=e.exports=o(37)(),t.push([e.id,".label{margin:1px}","",{version:3,sources:["/./js/components/datatable/cells/label.vue"],names:[],mappings:"AACA,OACI,UAAY,CACf",file:"label.vue",sourcesContent:["\n.label {\n    margin: 1px;\n}\n"],sourceRoot:"webpack://"}])},1137:function(e,t){e.exports=' <img :src="value | avatar_url field.width" :width=field.width :height=field.width /> '},1138:function(e,t){e.exports=' <time :datetime="value | dt YYYY-MM-DD">{{value | dt L}}</time> '},1139:function(e,t){e.exports=" <time :datetime=value>{{value | dt L LT}}</time> "},1140:function(e,t){e.exports=" <del v-if=item.deleted :title=\"_('This item has been deleted')\" :datetime=item.deleted>{{value}}</del> <span v-else>{{value}}</span> "},1141:function(e,t){e.exports=' <span v-for="label in labels" class="label label-{{label | color}}"> {{label | format}} </span> '},1142:function(e,t){e.exports=" <span class=badge :class=\"{\n    'bg-green': value > 0,\n    'bg-red': value == 0\n    }\">{{value}}</span> "},1143:function(e,t){e.exports=" <i class=\"fa fa-fw fa-{{value ? 'play' : 'stop'}} text-{{value ? 'green' : 'red'}}\"></i> "},1144:function(e,t){e.exports=' <div class="progress progress-sm"> <span class="progress-bar progress-bar-{{ progress_class }}" :style="{width: value + 1 + \'0%\'}" :title="_(\'Score:\') + \' \' + value"> </span> </div> '},1145:function(e,t){e.exports=" <time :datetime=value>{{value | since}}</time> "},1146:function(e,t){e.exports="<span>{{value}}</span>"},1147:function(e,t){e.exports=" <img :src=src :width=field.width :height=field.width /> "},1148:function(e,t){e.exports=" <time :datetime=value class=timeago>{{value | timeago}}</time> "},1149:function(e,t){e.exports=' <span class="label label-{{ status.type }}">{{ status.label }}</span> '},1150:function(e,t){e.exports=" <tr class=pointer :class=\"{ 'active': selected }\" @click=item_click(item)> <td v-for=\"field in fields\" track-by=key :class=\"{\n            'text-center': field.align === 'center',\n            'text-left': field.align === 'left',\n            'text-right': field.align === 'right',\n            'ellipsis': field.ellipsis\n        }\"> <component :is=\"field.type || 'text'\" :item=item :field=field> </component> </td> </tr> "},1151:function(e,t){e.exports=' <table class="table table-hover datatable"> <thead> <tr> <th v-for="field in fields" :class=classes_for(field) @click=header_click(field) :width="field.width | thwidth"> {{field.label}} <span class="fa fa-fw" v-if=field.sort :class=sort_classes_for(field)></span> </th> </tr> </thead> <tbody> <tr v-for="item in p.data" :track-by=trackBy is=row :item=item :fields=fields :selected="item === selected"> </tr> </tbody> </table> '},1152:function(e,t){e.exports=' <div> <box :title=title :icon=icon :boxclass=boxclasses bodyclass="table-responsive no-padding" footerclass="text-center clearfix" :loading="loading !== undefined ? loading : p.loading" :footer=show_footer> <aside slot=tools> <div class=btn-group v-show=downloads.length> <button type=button class="btn btn-box-tool dropdown-toggle" data-toggle=dropdown aria-expanded=false> <span class="fa fa-download"></span> </button> <ul class=dropdown-menu role=menu> <li v-for="download in downloads"> <a :href=download.url>{{download.label}}</a> </li> </ul> </div> <div class=box-search v-if=p.has_search> <div class=input-group> <input type=text class="form-control input-sm pull-right" style="width: 150px" :placeholder="_(\'Search\')" v-model=search_query debounce=500 @keyup.enter=search> <div class=input-group-btn> <button class="btn btn-sm btn-flat" @click=search> <i class="fa fa-search"></i> </button> </div> </div> </div> </aside> <header class=datatable-header> <slot name=header></slot> </header> <datatable v-if=p.has_data :p=p :fields=fields :track=track> </datatable> <div class="text-center lead" v-if=!p.has_data> {{ empty || _(\'No data\')}} </div> <footer slot=footer> <div :class="{ \'pull-right\': p.pages > 1 }" v-el:footer_container> <slot name=footer></slot> </div> <pagination-widget :p=p></pagination-widget> </footer> </box> </div> '},1153:function(e,t){e.exports=' <ul class="pagination pagination-sm no-margin" v-show="p && p.pages > 1"> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'First page\')" class=pointer @click=p.go_to_page(1)> &laquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'Previous page\')" class=pointer @click=p.previousPage()> &lsaquo; </a> </li> <li v-for="current in range" :class="{ \'active\': current == p.page }"> <a @click=p.go_to_page(current) class=pointer>{{ current }}</a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Next page\')" class=pointer @click=p.nextPage()> &rsaquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Last page\')" class=pointer @click=p.go_to_page(p.pages)> &raquo; </a> </li> </ul> '},1154:function(e,t,o){var s,i;o(1171),s=o(1095),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1155:function(e,t,o){var s,i;o(1172),s=o(1096),i=o(1137),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1156:function(e,t,o){var s,i;s=o(1097),i=o(1138),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1157:function(e,t,o){var s,i;s=o(1098),i=o(1139),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1158:function(e,t,o){var s,i;s=o(1099),i=o(1140),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1159:function(e,t,o){var s,i;o(1176),s=o(1100),i=o(1141),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1160:function(e,t,o){var s,i;s=o(1101),i=o(1142),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1161:function(e,t,o){var s,i;s=o(1102),i=o(1143),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1162:function(e,t,o){var s,i;s=o(1103),i=o(1144),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1163:function(e,t,o){var s,i;s=o(1104),i=o(1145),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1164:function(e,t,o){var s,i;s=o(1105),i=o(1146),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1165:function(e,t,o){var s,i;o(1173),s=o(1106),i=o(1147),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1166:function(e,t,o){var s,i;s=o(1107),i=o(1148),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1167:function(e,t,o){var s,i;s=o(1108),i=o(1149),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1168:function(e,t,o){var s,i;s=o(1109),i=o(1150),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1169:function(e,t,o){var s,i;o(1174),s=o(1110),i=o(1151),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1170:function(e,t,o){var s,i;s=o(1112),i=o(1153),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1171:function(e,t,o){var s=o(1129);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1172:function(e,t,o){var s=o(1130);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1173:function(e,t,o){var s=o(1131);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1174:function(e,t,o){var s=o(1132);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1175:function(e,t,o){var s=o(1133);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1176:function(e,t,o){var s=o(1134);"string"==typeof s&&(s=[[e.id,s,""]]);o(38)(s,{sourceMap:!0});s.locals&&(e.exports=s.locals)},1181:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0}),t.HarvestSource=t.VALIDATION_STATUS_I18N=t.VALIDATION_STATUS_CLASSES=void 0;var s=o(21),i=_interopRequireDefault(s),a=o(20),n=_interopRequireDefault(a),r=o(46),l=_interopRequireDefault(r),u=o(27),p=_interopRequireDefault(u),c=o(26),d=_interopRequireDefault(c),f=o(39),x=o(133),b=o(19),h=_interopRequireDefault(b),v=(t.VALIDATION_STATUS_CLASSES={pending:"default",accepted:"success",refused:"danger"},t.VALIDATION_STATUS_I18N={pending:(0,x._)("Pending"),accepted:(0,x._)("Accepted"),refused:(0,x._)("Refused")},t.HarvestSource=function(e){function HarvestSource(){return(0,n.default)(this,HarvestSource),(0,p.default)(this,(HarvestSource.__proto__||(0,i.default)(HarvestSource)).apply(this,arguments))}return(0,d.default)(HarvestSource,e),(0,l.default)(HarvestSource,[{key:"fetch",value:function(e){return e=e||this.id||this.slug,this.loading=!0,e?this.$api("harvest.get_harvest_source",{ident:e},this.on_fetched):h.default.error("Unable to fetch HarvestSource: no identifier specified"),this}},{key:"save",value:function(e){return this.id?this.update(this,e):(this.loading=!0,void this.$api("harvest.create_harvest_source",{payload:this},this.on_fetched,this.on_error(e)))}},{key:"update",value:function(e,t){this.loading=!0,this.$api("harvest.update_harvest_source",{ident:this.id,payload:e},this.on_fetched,this.on_error(t))}}]),HarvestSource}(f.Model));t.default=v},1193:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0}),t.HarvestJob=t.STATUS_I18N=t.STATUS_CLASSES=void 0;var s=o(21),i=_interopRequireDefault(s),a=o(20),n=_interopRequireDefault(a),r=o(46),l=_interopRequireDefault(r),u=o(27),p=_interopRequireDefault(u),c=o(26),d=_interopRequireDefault(c),f=o(39),x=o(19),b=_interopRequireDefault(x),h=o(133),v=(t.STATUS_CLASSES={pending:"default",initializing:"primary",initialized:"info",processing:"info",done:"success","done-errors":"warning",failed:"danger",deleted:"danger"},t.STATUS_I18N={pending:(0,h._)("Pending"),initializing:(0,h._)("Initializing"),initialized:(0,h._)("Initialized"),processing:(0,h._)("Processing"),done:(0,h._)("Done"),"done-errors":(0,h._)("Done with errors"),failed:(0,h._)("Failed"),deleted:(0,h._)("Deleted")},t.HarvestJob=function(e){function HarvestJob(){return(0,n.default)(this,HarvestJob),(0,p.default)(this,(HarvestJob.__proto__||(0,i.default)(HarvestJob)).apply(this,arguments))}return(0,d.default)(HarvestJob,e),(0,l.default)(HarvestJob,[{key:"fetch",value:function(){return this.id?(this.loading=!0,this.$api("harvest.get_harvest_job",{ident:this.id},this.on_fetched)):b.default.error("Unable to fetch Job"),this}}]),HarvestJob}(f.Model));t.default=v},1272:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(21),i=_interopRequireDefault(s),a=o(20),n=_interopRequireDefault(a),r=o(27),l=_interopRequireDefault(r),u=o(26),p=_interopRequireDefault(u),c=o(39),d=function(e){function HarvestSourcePage(e){(0,n.default)(this,HarvestSourcePage);var t=(0,l.default)(this,(HarvestSourcePage.__proto__||(0,i.default)(HarvestSourcePage)).call(this,e));return t.$options.ns="harvest",t.$options.fetch="list_harvest_sources",t}return(0,p.default)(HarvestSourcePage,e),HarvestSourcePage}(c.ModelPage);t.default=d},1278:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(39),i=o(1272),a=_interopRequireDefault(i),n=(o(1181),o(1193)),r=o(1036),l=_interopRequireDefault(r),u=o(101),p=_interopRequireDefault(u),c=["id","name","owner","last_job{status,ended}","organization{name,logo_thumbnail}","backend","validation{state}","deleted"];t.default={MASK:c,components:{Datatable:l.default},
props:{owner:{type:s.Model,default:function(){}}},data:function(){return{title:this._("Harvesters"),sources:new a.default({mask:c,query:{deleted:!0}})}},computed:{fields:function fields(){var e=this,fields=[];return this.owner instanceof s.Model||fields.push({key:function(e){return e.organization?p.default.org_logo(e.organization,30):p.default.user_avatar(e.owner,30)},type:"thumbnail",width:30}),fields.push({label:this._("Name"),key:"name",align:"left",type:"deletable-text"}),this.owner instanceof s.Model||fields.push({label:this._("Owner"),key:function(e){return e.organization?e.organization.name:e.owner.first_name+" "+e.owner.last_name},align:"left",type:"text",width:250}),fields.push({label:this._("Backend"),key:"backend",align:"left",type:"text",width:100},{label:this._("Status"),key:function(e){return e.deleted?"deleted":"pending"==e.validation.state?"validation":"refused"==e.validation.state?"refused":e.last_job.status},type:"label",width:100,label_type:function(e){return e?"validation"==e?"default":"refused"==e?"danger":n.STATUS_CLASSES[e]:"default"},label_func:function(t){return t?"validation"==t?e._("Validation"):"refused"==t?e._("Refused"):n.STATUS_I18N[t]:e._("No job yet")}},{label:this._("Last run"),key:"last_job.ended",align:"left",type:"timeago",width:120}),fields}},events:{"datatable:item:click":function(e){this.$go({name:"harvester",params:{oid:e.id}})}},ready:function(){this.owner instanceof s.Model?this.owner.id&&this.sources.fetch({owner:this.owner.id}):this.sources.fetch()},watch:{"owner.id":function(e){e&&this.sources.fetch({owner:e})}}}},1285:function(e,t){e.exports=" <div> <datatable :title=title icon=tasks boxclass=harvesters-widget :fields=fields :p=sources :loading=sources.loading :empty=\"_('No harvester')\"> </datatable> </div> "},1289:function(e,t,o){var s,i;s=o(1278),i=o(1285),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1390:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0}),t.jobs=t.Jobs=void 0;var s=o(21),i=_interopRequireDefault(s),a=o(20),n=_interopRequireDefault(a),r=o(27),l=_interopRequireDefault(r),u=o(26),p=_interopRequireDefault(u),c=o(39),d=o(19),f=(_interopRequireDefault(d),t.Jobs=function(e){function Jobs(e){(0,n.default)(this,Jobs);var t=(0,l.default)(this,(Jobs.__proto__||(0,i.default)(Jobs)).call(this,e));return t.$options.ns="workers",t.$options.fetch="list_jobs",t}return(0,p.default)(Jobs,e),Jobs}(c.List)),x=t.jobs=(new f).fetch();t.default=x},1445:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1390),i=_interopRequireDefault(s),a=o(1036),n=_interopRequireDefault(a);t.default={name:"jobs-list",components:{Datatable:n.default},data:function(){return{title:this._("Jobs"),jobs:i.default,fields:[{label:this._("Name"),key:"name",sort:"name",align:"left",type:"text"},{label:this._("Scheduling"),key:"schedule",sort:"schedule",align:"left",type:"text"},{label:"",key:"enabled",type:"playpause",width:"20px"}]}},events:{"datatable:item:click":function(e){this.$go("/job/"+e.id+"/")}}}},1446:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(982),i=_interopRequireDefault(s);t.default={name:"oauth-widget",components:{Box:i.default},data:function(){return{title:"OAuth",clients:[]}}}},1478:function(e,t,o){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var s=o(1075),i=_interopRequireDefault(s),a=o(1289),n=_interopRequireDefault(a),r=o(1624),l=_interopRequireDefault(r),u=o(1625),p=_interopRequireDefault(u);t.default={name:"SystemView",components:{HarvestersWidget:n.default,JobsWidget:l.default,OauthWidget:p.default,Layout:i.default}}},1542:function(e,t){e.exports=" <div> <datatable :title=title icon=cogs boxclass=jobs-widget :fields=fields :p=jobs :empty=\"_('No job')\"> </datatable> </div> "},1543:function(e,t){e.exports=" <div> <box title=OAuth icon=plug boxclass=box-info bodyclass=\"table-responsive no-padding\"> <table class=\"table table-hover\"> <thead> <tr> <th v-i18n=Name></th> <th v-i18n=Description></th> <th width=20px></th> </tr> </thead> <tbody> <tr v-for=\"client in clients\" v-link=\"'/oauth/clients/' + client.id + '/'\"> <td>{{client.name}}</td> <td>{{client.description}}</td> <td> <i class=\"fa fa-fw fa-{{client.enabled ? 'play' : 'stop'}} text-{{client.enabled ? 'green' : 'red'}}\"></i> </td> </tr> </tbody> </table> </box> </div> "},1575:function(e,t){e.exports=' <div> <layout :title="_(\'System\')"> <div class=row> <harvesters-widget class=col-xs-12></harvesters-widget> <jobs-widget class="col-xs-12 col-md-6"></jobs-widget> <oauth-widget class="col-xs-12 col-md-6"></oauth-widget> </div> </layout> </div> '},1624:function(e,t,o){var s,i;s=o(1445),i=o(1542),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)},1625:function(e,t,o){var s,i;s=o(1446),i=o(1543),e.exports=s||{},e.exports.__esModule&&(e.exports=e.exports.default),i&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=i)}});
//# sourceMappingURL=22.c4485eb1f4ecaa99fee5.js.map