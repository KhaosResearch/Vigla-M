<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
	<head>

	<%@ include file="/WEB-INF/jsp/htmlHead.jsp" %>
	
	<c:if test="${sessionScope.conectado!='true'}">
		<c:redirect url="login.jsp"/>
	</c:if>
	
	</head> 
	
	<body>
	
		<%@ include file="/WEB-INF/jsp/header.jsp" %>
		
		<div class="container">
		
			<%@ include file="/WEB-INF/jsp/messages.jsp" %>
		
			<div class="panel panel-default">
				<div class="panel-body">
					<%@ include file="/WEB-INF/jsp/title.jsp" %>
					<h3>Error</h3>
					<p>Something unexpected happened. This is embarrassing...</p>
					<p><a href=".">Back to home</a></p>
				</div>
			</div>
					
		</div><!-- /.container -->
		
		<%@ include file="/WEB-INF/jsp/footer.jsp" %>
		
		<%@ include file="/WEB-INF/jsp/javascript.jsp" %> 
		
	</body>
</html>