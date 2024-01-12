function DeleteProject(id){
    var confrim = window.confirm("Are you sure you want to Delete this Project?");
    
    if (id > 0 && confrim) {
        fetch('/delete', {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken"), },
            body: JSON.stringify({pid: id})
        })
        .then((response) => {return response.json()})
        .then((data) => { 
            if(data.status == "success"){
                document.querySelector(".project_ctn[data-pid='"+id+"']").remove()
                alert(data.message)
            }else{
                alert(data.message)
            }
        })
    }
}