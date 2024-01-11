class Tasks{
    constructor(data){
        Object.assign(this, data)
        console.log(this)
    }

    build(){
        return  '<div class="task_editor" data-id="'+this.id+'">'+
                '<div name="task_name">'+this.name+'</div><div name="task_descript">'+this.descript+'</div>'+
                '<div name="task_staff">'+this.staffname+'</div><div class="task_btn"></div></div>'
    }

    eventlistner(){

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
            var task = new Tasks(item)
            elmtaskmain[0].insertAdjacentHTML("beforeend", task.build() )
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