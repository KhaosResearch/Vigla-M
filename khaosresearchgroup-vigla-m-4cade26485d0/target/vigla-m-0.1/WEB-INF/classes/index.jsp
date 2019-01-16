<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html; charset=iso-8859-1" language="java"
	errorPage="" %>
<!DOCTYPE html>
<html lang="en" data-ng-app="melanomaApp">
	<head>

	<link href="vendors/bootstrap-slider/css/bootstrap-slider.min.css" rel="stylesheet">

	<%@ include file="/WEB-INF/jsp/htmlHead.jsp" %>
	
	<script src="vendors/angularjs/angular.min.js"></script>
	<script src="resources/js/heatMapFormCtrl.js?v=20180221"></script>
	
	<c:if test="${sessionScope.conectado!='true'}">
		<c:redirect url="login.jsp"/>
	</c:if>
	
	</head> 
	
	<body data-ng-controller="heatMapFormCtrl">
	
		<%@ include file="/WEB-INF/jsp/header.jsp" %>
		
		<div class="container" data-ng-init="init()">
		
			<%@ include file="/WEB-INF/jsp/messages.jsp" %>
		
			<div class="panel panel-default">
				<div class="panel-body">
					<%@ include file="/WEB-INF/jsp/title.jsp" %>
					
					<jsp:include page="/WEB-INF/jsp/loading.jsp">
						<jsp:param name="msg" value="Loading page..." />
						<jsp:param name="condition" value="::false" />
					</jsp:include>
					
					<jsp:include page="/WEB-INF/jsp/loading.jsp">
						<jsp:param name="msg" value="Recovering patient and sample data from the user." />
						<jsp:param name="condition" value="patients==null" />
					</jsp:include>
					
					<div class="row-fluid" data-ng-show="patients!=null" data-ng-cloak>
						<h3>Patients</h3>
						<p>Expand each patient to see a list of their samples. Select which samples you want to add to be processed.</p>
					</div>
					
					<div class="table-responsive" data-ng-show="patients!=null" data-ng-cloak>
						<table class="table">
							<thead>
								<tr>
									<td>
										<a href="#" data-ng-click="patientsTable.sortType = 'code'; patientsTable.sortReverse = !patientsTable.sortReverse">Code
											<span class="glyphicon glyphicon-triangle-bottom" data-ng-show="patientsTable.sortType == 'code' && patientsTable.sortReverse"></span>
											<span class="glyphicon glyphicon-triangle-top" data-ng-show="patientsTable.sortType == 'code' && !patientsTable.sortReverse"></span>
										</a>
									</td>
									<td>
										<a href="#" data-ng-click="patientsTable.sortType = 'sex'; patientsTable.sortReverse = !patientsTable.sortReverse">Sex
										<span class="glyphicon glyphicon-triangle-bottom" data-ng-show="patientsTable.sortType == 'sex' && patientsTable.sortReverse"></span>
										<span class="glyphicon glyphicon-triangle-top" data-ng-show="patientsTable.sortType == 'sex' && !patientsTable.sortReverse"></span>
										</a>
									</td>
									<td>
										<a href="#" data-ng-click="patientsTable.sortType = 'bornDate'; patientsTable.sortReverse = !patientsTable.sortReverse">Birth date
										<span class="glyphicon glyphicon-triangle-bottom" data-ng-show="patientsTable.sortType == 'bornDate' && patientsTable.sortReverse"></span>
										<span class="glyphicon glyphicon-triangle-top" data-ng-show="patientsTable.sortType == 'bornDate' && !patientsTable.sortReverse"></span>
										</a>
									</td>
									<td>
										<a href="#" data-ng-click="patientsTable.sortType = 'record'; patientsTable.sortReverse = !patientsTable.sortReverse">Record
										<span class="glyphicon glyphicon-triangle-bottom" data-ng-show="patientsTable.sortType == 'record' && patientsTable.sortReverse"></span>
										<span class="glyphicon glyphicon-triangle-top" data-ng-show="patientsTable.sortType == 'record' && !patientsTable.sortReverse"></span>
										</a>
									</td>
									<td></td>
								</tr>
							</thead>
							<tbody>
								<tr data-ng-repeat="patient in patients | orderBy:patientsTable.sortType:patientsTable.sortReverse">
									<td>{{patient.code}}</td>
									<td>{{patient.sex}}</td>
									<td>{{patient.bornDate | date: mediumDate}}</td>
									<td>{{patient.record}}</td>
									<td>
										<button type="submit" class="btn btn-default btn-xs"
												data-ng-click="showSamples(patient.code)">
											<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
											&nbsp;Sample
										</button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					
					<h3>Analysis</h3>
					
					<form id="submitForm" class="form-horizontal"  data-ng-cloak data-ng-submit="submitForm()">
					
						<div class="form-group">
							<label for="selected-samples-table" class="col-sm-4 control-label">Selected samples</label>
							<div class="col-sm-8">
								<div class="table-responsive" data-ng-cloak>
									<div data-ng-show="selected_samples.length==0" style="padding-top:7px;">
										<i>None added...</i>
									</div>
									<table class="table table-condensed" data-ng-show="selected_samples.length>0">
										<thead>
											<tr>
												<th></th>
												<th>Patient Code</th>
												<th>Sample ID</th>
												<th></th>
											</tr>
										</thead>
										<tbody>
											<tr data-ng-repeat="sample in selected_samples">
												<td>{{$index+1}}.</td>
												<td>{{sample.patientCode}}</td>
												<td>{{sample.sampleId}}</td>
												<td>
												<div class="btn-group" role="group" aria-label="...">
													<button type="submit" class="btn btn-link btn-xs" data-ng-disabled="$index==0"
															data-ng-click="moveUp($index)">
														<span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span>
													</button>
													<button type="submit" class="btn btn-link btn-xs" data-ng-disabled="$index==selected_samples.length-1"
															data-ng-click="moveDown($index)">
														<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>
													</button>
													<button type="submit" class="btn btn-link btn-xs" data-ng-click="removeSample(sample.patientCode, sample.sampleId, $index)">
														<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
													</button>
												</div>
												</td>
											</tr>
										</tbody>
									</table>
									<p class="help-block" data-ng-show="selected_samples.length>0">
										Reorder your selected samples or remove those you are not interested.
									</p>
								</div>
							</div>
						</div>
						
						<div class="form-group">
							<label for="services" class="col-sm-4 control-label">Services</label>
							<div class="col-sm-8">
								<div class="checkbox" id="services">
									<label>
										<input type="checkbox" data-ng-model="services.clusterHeatmap"> Cluster heatmap
									</label>
								</div>
								<div class="checkbox">
									<label>
										<input type="checkbox" data-ng-model="services.geneRegNetwork" data-ng-disabled="selected_samples.length<3"> Gene regulatory network
									</label>
								</div>
								<p class="help-block">
									Select at least one service to be executed.
								</p>
							</div>
						</div>
					
 						<div class="form-group">
							<label for="percentage1" class="col-sm-4 control-label">% of significantly altered gene expression levels</label>
							<div class="col-sm-8 slider-container">
								<input id="percentage1" data-slider-id='percentageSlider1' type="text"
										data-slider-min="1" data-slider-max="100" data-slider-step="1"
										data-slider-value="5" data-ng-model="perc1" data-slider-tooltip="hide"
										class="form-control"/>
								<span style="margin-left:15px;"><span id="percentageVal1">3</span> %</span>
							</div>
						</div>
						
 						<div class="form-group" data-ng-show="services.geneRegNetwork==true">
							<label for="percentage2" class="col-sm-4 control-label"># maximum of links of the Gene Regulatory Network</label>
							<div class="col-sm-8 slider-container">
								<input id="percentage2" data-slider-id='percentageSlider2' type="text"
										data-slider-min="1" data-slider-max="50" data-slider-step="1"
										data-slider-value="20" data-ng-model="perc2" data-slider-tooltip="hide"
										class="form-control"/>
								<span style="margin-left:15px;"><span id="percentageVal2">3</span> links</span>
							</div>
						</div>
						
						<div class="form-group">
							<div class="col-sm-offset-4 col-sm-8">
								<button id="execBtn" type="submit" class="btn btn-primary"
										data-ng-disabled="selected_samples.length==0 || !existsSelectedService()"
										style="margin-bottom:20px">Submit</button>
							</div>
						</div>
						
					</form>
					
					<%@ include file="/WEB-INF/jsp/contactMsg.jsp" %>
				</div>
			</div>
					
		</div><!-- /.container -->
		
		<%@ include file="/WEB-INF/jsp/footer.jsp" %>
		
		<%@ include file="/WEB-INF/jsp/javascript.jsp" %>
		
		<div class="modal fade" tabindex="-1" role="dialog" id="samplesModal">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
						<h3 class="modal-title">Samples</h3>
					</div>
					<div class="modal-body">
						<p><strong>Patient code:</strong> {{selectedPatient.code}}</p>
						<table class="table">
							<thead>
								<tr>
									<th>ID</th>
									<th>Sample date</th>
									<th>Experiment date</th>
									<th></th>
								</tr>
							</thead>
							<tbody>
								<tr data-ng-repeat="sample in selectedPatient.samples">
									<td>{{sample.id}}</td>
									<td>{{sample.sampleDate | date: mediumDate}}</td>
									<td>{{sample.experimentDate | date: mediumDate}}</td>
									<td>
										<button type="submit" class="btn btn-default btn-xs"
												data-ng-click="addSample(selectedPatient.code, sample.id)"
												data-ng-disabled="sample.added">
											<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
											&nbsp;Add
										</button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div><!-- /.modal-content -->
			</div><!-- /.modal-dialog -->
		</div><!-- /.modal -->
		
		<script src="vendors/bootstrap-slider/js/bootstrap-slider.min.js"></script>
		
		<script>

			$('#percentage1')
				.slider()
				.on("slide", function(slideEvt) {
					$("#percentageVal1").text(slideEvt.value);
				});
			$("#percentageVal1").text($('#percentage1').slider('getValue'));

			$('#percentage2')
				.slider()
				.on("slide", function(slideEvt) {
					$("#percentageVal2").text(slideEvt.value);
				});
			$("#percentageVal2").text($('#percentage2').slider('getValue'));

		</script>
		
	</body>
</html>