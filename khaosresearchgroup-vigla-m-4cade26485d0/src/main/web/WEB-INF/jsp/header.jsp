<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html; charset=iso-8859-1" language="java"
	errorPage="" %>

<nav class="navbar navbar-inverse navbar-fixed-top">
	<div class="container-fluid">
		<!-- Brand and toggle get grouped for better mobile display -->
		<div class="navbar-header">
			<c:if test="${sessionScope.conectado=='true'}">
				<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
			</c:if>
			<a class="navbar-brand" href='<c:url value="/." />' target="_self">ViGLA</a>
		</div>
		
		<!-- Collect the nav links, forms, and other content for toggling -->
		<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
			<p class="navbar-text navbar-right">
				<c:choose>
					<c:when test="${sessionScope.conectado=='true'}">
						Signed as <c:out value="${sessionScope.usuario}"/>
						&nbsp;
						<button type="button" class="btn btn-default btn-primary btn-xs" onClick="parent.location.href='./action/logoutAction.jsp'">
							<span class="glyphicon glyphicon-off" aria-hidden="true"></span> Log out
						</button>
					</c:when>
				</c:choose>
			</p>
		</div><!-- /.navbar-collapse -->
	</div><!-- /.container-fluid -->
</nav>
