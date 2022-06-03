 (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-67536262-1', 'auto');
  ga('send', 'pageview');

var noInternetMessage = "An error occurred. Please check if you have access to the internet.";

String.format = function() {
  var s = arguments[0];
  for (var i = 0; i < arguments.length - 1; i++) {       
      var reg = new RegExp("\\{" + i + "\\}", "gm");             
      s = s.replace(reg, arguments[i + 1]);
  }
  return s;
}

function clearInputsById()
{
	for (var i = 0; i < arguments.length; i++) {       
      $("#"+arguments[i]).val("");
  	}
}

function clearInputsByFormId(formId)
{
	var $inputs = $('#'+formId+' :input');
	$inputs.each(function() {
		if ($(this).attr("type") == "checkbox")return;
        $(this).val("");
    });
}

function createFormData(formId)
{
	var values = new FormData();
	var $inputs = $('#'+formId+' :input');
	$inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname)
        {
        	if ($(this).attr("type") == "file")
        	{
        		var allFiles = this.files;
        		var sz = allFiles.length;
        		for (var i=0;i<sz;i++)
        		{
        			values.append(aname, this.files[i]);
        		}

        	}
        	else if ($(this).attr("type") == "checkbox" && !$(this).is(":checked"))
        	{
        		values.append(aname, "");
        	}else{
        		values.append(aname, $(this).val());
        	}
        }
    });

	var $inputs = $('#'+formId+' div');
    $inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname)
        {
        	values.append(aname, $(this).html());
        }
    });

    return values;
}

function serializeForm(formId)
{
	var values = "";
	var $inputs = $('#'+formId+' :input');
	$inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname)
        {
        	if ($(this).attr("type") == "file")
        	{
        		var allFiles = this.files;
        		var sz = allFiles.length;
        		for (var i=0;i<sz;i++)
        		{
        			values = values + String.format("{0}={1}&", aname, encodeURIComponent(this.files[i]));
        		}
        	}
        	else if ($(this).attr("type") == "checkbox" && !$(this).is(":checked"))
        	{
        		values = values + String.format("{0}={1}&", aname, "");
        	}
        	else
        	{
        		values = values + String.format("{0}={1}&", aname, encodeURIComponent($(this).val()));
        	}
        }
    });

	var $inputs = $('#'+formId+' div');
    $inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname)
        {
        	values = values + String.format("{0}={1}&", aname, encodeURIComponent($(this).html()));
        }
    });
    
    if (values.length > 1 && values.substr(values.length-1)=="&")
    {
    	values = values.substr(0,values.length-1);
    }

    return values;
}

function fillInputsByFormId(formId, data)
{
	var $inputs = $('#'+formId+' :input');
    $inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname in data)
        {
        	$(this).val(data[aname]);
        }
    });

    var $inputs = $('#'+formId+' div');
    $inputs.each(function() {
        var aname = $(this).attr("name");
        if (aname in data)
        {
        	$(this).html(data[aname]);
        }
    });

}

function failedReport()
{
	var msg = "An error occurred. Check if you have access to internet.";
	if (arguments.length > 0 && arguments[0])
	{
		msgbox(msg);
	}
	else
	{
		alert(msg);
	}
}

function msgbox()
{
	if (arguments.length == 1)
	{
		var msg = arguments[0];
		bootbox.alert({ size: "medium",message: msg});
	}
	else if (arguments.length == 2)
	{
		var msg = arguments[0];
		var title = arguments[1];
		bootbox.alert({ size: "medium",message: msg, title: title});
	}
	else if (arguments.length == 3)
	{
		var msg = arguments[0];
		var title = arguments[1];
		var fcn = arguments[2];
		bootbox.alert({ size: "medium",message: msg, title: title, callback : function()
		{fcn();}});
	}
	
}

function switchState(btnId, state)
{
	if ((typeof btnId === "string") && btnId.length == 0) return;

	var btnH = (typeof btnId === "string") ? $("#"+btnId) : $(btnId);
	var key = "holdvalue";
	if (state)
	{
		btnH.data(key,btnH.html());
		var processText = "Processing";
		if (btnH.data().hasOwnProperty("processing"))
		{
			processText = btnH.data("processing");
		}
		btnH.html('<i class="fa fa-spinner fa-spin" ></i> '+processText);
	}
	else
	{
		btnH.html(btnH.data(key));
	}
	btnH.attr("disabled",state);
}

function randomId()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 10; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function fillMsgBox(resultId, flag, message)
{
	var closeId = randomId();
	var counterBoxId = randomId();
	var temp = '<div class="alert alert-{0} alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only" id="'+closeId+'">Close</span></button><span >{1}</span><br><span id="'+counterBoxId+'"></span></div>';
	var thesign = "danger";
	if (flag == "1")
	{
		thesign = "success";
	}
	
	temp = String.format(temp, thesign, message);
	$("#"+resultId).html(temp);

	if (flag == "0")
	{
		var waitTime = 10000;
		var countDwn = waitTime/1000;
		$("#"+counterBoxId).html("Closes after "+countDwn+" sec");
		var counterId = setInterval(function()
			{ 
				$hld = $('#'+counterBoxId);
				if (!jQuery.contains(document, $hld[0]))
				{
					clearInterval(counterId);
					return;
				}
				if (countDwn == 0 || $("#"+resultId).html() == "")
				{
					$("#"+resultId).html("");
					clearInterval(counterId);
					return;
				}
				$("#"+counterBoxId).html("Closes after "+(countDwn--)+" sec");
		},1000);
		$("#"+closeId).click(function(){clearInterval(counterId);});

	}
	
}

function scrollTo(destId)
{
	$('html, body').animate({ scrollTop: $("#"+destId).offset().top - 50 }, 1000);
}
function scrollToBottom(containerId)
{
	var elem    = $('#'+containerId);
	var height = elem[0].scrollHeight;
	elem.scrollTop(height);
}
function scrollToChild(parent, child)
{
	if (parent == null || child == null)
	{
		return;
	}
	var childElem = (typeof child === "string") ? $("#"+child) : child;
	var parentElem = (typeof parent === "string") ? $("#"+parent) : parent;
	var top = childElem.position().top-50;
	// childElem.parentsUntil(parentElem).each(function(index, elem)
	// {
	// 	top += $(elem).position().top;
	// });
	parentElem.scrollTop(top);
}
function loadResultTable(data, theType)
{
	if (theType == "one")
	{
		loadTableWithOneData(data, "result_table_header_id", "result_table_body_id");
	}
	else
	{
		loadTableWithManyData(data, "result_table_header_id", "result_table_body_id");
	}
}

function loadTableWithOneData(data, tableHeaderId, tableBodyId)
{
	var keys = Object.keys(data);
	var colSz = keys.length;
	var thTags = "<th>#</th>";
	var tbTags = "<td>1</td>";
	for (var i=0;i<colSz;i++)
	{
		var akey = keys[i];
		thTags += String.format("<th>{0}</th>", akey);
		tbTags += String.format("<td>{0}</td>", data[akey]);
	}
	thTags = String.format("<tr>{0}</tr>", thTags);
	tbTags = String.format("<tr>{0}</tr>", tbTags);
	$("#"+tableHeaderId).html(thTags);
	$("#"+tableBodyId).html(tbTags);
}

function loadTableWithManyData(data, tableHeaderId, tableBodyId)
{
	var keys = Object.keys(data);
	var colSz = keys.length;
	var thTags = "<th>#</th>";
	var tbTags = "";
	for (var i=0;i<colSz;i++)
	{
		var akey = keys[i];
		thTags += String.format("<th>{0}</th>", akey);
	}
	thTags = String.format("<tr>{0}</tr>", thTags);
	var rowSz = data[akey].length;
	for (i = 0;i<rowSz;i++)
	{
		var temp = String.format("<td>{0}</td>", i+1);
		for (var j=0;j<colSz;j++)
		{
			var akey = keys[j];
			temp += String.format("<td>{0}</td>", data[akey][i]);
		}
		tbTags += String.format("<tr>{0}</tr>", temp);
	}

	$("#"+tableHeaderId).html(thTags);
	$("#"+tableBodyId).html(tbTags);
}
function loadTableWithMenu(data, ids, tableHeaderId, tableBodyId, menuData)
{
	var keys = Object.keys(data);
	var colSz = keys.length;
	var thTags = "<th>#</th>";
	var tbTags = "";
	for (var i=0;i<colSz;i++)
	{
		var akey = keys[i];
		thTags += String.format("<th>{0}</th>", akey);
	}
	thTags = "<th></th>"+thTags;
	thTags = String.format("<tr>{0}</tr>", thTags);
	var menuName = menuData.name;
	var menuItems = menuData.items;
	var menuFcn = menuData.callback;
	var className = ("className" in menuData) ? menuData.className : "table-menu-button";

	var menuHTML = "";
	var itemSz = menuItems.length;
	for (var i=0;i<itemSz;i++)
	{
		var item = menuItems[i];
		var itemName = item.name;
		var itemTag = item.tag;
		var icon = ("icon" in item) ? item.icon : "";
		menuHTML += '<li><a href="#" data-id="{0}" data-tag="'+itemTag+'" class="'+className+'" >'+icon+' '+itemName+'</a></li>';
	}

	var menuTemplate = '<div class="dropdown" >' +
  '<button class="btn btn-success btn-xs dropdown-toggle" type="button" data-toggle="dropdown">' + menuName +
  '<span class="caret"></span></button>' +
  '<ul class="dropdown-menu" >' +
    menuHTML +
  '</ul></div>';

	var rowSz = data[akey].length;
	for (i = 0;i<rowSz;i++)
	{
		var temp = String.format("<td>{0}</td>", i+1);
		for (var j=0;j<colSz;j++)
		{
			var akey = keys[j];
			temp += String.format("<td>{0}</td>", data[akey][i]);
		}
		var id = ids[i];
		if (id != null && (id.toString().length > 1 || id > 0))
		{
			temp = String.format("<td>{0}</td>", String.format(menuTemplate, id)) + temp;
		}
		else
		{
			temp = "<td></td>" + temp;
		}
		
		tbTags += String.format("<tr>{0}</tr>", temp);
	}

	$("#"+tableHeaderId).html(thTags);
	$("#"+tableBodyId).html(tbTags);
	$('.'+className).click(function()
		{
			var id = $(this).data("id");
			var tag = $(this).data("tag");
			menuFcn(tag,id,this);
	});

}

function searchSalesPoint(addresId, resultBoxId, btnId)
{
	var addressE = $("#"+addresId);
	if (addressE.val().trim().length == 0)
	{
		return;
	}
	switchState(btnId, true);
	var values = "address="+encodeURIComponent(addressE.val());
	var request = $.post( "controller/sales_point.php",values, function(data) {
		try
		{
			var result = jQuery.parseJSON(data);
		  	$("#"+resultBoxId).html(result["message"]);
		}
		catch (err)
		{
			msgbox("Check if '"+addressE.val()+"' is a valid address.");
		}
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function download(productName)
{
	if (productName.length == 0) return false;

	var values = "productName="+productName;
	var request = $.post( "controller/download.php",values, function(data) {
		  
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  if (flag=="1")
		  {
		  	var url = result["message"];

		  	document.location = url;
		  	var lic = "Your download has started. Kindly read the End User License Agreement.<br><br> A Permission is hereby granted to any person who purchased a copy of this software and associated files (the \"Software\"), to use the Software subject to the following conditions: <br>    * No attempt should be made to reproduce the Software by whatever means. <br>    * A purchased copy may be shared with third parties but not sold to them. <br>THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE. <br><br> Copyright © 2017. All rights reserved. <br>Developed by: <br>IAF SAWII <br>Nigeria <br>https://www.testdriller.com";
		  	msgbox(lic,"End User License Agreement");
		  }
		  else
		  {
		  	failedReport(true);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	
		  });
	return false;
}

function downloadApp(productName)
{
	if (productName.length == 0) return false;

	var values = "productName="+productName;
	var request = $.post( "controller/download.php",values, function(data) {
		  
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  if (flag=="1")
		  {
		  	var url = result["message"];

		  	document.location = url;
		  	var lic = "Your download has started. Kindly read the End User License Agreement.<br><br> A Permission is hereby granted to any person who purchased a copy of this software and associated files (the \"Software\"), to use the Software subject to the following conditions: <br>    * No attempt should be made to reproduce the Software by whatever means. <br>    * A purchased copy may be shared with third parties but not sold to them. <br>THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE. <br><br> Copyright © 2017. All rights reserved. <br>Developed by: <br>IAF SAWII <br>Nigeria <br>https://www.testdriller.com";
		  	msgbox(lic,"End User License Agreement");
		  }
		  else
		  {
		  	failedReport(true);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	
		  });
	return false;
}

function activate(phoneNumberId, productNameId, pinId, productKeyId, resultBoxId, btnId)
{
	switchState(btnId, true);
	var phoneNumber = $("#"+phoneNumberId).val();
	var productName = $("#"+productNameId).val();
	var pin = $("#"+pinId).val();
	var productKey = $("#"+productKeyId).val();

	var values = String.format("phoneNumber={0}&productName={1}&pin={2}&productKey={3}", phoneNumber, productName, pin, productKey);
	
	var request = $.post( "controller/activate.php",values, function(data) {
			
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  //$("#"+resultBoxId).html(message);
		  fillMsgBox(resultBoxId, flag, message);
		})
		  .fail(function() {
		    failedReport();
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function buyDirect(productNameId, phoneNumberId, emailId, productKeyId, resultBoxId, btnId)
{
	switchState(btnId, true);
	var phoneNumber = $("#"+phoneNumberId).val();
	var productName = $("#"+productNameId).val();
	var email = $("#"+emailId).val();
	var productKey = $("#"+productKeyId).val();
	var parentDiv = $("#online_buy_container_id");
	
	var values = String.format("phoneNumber={0}&productName={1}&email={2}&productKey={3}", phoneNumber, productName, email, productKey);
	
	var request = $.post( "controller/buy_online.php",values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  
		  if (flag == "0")
		  {
		  	fillMsgBox(resultBoxId, flag, message);
		  }
		  else
		  {
		  	var btn = $("#"+btnId);
		  	$('#online-payment').modal('hide');
		  	btn.data("message",encodeURI(message));
		  	btn.data("title","Buy Activation Key");
		  	ShowCustomDialog(btn);
		  }

		})
		  .fail(function() {
		    failedReport();
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userLogin(emailId, passwordId, regCodeId, regCodeParentId, messageId, btnId)
{
	switchState(btnId, true);
	var email = $("#"+emailId).val();
	var password = $("#"+passwordId).val();
	var regCode = $("#"+regCodeId).val();
	var values = String.format("email={0}&password={1}", email, password);
	if ($("#"+regCodeParentId).is(":visible"))
	{
		values = values + "&regCode=" + regCode;
	}
	
	var request = $.post( "controller/login.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  //$("#"+messageId).html(message);
		  if (flag == "0")
		  {
		  	fillMsgBox(messageId, flag, message);
		  }
		  else if (result["action"] == "activate")
		  {
		  	fillMsgBox(messageId, "0", message);
		  	$("#"+regCodeParentId).removeClass("hidden");
		  }else if (result["action"] == "reset")
		  {
			  fillMsgBox(messageId, "1", message);
			  $("#"+emailId).val("");
			  $("#"+passwordId).val("");
		  }
		  else
		  {
		  	$("#"+messageId).html(message);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userForgetPassword(emailId, messageId, btnId)
{
	switchState(btnId, true);
	var email = $("#"+emailId).val();

	var values = String.format("email={0}", email);

	var request = $.post( "controller/forget_password.php",values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  fillMsgBox(messageId, flag, message);
		  if (flag=="1")
		  {
		  	$("#"+emailId).val("");
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userPasswordReset(passwordId, cpasswordId, tokId, messageId, btnId)
{
	var password = $("#"+passwordId).val();
	var cpassword = $("#"+cpasswordId).val();
	var tok = $("#"+tokId).val();

	if (password != cpassword)
	{
		fillMsgBox(messageId, "0", "Passwords do not agree.");
		return;
	}

	switchState(btnId, true);

	var values = String.format("password={0}&tok={1}", password, tok);

	var request = $.post( "controller/password_reset.php",values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  fillMsgBox(messageId, flag, message);
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userRegister(nameId, emailId, passwordId, confirmPasswordId, phoneId, stateId, addressId, messageId, btnId)
{
	var name = $("#"+nameId).val();
	var email = $("#"+emailId).val();
	var password = $("#"+passwordId).val();
	var confirmPassword = $("#"+confirmPasswordId).val();
	var phoneNumber = $("#"+phoneId).val();
	var state = $("#"+stateId).val();
	var address = $("#"+addressId).val();

	if (password != confirmPassword)
	{
		$("#"+messageId).html("Passwords do not agree.");
		return;
	}

	switchState(btnId, true);

	var values = String.format("name={0}&email={1}&password={2}&phoneNumber={3}&state={4}&address={5}", 
		name, email, password, phoneNumber, state, address);

	var request = $.post( "controller/register.php",values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (flag == "0")
		  {
		  	fillMsgBox(messageId, flag, message);
		  }
		  else
		  {
		  	$("#"+messageId).html(message);
		  }
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userActivationKey(formId, resultBoxId, btnId, action)
{
	switchState(btnId, true);

	var values = String.format("action={0}&{1}", action, serializeForm(formId));
	
	var request = $.post( "../controller/user_act_key.php",values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (flag == "1")
		  {
		  	clearInputsByFormId(formId);
		  	fillMsgBox(resultBoxId, flag, message);
		  }
		  else
		  {
		  	msgbox(message);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userGeneratePin(productNameId, numberPinId, resultBoxId, btnId, action)
{
	switchState(btnId, true);

	var productName = $("#"+productNameId).val();
	var number = $("#"+numberPinId).val();
	
	var values = String.format("productName={0}&number={1}&action={2}", productName, number, action);
	var request = $.post( "../controller/user_pin.php",values, function(data) {

		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];

		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	clearInputsById(productNameId, numberPinId);

		  	var printData = result["print"];
		  	showResultOptions(printData, jQuery.parseJSON(result['pin']), jQuery.parseJSON(result['sn']), "TestDriller PIN", "PIN");
		  }
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function userRetrievePin(batchNoId, resultBoxId, btnId, action)
{
	switchState(btnId, true);

	var batchNo = $("#"+batchNoId).val();
	
	var values = String.format("batchNo={0}&action={1}", batchNo, action);
	var request = $.post( "../controller/user_pin.php",values, function(data) {

		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	var printData = result["print"];
		  	showResultOptions(printData, jQuery.parseJSON(result['pin']), jQuery.parseJSON(result['sn']), "TestDriller PIN", "PIN");
		  }
		  

		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function userGeneratePassword(productNameId, passwordTimeId, numberPasswordId, resultBoxId, btnId, action)
{
	switchState(btnId, true);

	var productName = $("#"+productNameId).val();
	var passwordTime = $("#"+passwordTimeId).val();
	var number = $("#"+numberPasswordId).val();
	
	var values = String.format("productName={0}&time={1}&quantity={2}&action={3}", productName, passwordTime, number, action);
	var request = $.post( "../controller/user_practice_centre.php",values, function(data) {

		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];

		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	clearInputsById(productNameId, passwordTimeId, numberPasswordId);
		  	var printData = result["print"];
		  	
		  	$("#"+productNameId).val("");
		  	$("#"+passwordTimeId).val("");
		  	$("#"+numberPasswordId).val("");
		  	showResultOptions(printData, jQuery.parseJSON(result['password']), null, "TestDriller Password","Password");
		  }
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function userRetrievePassword(batchNoId, resultBoxId, btnId, action)
{
	switchState(btnId, true);

	var batchNo = $("#"+batchNoId).val();
	
	var values = String.format("batchNo={0}&action={1}", batchNo, action);
	var request = $.post( "../controller/user_practice_centre.php",values, function(data) {

		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	var printData = result["print"];
		  	showResultOptions(printData, jQuery.parseJSON(result['password']), null, "TestDriller Password", "Password");
		  }
		  

		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function userTopUp(amountId, resultBoxId, btnId)
{
	switchState(btnId, true);

	var amount = $("#"+amountId).val();
	
	var values = String.format("amount={0}", amount);
	var request = $.post( "../controller/user_top_up.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	var btn = $("#"+btnId);
		  	btn.data("message",encodeURI(message));
		  	btn.data("title","Top Up");
		  	ShowCustomDialog(btn);
		  }
		  

		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function userTransfer(productNameId, receiverId, quantityId, messageId, btnId)
{
	switchState(btnId, true);
	var productName = $("#"+productNameId).val();
	var receiver = $("#"+ receiverId).val();
	var quantity = $("#"+quantityId).val();

	var values = String.format("productName={0}&receiver={1}&quantity={2}", 
		productName, receiver, quantity);

	var request = $.post( "../controller/user_transfer.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  //$("#"+messageId).html(message);
		  msgbox(message);
		  if (flag == "1")
		  {
		  	clearInputsById(productNameId, receiverId, quantityId);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userBalanceToLicense(productNameId, licenseQuantityId, balanceId, messageId, btnId)
{
	switchState(btnId, true);
	var productName = $("#"+productNameId).val();
	var quantity = $("#"+licenseQuantityId).val();

	var values = String.format("productName={0}&quantity={1}", 
		productName, quantity);

	var request = $.post( "../controller/user_convert_license.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		 
		  if (flag == "1")
		  {
		  	msgbox(message, "Succesful", function(){location.reload();});
		  	
		  }
		  else
		  {
		  	msgbox(message,"Failed");
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function userLogout()
{
	var request = $.post( "../controller/user_log_out.php","", function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  $("body").html(message);
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  });
	return false;
}

function contactUs(nameId, emailId, phoneNumberId, inquiryId, messageId, resultBoxId, btnId)
{
	switchState(btnId, true);
	var name = $("#"+nameId).val();
	var email = $("#"+emailId).val();
	var phoneNumber = $("#"+ phoneNumberId).val();
	var inquiry = $("#"+inquiryId).val();
	var message = $("#"+messageId).val();

	var values = String.format("name={0}&email={1}&phoneNumber={2}&inquiry={3}&message={4}", 
		name, email, phoneNumber, inquiry, message);

	var request = $.post("controller/contact.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  msgbox(message);
		  if (flag == "1")
		  {
		  	clearInputsById(nameId, emailId, phoneNumberId, inquiryId, messageId);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function PrintIDContent(id)
{
	var headContent = $("head").html();
	var content = "<html><head>"+headContent+"</head><body>" + document.getElementById(id).innerHTML +"</body></html>";
	PrintDiv(content);
}
function PrintContent(mainContent)
{
	var headContent = $("head").html();
	var content = "<html><head>"+headContent+"</head><body>" + mainContent +"</body></html>";
	PrintDiv(content);
}
function PrintDiv(contents) {
	var frame1 = document.createElement('iframe');
	frame1.name = "frame1";
	frame1.style.position = "absolute";
	frame1.style.top = "-1000000px";
	
	document.body.appendChild(frame1);
	var frameDoc = frame1.contentWindow ? frame1.contentWindow : frame1.contentDocument.document ? frame1.contentDocument.document : frame1.contentDocument;
	frameDoc.document.open();
	frameDoc.document.write(contents);
	frameDoc.document.close();

	setTimeout(function () {
		window.frames["frame1"].focus();
		window.frames["frame1"].print();
		document.body.removeChild(frame1);
	}, 500);
	return false;
}

function showResultOptions(printTable, pins, sns, theTitle, codeName)
{
	var atable = "";
	var sz = pins.length;
	var i = 0;
	var unrolledPins = pins.join("\n");
	for (i=0;i<sz;i++)
	{
		var pin = pins[i];
		var sn = sns == null ? "" : sns[i];
		atable = atable + "<tr><td>"+(i+1)+"</td><td>"+splitText(pin,2)+"</td><td>"+splitText(sn,3)+"</td></tr>";
	}

	document.getElementById('modal_print_id').onclick = function(){PrintContent(printTable);};
	document.getElementById("modal_code_type_id").innerHTML = codeName;
	var hdle = document.getElementById('modal_pinTableBody');
	document.getElementById('modal_title').innerHTML = theTitle;
	
	hdle.innerHTML = atable;
	$('#modal_display').modal('show');
	
	document.getElementById('modal_copy_id').onclick = function(){
		$('#modal_display').modal('hide');
		copyTexToClipboard(unrolledPins, true);
		setTimeout(function(){$('#modal_display').modal('show');},1000);
	};
}

function splitText(text, division)
{
	var sz = text.length;
	var ct = sz/division;
	var i = 0;
	var stext = "";
	for (i=0;i<division;i++)
	{
		if (i < ct-1)
		{
			stext += text.substr(i*ct, ct)+" ";
		}
		else
		{
			stext += text.substr(i*ct);
		}
	}
	return stext;
}

function fnExcelReport(tableID, deleteFirstColumn)
{
    var tab_text = '<table border="1px" style="font-size:15px" ">';
    var textRange; 
    var j = 0;
    var tab = document.getElementById(tableID).cloneNode(true); // id of table
    var lines = tab.rows.length;

    // the first headline of the table
    if (lines > 0) {
    	arow =    tab.rows[0];
    	if (arguments.length == 2 && deleteFirstColumn)
    	{
    		arow.deleteCell(0);
    	}
        tab_text = tab_text + '<tr bgcolor="#DFDFDF">' + arow.innerHTML + '</tr>';
    }

    // table data lines, loop starting from 1
    for (j = 1 ; j < lines; j++) {
    	arow =    tab.rows[j];
    	if (arguments.length == 2 && deleteFirstColumn)
    	{
    		arow.deleteCell(0);
    	}
        tab_text = tab_text + "<tr>" + arow.innerHTML + "</tr>";
    }

    tab_text = tab_text + "</table>";
    tab_text = tab_text.replace(/<A[^>]*>|<\/A>/g, "");             //remove if u want links in your table
    tab_text = tab_text.replace(/<img[^>]*>/gi,"");                 // remove if u want images in your table
    tab_text = tab_text.replace(/<input[^>]*>|<\/input>/gi, "");    // reomves input params

    var ua = window.navigator.userAgent;
    var msie = ua.indexOf("MSIE "); 

     // if Internet Explorer
    if (msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./)) {
        txtArea1.document.open("txt/html","replace");
        txtArea1.document.write(tab_text);
        txtArea1.document.close();
        txtArea1.focus(); 
        sa = txtArea1.document.execCommand("SaveAs", true, "download.xls");
    }  
    else // other browser not tested on IE 11
        sa = window.open('data:application/vnd.ms-excel,' + encodeURIComponent(tab_text));  

    return (sa);
}

function seeMoreBlog(btnId, containerId)
{
	switchState(btnId, true);

	var lindex = $("#"+btnId).data("lindex");
	var values = String.format("lindex={0}", lindex);

	var request = $.post( "controller/blog_see_more.php",values, function(data) {
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  var docToAdd = result["document"];
		  var count = result["count"];
		  var last = result["last"];
		  lindex = result["lindex"];

		  if (flag == "0")
		  {
		  	msgbox(message);
		  }
		  else
		  {
		  	$("#"+btnId).data("count", count);
		  	$("#"+btnId).data("lindex", lindex);
		  	if (last == "1")
		  	{
		  		$("#"+btnId).hide();
		  	}
		  	$("#"+containerId).append(docToAdd);
		  }
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });

}

function searchBlog(inputId, btnId, containerId)
{
	switchState(btnId, true);

	var values = String.format("{0}={1}", "search", encodeURIComponent($("#"+inputId).val()));

	var request = $.post( "controller/blog_see_more.php",values, function(data) {
		
		  try
		  {
		  	var result = jQuery.parseJSON(data);
			  var flag = result["flag"];
			  var message = result["message"];
			  var doc = result["document"];

			  if (flag == "0")
			  {
			  	msgbox(message);
			  }
			  else
			  {
			  	$("#"+containerId).html(doc);
			  }
		  }
		  catch(err)
		  {
		  	msgbox("An error occurred");
		  }
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function registerEnterClick(parentId, btnId)
{
	var $inputs = $('#'+parentId+' input');
	$inputs.each(function() {
        var type = $(this).attr("type");
        if (type && type != "button")
        {
        	$(this).keydown(function(e)
        	{
        		if (e.which == 13) {
        			e.preventDefault();
			    }
        	});
        	$(this).keyup(function(e)
        	{
        		if (e.which == 13) {
			    	$("#"+btnId).trigger("click");
			    }
        	});
        }
    });
}

function addEditAndReload(formId, resultBoxId, btnId, controller)
{
	switchState(btnId, true);

	var values = createFormData(formId);

	$.ajax({
		url: controller, // Url to which the request is send
		type: "POST",             // Type of request to be send, called as method
		data: values, // Data sent to server, a set of key/value pairs (i.e. form fields and values)
		contentType: false,       // The content type used when sending data to the server.
		cache: false,             // To unable request pages to be cached
		processData:false,        // To send DOMDocument or non processed data file it is set to false
		success: function(data)   // A function to be called if request succeeds
		{
			  var result = jQuery.parseJSON(data);
			  var flag = result["flag"];
			  var message = result["message"];
			  fillMsgBox(resultBoxId, flag, message);
			  if (flag == "1")
			  {
			  	location.reload();
			  }
		},
	    error: function(xhr,status,error) {
	        failedReport();
	    },
	    complete: function()
	    {
	    	switchState(btnId, false);
	    }
	});
}

function postData(formId, btnId, presenterPath, resultFcn, messageId)
{
	switchState(btnId, true);
	var values = serializeForm(formId);
	var request = $.post( presenterPath,values, function(data) {
		
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (arguments.length == 4)
		  {
		  	resultFcn(flag, message, result);
		  }
		  else
		  {
		  	resultFcn(flag, message, result, messageId);
		  }
	
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}

function postDataValues(values, btnId, presenterPath, resultFcn, messageId)
{
	switchState(btnId, true);
	var request = $.post( presenterPath,values, function(data) {
	
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  if (arguments.length == 4)
		  {
		  	resultFcn(flag, message, result);
		  }
		  else
		  {
		  	resultFcn(flag, message, result, messageId);
		  }
		  
		})
		  .fail(function() {
		    failedReport(true);
		  })
		  .always(function(){
		  	switchState(btnId, false);
		  });
}
function ajaxPost(data, url, afterCallback, btn, beforeCallback, timeout)
{
	var btnVal = "";
	var btnH = null;
	var hasBeforeSend = arguments.length >= 5  && typeof beforeCallback != "string";
	var hasTimeout = arguments.length >= 6;
	if (arguments.length > 3)
	{
		if (!(typeof btn === "string"))
		{
			btnH = $(btn);
		}
		else if ((typeof btn === "string") && btn.length > 0)
		{
			btnH = $("#"+btn);
		}
		if (btnH != null)
		{
			btnVal = btnH.html();
			var tempVal = '<span style="visibility: hidden;">'+btnVal+'</span>';
			btnH.html('<i class="fa fa-spinner fa-spin" ></i> '+tempVal);
			btnH.attr("disabled", true);
		}
	}
	var requestId = randomId();
	$.ajax({
        type: 'post',
        contentType: 'application/x-www-form-urlencoded',
        url:url,
        dataType: "json",
        data: data,
        
        beforeSend: function(jqXHR, settings){
        	if (hasBeforeSend)
        	{
        		beforeCallback(requestId);
        	}
        },
        success: function(result){
            afterCallback(result, requestId);
        },
        error: function(data, status, errorThrown){
            var result = {"flag":"0","message":"No access to internet"};
            result["error"] = errorThrown;
            result["failed"] = "1";
            afterCallback(result, requestId);
        },
        complete: function(obj, status){
        	if (btnH != null)
			{
				btnH.html(btnVal);
				btnH.attr("disabled", false);
			}
        }
    });

    return requestId;
}

function serializePostData()
{
	var sz = arguments.length;
	var values = "";
	if (sz == 1)
	{
		var data = arguments[0];
		return $.param(data);
	}
	else
	{
		for (var i = 0; i < sz; i+=2) {       
		    values += String.format("{0}={1}&", arguments[i], encodeURIComponent(arguments[i+1]));
		}
	}

	if (values.length > 1 && values.endsWith("&"))
    {
    	values = values.substr(0,values.length-1);
    }
	
	return values;
}

function urldecode(str) 
{ 
	if (typeof str != "string") 
	{ 
		return str; 
	} 
	return decodeURIComponent(str.replace(/\+/g, ' ')); 
}

function notifyAlert(message)
{
	$.notify({message:message},{z_index: 50000,animate: {
        enter: 'animated bounceIn',
        exit: 'animated bounceOut'
    }});
}

function ShowDialog(btn)
{
	var btnObj = $(btn);
	var msg = urldecode(btnObj.data("message"));
	var title = btnObj.data("title");
	msgbox(msg, title);
}

function ShowCustomDialog(btn)
{
	var btnObj = $(btn);
	var msg = urldecode(btnObj.data("message"));
	var title = btnObj.data("title");
	var dialog = bootbox.dialog({
                title: title,
                message: msg,
                size: 'medium',
                onEscape: true
            });
}

function CloseAllDialog()
{
	bootbox.hideAll();
}

function MakeOnlinePayment(btn, formId, msgId)
{
	switchState(btn, true);
	var btnObj = $(btn);
	var values = serializeForm(formId);
	var parentDiv = $("#"+formId).parent();
	var request = $.post( "controller/buy_online.php",values, function(data) {
			
		  var result = jQuery.parseJSON(data);
		  var flag = result["flag"];
		  var message = result["message"];
		  
		  if (flag == "0")
		  {
		  	notifyAlert(message);
		  }
		  else
		  {
		  	//$("#"+msgId).html(message);
		  	parentDiv.html(message);
		  }

		})
		  .fail(function() {
		    notifyAlert(noInternetMessage);
		  })
		  .always(function(){
		  	switchState(btn, false);
		  });
}

function SetPriceValue(btn)
{
	var btnObj = $(btn);
	var data = jQuery.parseJSON(urldecode(btnObj.data("data")));
	var dispId = btnObj.data("display");
	var selVal = btnObj.val();
	if (selVal.length == 0)
	{
		$("#"+dispId).html("-");
		return;
	}
	var price = data[selVal];
	$("#"+dispId).html(price);
}
function copyTexToClipboard(element, isText)
{
	var $temp = $("<textarea>");
	$("body").append($temp);
	if (arguments.length > 1 && isText)
	{
		$temp.val(element).select();
	}
	else
	{
		$temp.val($(element).text()).select();
	}
	document.execCommand("copy");
	$temp.remove();
	notifyAlert("Copied to clipboard");
}
function resizeTextArea(textbox, maxrows) {

	var maxrows= arguments.length == 2 ? maxrows : 10; 

	var txt = $(textbox).val();

	var arraytxt=txt.split('\n');
	var rows=arraytxt.length; 

	if (rows>maxrows) 
	{
		$(textbox).attr('rows', maxrows);
	}
	else
	{
		$(textbox).attr('rows', rows);
	}
}
function showLoadingAlert(id)
{
    var elem = '<div style="width: 100px;height: 40px;text-align:center;background:#FFF9C4;border:3px solid #FFA000;position:absolute;left:calc(50% - 50px);top:100px;z-index:20000;border-radius:10px;" id="'+id+'">Loading...</di>';
    $('body').append(elem);
}
function removeLoadingAlert(id)
{
    if ($("#"+id))
    {
        $("#"+id).remove();
    }
}
function isElementInView(child, parent)
{
	var childElem = (typeof child === "string") ? $("#"+child) : child;
	var parentElem = (typeof parent === "string") ? $("#"+parent) : parent;
	var parentViewTop = parentElem.scrollTop();
    var parentViewBottom = parentViewTop + parentElem.height();
    if (childElem)
    {
    	var elemTop = childElem.position().top;
        var elemBottom = elemTop + childElem.height();
        return ((elemTop <= parentViewBottom) && (elemBottom >= parentViewTop));
    }
    else
    {
    	return false;
    }
}
function distanceFromScrollBottom(child, parent)
{
	var childElem = (typeof child === "string") ? $("#"+child) : child;
	var parentElem = (typeof parent === "string") ? $("#"+parent) : parent;
	var parentViewTop = parentElem.scrollTop();
    var parentViewBottom = parentViewTop + parentElem.height();
    var elemTop = childElem.position().top;
    var elemBottom = elemTop + childElem.height();
    return (parentViewBottom - elemBottom);
}
function GetFrom(btn, url, values)
{
	var resultFcn = function(flag, message, result){
		if (flag == "0")
		{
			msgbox(message,"Failed");
		}
		else
		{
			msgbox(message,"Succesful");
		}
	};
	postDataValues(values, btn, url, resultFcn);

}


