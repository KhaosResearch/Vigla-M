<!DOCTYPE html>
<html lang="en">
	<head>

	<%@ include file="/WEB-INF/jsp/htmlHead.jsp" %>
	
	</head> 
	
	<body>
	
		<%@ include file="/WEB-INF/jsp/header.jsp" %>
		
		<div class="container">
		
			<%@ include file="/WEB-INF/jsp/messages.jsp" %>
		
			<div class="panel panel-default">
				<div class="panel-body">
					<%@ include file="/WEB-INF/jsp/title.jsp" %>
					<h3>Log in</h3>
					<form id="myForm" name="myForm" class="form-horizontal" method="post" action="./action/loginAction.jsp">
						<input id="from" name="from" type=hidden value="${param.from}" />
						<div class="form-group">
							<label for="username" class="col-sm-2 control-label">Username</label>
							<div class="col-sm-10">
								<input type="text" class="form-control" id="username" name="username">
							</div>
						</div>
						<div class="form-group">
							<label for="pass" class="col-sm-2 control-label">Password</label>
							<div class="col-sm-10">
								<input type="password" class="form-control" id="pass" name="pass">
							</div>
						</div>
						<div class="form-group">
							<div class="col-sm-offset-2 col-sm-10">
								<button id="execBtn" type="submit" class="btn btn-primary">Log in</button>
							</div>
						</div>
					</form>
					<%@ include file="/WEB-INF/jsp/contactMsg.jsp" %>
				</div>
			</div>
					
		</div><!-- /.container -->
		
		<%@ include file="/WEB-INF/jsp/footer.jsp" %>
		
		<%@ include file="/WEB-INF/jsp/javascript.jsp" %> 
		
	</body>
</html>