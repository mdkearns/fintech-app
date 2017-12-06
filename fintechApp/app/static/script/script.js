encFileCount = 0;

function pageScript(){
    if(window.location.pathname == "/app/reports/" || window.location.pathname == "/app/reports_search/" || window.location.pathname == "/app/"){
        $('#content-container').css("padding-left", "0");
    }

    if(window.location.pathname.substr(0,12) == "/app/report/"){
        $('#content-container').css("padding-left", "20%");
    }

    if(window.location.pathname == "/app/reports_search/"){
        var query = location.search.substr(1);
        var result = {};
        query.split("&").forEach(function(part) {
          var item = part.split("=");
          result[item[0]] = decodeURIComponent(item[1]);
        });
        
        if(result['reportNameExact']){
            $("[name='reportNameExact']").prop("checked",true);
        }
        if(result['companyNameExact']){
            $("[name='companyNameExact']").prop("checked",true);
        }
        if(result['companyCEOExact']){
            $("[name='companyCEOExact']").prop("checked",true);
        }
        if(result['companyLocationExact']){
            $("[name='companyLocationExact']").prop("checked",true);
        }
        if(result['companyCountryExact']){
            $("[name='companyCountryExact']").prop("checked",true);
        }
        if(result['sectorExact']){
            $("[name='sectorExact']").prop("checked",true);
        }
        if(result['industryExact']){
            $("[name='industryExact']").prop("checked",true);
        }
        if(result['myReports']){
            $("[name='myReports']").prop("checked",true);
        }
        if(result['favorited']){
            $("[name='favorited']").prop("checked",true);
        }

        $("[name='reportName']")[0].value = result['reportName'];
        $("[name='daterange']")[0].value = result['daterange'].split('+').join(" ");
        $("[name='companyName']")[0].value = result['companyName'];
        $("[name='companyCEO']")[0].value = result['companyCEO'];
        $("[name='companyLocation']")[0].value = result['companyLocation'];
        $("[name='companyCountry']")[0].value = result['companyCountry'];
        $("[name='sector']")[0].value = result['sector'];
        $("[name='industry']")[0].value = result['industry'];
        $("[name='currentProjects']")[0].value = result['currentProjects'];

    }

    
    $(function() {
        $('input[name="daterange"]').daterangepicker({
            timePicker: true,
            timePickerIncrement: 30,
            locale: {
                format: 'MM/DD/YYYY h:mm A'
            }
        });
    });
}


function addEncCount(a){
    if(a){
        $('#encCount')[0].innerText = encFileCount + " encrypted files";
    }
    else{
        encFileCount++;
    }
}

function addRating(){
    var ratings = $("#allRatings")[0].innerHTML.replace(/\s/g,'').split("");
    var total = 0;
    ratings.forEach(function(x){
        total += parseInt(x);
    });
    total = (total/ratings.length);
    if(ratings.length > 0){
        $("#rating")[0].innerHTML = "Average Rating: " + total + ' </div><span id="star" class="glyphicon glyphicon-star"></span> (' + ratings.length + ')';
    }else{
        $("#rating")[0].innerHTML = "No Ratings " + ' <span id="star" class="glyphicon glyphicon-star-empty"></span>';
    }
    
}