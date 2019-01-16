angular.module('melanomaApp',[])
.controller('heatMapResponseCtrl', ['$scope', '$sce', '$sceDelegate', '$http', '$location', function ($scope, $sce, $sceDelegate, $http, $location) {
    	
    $scope.clusterHeatmap = { selected : false, status : 0 };
    $scope.geneRegNetwork = { selected : false, status : 0 };
    	
	$scope.init = function() {
		$scope.ids = $location.search().id;
		$scope.labels = $location.search().label;
		$scope.percentage1 = $location.search().percentage1;
		$scope.max_links = $location.search().max_links;
        $scope.clusterHeatmap.selected = $location.search().clusterHeatmap === 'true';
		$scope.geneRegNetwork.selected = $location.search().geneRegNetwork == 'true';
		fetch();
	};
	
	$scope.isDefined = function(v) {
		return angular.isDefined(v);
    };
	
	function fetch() {
		if ($scope.clusterHeatmap.selected) {
			$http({
				method : 'GET',
				url : "api/service/cluster_heatmap",
				//dataType: "html",
				params: {
					 "id" : $scope.ids, // ids is [1, 2, 3, 4]
					 "label" : '$scope.labels',
					 "percentage" : $scope.percentage1 
				}
			})
			.then(
					function (response) {

						console.log("SUCCESS!!!");
						//console.log(response);
						console.log($scope.ids);
                        //console.log(response.data);
                        //$scope.codigohtml= response.data;
                        $('#codigohtml').html(response.data);

                        $scope.clusterHeatmap.status = 1;

					},
					function (response) {
						console.log("ERROR!!!");
				    	console.log(response);
                        $scope.clusterHeatmap.status = -1;
					}
			);
		}
		
		if ($scope.geneRegNetwork.selected) {
			$http({
				method : 'GET',
				url : "api/service/gene_regulatory_network",
				params: {
					 "id" : $scope.ids, // ids is [1, 2, 3, 4]
					 "label" : '$scope.labels',
					 "percentage1" : $scope.percentage1,
					 "max_links" : $scope.max_links
				}
			})
			.then(
					function (response) {
						console.log("SUCCESS!!!");
						console.log(response);
                        console.log(response.data);

                        //$scope.codigogrn = response.data;
                        $('#codigogrn').html(response.data);

                        $scope.geneRegNetwork.status = 1;
						//$scope.geneRegNetwork.id = response.data;
                        /*$(function(){
                            $("#sandrous").load("/home/khaosdev/AnacondaProjects/PGenes/3DNetworkx_2018-09-26_122738.html");
                        })*/
                        //$scope.myHtmlVarGRN= $sceDelegate.trustAs($sce.HTML,response.data)



                    },
					function (response) {
						console.log("ERROR!!!");
				    	console.log(response.data);
			    		$scope.geneRegNetwork.status = -1;
					}
			);
		}
	}
	
	function getParameters() {
		var ret = "?percentage=" + $scope.percentage;
		for (var i=0; i<$scope.ids.length; i++) {
			ret += "&id=" + $scope.ids[i];
		}
		for (var i=0; i<$scope.labels.length; i++) {
			ret += "&label=" + $scope.labels[i];
		}
		return ret;
	}
	
}]).config(['$locationProvider', function($locationProvider) {
	$locationProvider.html5Mode(true);
}]);
