<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html; charset=iso-8859-1" language="java"
	errorPage="" %>
<!DOCTYPE html>
<html lang="en" data-ng-app="melanomaApp">
	<head>

	<%@ include file="/WEB-INF/jsp/htmlHead.jsp" %>
	
	<base href="/melanoma/">
	<!-- <base href="/"> -->
	
	<script src="vendors/angularjs/angular.min.js"></script>
	<script src="vendors/angularjs/angular-sanitize.min.js"></script>
	<script src="resources/js/heatMapResponseCtrl.js?v=20180221"></script>
	<script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.js"></script>

	<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.12.14.min.css" type="text/css" />
	<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.14.min.css" type="text/css" />
	<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-tables-0.12.14.min.css" type="text/css">
	<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.12.14.min.js"></script>
	<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-api-0.12.14.min.js"></script>
	<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.14.min.js"></script>
	<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-tables-0.12.14.min.js"></script>
	<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>




		<c:if test="${sessionScope.conectado!='true'}">
		<c:redirect url="login.jsp"/>
	</c:if>
	
	</head> 
	
	<body data-ng-controller="heatMapResponseCtrl">
	
		<%@ include file="/WEB-INF/jsp/header.jsp" %>
		
		<div class="container" data-ng-init="init()">
		
			<%@ include file="/WEB-INF/jsp/messages.jsp" %>
			
			<div class="panel panel-default">
				<div class="panel-body">
					<%@ include file="/WEB-INF/jsp/title.jsp" %>
					
					<div class="row-fluid" data-ng-cloak data-ng-show="clusterHeatmap.selected==true">
					
						<h3>Cluster heatmap</h3>
						
						<jsp:include page="/WEB-INF/jsp/loading.jsp">
							<jsp:param name="msg" value="Generating image. This could take some minutes. Please, don't close this page." />
							<jsp:param name="condition" value="clusterHeatmap.status==0" />
						</jsp:include>
						
						<div class="alert alert-danger" role="alert" data-ng-show="clusterHeatmap.status==-1">
							There has been an error executing the service.
						</div>

						<div data-ng-show="clusterHeatmap.status==1" id="codigohtml"></div>


					<!--	<a href="api/img/{{clusterHeatmap.id}}" target="_blank" data-ng-show="clusterHeatmap.status==1">
                                <img data-ng-src="api/img/{{clusterHeatmap.id}}" class="melanoma-python-img" />
						</a> -->

					</div>

					<div class="row-fluid" data-ng-cloak data-ng-show="geneRegNetwork.selected==true">
					
						<h3>Gene regulatory network</h3>
						
						<jsp:include page="/WEB-INF/jsp/loading.jsp">
							<jsp:param name="msg" value="Generating image. This could take some minutes. Please, don't close this page." />
							<jsp:param name="condition" value="geneRegNetwork.status==0" />
						</jsp:include>
						
						<div class="alert alert-danger" role="alert" data-ng-show="geneRegNetwork.status==-1">
							There has been an error executing the service.
						</div>
						<div data-ng-show="geneRegNetwork.status==1"  id="codigogrn"></div>


						<!--	<a href="api/img/{{geneRegNetwork.id}}" target="_blank" data-ng-show="geneRegNetwork.status==1">
							<img data-ng-src="api/img/{{geneRegNetwork.id}}" class="melanoma-python-img" />
						</a>-->

					</div>

					<%@ include file="/WEB-INF/jsp/contactMsg.jsp" %>
				</div>
			</div>
		</div><!-- /.container -->
		
		<%@ include file="/WEB-INF/jsp/footer.jsp" %>
		
		<%@ include file="/WEB-INF/jsp/javascript.jsp" %>

	</body>
</html>