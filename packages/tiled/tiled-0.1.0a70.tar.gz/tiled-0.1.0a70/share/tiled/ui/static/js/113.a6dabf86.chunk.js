"use strict";(self.webpackChunktiled=self.webpackChunktiled||[]).push([[113],{91697:function(n,e,t){t(72791);var r=t(54535),i=t(64554),a=t(68096),c=t(47071),s=t(30829),o=t(77865),l=t(80184);e.Z=function(n){var e=Array.from(Array(n.npartitions).keys());return(0,l.jsx)(i.Z,{children:(0,l.jsxs)(a.Z,{sx:{my:2},children:[(0,l.jsx)(s.Z,{id:"partition-select-helper-label",children:"Partition"}),(0,l.jsx)(r.Z,{labelId:"partition-select-label",id:"partition-select",value:n.value,label:"Partition",onChange:function(e){n.setValue(e.target.value)},children:e.map((function(n){return(0,l.jsx)(o.Z,{value:n,children:n},"partition-".concat(n))}))}),(0,l.jsx)(c.Z,{children:"A portion of the rows"})]})})}},87432:function(n,e,t){t.d(e,{U:function(){return P}});var r=t(1413),i=t(15861),a=t(70885),c=t(87757),s=t.n(c),o=t(72791),l=t(54535),u=t(64554),d=t(24518),f=t(50194),p=t(68096),m=t(13400),h=t(30829),x=t(77865),Z=t(18340),j=t(47047),v=t(53767),b=t(48550),g=t(20068),k=t(46348),y=t(1829),w=t.n(y),C=t(9478),S=t(80184),P=function(n){var e=(0,o.useState)(),t=(0,a.Z)(e,2),c=t[0],y=t[1],P=(0,o.useState)(),O=(0,a.Z)(P,2),F=O[0],_=O[1],A=o.useState(null),I=(0,a.Z)(A,2),L=I[0],M=I[1];(0,o.useMemo)((function(){function n(){return(n=(0,i.Z)(s().mark((function n(){var e;return s().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,(0,k.jZ)();case 2:e=n.sent,_(e);case 4:case"end":return n.stop()}}),n)})))).apply(this,arguments)}!function(){n.apply(this,arguments)}()}),[]),(0,o.useEffect)((function(){var e=new AbortController;function t(){return t=(0,i.Z)(s().mark((function t(){var r,i;return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,(0,C.M)(e.signal);case 2:r=t.sent,i=r.structure_families[n.structureFamily].formats,y(i);case 5:case"end":return t.stop()}}),t)}))),t.apply(this,arguments)}return function(){t.apply(this,arguments)}(),function(){e.abort()}}),[n.structureFamily]);var N=Boolean(L),U=N?"link-popover":void 0;if(void 0===c||void 0===F)return(0,S.jsx)(j.Z,{variant:"rectangular"});var V=void 0!==n.format?n.format.mimetype:"";return(0,S.jsxs)(v.Z,{spacing:2,direction:"column",children:[(0,S.jsx)(u.Z,{sx:{minWidth:120},children:(0,S.jsxs)(p.Z,{fullWidth:!0,children:[(0,S.jsx)(h.Z,{id:"formats-select-label",children:"Format *"}),(0,S.jsx)(l.Z,{labelId:"formats-select-label",id:"formats-select",value:V,label:"Format",onChange:function(e){var t=e.target.value,r=c.find((function(n){return n.mimetype===t}));n.setFormat(r)},required:!0,children:c.map((function(e){return F.formats[n.structureFamily].includes(e.mimetype)?(0,S.jsx)(x.Z,{value:e.mimetype,children:e.display_name},"format-".concat(e.mimetype)):""}))})]})}),(0,S.jsxs)(v.Z,{spacing:1,direction:"row",children:[(0,S.jsx)(g.Z,{title:"Download to a file",children:(0,S.jsx)("span",{children:(0,S.jsx)(d.Z,(0,r.Z)((0,r.Z)({component:"a",href:n.link?"".concat(n.link,"&filename=").concat(n.name).concat(n.format.extension):"#",variant:"outlined"},n.link?{}:{disabled:!0}),{},{children:"Download"}))})}),(0,S.jsx)(g.Z,{title:"Get a URL to this specific data",children:(0,S.jsx)("span",{children:(0,S.jsx)(d.Z,(0,r.Z)((0,r.Z)({"aria-describedby":U,variant:"outlined"},n.link?{}:{disabled:!0}),{},{onClick:function(n){M(n.currentTarget)},children:"Link"}))})}),(0,S.jsx)(Z.ZP,{id:U,open:N,anchorEl:L,onClose:function(){M(null)},anchorOrigin:{vertical:"bottom",horizontal:"right"},transformOrigin:{vertical:"top",horizontal:"right"},PaperProps:{style:{width:500}},children:(0,S.jsxs)(u.Z,{sx:{px:2,py:2},children:[(0,S.jsx)(v.Z,{direction:"row",spacing:1}),(0,S.jsx)(b.Z,{id:"link-text",label:"Link",sx:{width:"90%"},defaultValue:n.link,InputProps:{readOnly:!0},variant:"outlined"}),(0,S.jsx)(g.Z,{title:"Copy to clipboard",children:(0,S.jsx)(m.Z,{onClick:function(){w()(n.link)},children:(0,S.jsx)(f.Z,{})})})]})}),(0,S.jsx)(g.Z,{title:"Open in a new tab (if format is supported by web browser)",children:(0,S.jsx)("span",{children:(0,S.jsx)(d.Z,(0,r.Z)((0,r.Z)({component:"a",href:n.link?n.link:"#",target:"_blank",variant:"outlined"},n.link?{}:{disabled:!0}),{},{children:"Open"}))})})]})]})}},87113:function(n,e,t){t.r(e),t.d(e,{default:function(){return y}});var r=t(70885),i=t(72791),a=t(87432),c=t(64554),s=t(94454),o=t(91697),l=t(42982),u=t(24518),d=t(2199),f=t(90493),p=t(15021),m=t(76278),h=t(57064),x=t(49900),Z=t(79834),j=t(53767),v=t(80184),b=function(n){var e=function(e){return function(){var t=n.columns.indexOf(e),r=(0,l.Z)(n.columns);-1===t?r.push(e):r.splice(t,1),n.setColumns(r)}};return(0,v.jsxs)(j.Z,{spacing:1,direction:"column",children:[(0,v.jsx)(f.Z,{sx:{width:"100%",maxWidth:500,overflow:"auto",maxHeight:300,bgcolor:"background.paper"},subheader:(0,v.jsx)(Z.Z,{component:"div",id:"column-list-heading",children:n.heading}),children:n.allColumns.map((function(t){var r="checkbox-list-label-".concat(t);return(0,v.jsx)(p.ZP,{disablePadding:!0,children:(0,v.jsxs)(m.Z,{role:void 0,onClick:e(t),dense:!0,children:[(0,v.jsx)(h.Z,{children:(0,v.jsx)(s.Z,{edge:"start",checked:-1!==n.columns.indexOf(t),tabIndex:-1,disableRipple:!0,inputProps:{"aria-labelledby":r}})}),(0,v.jsx)(x.Z,{id:r,primary:t})]})},t)}))}),(0,v.jsxs)(d.Z,{variant:"text","aria-label":"check-all-or-none",children:[(0,v.jsx)(u.Z,{onClick:function(){n.setColumns(n.allColumns)},children:"Select All"}),(0,v.jsx)(u.Z,{onClick:function(){n.setColumns([])},children:"Select None"})]})]})},g=t(85523),k=t(79012),y=function(n){var e,t=n.macrostructure.npartitions,l=(0,i.useState)(),u=(0,r.Z)(l,2),d=u[0],f=u[1],p=(0,i.useState)(0),m=(0,r.Z)(p,2),h=m[0],x=m[1],Z=(0,i.useState)(1===t),y=(0,r.Z)(Z,2),w=y[0],C=y[1],S=(0,i.useState)(n.macrostructure.columns),P=(0,r.Z)(S,2),O=P[0],F=P[1];if(void 0!==d&&0!==O.length){if(e=w?"".concat(n.full_link,"?format=").concat(d.mimetype):"".concat(n.partition_link.replace("{index}",h.toString()),"&format=").concat(d.mimetype),O.join(",")!==n.macrostructure.columns.join(",")){var _=O.map((function(n){return"&field=".concat(n)})).join("");e=e.concat(_)}}else e="";return(0,v.jsx)(c.Z,{children:(0,v.jsxs)(j.Z,{spacing:2,direction:"column",children:[(0,v.jsxs)(j.Z,{spacing:1,direction:"row",children:[(0,v.jsx)(b,{heading:"Columns",allColumns:n.macrostructure.columns,columns:O,setColumns:F}),t>1?(0,v.jsxs)(c.Z,{children:[(0,v.jsx)(k.Z,{children:(0,v.jsx)(g.Z,{control:(0,v.jsx)(s.Z,{checked:w,onChange:function(n){C(n.target.checked)}}),label:"All rows"})}),w?"":(0,v.jsx)(o.Z,{npartitions:t,value:h,setValue:x})]}):""]}),(0,v.jsx)(a.U,{name:n.name,format:d,setFormat:f,structureFamily:n.structureFamily,link:e})]})})}},9478:function(n,e,t){t.d(e,{M:function(){return u}});var r=t(70885),i=t(15861),a=t(87757),c=t.n(a),s=t(88705),o=function(){var n=(0,i.Z)(c().mark((function n(e){var t,r,i;return c().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,fetch("".concat("/ui","/configuration_manifest.yml"),{signal:e});case 2:return t=n.sent,n.next=5,t.text();case 5:return r=n.sent,i=s.ZP.load(r),n.abrupt("return",i.manifest);case 8:case"end":return n.stop()}}),n)})));return function(e){return n.apply(this,arguments)}}(),l=function(){var n=(0,i.Z)(c().mark((function n(e,t){var r,i,a;return c().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,fetch("".concat("/ui","/").concat(e),{signal:t});case 2:return r=n.sent,n.next=5,r.text();case 5:return i=n.sent,a=s.ZP.load(i),n.abrupt("return",a);case 8:case"end":return n.stop()}}),n)})));return function(e,t){return n.apply(this,arguments)}}(),u=function(){var n=(0,i.Z)(c().mark((function n(e){var t,i,a,s,u;return c().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:if(null!==(t=sessionStorage.getItem("config"))){n.next=14;break}return n.next=4,o(e);case 4:return a=n.sent,n.next=7,Promise.all(a.map((function(n){return l(n,e)})));case 7:return s=n.sent,u={specs:[],structure_families:{}},s.map((function(n,e){(n.specs||[]).map((function(n){u.specs.push(n)}));for(var t=0,i=Object.entries(n.structure_families||{});t<i.length;t++){var c=(0,r.Z)(i[t],2),s=c[0],o=c[1];u.structure_families[s]=o}console.log("Loaded config ".concat(a[e]))})),sessionStorage.setItem("config",JSON.stringify(u)),n.abrupt("return",u);case 14:return i=t,n.abrupt("return",JSON.parse(i));case 16:case"end":return n.stop()}}),n)})));return function(e){return n.apply(this,arguments)}}()}}]);
//# sourceMappingURL=113.a6dabf86.chunk.js.map