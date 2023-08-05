/*! For license information please see 35.70c396fb.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[35],{1822:function(e,t,a){"use strict";a.r(t),a.d(t,"default",(function(){return E}));var n=a(5),r=a(17),i=a(9),s=a.n(i),o=a(67),c=a(2),u=a(4),h=a(6),l=a(7),d=a(0),g=a(75),f=a(24),p=a(240),b=a.n(p),v=a(212),w=a(189),m=a(96),O=a(1521),j=a(1254),x=a(8),y=Object(x.a)("div",{target:"e10fe9o10"})((function(e){var t=e.theme;return{"&.vega-embed":{".vega-actions":{zIndex:t.zIndices.popupMenu},summary:{height:"auto",zIndex:t.zIndices.menuButton}}}}),""),V=a(1),k="(index)",z="source",D=new Set(["datetimeIndex","float_64Index","int_64Index","rangeIndex","timedeltaIndex","uint_64Index"]),C=function(e){Object(h.a)(a,e);var t=Object(l.a)(a);function a(){var e;Object(c.a)(this,a);for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];return(e=t.call.apply(t,[this].concat(r))).vegaView=void 0,e.vegaFinalizer=void 0,e.defaultDataName=z,e.element=null,e.state={error:void 0},e.finalizeView=function(){e.vegaFinalizer&&e.vegaFinalizer(),e.vegaFinalizer=void 0,e.vegaView=void 0},e.generateSpec=function(){var t=e.props,a=t.element,n=t.theme,r=JSON.parse(a.get("spec")),i=JSON.parse(a.get("useContainerWidth"));if(r.config=T(r.config,n),e.props.height?(r.width=e.props.width-38,r.height=e.props.height):i&&(r.width=e.props.width-38),r.padding||(r.padding={}),null==r.padding.bottom&&(r.padding.bottom=20),r.datasets)throw new Error("Datasets should not be passed as part of the spec");return r},e}return Object(u.a)(a,[{key:"componentDidMount",value:function(){var e=Object(o.a)(s.a.mark((function e(){var t;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,this.createView();case 3:e.next=9;break;case 5:e.prev=5,e.t0=e.catch(0),t=Object(m.a)(e.t0),this.setState({error:t});case 9:case"end":return e.stop()}}),e,this,[[0,5]])})));return function(){return e.apply(this,arguments)}}()},{key:"componentWillUnmount",value:function(){this.finalizeView()}},{key:"componentDidUpdate",value:function(){var e=Object(o.a)(s.a.mark((function e(t){var a,n,i,o,c,u,h,l,d,g,p,b,v,w,O,j,x,y,V,k,z,D;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(a=t.element,n=t.theme,i=this.props,o=i.element,c=i.theme,u=a.get("spec"),h=o.get("spec"),this.vegaView&&u===h&&n===c&&t.width===this.props.width&&t.height===this.props.height){e.next=16;break}return Object(f.c)("Vega spec changed."),e.prev=6,e.next=9,this.createView();case 9:e.next=15;break;case 11:e.prev=11,e.t0=e.catch(6),l=Object(m.a)(e.t0),this.setState({error:l});case 15:return e.abrupt("return");case 16:for(d=a.get("data"),g=o.get("data"),(d||g)&&this.updateData(this.defaultDataName,d,g),p=I(a)||{},b=I(o)||{},v=0,w=Object.entries(b);v<w.length;v++)O=Object(r.a)(w[v],2),j=O[0],x=O[1],y=j||this.defaultDataName,V=p[y],this.updateData(y,V,x);for(k=0,z=Object.keys(p);k<z.length;k++)D=z[k],b.hasOwnProperty(D)||D===this.defaultDataName||this.updateData(D,null,null);this.vegaView.resize().runAsync();case 24:case"end":return e.stop()}}),e,this,[[6,11]])})));return function(t){return e.apply(this,arguments)}}()},{key:"updateData",value:function(e,t,a){if(!this.vegaView)throw new Error("Chart has not been drawn yet");if(a&&a.get("data"))if(t&&t.get("data")){var n=Object(w.g)(t.get("data")),i=Object(r.a)(n,2),s=i[0],o=i[1],c=Object(w.g)(a.get("data")),u=Object(r.a)(c,2),h=u[0];if(function(e,t,a,n,r,i){if(a!==i)return!1;if(t>=r)return!1;if(0===t)return!1;var s=e.get("data"),o=n.get("data"),c=i-1,u=t-1;if(Object(w.f)(s,c,0)!==Object(w.f)(o,c,0)||Object(w.f)(s,c,u)!==Object(w.f)(o,c,u))return!1;return!0}(t,s,o,a,h,u[1]))s<h&&this.vegaView.insert(e,N(a,s));else{var l=j.changeset().remove(j.truthy).insert(N(a));this.vegaView.change(e,l),Object(f.c)("Had to clear the ".concat(e," dataset before inserting data through Vega view."))}}else this.vegaView.insert(e,N(a));else this.vegaView._runtime.data.hasOwnProperty(e)&&this.vegaView.remove(e,j.truthy)}},{key:"createView",value:function(){var e=Object(o.a)(s.a.mark((function e(){var t,a,n,i,o,c,u,h,l,d,g,p,b,v,w,m;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(Object(f.c)("Creating a new Vega view."),this.element){e.next=3;break}throw Error("Element missing.");case 3:return this.finalizeView(),t=this.props.element,a=this.generateSpec(),e.next=8,Object(O.a)(this.element,a);case 8:if(n=e.sent,i=n.vgSpec,o=n.view,c=n.finalize,this.vegaView=o,this.vegaFinalizer=c,u=F(t),1===(h=u?Object.keys(u):[]).length?(l=Object(r.a)(h,1),d=l[0],this.defaultDataName=d):0===h.length&&i.data&&(this.defaultDataName=z),(g=S(t))&&o.insert(this.defaultDataName,g),u)for(p=0,b=Object.entries(u);p<b.length;p++)v=Object(r.a)(b[p],2),w=v[0],m=v[1],o.insert(w,m);return e.next=22,o.runAsync();case 22:this.vegaView.resize().runAsync();case 23:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){var e=this;if(this.state.error)throw this.state.error;return Object(V.jsx)(y,{"data-testid":"stVegaLiteChart",ref:function(t){e.element=t}})}}]),a}(d.PureComponent);function S(e){var t=e.get("data");return t?N(t):null}function F(e){var t=I(e);if(null==t)return null;for(var a={},n=0,i=Object.entries(t);n<i.length;n++){var s=Object(r.a)(i[n],2),o=s[0],c=s[1];a[o]=N(c)}return a}function I(e){if(!e.get("datasets")||e.get("datasets").isEmpty())return null;var t={};return e.get("datasets").forEach((function(e,a){if(e){var n=e.get("hasName")?e.get("name"):null;t[n]=e.get("data")}})),t}function N(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;if(!e.get("data"))return[];if(!e.get("index"))return[];if(!e.get("columns"))return[];for(var a=[],n=Object(w.g)(e.get("data")),i=Object(r.a)(n,2),s=i[0],o=i[1],c=e.get("index").get("type"),u=D.has(c),h=t;h<s;h++){var l={};u&&(l[k]=Object(w.e)(e.get("index"),0,h));for(var d=0;d<o;d++)l[Object(w.e)(e.get("columns"),0,d)]=Object(w.f)(e.get("data"),d,h);a.push(l)}return a}function T(e,t){var a=t.colors,r=t.fontSizes,i=t.genericFonts,s={labelFont:i.bodyFont,titleFont:i.bodyFont,labelFontSize:r.twoSmPx,titleFontSize:r.twoSmPx},o={background:a.bgColor,axis:Object(n.a)({labelColor:a.bodyText,titleColor:a.bodyText,gridColor:a.fadedText10},s),legend:Object(n.a)({labelColor:a.bodyText,titleColor:a.bodyText},s),title:Object(n.a)({color:a.bodyText,subtitleColor:a.bodyText},s),header:{labelColor:a.bodyText},view:{continuousHeight:300,continuousWidth:400}};return e?b()({},o,e||{}):o}var E=Object(g.f)(Object(v.a)(C))}}]);