document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.btn').forEach(button =>{
        button.onclick = function() {
            LikeToggle(this.dataset.page)
        }
    })
})

document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.follow').forEach(button =>{
        button.onclick = function() {
            FollowToggle(this.dataset.profile)
        }
    })
})

// Toggle the like and unlike/ Update heart color
function LikeToggle(id){
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(data =>{
        if (data.status == true){
            document.querySelector(`#btn_${id}`).style.color = "red";
        }else{
            document.querySelector(`#btn_${id}`).style.color = "grey";
        }
        document.querySelector(`#like_${id}`).innerHTML = data.likes;
    })

}

// Toggle the follow and unfollow/ Update follower count
function FollowToggle(id){
    fetch(`/follow/${id}`)
    .then(response => response.json())
    .then(data =>{
        if (data.status == true){
            document.querySelector(`#follow_${id}`).innerHTML = "Unfollow";
        }else{
            document.querySelector(`#follow_${id}`).innerHTML = "Follow";
        }
        document.querySelector(`#count_${id}`).innerHTML = `Follower: ${data.followers}`;
    })
}

// https://www.w3schools.com/howto/howto_js_popup_form.asp
// Open the edit form
function openForm(id) {
    document.getElementById(`myForm_${id}`).style.display = "block";
  }

// Close the edit form
function closeForm(id) {
    document.getElementById(`myForm_${id}`).style.display = "none";
}

// Edit the content
function Edit(id, edit){
    fetch(`/edit/${id}/${edit}`)
    .then(response => response.json())
    .then(data =>{
        document.querySelector(`#content_${id}`).innerHTML = data.edit;
    })
}





