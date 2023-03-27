document.getElementById('id_profile_photo').onchange = function () {
    var src = URL.createObjectURL(this.files[0])
    document.getElementById('image').src = src
}