(self.webpackChunkPaddleLabel_Frontend=self.webpackChunkPaddleLabel_Frontend||[]).push([[531],{34687:function(S){S.exports={container:"container___1sYa-",lang:"lang___l6cji",content:"content___2zk1-",icon:"icon___rzGKO",logo:"logo___2hXsy"}},80979:function(S,T,a){"use strict";a.r(T),a.d(T,{default:function(){return _}});var ne=a(18106),Z=a(35576),ue=a(34792),y=a(48086),f=a(11849),v=a(3182),N=a(2824),le=a(17462),E=a(76772),G=a(94043),o=a.n(G),D=a(78874),W=a(11013),Y=a(89366),I=a(2603),K=a(80521),P=a(67294),R=a(83039),L=a(5966),V=a(16434),X=a(63434),r=a(48971),J=a(29791),Q=a(36571);function w(x,p){return B.apply(this,arguments)}function B(){return B=(0,v.Z)(o().mark(function x(p,m){return o().wrap(function(h){for(;;)switch(h.prev=h.next){case 0:return h.abrupt("return",(0,r.WY)("/api/login/captcha",(0,f.Z)({method:"GET",params:(0,f.Z)({},p)},m||{})));case 1:case"end":return h.stop()}},x)})),B.apply(this,arguments)}var k=a(34687),g=a.n(k),e=a(85893),b=function(p){var m=p.content;return(0,e.jsx)(E.Z,{style:{marginBottom:24},message:m,type:"error",showIcon:!0})},q=function(){var p=(0,P.useState)({}),m=(0,N.Z)(p,2),C=m[0],h=m[1],ee=(0,P.useState)("account"),A=(0,N.Z)(ee,2),M=A[0],ae=A[1],H=(0,r.tT)("@@initialState"),j=H.initialState,se=H.setInitialState,n=(0,r.YB)(),re=function(){var c=(0,v.Z)(o().mark(function u(){var l,i;return o().wrap(function(s){for(;;)switch(s.prev=s.next){case 0:return s.next=2,j==null||(l=j.fetchUserInfo)===null||l===void 0?void 0:l.call(j);case 2:if(i=s.sent,!i){s.next=6;break}return s.next=6,se(function(F){return(0,f.Z)((0,f.Z)({},F),{},{currentUser:i})});case 6:case"end":return s.stop()}},u)}));return function(){return c.apply(this,arguments)}}(),te=function(){var c=(0,v.Z)(o().mark(function u(l){var i,d,s,F,z,$;return o().wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,(0,Q.x4)((0,f.Z)((0,f.Z)({},l),{},{type:M}));case 3:if(i=t.sent,i.status!=="ok"){t.next=15;break}return d=n.formatMessage({id:"pages.login.success",defaultMessage:"\u767B\u5F55\u6210\u529F\uFF01"}),y.default.success(d),t.next=9,re();case 9:if(r.m8){t.next=11;break}return t.abrupt("return");case 11:return s=r.m8.location.query,F=s,z=F.redirect,r.m8.push(z||"/"),t.abrupt("return");case 15:console.log(i),h(i),t.next=23;break;case 19:t.prev=19,t.t0=t.catch(0),$=n.formatMessage({id:"pages.login.failure",defaultMessage:"\u767B\u5F55\u5931\u8D25\uFF0C\u8BF7\u91CD\u8BD5\uFF01"}),y.default.error($);case 23:case"end":return t.stop()}},u,null,[[0,19]])}));return function(l){return c.apply(this,arguments)}}(),O=C.status,U=C.type;return(0,e.jsxs)("div",{className:"".concat(g().container," container"),children:[(0,e.jsx)("div",{className:g().lang,"data-lang":!0,children:r.pD&&(0,e.jsx)(r.pD,{})}),(0,e.jsx)("div",{className:g().content,children:(0,e.jsxs)(R.U,{logo:(0,e.jsx)("img",{id:g().logo,alt:"logo",src:"./logo.png"}),title:"",subTitle:n.formatMessage({id:"pages.layouts.userLayout.title"}),initialValues:{autoLogin:!0},actions:[(0,e.jsx)(r._H,{id:"pages.login.loginWith",defaultMessage:"\u5176\u4ED6\u767B\u5F55\u65B9\u5F0F"},"loginWith"),(0,e.jsx)(D.Z,{className:g().icon},"AlipayCircleOutlined"),(0,e.jsx)(W.Z,{className:g().icon},"TaobaoCircleOutlined")],onFinish:function(){var c=(0,v.Z)(o().mark(function u(l){return o().wrap(function(d){for(;;)switch(d.prev=d.next){case 0:return d.next=2,te(l);case 2:case"end":return d.stop()}},u)}));return function(u){return c.apply(this,arguments)}}(),children:[(0,e.jsxs)(Z.Z,{activeKey:M,onChange:ae,children:[(0,e.jsx)(Z.Z.TabPane,{tab:n.formatMessage({id:"pages.login.accountLogin.tab",defaultMessage:"\u8D26\u6237\u5BC6\u7801\u767B\u5F55"})},"account"),(0,e.jsx)(Z.Z.TabPane,{tab:n.formatMessage({id:"pages.login.phoneLogin.tab",defaultMessage:"\u624B\u673A\u53F7\u767B\u5F55"})},"mobile")]}),O==="error"&&U==="account"&&(0,e.jsx)(b,{content:n.formatMessage({id:"pages.login.accountLogin.errorMessage",defaultMessage:"\u8D26\u6237\u6216\u5BC6\u7801\u9519\u8BEF(admin/ant.design)"})}),M==="account"&&(0,e.jsxs)(e.Fragment,{children:[(0,e.jsx)(L.Z,{name:"username",fieldProps:{size:"large",prefix:(0,e.jsx)(Y.Z,{className:g().prefixIcon})},placeholder:n.formatMessage({id:"pages.login.username.placeholder",defaultMessage:"\u7528\u6237\u540D: admin or user"}),rules:[{required:!0,message:(0,e.jsx)(r._H,{id:"pages.login.username.required",defaultMessage:"\u8BF7\u8F93\u5165\u7528\u6237\u540D!"})}]}),(0,e.jsx)(L.Z.Password,{name:"password",fieldProps:{size:"large",prefix:(0,e.jsx)(I.Z,{className:g().prefixIcon})},placeholder:n.formatMessage({id:"pages.login.password.placeholder",defaultMessage:"\u5BC6\u7801: ant.design"}),rules:[{required:!0,message:(0,e.jsx)(r._H,{id:"pages.login.password.required",defaultMessage:"\u8BF7\u8F93\u5165\u5BC6\u7801\uFF01"})}]})]}),O==="error"&&U==="mobile"&&(0,e.jsx)(b,{content:"\u9A8C\u8BC1\u7801\u9519\u8BEF"}),M==="mobile"&&(0,e.jsxs)(e.Fragment,{children:[(0,e.jsx)(L.Z,{fieldProps:{size:"large",prefix:(0,e.jsx)(K.Z,{className:g().prefixIcon})},name:"mobile",placeholder:n.formatMessage({id:"pages.login.phoneNumber.placeholder",defaultMessage:"\u624B\u673A\u53F7"}),rules:[{required:!0,message:(0,e.jsx)(r._H,{id:"pages.login.phoneNumber.required",defaultMessage:"\u8BF7\u8F93\u5165\u624B\u673A\u53F7\uFF01"})},{pattern:/^1\d{10}$/,message:(0,e.jsx)(r._H,{id:"pages.login.phoneNumber.invalid",defaultMessage:"\u624B\u673A\u53F7\u683C\u5F0F\u9519\u8BEF\uFF01"})}]}),(0,e.jsx)(V.Z,{fieldProps:{size:"large",prefix:(0,e.jsx)(I.Z,{className:g().prefixIcon})},captchaProps:{size:"large"},placeholder:n.formatMessage({id:"pages.login.captcha.placeholder",defaultMessage:"\u8BF7\u8F93\u5165\u9A8C\u8BC1\u7801"}),captchaTextRender:function(u,l){return u?"".concat(l," ").concat(n.formatMessage({id:"pages.getCaptchaSecondText",defaultMessage:"\u83B7\u53D6\u9A8C\u8BC1\u7801"})):n.formatMessage({id:"pages.login.phoneLogin.getVerificationCode",defaultMessage:"\u83B7\u53D6\u9A8C\u8BC1\u7801"})},name:"captcha",rules:[{required:!0,message:(0,e.jsx)(r._H,{id:"pages.login.captcha.required",defaultMessage:"\u8BF7\u8F93\u5165\u9A8C\u8BC1\u7801\uFF01"})}],onGetCaptcha:function(){var c=(0,v.Z)(o().mark(function u(l){var i;return o().wrap(function(s){for(;;)switch(s.prev=s.next){case 0:return s.next=2,w({phone:l});case 2:if(i=s.sent,i!==!1){s.next=5;break}return s.abrupt("return");case 5:y.default.success(n.formatMessage({id:"pages.login.getFakeCaptchaMessage"}));case 6:case"end":return s.stop()}},u)}));return function(u){return c.apply(this,arguments)}}()})]}),(0,e.jsxs)("div",{style:{marginBottom:24},children:[(0,e.jsx)(X.Z,{noStyle:!0,name:"autoLogin",children:(0,e.jsx)(r._H,{id:"pages.login.rememberMe",defaultMessage:"\u81EA\u52A8\u767B\u5F55"})}),(0,e.jsx)("a",{style:{float:"right"},children:(0,e.jsx)(r._H,{id:"pages.login.forgotPassword",defaultMessage:"\u5FD8\u8BB0\u5BC6\u7801"})})]})]})}),(0,e.jsx)(J.Z,{})]})},_=q}}]);
