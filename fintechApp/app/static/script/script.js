function toggleSearch(toggle){
    if(toggle){
        document.getElementById('reportSearch').style.display = 'inline'; 
        document.getElementById('showSearch').style.display = 'none';
    }
    else{
        document.getElementById('reportSearch').style.display = 'none'; 
        document.getElementById('showSearch').style.display = 'inline';
    }
}