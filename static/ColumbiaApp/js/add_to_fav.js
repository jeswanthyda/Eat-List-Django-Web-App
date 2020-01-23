async function add_to_fav(name, cuisine){
    name = name.split(' ').join('+');
    cuisine = cuisine.split(' ').join('+');
    const response = await fetch('/add_to_fav?name=' + name + '&cuisine=' + cuisine);
    const rsp = await response.json(); //extract JSON from the http response
    alert(rsp['message'])
}