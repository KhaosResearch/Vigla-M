angular.module('melanomaApp',[])
    .controller('heatMapFormCtrl', ['$scope', '$http', '$filter', '$location', function ($scope, $http, $filter, $location) {
	
	$scope.selected_samples = [];
	$scope.services = {
			clusterHeatmap : false,
			geneRegNetwork : false
	};
	$scope.patients = null;
	$scope.selectedPatient = {};
	
	$scope.patientsTable = {
			sortType: 'code',
			sortReverse: false
	};
	
	$scope.init = function() {
		fetch();
	};
	
	$scope.showSamples = function(patientCode) {
		$scope.selectedPatient = $filter('filter')($scope.patients, {'code': patientCode})[0];
		$('#samplesModal').modal();
	};
	
	$scope.addSample = function(patientCode, sampleId) {
		var patient = $filter('filter')($scope.patients, {'code': patientCode})[0];
		var sample = $filter('filter')(patient.samples, {'id': sampleId})[0];
		sample.added = true;
		$scope.selected_samples.push({
			patientCode: patientCode,
			sampleId: sampleId
//			patient_idx: patient_idx,
//			sample_idx: sample_idx
		});
	};
	
	$scope.removeSample = function(patientCode, sampleId, idx) {
		selected_sample = $scope.selected_samples[idx];
		var patient = $filter('filter')($scope.patients, {'code': patientCode})[0];
		var sample = $filter('filter')(patient.samples, {'id': sampleId})[0];
		sample.added = false;
		$scope.selected_samples.splice(idx, 1);
	};
	
	$scope.moveUp = function(idx) {
		swapElement($scope.selected_samples, idx-1, idx);
	};
	
	$scope.moveDown = function(idx) {
		swapElement($scope.selected_samples, idx, idx+1);
	};
	
	$scope.existsSelectedService = function() {
		return ($scope.services.clusterHeatmap || $scope.services.geneRegNetwork);
	};
	
	$scope.submitForm = function() {
		var labelList = "";
		var idList = "";
		for (i in $scope.selected_samples) {
			var sample = $scope.selected_samples[i];
			labelList += "&label=" + sample.patientCode +  "-" + sample.sampleId;
			idList += "&id=" + sample.sampleId;
			console.log(labelList);
			console.log(idList);
		}
		
		var percentage1 = $('#percentage1').slider('getValue') / 100;
		var maxLinks = $('#percentage2').slider('getValue') / 100;
		var url = "result.jsp?percentage1=" + percentage1
			+ "&max_links=" + maxLinks 
			+ "&clusterHeatmap=" + $scope.services.clusterHeatmap
			+ "&geneRegNetwork=" + $scope.services.geneRegNetwork
			+ labelList + idList;
		window.location.href = url;
	};
	
	function fetch() {
		$http.get("api/db/patients_and_samples")
		.then(function(response) {
			$scope.patients = response.data;
		});
	}
	
}]);

function swapElement(array, indexA, indexB) {
	var tmp = array[indexA];
	array[indexA] = array[indexB];
	array[indexB] = tmp;
}