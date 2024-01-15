class NewTasks{
    constructor(id, staffs){
        this.id         = id
        this.staffs     = staffs
        this.name       = "new task",
        this.descript   = "",
        this.staffid    = 0
        

    }

    #setName(val){ this.name = val;}
    #setDescript(val){ this.descript = val;}
    #setStaff(val){ this.staffid = val;}

    #dropdownSelected(elm, value){
        var select = document.querySelectorAll(elm)[0];
        var option;

        for (var i=0; i<select.options.length; i++) {
            option = select.options[i];

            if (option.value == value) {
                option.setAttribute('selected', true);
                return; 
            } 
        }
    }

    getData(){
        return {
            name:       this.name,
            descript:   this.descript,
            staffid:    this.staffid
        }
    }

    build(){
        return  '<div class="task_editor" data-id="'+this.id+'">'+
                '<input name="task_name" value="'+this.name+'"  maxlenght="200" placeholder="Task Name"/>'+
                '<textarea name="task_descript" value="'+this.descript+'" maxlenght="1024" placeholder="Task Description"></textarea></td>'+
                '<select name="task_staff" required>'+this.buildStaffSelect()+'</select>'+
                '<button class="remove_task" type="button">remove</button>'+
                '</div>'
    }

    buildStaffSelect(data){
        return  '<option disabled selected value >Not Assigned</option>'+
                this.staffs.map(function(staff, index){ 
                    return '<option value="'+staff.id+'">'+ staff.staffname +'</option>' 
                }).join('')
    }

    eventlistener(callback){
        var _ = this, elm = document.querySelectorAll(".task_editor[data-id='"+this.id+"']")
    
        if (elm[0].querySelector("input[name='task_name']") != null){
            var elminput = elm[0].querySelectorAll("input[name='task_name']")
            elminput[0].addEventListener("input",function(input){
                _.#setName( this.value )
            });
        }

        if (elm[0].querySelector("textarea[name='task_descript']") != null){
            var elminput = elm[0].querySelectorAll("textarea[name='task_descript']")
            elminput[0].addEventListener("input",function(){
                _.#setDescript( this.value )
            });
        }

        if (elm[0].querySelector("select[name='task_staff']") != null){
            var elminput = elm[0].querySelectorAll("select[name='task_staff']")
            elminput[0].addEventListener("change",function(){
                _.#setStaff( this.value )
            });
        }

        if (elm[0].querySelector("button.remove_task") != null){
            var elmbtn = elm[0].getElementsByClassName("remove_task")
            elmbtn[0].addEventListener("click",function(){
                var confrim = window.confirm("Are you sure you want to Delete this Task?");

                if (_.id > 0 && confrim) {
                    callback("delete", _.id)
                    elm[0].remove()
                }
            });
        }
    }
}

class NewProject{
    constructor(data){
        Object.assign(this, data)
        this.staffs     = []
    }

    #setDescript(val){  this.descript = val;}
    #setTitle(val){     this.name = val;}
    #setDueDate(val){   this.duedate = val; }
    #setPriority(val){  this.priority = val; }
    #setType(val){      this.type = val; }

    #getData(){
        return {
            name:       this.name,
            descript:   this.descript,
            duedate:    this.duedate,
            priority:   this.priority,
            type:       this.type,
            tasks:      this.tasks.map(function(task, index){ return task.getData() })
        }
    }

    #RemoveTask(id){
		var index = this.tasks.findIndex(obj => obj.id == id)
		if (index > -1) { this.tasks.splice(index, 1) }
    }

    #CreatTask(){
        var _ = this, id = this.#checkID()
        var elmtaskmain = document.querySelectorAll("div.task_main")
        var tasks = new NewTasks(id, this.staffs)

        this.tasks.push(tasks)
        elmtaskmain[0].insertAdjacentHTML("beforeend", tasks.build() )
        tasks.eventlistener(function(op, id){
            if(op == "delete" && id > 0){
                _.#RemoveTask(id)
            }
        })
    }

    #checkID(){
        var id = 1;
    
        while ( this.tasks.some(item => item.id == "newtask-"+id) ) {
            id ++;
        }
        return id;
    }

    #dropdownSelected(elm, value){
        var select = document.querySelectorAll(elm)[0];
        var option;

        for (var i=0; i<select.options.length; i++) {
            option = select.options[i];

            if (option.value == value) {
                option.setAttribute('selected', true);
                return; 
            } 
        }
    }

    AppendData(){
        document.querySelectorAll("input[name='project_name']")[0].value        = this.name;
        document.querySelectorAll("textarea[name='project_descript']")[0].innerHTML = this.descript;
        this.#dropdownSelected("select[name='project_priority']", this.priority)
        this.#dropdownSelected("select[name='project_type']", this.type)
    }

    addEventListener(){
        this.#getStaffs()
        var _ = this;
        
        if (document.querySelector("input[name='project_name']") != null){
            var elminput = document.querySelectorAll("input[name='project_name']")
            elminput[0].addEventListener("input",function(input){
                _.#setTitle( this.value )
            });
        }

        if (document.querySelector("textarea[name='project_descript']") != null){
            var elminput = document.querySelectorAll("textarea[name='project_descript']")
            elminput[0].addEventListener("input",function(){
                _.#setDescript( this.value )
            });
        }

        if (document.querySelector("input[name='project_duedate']") != null){
            var elminput = document.querySelectorAll("input[name='project_duedate']")
            elminput[0].addEventListener("input",function(input){
                _.#setDueDate( this.value )
            });
        }

        if (document.querySelector("select[name='project_priority']") != null){
            var elminput = document.querySelectorAll("select[name='project_priority']")
            elminput[0].addEventListener("change",function(){
                _.#setPriority( this.value )
            });
        }

        if (document.querySelector("select[name='project_type']") != null){
            var elminput = document.querySelectorAll("select[name='project_type']")
            elminput[0].addEventListener("change",function(){
                _.#setType( this.value )
            });
        }

        if (document.querySelector("button.view_project_list") != null){
            var elmbtn = document.getElementsByClassName("view_project_list")
            elmbtn[0].addEventListener("click",function(button){
                location.href = "/";
            });
        }

        if (document.querySelector("button.create_task") != null){
            var elmbtn = document.getElementsByClassName("create_task")
            
            elmbtn[0].addEventListener("click",function(button){
                _.#CreatTask()
            });
        }

        if (document.querySelector("form#project_detail_ctn")!= null){
            var elmform = document.getElementById("project_detail_ctn")
            
            elmform.addEventListener("submit",function(evt){
                evt.preventDefault()
                evt.stopPropagation()

                if (_.tasks.length > 0 && !_.#taskHasNames() && !_.#taskHasStaff() ){
                    //_.#EditProject()
                }else if(_.tasks.length == 0){
                    alert("Add tasks to the project")
                }else if( _.#taskHasNames() ){
                    alert("Please give a title to the tasks")
                }else if( _.#taskHasStaff() ){
                    alert("Please assign a staffmember to the tasks")
                }

                return false;
            });
        }
    }

    #taskHasNames(){ return this.tasks.some(obj => (obj.name == "") ) }
    #taskHasStaff(){ return this.tasks.some(obj => (obj.staffid == 0) ) }

    #EditProject(){
        var _ = this, formData = new FormData()
        formData.append("details", JSON.stringify(_.#getData()) )
        fetch('/projectEdit', {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken"), },
            body: JSON.stringify(_.#getData()),
        })
        .then((response) => {return response.json()})
        .then((data) => { 
            if(data.status == "success"){
                //_.#resetData()
                alert( data.message )
                window.location.href = "/projectDetail"
            }
        })
    }

    #getStaffs(){
        var _ = this
        fetch('/fectstaffs', {
            method: "POST",
            headers: { "X-CSRFToken": getCookie("csrftoken"), }
        })
        .then((response) => {return response.json()})
        .then((data) => { _.staffs = data })
    }
}

document.addEventListener("DOMContentLoaded", function(){
    fetch('/getEditDetails', {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken"), }
    })
    .then((response) => {return response.json()})
    .then((data) => { 
        var createProject = new NewProject(data)
        createProject.AppendData()
        createProject.addEventListener()
    })    
})