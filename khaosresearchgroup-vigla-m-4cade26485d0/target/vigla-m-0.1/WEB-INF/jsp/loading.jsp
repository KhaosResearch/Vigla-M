<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:set var="msg" value="${param['msg']}" />
<c:set var="condition" value="${param['condition']}" />

<div class="alert alert-melanoma" role="alert" data-ng-show="${condition}">
	<div class="row">
		<div class="col-xs-1">
			<div class="loader"></div>
		</div>
		<div class="col-xs-11">${msg}</div>
	</div>
</div>
