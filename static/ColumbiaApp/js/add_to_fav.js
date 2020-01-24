async function add_to_fav(name, cuisine){
    name = name.split(' ').join('+');
    cuisine = cuisine.split(' ').join('+');
    const response = await fetch('/add_to_fav?name=' + name + '&cuisine=' + cuisine);
    const rsp = await response.json(); //extract JSON from the http response
    if(rsp['m_type'] == "failure") {
        $.notify({
            // options
            message: rsp['message'] 
        },{
            // settings
            type: 'danger',
            placement: {
                from: "top",
                align: "center"
            },
        });
    } else if(rsp['m_type'] == "success"){
        $.notify({
            // options
            message: rsp['message']
        },{
            // settings
            type: 'success'
        });
    } else {
        $.notify({
            // options
            message: rsp['message']
        },{
            // settings
            type: 'info'
        });
    }
}