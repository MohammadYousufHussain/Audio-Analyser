var keyaud = []
    var keysr = []
    var bigaud = []
    var bigsr = []
    var search1aud = []
    var search1sr = []
    var search2aud = []
    var search2sr = []
    var search3aud = []
    var search3sr = []
    
    var endpoint = 'searchplot'
    $.ajax({
        
        method: "GET",
        url: endpoint,
        success: function(data){
            keyaud = data.keyaud
            keysr = data.keysr
            bigaud = data.bigaud
            bigsr = data.bigsr
            search1aud = data.search1aud
            search1sr = data.search1sr
            search2aud = data.search2aud
            search2sr = data.search2sr
            search3aud = data.search3aud
            search3sr = data.search3sr
            rmse = data.rmse
            lentime = data.lentime

            

            console.log("successful")
            
            var ctx = document.getElementById('keyword').getContext('2d');
            
            var keyword = new Chart(ctx, {
            type: 'line',
            data: {
                labels: keysr,
                datasets: [{
                    label: 'Amplitude',
                    data: keyaud,
                    backgroundColor: [
                    'rgba(54, 162, 235, 1)'
                ],
                borderColor: [
                'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 0.1,
                
                pointRadius: 0
                    
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            
                            stepSize: 0.5,
                            maxTicksLimit: 10
                        }
                    }]
                }
            }
            
            })
            var ctx = document.getElementById('large').getContext('2d');
            var large = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: bigsr,
                    datasets: [{
                        yAxisID: 'first-y-axis',
                        label: 'Amplitude',
                        data: bigaud,
                        backgroundColor: 'rgba(54, 162, 235, 1)',
                    borderColor: [
                    'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0,
                    
                        
                    },
                    {
                        yAxisID: 'second-y-axis',
                        label: 'Keyword',
                        data: lentime,
                        backgroundColor: [
                        'rgba(255, 159, 64, 0.2)'
                    ],
                        borderColor: [
                    'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0,
                    
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                
                                stepSize: 0.5,
                                maxTicksLimit: 10
                            }
                        }],
                        yAxes: [{
                            id: 'first-y-axis',
                            type: 'linear',
                            position: 'left',
                            scaleLabel: 'Amplitude'

                        }, {
                            id: 'second-y-axis',
                            type: 'linear',
                            position: 'right',
                            display: false
                        }]
                    }
                }
            })
            var ctx = document.getElementById('search_1').getContext('2d');
            var search_1 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: search1sr,
                    datasets: [{
                        label: 'Amplitude',
                        data: search1aud,
                        backgroundColor: [
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderColor: [
                    'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0
                        
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                
                                stepSize: 0.5,
                                maxTicksLimit: 10
                            }
                        }]
                    }
                }
            })

            var ctx = document.getElementById('largeB').getContext('2d');
            var large = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: bigsr,
                    datasets: [{
                        yAxisID: 'first-y-axis',
                        label: 'Amplitude',
                        data: bigaud,
                        backgroundColor: [
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderColor: [
                    'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0
                        
                    },
                    {
                        yAxisID: 'second-y-axis',
                        label: 'Rmse Values',
                        data: rmse,
                        backgroundColor: [
                        'rgba(255, 159, 64, 0.2)'
                    ],
                        borderColor: [
                    'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                
                                stepSize: 0.5,
                                maxTicksLimit: 10
                            }
                        }],
                        yAxes: [{
                            id: 'first-y-axis',
                            type: 'linear',
                            position: 'left',
                        }, {
                            id: 'second-y-axis',
                            type: 'linear',
                            position: 'right',
                        }]
                    }
                }
            })
            /*
            var ctx = document.getElementById('search_2').getContext('2d');
            var search_2 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: search2sr,
                    datasets: [{
                        label: 'Amplitude',
                        data: search2aud,
                        backgroundColor: [
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderColor: [
                    'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0
                        
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                
                                stepSize: 0.5,
                                maxTicksLimit: 10
                            }
                        }]
                    }
                }
            })
            var ctx = document.getElementById('search_3').getContext('2d');
            var search_3 = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: search3sr,
                    datasets: [{
                        label: 'Amplitude',
                        data: search3aud,
                        backgroundColor: [
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderColor: [
                    'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 0.1,
                    
                    pointRadius: 0
                        
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            ticks: {
                                
                                stepSize: 0.5,
                                maxTicksLimit: 10
                            }
                        }]
                    }
                }
            })*/
                
        },
        error: function(eror_data){
            console.log("error occured")
            console.log(bigsr)
            
        }
    })
    