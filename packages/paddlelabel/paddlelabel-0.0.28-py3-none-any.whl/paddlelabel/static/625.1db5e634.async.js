(self.webpackChunkPaddleLabel_Frontend=self.webpackChunkPaddleLabel_Frontend||[]).push([[625],{34442:function(){},93766:function(rr,Se,s){"use strict";s.d(Se,{Z:function(){return Ur}});var p=s(22122),ue=s(90484),B=s(28481),I=s(96156),a=s(67294),we=s(94184),re=s.n(we),te=s(66646),ge=s(65632),Pe=s(98423),oe=a.createContext({labelAlign:"right",vertical:!1,itemRef:function(){}}),Me=a.createContext(null),tr=function(r){var n=(0,Pe.Z)(r,["prefixCls"]);return a.createElement(te.FormProvider,n)},be=a.createContext({prefixCls:""});function Le(e){return typeof e=="object"&&e!=null&&e.nodeType===1}function Te(e,r){return(!r||e!=="hidden")&&e!=="visible"&&e!=="clip"}function Ee(e,r){if(e.clientHeight<e.scrollHeight||e.clientWidth<e.scrollWidth){var n=getComputedStyle(e,null);return Te(n.overflowY,r)||Te(n.overflowX,r)||function(t){var l=function(o){if(!o.ownerDocument||!o.ownerDocument.defaultView)return null;try{return o.ownerDocument.defaultView.frameElement}catch(i){return null}}(t);return!!l&&(l.clientHeight<t.scrollHeight||l.clientWidth<t.scrollWidth)}(e)}return!1}function he(e,r,n,t,l,o,i,c){return o<e&&i>r||o>e&&i<r?0:o<=e&&c<=n||i>=r&&c>=n?o-e-t:i>r&&c<n||o<e&&c>n?i-r+l:0}function Ae(e,r){var n=window,t=r.scrollMode,l=r.block,o=r.inline,i=r.boundary,c=r.skipOverflowHiddenElements,m=typeof i=="function"?i:function(pe){return pe!==i};if(!Le(e))throw new TypeError("Invalid target");for(var v=document.scrollingElement||document.documentElement,y=[],d=e;Le(d)&&m(d);){if((d=d.parentElement)===v){y.push(d);break}d!=null&&d===document.body&&Ee(d)&&!Ee(document.documentElement)||d!=null&&Ee(d,c)&&y.push(d)}for(var u=n.visualViewport?n.visualViewport.width:innerWidth,g=n.visualViewport?n.visualViewport.height:innerHeight,F=window.scrollX||pageXOffset,f=window.scrollY||pageYOffset,h=e.getBoundingClientRect(),L=h.height,R=h.width,w=h.top,A=h.right,T=h.bottom,P=h.left,C=l==="start"||l==="nearest"?w:l==="end"?T:w+L/2,b=o==="center"?P+R/2:o==="end"?A:P,H=[],N=0;N<y.length;N++){var Z=y[N],W=Z.getBoundingClientRect(),U=W.height,V=W.width,j=W.top,M=W.right,Y=W.bottom,$=W.left;if(t==="if-needed"&&w>=0&&P>=0&&T<=g&&A<=u&&w>=j&&T<=Y&&P>=$&&A<=M)return H;var G=getComputedStyle(Z),q=parseInt(G.borderLeftWidth,10),_=parseInt(G.borderTopWidth,10),ae=parseInt(G.borderRightWidth,10),Q=parseInt(G.borderBottomWidth,10),D=0,O=0,ie="offsetWidth"in Z?Z.offsetWidth-Z.clientWidth-q-ae:0,se="offsetHeight"in Z?Z.offsetHeight-Z.clientHeight-_-Q:0;if(v===Z)D=l==="start"?C:l==="end"?C-g:l==="nearest"?he(f,f+g,g,_,Q,f+C,f+C+L,L):C-g/2,O=o==="start"?b:o==="center"?b-u/2:o==="end"?b-u:he(F,F+u,u,q,ae,F+b,F+b+R,R),D=Math.max(0,D+f),O=Math.max(0,O+F);else{D=l==="start"?C-j-_:l==="end"?C-Y+Q+se:l==="nearest"?he(j,Y,U,_,Q+se,C,C+L,L):C-(j+U/2)+se/2,O=o==="start"?b-$-q:o==="center"?b-($+V/2)+ie/2:o==="end"?b-M+ae+ie:he($,M,V,q,ae+ie,b,b+R,R);var Ce=Z.scrollLeft,ye=Z.scrollTop;C+=ye-(D=Math.max(0,Math.min(ye+D,Z.scrollHeight-U+se))),b+=Ce-(O=Math.max(0,Math.min(Ce+O,Z.scrollWidth-V+ie)))}H.push({el:Z,top:D,left:O})}return H}function Ve(e){return e===Object(e)&&Object.keys(e).length!==0}function nr(e,r){r===void 0&&(r="auto");var n="scrollBehavior"in document.body.style;e.forEach(function(t){var l=t.el,o=t.top,i=t.left;l.scroll&&n?l.scroll({top:o,left:i,behavior:r}):(l.scrollTop=o,l.scrollLeft=i)})}function ar(e){return e===!1?{block:"end",inline:"nearest"}:Ve(e)?e:{block:"start",inline:"nearest"}}function lr(e,r){var n=e.isConnected||e.ownerDocument.documentElement.contains(e);if(Ve(r)&&typeof r.behavior=="function")return r.behavior(n?Ae(e,r):[]);if(!!n){var t=ar(r);return nr(Ae(e,t),t.behavior)}}var or=lr,ir=["parentNode"],sr="form_item";function de(e){return e===void 0||e===!1?[]:Array.isArray(e)?e:[e]}function je(e,r){if(!!e.length){var n=e.join("_");if(r)return"".concat(r,"_").concat(n);var t=ir.indexOf(n)>=0;return t?"".concat(sr,"_").concat(n):n}}function We(e){var r=de(e);return r.join("_")}function $e(e){var r=(0,te.useForm)(),n=(0,B.Z)(r,1),t=n[0],l=a.useRef({}),o=a.useMemo(function(){return e!=null?e:(0,p.Z)((0,p.Z)({},t),{__INTERNAL__:{itemRef:function(c){return function(m){var v=We(c);m?l.current[v]=m:delete l.current[v]}}},scrollToField:function(c){var m=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},v=de(c),y=je(v,o.__INTERNAL__.name),d=y?document.getElementById(y):null;d&&or(d,(0,p.Z)({scrollMode:"if-needed",block:"nearest"},m))},getFieldInstance:function(c){var m=We(c);return l.current[m]}})},[e,t]);return[o]}var De=s(97647),cr=function(e,r){var n={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var l=0,t=Object.getOwnPropertySymbols(e);l<t.length;l++)r.indexOf(t[l])<0&&Object.prototype.propertyIsEnumerable.call(e,t[l])&&(n[t[l]]=e[t[l]]);return n},ur=function(r,n){var t,l=a.useContext(De.Z),o=a.useContext(ge.E_),i=o.getPrefixCls,c=o.direction,m=o.form,v=r.prefixCls,y=r.className,d=y===void 0?"":y,u=r.size,g=u===void 0?l:u,F=r.form,f=r.colon,h=r.labelAlign,L=r.labelWrap,R=r.labelCol,w=r.wrapperCol,A=r.hideRequiredMark,T=r.layout,P=T===void 0?"horizontal":T,C=r.scrollToFirstError,b=r.requiredMark,H=r.onFinishFailed,N=r.name,Z=cr(r,["prefixCls","className","size","form","colon","labelAlign","labelWrap","labelCol","wrapperCol","hideRequiredMark","layout","scrollToFirstError","requiredMark","onFinishFailed","name"]),W=(0,a.useMemo)(function(){return b!==void 0?b:m&&m.requiredMark!==void 0?m.requiredMark:!A},[A,b,m]),U=f!=null?f:m==null?void 0:m.colon,V=i("form",v),j=re()(V,(t={},(0,I.Z)(t,"".concat(V,"-").concat(P),!0),(0,I.Z)(t,"".concat(V,"-hide-required-mark"),W===!1),(0,I.Z)(t,"".concat(V,"-rtl"),c==="rtl"),(0,I.Z)(t,"".concat(V,"-").concat(g),g),t),d),M=$e(F),Y=(0,B.Z)(M,1),$=Y[0],G=$.__INTERNAL__;G.name=N;var q=(0,a.useMemo)(function(){return{name:N,labelAlign:h,labelCol:R,labelWrap:L,wrapperCol:w,vertical:P==="vertical",colon:U,requiredMark:W,itemRef:G.itemRef}},[N,h,R,w,P,U,W]);a.useImperativeHandle(n,function(){return $});var _=function(Q){H==null||H(Q);var D={block:"nearest"};C&&Q.errorFields.length&&((0,ue.Z)(C)==="object"&&(D=C),$.scrollToField(Q.errorFields[0].name,D))};return a.createElement(De.q,{size:g},a.createElement(oe.Provider,{value:q},a.createElement(te.default,(0,p.Z)({id:N},Z,{name:N,onFinishFailed:_,form:$,className:j}))))},dr=a.forwardRef(ur),mr=dr,K=s(85061),Ue=s(42550),fr=s(92820),vr=s(93355),k=s(21687),gr=s(1870),ze=s(21584),hr=s(42051),Cr=s(85636),yr=s(31097),pr=function(e,r){var n={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var l=0,t=Object.getOwnPropertySymbols(e);l<t.length;l++)r.indexOf(t[l])<0&&Object.prototype.propertyIsEnumerable.call(e,t[l])&&(n[t[l]]=e[t[l]]);return n};function Fr(e){return e?(0,ue.Z)(e)==="object"&&!a.isValidElement(e)?e:{title:e}:null}var br=function(r){var n=r.prefixCls,t=r.label,l=r.htmlFor,o=r.labelCol,i=r.labelAlign,c=r.colon,m=r.required,v=r.requiredMark,y=r.tooltip,d=(0,hr.E)("Form"),u=(0,B.Z)(d,1),g=u[0];return t?a.createElement(oe.Consumer,{key:"label"},function(F){var f,h=F.vertical,L=F.labelAlign,R=F.labelCol,w=F.labelWrap,A=F.colon,T,P=o||R||{},C=i||L,b="".concat(n,"-item-label"),H=re()(b,C==="left"&&"".concat(b,"-left"),P.className,(0,I.Z)({},"".concat(b,"-wrap"),!!w)),N=t,Z=c===!0||A!==!1&&c!==!1,W=Z&&!h;W&&typeof t=="string"&&t.trim()!==""&&(N=t.replace(/[:|：]\s*$/,""));var U=Fr(y);if(U){var V=U.icon,j=V===void 0?a.createElement(gr.Z,null):V,M=pr(U,["icon"]),Y=a.createElement(yr.Z,M,a.cloneElement(j,{className:"".concat(n,"-item-tooltip"),title:""}));N=a.createElement(a.Fragment,null,N,Y)}v==="optional"&&!m&&(N=a.createElement(a.Fragment,null,N,a.createElement("span",{className:"".concat(n,"-item-optional"),title:""},(g==null?void 0:g.optional)||((T=Cr.Z.Form)===null||T===void 0?void 0:T.optional))));var $=re()((f={},(0,I.Z)(f,"".concat(n,"-item-required"),m),(0,I.Z)(f,"".concat(n,"-item-required-mark-optional"),v==="optional"),(0,I.Z)(f,"".concat(n,"-item-no-colon"),!Z),f));return a.createElement(ze.Z,(0,p.Z)({},P,{className:H}),a.createElement("label",{htmlFor:l,className:$,title:typeof t=="string"?t:""},N))}):null},Er=br,Zr=s(7085),xr=s(43061),Rr=s(38819),Nr=s(68855),Be=s(60444),Ke=s(33603),He=[];function Ze(e,r,n){var t=arguments.length>3&&arguments[3]!==void 0?arguments[3]:0;return{key:typeof e=="string"?e:"".concat(n,"-").concat(t),error:e,errorStatus:r}}function Ye(e){var r=e.help,n=e.helpStatus,t=e.errors,l=t===void 0?He:t,o=e.warnings,i=o===void 0?He:o,c=e.className,m=a.useContext(be),v=m.prefixCls,y=a.useContext(ge.E_),d=y.getPrefixCls,u="".concat(v,"-item-explain"),g=d(),F=a.useMemo(function(){return r!=null?[Ze(r,n,"help")]:[].concat((0,K.Z)(l.map(function(f,h){return Ze(f,"error","error",h)})),(0,K.Z)(i.map(function(f,h){return Ze(f,"warning","warning",h)})))},[r,n,l,i]);return a.createElement(Be.Z,(0,p.Z)({},Ke.Z,{motionName:"".concat(g,"-show-help"),motionAppear:!1,motionEnter:!1,visible:!!F.length,onLeaveStart:function(h){return h.style.height="auto",{height:h.offsetHeight}}}),function(f){var h=f.className,L=f.style;return a.createElement("div",{className:re()(u,h,c),style:L},a.createElement(Be.V,(0,p.Z)({keys:F},Ke.Z,{motionName:"".concat(g,"-show-help-item"),component:!1}),function(R){var w=R.key,A=R.error,T=R.errorStatus,P=R.className,C=R.style;return a.createElement("div",{key:w,role:"alert",className:re()(P,(0,I.Z)({},"".concat(u,"-").concat(T),T)),style:C},A)}))})}var Ir={success:Rr.Z,warning:Nr.Z,error:xr.Z,validating:Zr.Z},Or=function(r){var n=r.prefixCls,t=r.status,l=r.wrapperCol,o=r.children,i=r.errors,c=r.warnings,m=r.hasFeedback,v=r._internalItemRender,y=r.validateStatus,d=r.extra,u=r.help,g="".concat(n,"-item"),F=a.useContext(oe),f=l||F.wrapperCol||{},h=re()("".concat(g,"-control"),f.className),L=y&&Ir[y],R=m&&L?a.createElement("span",{className:"".concat(g,"-children-icon")},a.createElement(L,null)):null,w=a.useMemo(function(){return(0,p.Z)({},F)},[F]);delete w.labelCol,delete w.wrapperCol;var A=a.createElement("div",{className:"".concat(g,"-control-input")},a.createElement("div",{className:"".concat(g,"-control-input-content")},o),R),T=a.useMemo(function(){return{prefixCls:n,status:t}},[n,t]),P=a.createElement(be.Provider,{value:T},a.createElement(Ye,{errors:i,warnings:c,help:u,helpStatus:t,className:"".concat(g,"-explain-connected")})),C=d?a.createElement("div",{className:"".concat(g,"-extra")},d):null,b=v&&v.mark==="pro_table_render"&&v.render?v.render(r,{input:A,errorList:P,extra:C}):a.createElement(a.Fragment,null,A,P,C);return a.createElement(oe.Provider,{value:w},a.createElement(ze.Z,(0,p.Z)({},f,{className:h}),b))},Sr=Or,ke=s(96159),Qe=s(75164);function wr(e){var r=a.useState(e),n=(0,B.Z)(r,2),t=n[0],l=n[1],o=(0,a.useRef)(null),i=(0,a.useRef)([]),c=(0,a.useRef)(!1);a.useEffect(function(){return function(){c.current=!0,Qe.Z.cancel(o.current)}},[]);function m(v){c.current||(o.current===null&&(i.current=[],o.current=(0,Qe.Z)(function(){o.current=null,l(function(y){var d=y;return i.current.forEach(function(u){d=u(d)}),d})})),i.current.push(v))}return[t,m]}function Xe(e){var r=a.useState(e),n=(0,B.Z)(r,2),t=n[0],l=n[1];return a.useEffect(function(){var o=setTimeout(function(){l(e)},e.length?0:10);return function(){clearTimeout(o)}},[e]),t}function Pr(){var e=a.useContext(oe),r=e.itemRef,n=a.useRef({});function t(l,o){var i=o&&(0,ue.Z)(o)==="object"&&o.ref,c=l.join("_");return(n.current.name!==c||n.current.originRef!==i)&&(n.current.name=c,n.current.originRef=i,n.current.ref=(0,Ue.sQ)(r(l),i)),n.current.ref}return t}var Mr=function(e,r){var n={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var l=0,t=Object.getOwnPropertySymbols(e);l<t.length;l++)r.indexOf(t[l])<0&&Object.prototype.propertyIsEnumerable.call(e,t[l])&&(n[t[l]]=e[t[l]]);return n},Lr="__SPLIT__",Yr=(0,vr.b)("success","warning","error","validating",""),Tr=a.memo(function(e){var r=e.children;return r},function(e,r){return e.value===r.value&&e.update===r.update});function Ar(e){return e===null&&(0,k.Z)(!1,"Form.Item","`null` is passed as `name` property"),e!=null}function Je(){return{errors:[],warnings:[],touched:!1,validating:!1,name:[]}}function Vr(e){var r=e.name,n=e.noStyle,t=e.dependencies,l=e.prefixCls,o=e.style,i=e.className,c=e.shouldUpdate,m=e.hasFeedback,v=e.help,y=e.rules,d=e.validateStatus,u=e.children,g=e.required,F=e.label,f=e.messageVariables,h=e.trigger,L=h===void 0?"onChange":h,R=e.validateTrigger,w=e.hidden,A=Mr(e,["name","noStyle","dependencies","prefixCls","style","className","shouldUpdate","hasFeedback","help","rules","validateStatus","children","required","label","messageVariables","trigger","validateTrigger","hidden"]),T=(0,a.useContext)(ge.E_),P=T.getPrefixCls,C=(0,a.useContext)(oe),b=C.name,H=C.requiredMark,N=typeof u=="function",Z=(0,a.useContext)(Me),W=(0,a.useContext)(te.FieldContext),U=W.validateTrigger,V=R!==void 0?R:U,j=Ar(r),M=P("form",l),Y=a.useContext(te.ListContext),$=a.useRef(),G=wr({}),q=(0,B.Z)(G,2),_=q[0],ae=q[1],Q=a.useState(function(){return Je()}),D=(0,B.Z)(Q,2),O=D[0],ie=D[1],se=function(S){var z=Y==null?void 0:Y.getKey(S.name);if(ie(S.destroy?Je():S),n&&Z){var E=S.name;if(S.destroy)E=$.current||E;else if(z!==void 0){var x=(0,B.Z)(z,2),le=x[0],ee=x[1];E=[le].concat((0,K.Z)(ee)),$.current=E}Z(S,E)}},Ce=function(S,z){ae(function(E){var x=(0,p.Z)({},E),le=[].concat((0,K.Z)(S.name.slice(0,-1)),(0,K.Z)(z)),ee=le.join(Lr);return S.destroy?delete x[ee]:x[ee]=S,x})},ye=a.useMemo(function(){var X=(0,K.Z)(O.errors),S=(0,K.Z)(O.warnings);return Object.values(_).forEach(function(z){X.push.apply(X,(0,K.Z)(z.errors||[])),S.push.apply(S,(0,K.Z)(z.warnings||[]))}),[X,S]},[_,O.errors,O.warnings]),pe=(0,B.Z)(ye,2),zr=pe[0],Br=pe[1],xe=Xe(zr),Re=Xe(Br),Kr=Pr();function Ge(X,S,z){var E;if(n&&!w)return X;var x="";d!==void 0?x=d:(O==null?void 0:O.validating)?x="validating":xe.length?x="error":Re.length?x="warning":(O==null?void 0:O.touched)&&(x="success");var le=(E={},(0,I.Z)(E,"".concat(M,"-item"),!0),(0,I.Z)(E,"".concat(M,"-item-with-help"),v!=null||xe.length||Re.length),(0,I.Z)(E,"".concat(i),!!i),(0,I.Z)(E,"".concat(M,"-item-has-feedback"),x&&m),(0,I.Z)(E,"".concat(M,"-item-has-success"),x==="success"),(0,I.Z)(E,"".concat(M,"-item-has-warning"),x==="warning"),(0,I.Z)(E,"".concat(M,"-item-has-error"),x==="error"),(0,I.Z)(E,"".concat(M,"-item-is-validating"),x==="validating"),(0,I.Z)(E,"".concat(M,"-item-hidden"),w),E);return a.createElement(fr.Z,(0,p.Z)({className:re()(le),style:o,key:"row"},(0,Pe.Z)(A,["colon","extra","fieldKey","getValueFromEvent","getValueProps","htmlFor","id","initialValue","isListField","labelAlign","labelWrap","labelCol","normalize","preserve","tooltip","validateFirst","valuePropName","wrapperCol","_internalItemRender"])),a.createElement(Er,(0,p.Z)({htmlFor:S,required:z,requiredMark:H},e,{prefixCls:M})),a.createElement(Sr,(0,p.Z)({},e,O,{errors:xe,warnings:Re,prefixCls:M,status:x,validateStatus:x,help:v}),a.createElement(Me.Provider,{value:Ce},X)))}if(!j&&!N&&!t)return Ge(u);var me={};return typeof F=="string"?me.label=F:r&&(me.label=String(r)),f&&(me=(0,p.Z)((0,p.Z)({},me),f)),a.createElement(te.Field,(0,p.Z)({},e,{messageVariables:me,trigger:L,validateTrigger:V,onMetaChange:se}),function(X,S,z){var E=de(r).length&&S?S.name:[],x=je(E,b),le=g!==void 0?g:!!(y&&y.some(function(J){if(J&&(0,ue.Z)(J)==="object"&&J.required&&!J.warningOnly)return!0;if(typeof J=="function"){var ce=J(z);return ce&&ce.required&&!ce.warningOnly}return!1})),ee=(0,p.Z)({},X),fe=null;if((0,k.Z)(!(c&&t),"Form.Item","`shouldUpdate` and `dependencies` shouldn't be used together. See https://ant.design/components/form/#dependencies."),Array.isArray(u)&&j)(0,k.Z)(!1,"Form.Item","`children` is array of render props cannot have `name`."),fe=u;else if(N&&(!(c||t)||j))(0,k.Z)(!!(c||t),"Form.Item","`children` of render props only work with `shouldUpdate` or `dependencies`."),(0,k.Z)(!j,"Form.Item","Do not use `name` with `children` of render props since it's not a field.");else if(t&&!N&&!j)(0,k.Z)(!1,"Form.Item","Must set `name` or use render props when `dependencies` is set.");else if((0,ke.l$)(u)){(0,k.Z)(u.props.defaultValue===void 0,"Form.Item","`defaultValue` will not work on controlled Field. You should use `initialValues` of Form instead.");var ve=(0,p.Z)((0,p.Z)({},u.props),ee);ve.id||(ve.id=x),(0,Ue.Yr)(u)&&(ve.ref=Kr(E,u));var Hr=new Set([].concat((0,K.Z)(de(L)),(0,K.Z)(de(V))));Hr.forEach(function(J){ve[J]=function(){for(var ce,qe,Ne,_e,Ie,er=arguments.length,Oe=new Array(er),Fe=0;Fe<er;Fe++)Oe[Fe]=arguments[Fe];(Ne=ee[J])===null||Ne===void 0||(ce=Ne).call.apply(ce,[ee].concat(Oe)),(Ie=(_e=u.props)[J])===null||Ie===void 0||(qe=Ie).call.apply(qe,[_e].concat(Oe))}}),fe=a.createElement(Tr,{value:ee[e.valuePropName||"value"],update:u},(0,ke.Tm)(u,ve))}else N&&(c||t)&&!j?fe=u(z):((0,k.Z)(!E.length,"Form.Item","`name` is only used for validate React element. If you are using Form.Item as layout display, please remove `name` instead."),fe=u);return Ge(fe,x,le)})}var jr=Vr,Wr=function(e,r){var n={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&r.indexOf(t)<0&&(n[t]=e[t]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var l=0,t=Object.getOwnPropertySymbols(e);l<t.length;l++)r.indexOf(t[l])<0&&Object.prototype.propertyIsEnumerable.call(e,t[l])&&(n[t[l]]=e[t[l]]);return n},$r=function(r){var n=r.prefixCls,t=r.children,l=Wr(r,["prefixCls","children"]);(0,k.Z)(!!l.name,"Form.List","Miss `name` prop.");var o=a.useContext(ge.E_),i=o.getPrefixCls,c=i("form",n),m=a.useMemo(function(){return{prefixCls:c,status:"error"}},[c]);return a.createElement(te.List,l,function(v,y,d){return a.createElement(be.Provider,{value:m},t(v.map(function(u){return(0,p.Z)((0,p.Z)({},u),{fieldKey:u.key})}),y,{errors:d.errors,warnings:d.warnings}))})},Dr=$r,ne=mr;ne.Item=jr,ne.List=Dr,ne.ErrorList=Ye,ne.useForm=$e,ne.Provider=tr,ne.create=function(){(0,k.Z)(!1,"Form","antd v4 removed `Form.create`. Please remove or use `@ant-design/compatible` instead.")};var Ur=ne},9715:function(rr,Se,s){"use strict";var p=s(38663),ue=s.n(p),B=s(34442),I=s.n(B),a=s(6999),we=s(22385)}}]);
