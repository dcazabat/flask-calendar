function validate_month(selectedStand){
    document.location.href="/"+selectedStand.value
}

function validate_date(selectedItem){
    const days_week = [
        'domingo',
        'lunes',
        'martes',
        'miércoles',
        'jueves',
        'viernes',
        'sábado',
      ];
    console.log(selectedItem.id, selectedItem.value);
    if (selectedItem.id == 'day') {
        day = selectedItem.value;}
    else{
        day = document.getElementById('day').value;
    }
    if (selectedItem.id == 'month') {
        month = selectedItem.value;
    } else {
        month = document.getElementById('month').value;
    }
    if (selectedItem.id == 'year') {
        year = selectedItem.value;
    } else {
        year = document.getElementById('year').value;
    }

    let isValidDate = Date.parse(month+'/'+day+'/'+year);

    if (isNaN(isValidDate)) {
        document.getElementById('btn_game').disabled = true;
        document.getElementById('message').innerHTML = "This is not a valid date format.";
    }
    else{
        document.getElementById('btn_game').disabled = false;
        document.getElementById('message').innerHTML = "Desde JS <br> El dia de la Semana: "+days_week[new Date(month+'/'+day+'/'+year).getDay()];"";
    }
}