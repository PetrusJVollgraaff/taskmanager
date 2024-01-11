document.addEventListener("DOMContentLoaded", function(){

    if (document.querySelector("li.display_by") != null){
        document.querySelectorAll("li.display_by").forEach(function(button){
            button.onclick = function(e){
                var displayby = this.dataset.by;
                document.cookie = "project_by="+displayby;
                location.reload();
            }
        });
    }
    
    if (document.querySelector("button.view_project_list") != null){
        var elmbtn = document.getElementsByClassName("view_project_list")
        elmbtn[0].addEventListener("click",function(button){
            location.href = "/myprojects";
        });
    }

    if (document.querySelector("button.show_modal") != null){
        var elmbtn = document.getElementsByClassName("show_modal")
        elmbtn[0].addEventListener("click",function(button){
            var back_modal = document.getElementsByClassName("back_modal")
            back_modal[0].classList.add("show")
        });
    }

    if (document.querySelector("button.cancel_form") != null){
        var elmbtn = document.getElementsByClassName("cancel_form")
        elmbtn[0].addEventListener("click",function(button){
            var back_modal = document.getElementsByClassName("back_modal")
            back_modal[0].classList.remove("show")
        });
    }

    if (document.querySelector("button.view_project_delete") != null){
        document.querySelectorAll("button.view_project_delete").forEach(function(button){
            button.onclick = function(e){
                var id = this.dataset.id;
                var confrim = window.confirm("Are you sure you want to delete this project?");
                if (id > 0 && confrim ){
                    DeleteElms(id, "/projectdelete")
                }
            }
        });
    }

    if (document.querySelector("button.view_project_details") != null){
        document.querySelectorAll("button.view_project_details").forEach(function(button){
            button.onclick = function(e){
                var id = this.dataset.id;
                location.href = "/projectdetail?id="+id;
            }
        });
    }

    if (document.querySelector("button.view_project_edit") != null){
        document.querySelectorAll("button.view_project_edit").forEach(function(button){
            button.onclick = function(e){
                var id = this.dataset.id;
                location.href = "/projectedit?id="+id;
            }
        });
    }

    if (document.querySelector("button.view_project_tasks_edit") != null){
        document.querySelectorAll("button.view_project_tasks_edit").forEach(function(button){
            button.onclick = function(e){
                var id = this.dataset.id;
                location.href = "/projecttaskstatus?id="+id;
            }
        });
    }
})

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function CreateTasks(form){
    var istr = false;
    CreateElm(form, "/createtasks", "task", "/show_tasks")

    return istr;
}


function DeleteTasks(that){
    var id = that.dataset.id;
    var confrim = window.confirm("Are you sure you want to delete this Task?");
    
    if (confrim ){ 
        DeleteElms(id, "/deletetasks")      
    }
}

function removeElems(elms){
    document.querySelectorAll(elms).forEach(function(elm){
        elm.remove();
    });
}

function CreateElm(form, url1, type, url2){
    const data = GetFormData(form)
    
    fetch(url1, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), },
        body: data,
    }).then((response) => {return response.json()} )
    .then((data) => { 
        
        if (data.status == "success"){
            var ctn = document.getElementsByClassName("project_list")
            var html = BuildCard(type, data)
            ctn[0].insertAdjacentHTML("beforeend",  html );
            
            var confrim = window.confirm(data.message);
            if (confrim ){
                form.reset()
            }else{
                location.href = url2;
            }
        }
    })
}

function BuildCard(type, data){
    var html ='<div class="project_ctn" data-id="'+data.id+'">'

    switch(type){
        case "priority":
            html += '<button onclick="DeletePriorities(this)" class="priority_delete" data-id="'+data.id+'">Delete Project Priority</button>'+
                    '<h3><span>Priority Name: </span><span>'+data.name+'</span></h3><hr><p>Priority description: </p>'+
                    '<p>'+data.descript+'</p><hr><p><span>Priority Level:</span><span>'+data.order+'</span></p>';
            break;
        case "type":
            html += '<button onclick="DeleteTypes(this)"data-id="'+data.id+'"  class="type_delete">Delete Project Type</button>'+
                    '<h3><span>Type Name: </span><span>'+data.name+'</span></h3><hr><p>Type description: </p><p>'+data.descript+'</p>';
            break;
        case "task":
            html += '<button onclick="DeleteTasks(this)"  class="type_delete" data-id="'+data.id+'">Delete Project Task</button>'+
                    '<h3><span>Task Name: </span><span>'+data.name+'</span></h3><hr><p>Task description: </p>'+
                    '<p>'+data.descript+'</p><hr><h4><span>Task order: </span><span>'+data.order+'</span></h4>'+
                    '<h4><span>Linked to Project Type: </span><span>'+data.typename+'</span></h4>';
            break;
    }

    html += 'div'
    
    return html;
}

function DeleteElms(id, url){
    fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), },
        body: JSON.stringify({ 'id': id }),
    }).then((response) => {return response.json()} )
    .then((data) => { 
        if(data.status == "success"){
            removeElems('div.project_ctn[data-id="'+id+'"]')
        }
    })
}

function GetFormData(form){
    const data = new URLSearchParams();
    for (const pair of new FormData(form)) {
        data.append(pair[0], pair[1]);
    }

    return data;
}

