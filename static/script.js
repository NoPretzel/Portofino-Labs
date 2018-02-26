function populateLog(logEndpoint, logID) {
    $.getJSON({'url':'http://localhost:5000/v1'+logEndpoint,
    'beforeSend':
     function(xhr) {
        xhr.setRequestHeader("Authorization",
            "Basic " + btoa('admin' + ":" + 'secret'));
    }, 'success':
     function(result){
        var logs = result['logs'];
        var aggregates = {};
        for (var log in logs) {
            var timestamp = new Date(Math.ceil(logs[log]['timestamp']) * 1000).toISOString();
            $('#raw-'+logID).append('<tr><td>'+logs[log]['ip']+'</td><td>'+timestamp+'</td></tr>');
            if (!(logs[log]['ip'] in aggregates)) {
                aggregates[logs[log]['ip']] = {};
            }
            console.log(Date.now());
            console.log(logs[log]['timestamp']);
            var minutesAgo = Math.ceil((Math.ceil(Date.now()/1000) - Math.ceil(logs[log]['timestamp']))/60).toString();

            if (!(minutesAgo in aggregates[logs[log]['ip']])) {
                aggregates[logs[log]['ip']][minutesAgo] = 1;
            } else {
                aggregates[logs[log]['ip']][minutesAgo] += 1;
            }
        }

        for (var ip in aggregates) {
            var row = '<tr><td>'+ip+'</td><td>';
            for(var minuteAggregate in aggregates[ip]) {
                row += aggregates[ip][minuteAggregate].toString() + ' hit(s) ' + minuteAggregate + ' minute(s) ago <br />';
            }
            row += '</td></tr>';
            $('#aggregate-'+logID).append(row);
        }
    }});
}

populateLog('/hello-world/logs', 'hello-world');
populateLog('/logs', 'all');