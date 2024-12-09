let totp = "/otp_code/{{ iid }}"
    let email= "/send_email/{{ iid }}"
    let form= document.getElementById('form_2fa')
    let button=document.getElementById('change_route')
    button.addEventListener('click',()=>{
        let select = document.getElementById('select_method')
        if (select.value === 'TOTP'){
            form.action=totp
        }
        else{
            form.action=email
            fetch(form.action,{
                method: 'POST'
            }).then((r) => {console.log(r)})

        }
        console.log(form.action)
    })