function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$( ".delete-button" ).each( function () {
    var button = $(this);
    button.click(function(){
        var answer;
        if(this.id == 0){
            answer = window.confirm("Clear cart?");
        }
        else{
            answer = true;
        }
        if (answer) {
            $.ajax({
                url: delete_url,
                type:"POST",
                headers: {'X-CSRFToken': csrftoken},
                data:{cart_id: this.id},
                success: () => {window.location.replace(window.location.href)}
                }
              )  
        }        
    })
});