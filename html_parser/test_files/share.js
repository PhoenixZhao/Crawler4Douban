(Do&&Do.ready?Do.ready:$)(function(){var d=140;function c(j){return dui.Dialog($.extend({width:525},j),true)}$("[data-share-dialog]").bind("click",function(p){p.preventDefault();var v=$(this),r=v.data("dialog-title"),s=$(v.data("share-dialog")).html();window.sharingDialog=c({title:r,content:s});setTimeout(function(){sharingDialog.update().open()},20);var n=sharingDialog.node,l=n.find(".notification"),t=n.find("textarea"),o=n.find(".avail-num-indicator"),k=n.find(":submit"),u=n.find(".mentioned-highlighter");n.addClass("movie-share-dialog");e(t.get(0),0);a(t);t.bind("actualChange",function(){g(t,o)});t.textbox({itemCount:6,dataUrl:t.data("mention-api"),listTmpl:$("#suggest-mention-tmpl").html(),highlighter:u});g(t,o);t.bind({limitExceed:function(){k.attr("disabled",true)},limitFufill:function(){k.removeAttr("disabled")}});var j=n.find("form"),q=n.find(".error"),m=j.find("input").add(j.find("textarea"));j.bind("afterSubmit",function(){q.hide();m.attr("disabled",true)});i(j,function(w){if(w.r){sharingDialog.setContent(['<p class="dialog-only-text">',"分享成功!","</p>"].join("")).set({height:155});setTimeout(function(){sharingDialog.close()},1500);return}n.find(".error").hide().text(w.reason||"服务器开小差了，请稍候再试……").fadeIn();m.removeAttr("disabled")},"json",function(w){if(w.name==="text"){w.value=b(u)||w.value}return w})});function i(l,j,k,m){l.submit(function(p){p.preventDefault();var o=$(this),n=o.attr("action");$.ajax({type:(o.attr("method")||"POST").toUpperCase(),url:n,data:$.map(o.serializeArray(),m||f),dataType:k,success:j,error:function(){j({r:false,reason:"服务器开小差了，稍后再试吧"})}});o.trigger("afterSubmit")})}function e(j,k){if(k==="end"){k=j.value.length}h(j,k,k)}var h=document.selection?function(l,m,j){var k=l.createTextRange();k.moveEnd("character",-l.value.length);k.moveEnd("character",j);k.moveStart("character",m);k.select()}:function(k,l,j){k.setSelectionRange(l,j);k.focus()};function a(j){if(j.data("isPollingForChange")){return}var k=j.val();setInterval(function(){var l=j.val();if(k===l){return}j.trigger("actualChange")},250)}function g(k,n){var j=k.val().length,l=d-j,m=l<0;n.text(l.toString(10))[m?"addClass":"removeClass"]("error");k.trigger(m?"limitExceed":"limitFufill")}function f(j){return j}function b(j){j=j.clone();j.find("[data-id]").each(function(k,l){l=$(l);l.text("@"+l.data("id"))});return j.text()}});