class Tasks{
    constructor(data, projectid){
        Object.assign(this, data)
        this.projectid = projectid
    }

    #setStatus(val){ this.status = val }

    #changeStatus(val){ 
        var _ = this, elm = document.querySelectorAll(".task_editor[data-id='"+this.id+"']")

        fetch('/taskstatus', {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken"), },
            body: JSON.stringify({ taskid: _.id, projectid: _.projectid, status: val }),
        })
        .then((response) => { return response.json() })
        .then((data) => { 
            if(data.status == "success"){
                _.#setStatus(val)
                location.reload()
                /*if (elm[0].querySelector("button.btn") != null){
                    var elmbtn = document.getElementsByClassName("btn")
                    //elmbtn[0].removeEventListener("click");

                    elmbtn[0].outerHTML = _.#buildbtn()
                    _.eventlistner()
                }*/
                                
                alert(data.message)
            }else{
                alert(data.message)
            }            
        })
    }
    
    #buildbtn(){
        var Title = (this.status == "complete")? "Call Back": (this.status == "start")? "Complete" : "Start";
        var type = (this.status == "complete")? "callback": (this.status == "start")? "complete" : "start";
        return '<button class="btn" data-t="'+type+'">'+Title +'</button>'
    }

    build(){
        return  '<div class="task_editor" data-id="'+this.id+'">'+
                '<div name="task_name">'+this.name+'</div><div name="task_descript">'+this.descript+'</div>'+
                '<div name="task_staff">'+this.staffname+'</div><div class="task_btn">'+this.#buildbtn()+'</div></div>'
    }

    eventlistner(){
        var _ = this, elm = document.querySelectorAll(".task_editor[data-id='"+this.id+"']")
        if (elm[0].querySelector("button.btn") != null){
            var elmbtn = document.getElementsByClassName("btn")
            elmbtn[0].addEventListener("click",function(button){
                var val = button.target.dataset.t
                _.#changeStatus(val)
            });
        }
    }


}

class ProjectDetails{
    constructor(data){
        Object.assign(this, data)
        console.log(this)
    }

    #buildTasks(){
        var _ = this;
        var elmtaskmain = document.querySelectorAll("div.task_main")
        this.tasks.forEach(function(item, index){
            var task = new Tasks(item, _.id)
            elmtaskmain[0].insertAdjacentHTML("beforeend", task.build() )
            task.eventlistner()
        })
    }

    build(){
        var _ = this, elmP = document.getElementById("project_detail_ctn")

        elmP.querySelector('div[name="project_name"]').innerHTML        = this.projectname
        elmP.querySelector('div[name="project_descript"]').innerHTML    = this.projectdescript
        elmP.querySelector('div[name="project_duedate"]').innerHTML     = this.DueDate
        elmP.querySelector('div[name="project_priority"]').innerHTML    = this.priorityname
        elmP.querySelector('div[name="project_type"]').innerHTML        = this.typename

        _.#buildTasks()
    }

    eventlistner(){

    }
}

document.addEventListener("DOMContentLoaded", function(){
    fetch('/getDetails', {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), }
    })
    .then((response) => {return response.json()})
    .then((data) => { 
        var project = new ProjectDetails(data)
        project.build()
        project.eventlistner()
    })
})