logindiv = document.getElementById('login')
body = document.querySelector('body')
browse = document.getElementById('browse')
category = document.getElementsByClassName('category')[0]

/*login.addEventListener('click',function(){
    if('{{ session.logged_in}} == True')
    {
        
    }
    else{
        log()
    }
})*/
function login()
{
    logindiv.style.display = 'flex'
    body.style.overflow = 'hidden'
}

function closed()
{
    logindiv.style.display = 'none'
    body.style.overflow = 'visible'
}


function logged()
{

}

browse.addEventListener('mouseover',() =>{
    category.classList.add('active');
    category.style.display = "block"
});

browse.addEventListener('mouseout', () => {
    category.classList.remove('active');
    category.style.display = "none"
});

category.addEventListener('mouseover',() =>{
    category.style.display = "block"
})
category.addEventListener('mouseout',() =>{
    category.style.display = "none"
})