<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<c:choose>
	<c:when test="${successMsg!=null}">
		<div class="alert alert-success alert-dismissible" role="alert">
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
			${successMsg}
		</div>
	</c:when>
</c:choose>
<c:choose>
	<c:when test="${errorMsg!=null}">
		<div class="alert alert-danger alert-dismissible" role="alert">
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
			${errorMsg}
		</div>
	</c:when>
</c:choose>
<c:choose>
	<c:when test="${warningMsg!=null}">
		<div class="alert alert-warning alert-dismissible" role="alert">
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
			${warningMsg}
		</div>
	</c:when>
</c:choose>
<c:remove var="errorMsg" scope="session" />
<c:remove var="warningMsg" scope="session" /> 
<c:remove var="successMsg" scope="session" />